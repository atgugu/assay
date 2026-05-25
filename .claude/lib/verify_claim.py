#!/usr/bin/env python3
# verify_claim.py — Deterministic numeric-claim grounding verifier.
#
# Why this exists: Source Protocol §8 in CLAUDE.md says every numeric claim
# must be re-checked by quoting the cited span. Today that check is done by
# the LLM, which means the LLM grades its own CoVe verification log. MAST
# (NeurIPS 2025) attributes 21% of multi-agent failures to verification gaps.
# This script grounds claims in a separate subprocess via deterministic regex
# over the fetched page text — the LLM cannot fake VERIFIED here.
#
# Usage:
#   python3 verify_claim.py \
#     --claim   "DE Bundesliga attendance 2024 = 13.4M" \
#     --url     "https://www.bundesliga.com/..." \
#     --context "Bundesliga,attendance,2024"
#
#   python3 verify_claim.py --self-test
#
#   # Offline mode (testing or already-fetched HTML):
#   python3 verify_claim.py --claim "..." --html-fixture page.html --context "..."
#
# Output: single-line JSON on stdout. Keys:
#   status:            VERIFIED | VERIFIED_FUZZY | NUMBER_MISSING |
#                      NO_CLAIM_NUMBER | FETCH_FAILED | PAYWALLED | JS_REQUIRED
#   claim_text:        echo of input claim
#   url:               echo of input URL (or file://… if fixture)
#   claim_value:       parsed float of the claim's first numeric token
#   matched_value:     float found on page (only if VERIFIED/VERIFIED_FUZZY)
#   matched_span:      ≤240-char window around the page match (only if VERIFIED*)
#   delta_pct:         relative delta % (only if VERIFIED*)
#   context_terms_found: list of context terms found within ±200 chars of match
#   cache_hit:         bool — was the page served from disk cache
#   http_code:         int
#   fetched_at:        ISO timestamp
#   notes:             free-text annotations (paywall markers, currency mismatch…)
#
# Exit 0 always on successful logic (status reported in JSON); 1 on infra
# failure (couldn't even attempt); 2 on bad CLI args.

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# --- Configuration ----------------------------------------------------------

CACHE_DIR = Path.home() / ".cache" / "idea_verify_claim"
CACHE_TTL_SEC = 24 * 3600
FETCH_TIMEOUT_SEC = 15
CONTEXT_WINDOW_CHARS = 200
FUZZY_TOLERANCE = 0.05  # 5% — VERIFIED_FUZZY
EXACT_TOLERANCE = 0.005  # 0.5% — accounts for rounding (13.4M vs 13.43M is fuzzy, 13.4M vs 13.4M is exact)
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) idea-audit-claim-verifier/1.0"
)

# --- Number parsing ---------------------------------------------------------

# Lowercase keys; mag tokens lowercased before lookup.
MAG_MULTIPLIER = {
    "k": 1e3, "thousand": 1e3, "thousands": 1e3, "tsd": 1e3, "tausend": 1e3,
    "m": 1e6, "mn": 1e6, "mio": 1e6, "mln": 1e6,
    "million": 1e6, "millions": 1e6, "millionen": 1e6,
    "b": 1e9, "bn": 1e9, "bln": 1e9, "mrd": 1e9,
    "billion": 1e9, "billions": 1e9, "milliarden": 1e9,
    "t": 1e12, "tn": 1e12, "trillion": 1e12, "trillions": 1e12,
}

# Numeric token with optional currency prefix, magnitude suffix, and percent suffix.
# - \b anchors the leading digit so we don't match middle-of-word integers.
# - \b after mag prevents "M" from matching "Money" → mag must be followed by a word boundary.
# - num grammar allows European thousands separators (space, NBSP, comma, dot).
NUMBER_PATTERN = re.compile(
    r"""
    (?P<currency>[€$£¥])?
    \s?
    \b
    (?P<num>\d{1,3}(?:[,.  \s]\d{3})*(?:[.,]\d+)?)
    (?:
        \s?
        (?P<mag>
            millionen|milliarden|tausend
            | million[s]? | billion[s]? | trillion[s]?
            | thousand[s]?
            | mio | mrd | mln | bln | mn | bn | tn | tsd
            | k | K | M | B | T
        )
        \b
    )?
    \s?
    (?P<pct>%|‰|percent)?
    """,
    re.VERBOSE | re.IGNORECASE | re.UNICODE,
)


def _normalize_number_string(s: str) -> Optional[float]:
    """Parse '13.4' / '13,4' / '13,400' / '13.400' / '13 400' / '13,400.5' / '13.400,5' into float.

    Heuristic for ambiguous '13.400' / '13,400' (one separator, 3 digits after):
      - if only commas → treat as thousands ('13,400' → 13400)
      - if only dots   → keep as decimal ('13.400' → 13.4)   [Python float convention]
    For mixed separators, the LAST separator is the decimal point.
    For multiple identical separators, they're all thousands.
    """
    s = s.replace(" ", "").replace(" ", "").replace(" ", "")
    has_dot = "." in s
    has_comma = "," in s

    if has_dot and has_comma:
        last_dot = s.rfind(".")
        last_comma = s.rfind(",")
        if last_dot > last_comma:
            # US convention: '13,400.50'
            cleaned = s.replace(",", "")
        else:
            # EU convention: '13.400,50'
            cleaned = s[:last_comma].replace(".", "").replace(",", "") + "." + s[last_comma + 1:]
    elif has_comma:
        commas = s.count(",")
        if commas >= 2:
            # Multiple commas → thousands separators ('13,400,000')
            cleaned = s.replace(",", "")
        else:
            last_idx = s.rfind(",")
            digits_after = len(s) - last_idx - 1
            if digits_after == 3:
                # '13,400' — thousands
                cleaned = s.replace(",", "")
            else:
                # '13,4' — European decimal
                cleaned = s.replace(",", ".")
    elif has_dot:
        dots = s.count(".")
        if dots >= 2:
            # Multiple dots → European thousands ('13.400.000')
            cleaned = s.replace(".", "")
        else:
            # Ambiguous '13.400' — Python convention keeps as decimal.
            cleaned = s
    else:
        cleaned = s

    try:
        return float(cleaned)
    except ValueError:
        return None


@dataclass
class ParsedNumber:
    value: float
    currency: Optional[str]
    is_percent: bool
    has_magnitude: bool
    raw_match: str
    span: tuple


def _build(m: re.Match) -> Optional[ParsedNumber]:
    n = m.group("num")
    v = _normalize_number_string(n)
    if v is None:
        return None
    mag_raw = m.group("mag") or ""
    has_mag = bool(mag_raw)
    multiplier = MAG_MULTIPLIER.get(mag_raw.lower(), 1.0)
    v *= multiplier
    pct = m.group("pct")
    is_pct = bool(pct and pct.strip())
    return ParsedNumber(
        value=v,
        currency=m.group("currency"),
        is_percent=is_pct,
        has_magnitude=has_mag,
        raw_match=m.group(0).strip(),
        span=m.span(),
    )


def parse_first_number(text: str) -> Optional[ParsedNumber]:
    """Pick the most-decorated number in the claim text.

    Real claims like 'Bundesliga 2024 = 13.4M' have a bare year before the
    load-bearing value. Years are undecorated; the load-bearing value almost
    always carries currency, percent, or magnitude. Tier 1 wins over Tier 2.
    """
    candidates = extract_all_numbers(text)
    if not candidates:
        return None
    decorated = [c for c in candidates if c.currency or c.is_percent or c.has_magnitude]
    if decorated:
        return decorated[0]
    return candidates[0]


def extract_all_numbers(text: str) -> list:
    out = []
    for m in NUMBER_PATTERN.finditer(text):
        p = _build(m)
        if p is not None:
            out.append(p)
    return out


# --- Fetch + cache ----------------------------------------------------------

def _cache_paths(url: str):
    h = hashlib.sha256(url.encode("utf-8")).hexdigest()
    return CACHE_DIR / f"{h}.html", CACHE_DIR / f"{h}.meta.json"


def fetch_page(url: str) -> dict:
    """Return dict with text, http_code, cache_hit, fetched_at, final_url, error?."""
    cache, meta = _cache_paths(url)
    if cache.exists() and meta.exists():
        try:
            age = time.time() - cache.stat().st_mtime
            if age < CACHE_TTL_SEC:
                text = cache.read_text(encoding="utf-8", errors="replace")
                m = json.loads(meta.read_text())
                return {
                    "text": text,
                    "http_code": m.get("http_code", 200),
                    "cache_hit": True,
                    "fetched_at": m.get("fetched_at"),
                    "final_url": m.get("final_url", url),
                }
        except Exception:
            pass  # cache corrupt — fall through to fresh fetch

    try:
        import requests  # type: ignore
    except ImportError:
        return {
            "text": "", "http_code": 0, "cache_hit": False,
            "fetched_at": None, "final_url": url,
            "error": "requests library not available",
        }

    try:
        resp = requests.get(
            url,
            timeout=FETCH_TIMEOUT_SEC,
            headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml,*/*"},
            allow_redirects=True,
        )
    except Exception as e:
        return {
            "text": "", "http_code": -1, "cache_hit": False,
            "fetched_at": None, "final_url": url, "error": str(e),
        }

    iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache.write_text(resp.text, encoding="utf-8")
        meta.write_text(json.dumps({
            "http_code": resp.status_code,
            "fetched_at": iso,
            "final_url": resp.url,
        }))
    except Exception:
        pass  # cache write failure is non-fatal

    return {
        "text": resp.text,
        "http_code": resp.status_code,
        "cache_hit": False,
        "fetched_at": iso,
        "final_url": resp.url,
    }


def html_to_text(html: str) -> str:
    try:
        from bs4 import BeautifulSoup  # type: ignore
    except ImportError:
        # Conservative fallback: strip tags by regex, collapse whitespace.
        stripped = re.sub(r"<[^>]+>", " ", html)
        return re.sub(r"\s+", " ", stripped).strip()
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return soup.get_text(separator=" ", strip=True)


# --- Verification logic ----------------------------------------------------

PAYWALL_MARKERS = (
    "subscribe to read", "subscriber-only", "subscribers only",
    "paywall", "premium content", "subscribe now",
    "create a free account to continue", "log in to access",
    "this article is for subscribers", "register to read",
)


def detect_paywall(text: str) -> bool:
    low = text.lower()
    return any(m in low for m in PAYWALL_MARKERS) and len(text) < 5000


def detect_js_required(text: str, http_code: int) -> bool:
    return http_code == 200 and len(text.strip()) < 300


def values_compatible(claim: ParsedNumber, page: ParsedNumber) -> bool:
    if claim.is_percent != page.is_percent:
        return False
    # Currency: if both stated and they differ → incompatible.
    if claim.currency and page.currency and claim.currency != page.currency:
        return False
    return True


def relative_delta(a: float, b: float) -> float:
    if a == 0 and b == 0:
        return 0.0
    if a == 0 or b == 0:
        return 1.0
    return abs(a - b) / max(abs(a), abs(b))


def find_context_terms_near(text: str, position: int, terms: list, window: int) -> list:
    if not terms:
        return []
    lo = max(0, position - window)
    hi = min(len(text), position + window)
    window_text = text[lo:hi].lower()
    found = []
    for t in terms:
        t_norm = t.strip().lower()
        if t_norm and t_norm in window_text:
            found.append(t.strip())
    return found


def slice_span(text: str, position: int, span_chars: int = 240) -> str:
    half = span_chars // 2
    lo = max(0, position - half)
    hi = min(len(text), position + half)
    s = text[lo:hi]
    s = re.sub(r"\s+", " ", s).strip()
    return s


def verify_claim_in_text(claim_text: str, page_text: str, context_terms: list) -> dict:
    claim_n = parse_first_number(claim_text)
    if claim_n is None:
        return {
            "status": "NO_CLAIM_NUMBER",
            "notes": "could not extract a numeric value from the claim",
        }

    page_numbers = extract_all_numbers(page_text)
    if not page_numbers:
        return {
            "status": "NUMBER_MISSING",
            "claim_value": claim_n.value,
            "notes": "page contains no parseable numeric values",
        }

    exact_matches = []  # (page_num, delta)
    fuzzy_matches = []
    for pn in page_numbers:
        if not values_compatible(claim_n, pn):
            continue
        d = relative_delta(claim_n.value, pn.value)
        if d <= EXACT_TOLERANCE:
            exact_matches.append((pn, d))
        elif d <= FUZZY_TOLERANCE:
            fuzzy_matches.append((pn, d))

    exact_matches.sort(key=lambda x: x[1])
    fuzzy_matches.sort(key=lambda x: x[1])

    require_context = bool(context_terms)

    for pn, d in exact_matches:
        ctx = find_context_terms_near(page_text, pn.span[0], context_terms, CONTEXT_WINDOW_CHARS)
        if ctx or not require_context:
            return {
                "status": "VERIFIED",
                "claim_value": claim_n.value,
                "matched_value": pn.value,
                "matched_span": slice_span(page_text, pn.span[0]),
                "context_terms_found": ctx,
                "delta_pct": round(d * 100, 4),
            }

    for pn, d in fuzzy_matches:
        ctx = find_context_terms_near(page_text, pn.span[0], context_terms, CONTEXT_WINDOW_CHARS)
        if ctx or not require_context:
            return {
                "status": "VERIFIED_FUZZY",
                "claim_value": claim_n.value,
                "matched_value": pn.value,
                "matched_span": slice_span(page_text, pn.span[0]),
                "context_terms_found": ctx,
                "delta_pct": round(d * 100, 4),
            }

    if exact_matches or fuzzy_matches:
        return {
            "status": "NUMBER_MISSING",
            "claim_value": claim_n.value,
            "notes": (
                f"found {len(exact_matches)} exact and {len(fuzzy_matches)} fuzzy "
                f"numeric match(es) on page, but none within ±{CONTEXT_WINDOW_CHARS} "
                f"chars of any context term: {context_terms}"
            ),
        }

    return {
        "status": "NUMBER_MISSING",
        "claim_value": claim_n.value,
        "notes": "claim value not present on page within ±5% tolerance",
    }


# --- Main entry ------------------------------------------------------------

def emit(d: dict) -> None:
    sys.stdout.write(json.dumps(d, ensure_ascii=False, separators=(",", ":")) + "\n")
    sys.stdout.flush()


def _split_context(s) -> list:
    if not s:
        return []
    return [t.strip() for t in s.split(",") if t.strip()]


def run(args) -> int:
    if args.html_fixture:
        try:
            raw = Path(args.html_fixture).read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            emit({"status": "FETCH_FAILED", "claim_text": args.claim,
                  "url": f"file://{args.html_fixture}", "notes": f"fixture read failed: {e}"})
            return 0
        page_text = html_to_text(raw) if "<" in raw and ">" in raw else raw
        result = verify_claim_in_text(args.claim, page_text, _split_context(args.context))
        result.update({
            "claim_text": args.claim,
            "url": args.url or f"file://{args.html_fixture}",
            "http_code": 0,
            "cache_hit": False,
            "fetched_at": None,
        })
        emit(result)
        return 0

    fetched = fetch_page(args.url)
    if "error" in fetched:
        emit({
            "status": "FETCH_FAILED",
            "claim_text": args.claim,
            "url": args.url,
            "http_code": fetched.get("http_code", -1),
            "notes": fetched["error"],
            "cache_hit": False,
        })
        return 0

    http_code = fetched["http_code"]
    if http_code in (401, 402, 403):
        emit({
            "status": "PAYWALLED",
            "claim_text": args.claim,
            "url": args.url,
            "http_code": http_code,
            "cache_hit": fetched["cache_hit"],
            "fetched_at": fetched["fetched_at"],
        })
        return 0
    if http_code >= 400:
        emit({
            "status": "FETCH_FAILED",
            "claim_text": args.claim,
            "url": args.url,
            "http_code": http_code,
            "cache_hit": fetched["cache_hit"],
            "fetched_at": fetched["fetched_at"],
        })
        return 0

    page_text = html_to_text(fetched["text"])

    if detect_js_required(page_text, http_code):
        emit({
            "status": "JS_REQUIRED",
            "claim_text": args.claim,
            "url": args.url,
            "http_code": http_code,
            "cache_hit": fetched["cache_hit"],
            "fetched_at": fetched["fetched_at"],
            "notes": "HTTP 200 but extracted text < 300 chars — likely JS-rendered",
        })
        return 0
    if detect_paywall(page_text):
        emit({
            "status": "PAYWALLED",
            "claim_text": args.claim,
            "url": args.url,
            "http_code": http_code,
            "cache_hit": fetched["cache_hit"],
            "fetched_at": fetched["fetched_at"],
            "notes": "paywall markers detected in page",
        })
        return 0

    result = verify_claim_in_text(args.claim, page_text, _split_context(args.context))
    result.update({
        "claim_text": args.claim,
        "url": fetched["final_url"],
        "http_code": http_code,
        "cache_hit": fetched["cache_hit"],
        "fetched_at": fetched["fetched_at"],
    })
    emit(result)
    return 0


# --- Self test -------------------------------------------------------------

def run_self_test() -> int:
    failures = 0
    total = 0

    def check(name, got_status, expected_status, extra=""):
        nonlocal failures, total
        total += 1
        ok = got_status == expected_status
        marker = "PASS" if ok else "FAIL"
        msg = f"  [{marker}] T{total} {name}: got={got_status}, expected={expected_status}"
        if extra:
            msg += f" -- {extra}"
        print(msg)
        if not ok:
            failures += 1

    # T1 — exact number with context word
    page = "The 2024 Bundesliga season saw total attendance reach 13.4 million across all matches."
    r = verify_claim_in_text("DE Bundesliga attendance 2024 = 13.4M", page, ["Bundesliga", "attendance"])
    check("exact+context", r["status"], "VERIFIED")

    # T2 — fuzzy match (13.4M claimed, 13.7M on page) — clearly outside 0.5% exact tolerance
    page = "Bundesliga attendance in 2024 totaled 13.7 million spectators."
    r = verify_claim_in_text("DE Bundesliga attendance 2024 = 13.4M", page, ["Bundesliga"])
    check("fuzzy+context", r["status"], "VERIFIED_FUZZY")

    # T3 — number present but no context within ±200 chars
    page = ("Apple Inc. reported quarterly revenue of 13.4 million dollars. "
            + ("filler word " * 80)
            + "Bundesliga attendance was up significantly.")
    r = verify_claim_in_text("DE Bundesliga attendance 2024 = 13.4M", page, ["Bundesliga", "attendance"])
    check("number-without-context", r["status"], "NUMBER_MISSING")

    # T4 — number completely absent
    page = "The Bundesliga is a German football league. Many fans attend matches."
    r = verify_claim_in_text("DE Bundesliga attendance 2024 = 13.4M", page, ["Bundesliga"])
    check("number-absent", r["status"], "NUMBER_MISSING")

    # T5 — percent claim, percent on page
    page = "Personio reported NRR of 110% in their 2024 annual report."
    r = verify_claim_in_text("Personio NRR 110%", page, ["Personio", "NRR"])
    check("percent-exact", r["status"], "VERIFIED")

    # T6 — percent claim vs absolute on page
    page = "Personio reported revenue of 110 million euros."
    r = verify_claim_in_text("Personio NRR 110%", page, ["Personio"])
    check("percent-vs-absolute", r["status"], "NUMBER_MISSING")

    # T7 — currency mismatch
    page = "Komoot ARPU reached $25.3 per user in 2023."
    r = verify_claim_in_text("Komoot ARPU €25/yr", page, ["Komoot", "ARPU"])
    check("currency-mismatch", r["status"], "NUMBER_MISSING")

    # T8 — German decimal format on page
    page = "Im Jahr 2024 erreichte die Bundesliga eine Zuschauerzahl von 13,4 Millionen."
    r = verify_claim_in_text("Bundesliga 2024 attendance = 13.4M", page, ["Bundesliga", "Zuschauerzahl"])
    check("EU-decimal", r["status"], "VERIFIED")

    # T9 — thousand-suffix 'k'
    page = "MVP cost: €350k for the first prototype."
    r = verify_claim_in_text("MVP cost €350k", page, ["MVP", "cost"])
    check("thousand-k", r["status"], "VERIFIED")

    # T10 — within fuzzy tolerance (~3%)
    page = "Approximately 13.0 million people attended Bundesliga matches in 2024."
    r = verify_claim_in_text("Bundesliga 2024 = 13.4M", page, ["Bundesliga"])
    check("fuzzy-3pct", r["status"], "VERIFIED_FUZZY")

    # T11 — outside fuzzy tolerance (~15%)
    page = "Approximately 11.4 million people attended Bundesliga matches in 2024."
    r = verify_claim_in_text("Bundesliga 2024 = 13.4M", page, ["Bundesliga"])
    check("outside-fuzzy", r["status"], "NUMBER_MISSING")

    # T12 — percent stated with "percent" word
    page = "Market growth CAGR was 11 percent in 2024."
    r = verify_claim_in_text("CAGR 11%", page, ["CAGR"])
    check("percent-word", r["status"], "VERIFIED")

    # T13 — comma-separated thousands
    page = "Total active developers: 13,400,000 across the platform."
    r = verify_claim_in_text("13.4M developers", page, ["developers"])
    check("comma-thousands", r["status"], "VERIFIED")

    # T14 — claim with no number at all
    r = verify_claim_in_text("Bundesliga is popular in Germany", "any page", ["Bundesliga"])
    check("no-claim-number", r["status"], "NO_CLAIM_NUMBER")

    # T15 — letter-mag false-positive guard: "13Money" should NOT parse as 13M
    page = "Komoot ARPU €25.3 in 2023 — they made 13Money was not the issue."
    r = verify_claim_in_text("ARPU €25.3", page, ["ARPU"])
    check("letter-mag-guard", r["status"], "VERIFIED")

    # T16 — paywall detection: short page with paywall marker
    short_paywall_text = "Subscribe to read the full article. Premium content."
    js_short = detect_paywall(short_paywall_text)
    check("paywall-marker-detect", "PAYWALLED" if js_short else "NOPE", "PAYWALLED")

    # T17 — German Mio. suffix
    page = "Der Umsatz lag 2023 bei 56 Mio. Euro laut Jahresbericht."
    r = verify_claim_in_text("Komoot revenue €56M 2023", page, ["Umsatz"])
    check("german-Mio", r["status"], "VERIFIED")

    # T18 — billion magnitude
    page = "EU SaaS market reached €120 billion in total enterprise value in 2024."
    r = verify_claim_in_text("EU SaaS €120B 2024", page, ["SaaS", "EU"])
    check("billion-suffix", r["status"], "VERIFIED")

    # T19 — currency match where page omits currency
    page = "MVP build cost was 350k for the first prototype."
    r = verify_claim_in_text("MVP cost €350k", page, ["MVP"])
    check("page-omits-currency", r["status"], "VERIFIED")

    # T20 — empty page text
    r = verify_claim_in_text("13.4M", "", ["Bundesliga"])
    check("empty-page", r["status"], "NUMBER_MISSING")

    print()
    if failures == 0:
        print(f"All {total} self-tests passed.")
        return 0
    print(f"{failures}/{total} self-tests FAILED.")
    return 1


def main() -> int:
    p = argparse.ArgumentParser(
        description="Deterministic numeric claim grounding verifier. "
                    "Reads a (claim, url, context) triple and returns a JSON "
                    "VERIFIED|VERIFIED_FUZZY|NUMBER_MISSING|… status."
    )
    p.add_argument("--claim", help="Claim text containing the numeric value to verify.")
    p.add_argument("--url", help="Source URL whose content should support the claim.")
    p.add_argument("--context", help="Comma-separated context terms required within ±200 chars of the match.")
    p.add_argument("--html-fixture", help="(testing/offline) Path to local HTML/text file instead of fetching URL.")
    p.add_argument("--self-test", action="store_true", help="Run built-in self-tests and exit.")
    args = p.parse_args()

    if args.self_test:
        return run_self_test()

    if not args.claim or (not args.url and not args.html_fixture):
        p.error("--claim and either --url or --html-fixture are required (or pass --self-test)")
        return 2

    return run(args)


if __name__ == "__main__":
    sys.exit(main())
