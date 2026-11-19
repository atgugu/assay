# Ideas

A no-bullshit feasibility audit pipeline for business ideas. Take a one-line seed → produce a deep, source-grounded market & feasibility audit → end in a categorical verdict (**GO / PIVOT / NO_GO / DEFER**) backed by tagged evidence and a deterministic claim verifier.

Built on [Claude Code](https://github.com/anthropics/claude-code) skills + agents. Defaults to EU27 geography and a solo-founder cost model.

---

## What it does

Given a seed like

```
/idea_audit "EU AI Act compliance audit tool for German SaaS, €5k/mo"
```

…it runs a 12-step wizard with `AskUserQuestion` checkpoints between every step, producing:

- **Categorical verdict** — GO / PIVOT / NO_GO / DEFER with high/med/low confidence
- **Scale-mode aware** — L1 (replace-salary, default) / L2 (indie) / L3 (venture); same evidence, different thresholds
- **Scorecard** with the top 10 load-bearing KPIs, each tagged `[FATAL|BLOCKER|RISK|ADVANTAGE]` and traced to a cited URL with access date
- **Killer finding + decision frame + cheapest discriminating experiment** (< €5k, < 4 weeks) attached to every verdict — including `NO_GO`
- **Calibration check** against a running ledger of prior audits (`audits/_calibration.jsonl`)
- **Funding research** (Phase C, `GO`/`PIVOT` only) — a named-entity registry across 4 avenues: grants · angels · VCs · anchor procurement

Sample scorecard — the real rows from `audits/2026-05-25_predictive-crowd-movement/10_verdict.md`, abridged.
**This is an early partial run** (7 of 12 steps were stubs, so no unit economics, customer or red-team evidence) and it was
judged on venture-style thresholds, not on the L1 default described below. Treat it as a format demo, not a model verdict:

```
VERDICT:         NO_GO                                  Confidence: med
LOAD-BEARING KPIs
  SAM 5-yr (wedge, post-CoVe)        €33M/yr (range €22–58M)         ≥€80M FATAL-1 threshold      [FATAL]
  B2G procurement to first pilot     12–24 mo realistic              ≤9 mo BLOCKER-4 threshold    [BLOCKER]
  "Why now?" verified triggers       0/3 survive primary check       ≥1 strong leg required       [BLOCKER]
  EU AI Act Annex III class          borderline §5(d)                clean exemption required     [BLOCKER]
  EU seed/Series-A ≥€5M in wedge     1 hit (Liftango, AU-HQ)         ≥3 EU-HQ rounds              [RISK]
  ...
TAG TALLY     FATAL: 1   BLOCKER: 3   RISK: 2   ADVANTAGE: 1
```

Known problems in that example, found in review (a rebuild is in progress): the €80M floor is a VC-scale threshold that
`CLAUDE.md` itself calls a false-negative trap at L1; the deterministic verifier below was written after this audit ran, so
its claims were not machine-checked; the headline SAM was corrected from €78M to €33M by the model re-adding its own numbers,
and the text still contains stale figures; and the tag tally was applied by an LLM, not by code.

---

## Why bother — what's load-bearing

Anti-bullshit discipline is enforced **mechanically**, not stylistically.

- **Source Protocol** — every major numeric claim has ≥5 cited sources (≥2 primary), every URL is WebFetch-verified with an access date, and every TAM/SAM/SOM shows the bottom-up arithmetic (`N_buyers × ARPU × penetration`).
- **Deterministic claim grounding** — `.claude/lib/verify_claim.py` runs as a subprocess regex check on every load-bearing numeric claim. The LLM cannot self-grade — the regex engine does. `NUMBER_MISSING` forces an `[ESTIMATE]` flag; the agent is re-invoked. Closes the verification-gap category from MAST (NeurIPS 2025, 21% of multi-agent failures). *(Design intent: see "The verifier" below for what currently works and what does not.)*
- **Cross-step numeric reconciliation** — CAC, ARPU, build-cost have to agree across agents within 2×, else a `[RECONCILE]` flag downgrades the synthesizer's confidence.
- **Banned-language regex audit** — re-invokes the agent if the artifact contains vague phrases (`huge market`, `AI-powered` as differentiation, `studies show` without URL, …).
- **5 anti-confirmation-bias closing blocks** in every research artifact — negative results, named analogs, inverse falsifier, confidence diary, CoVe verification log.
- **Persona discipline** — agents are skeptical-neutral (anti-warmth, anti-direction-echo, isolation). Sanitized briefs prevent the TRUTH-DECAY drift documented in Nature 2025 (~36.8% accuracy loss after 3 biased follow-ups).
- **MAST defenses** — rigid output schemas (specification-ambiguity 47%), no agent-to-agent messaging (coordination-breakdowns 32%), deterministic verifier (verification-gaps 21%).

---

## Quickstart

Prerequisites: Claude Code, Python 3.10+, `requests`, `beautifulsoup4`.

```bash
# 1. Confirm the deterministic verifier works in your env
python3 .claude/lib/verify_claim.py --self-test
# → All 20 self-tests passed.

# 2. Bootstrap (idempotent — safe to re-run)
/idea_init

# 3. Run a deep audit (wizard mode, checkpoints between every step)
/idea_audit "<your seed idea>"

# Alternatively, run individual stages:
/idea_triage   "<seed>"            # 5-minute kill/keep gate
/idea_market   "<seed>"            # TAM/SAM/SOM + why-now + demand signals
/idea_compete  "<seed>"            # competitive landscape + incumbent response
/idea_business "<slug>"            # unit-econ + GTM + capital-fit (3-agent bundle)
/idea_verdict  "<slug>"            # re-synthesize from existing artifacts

# Read-only status of any audit
/idea_status   "<slug>"

# Funding research after a GO/PIVOT verdict
/idea_funding  "<slug>"
```

Common flags: `--scale=L1|L2|L3` · `--geo=EU27|DE|FR|+US|global` · `--depth=quick|deep|paranoid` · `--resume` · `--no-checkpoints`.

---

## The verifier

`.claude/lib/verify_claim.py` checks a numeric claim against a fetched page by regex and returns one JSON line:

```bash
python3 .claude/lib/verify_claim.py --self-test      # offline, 20 built-in cases
python3 .claude/lib/verify_claim.py --claim "<text>" --url "<src>" --context "<comma,separated,terms>"
```

Statuses: `VERIFIED` · `VERIFIED_FUZZY` (≤5% delta) · `NUMBER_MISSING` · `FETCH_FAILED` · `PAYWALLED` · `JS_REQUIRED` · `NO_CLAIM_NUMBER`.
Disk-cached 24 h at `~/.cache/idea_verify_claim/`. Handles currency, magnitude suffixes (k / M / B / Mio / Mrd …), percent, and EU vs US separators.

**Known limitations (honest status):** bare integers of 4+ digits without a magnitude or currency are mis-parsed (`2021` reads as 202);
a single context word within ±200 characters is enough to pass, so a nearby unrelated number can verify; an empty `--context`
matches any equal number; and the wizard is not currently permitted to run Python, so the example audit was not machine-verified.

---

## Scale modes (the most consequential design choice)

VC-fundable thresholds systematically false-negative on indie-SaaS-scale ideas, so the system defaults to **L1 (replace-salary)**. Three modes, same evidence, different thresholds:

| Mode | Target ARR (24–60 mo) | First customer | LTV/CAC floor | Capital path |
|---|---|---|---|---|
| **L1** (default) | €50 k – €500 k | < 6 weeks | ≥ 2 (universal) | bootstrap-only |
| **L2** (indie) | €500 k – €5 M | < 12 weeks | ≥ 2 (universal) | bootstrap or angel < €200 k |
| **L3** (venture) | €5 M – €100 M + | < 8 weeks | ≥ 2 (universal) | pre-seed → seed → Series A |

`LTV/CAC < 1 = FATAL · < 2 = BLOCKER` is universal across all three. The verdict-synthesizer reads `state.yaml.scale_mode` and re-evaluates every emitted tag against the matching threshold column from the KPI table in `CLAUDE.md`.

---

## Layout

```
.claude/
  agents/             — 11 specialist agents
    market-size-analyst.md            (canonical Source Protocol reference)
    competitive-landscape-analyst.md
    customer-segment-analyst.md
    regulatory-compliance-analyst.md
    technical-feasibility-engineer.md
    unit-economics-analyst.md
    gtm-channel-analyst.md
    capital-and-investor-fit-analyst.md
    red-team-analyst.md               (DA + premortem dual mode)
    verdict-synthesizer.md            (aggregation + scorecard + adversarial debate)
    funding-sourcing-analyst.md       (Phase C — named-entity funding registry)
  commands/           — 13 skills
    idea_init.md, idea_audit.md, idea_status.md, idea_verdict.md,
    idea_triage.md, idea_market.md, idea_compete.md, idea_customer.md,
    idea_regulatory.md, idea_technical.md, idea_business.md, idea_redteam.md,
    idea_funding.md
  lib/
    verify_claim.py   — deterministic numeric-claim grounding verifier (subprocess)
audits/
  _calibration.jsonl  — append-only verdict ledger (one JSON line per audit)
  <YYYY-MM-DD>_<slug>/
    00_seed.md            — original seed + invocation args
    01_clarification.md   — well-formed problem statement
    01b_falsifier.md      — pre-registered kill criteria (deep mode)
    02_triage.md          — fast kill/keep verdict
    03_market.md          — TAM/SAM/SOM with bottom-up math
    04_competition.md     — competitive landscape + incumbent response
    05_customer.md        — JTBD / WTP / pain-severity
    06_regulatory.md      — EU AI Act / GDPR / sector / global
    07_technical.md       — build cost / time-to-MVP / tech risk
    08_business.md        — unit-econ + GTM + capital-fit (3-agent bundle)
    09_redteam.md         — DA + premortem
    10_verdict.md         — SCORECARD + decision frame + cheapest experiment
    11_funding.md         — (Phase C, GO/PIVOT only) named funding entities
    sources.md            — every cited URL with access date + fetch status
    state.yaml            — wizard progress + running tag tally
CLAUDE.md             — workspace contract (read this first if you're editing the system)
SMOKE_TEST.md         — end-to-end test recipes
ideas.md              — seed file (one line per seed)
README.md             — this file
```

---

## Example audit included

`audits/2026-05-25_predictive-crowd-movement/` contains a real Phase-A run on the seed *"predictive crowd movement — tourist flow, protests, football games"* that ended in `NO_GO` (judged on venture-style thresholds, not L1; 7 of 12 steps were stubs). Worth reading:

- `00_seed.md` — what a seed looks like after the wizard's clarification pass
- `01b_falsifier.md` — pre-registered kill criteria, written before research starts
- `03_market.md` — TAM/SAM/SOM with bottom-up math; every input to the €33M SAM is an estimate, anchored to cited sources (see the verdict's known problems above)
- `10_verdict.md` — the SCORECARD, plus the < €5k discriminating experiment that would change the verdict (a pivot to insurance-data-feed wedge)
- `sources.md` — every URL, access date, primary/secondary tag, fetch-status

---

## Reading order if you're new

1. **`CLAUDE.md`** — the workspace contract: source protocol, banned phrases, persona discipline, scale-mode threshold tables, MAST defenses. 30 min.
2. **`.claude/commands/idea_audit.md`** — the wizard. The Standard Step Driver pattern lives here.
3. **`.claude/agents/market-size-analyst.md`** — the canonical Source Protocol reference. Every other research agent inherits from this template.
4. **`audits/2026-05-25_predictive-crowd-movement/10_verdict.md`** — what the output looks like end-to-end.

---

## Status

- **Phase A** — initial scaffold + 12 steps with stubs. Complete.
- **Phase B** — all 12 steps wired with real agents; Standard Step Driver; cross-step numeric reconciliation; multi-agent reflexion; sentence-level grounding via `.claude/lib/verify_claim.py`. Complete.
- **Phase C** — funding-research extension (Step 13) — `funding-sourcing-analyst` + `/idea_funding` + scale-mode-aware emphasis (L1 → §4 anchor procurement primary; L2 → balanced; L3 → §3 VCs primary). Complete.

Calibration prior (tentative anchor, recalibrate from `_calibration.jsonl` after 10 phase-B audits): GO 10–15% · PIVOT 25–35% · NO_GO 35–45% · DEFER 10–20%.
