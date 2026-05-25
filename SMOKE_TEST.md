# Smoke-test plan — verify the idea_* system end-to-end

This document is for the **user to execute in a fresh Claude Code session** at `/home/atgu/Projects/Ideas/`. Project-local skills (`/idea_*`) and agents are picked up by Claude Code on session start in this directory, so they cannot be smoke-tested from the session that wrote them.

## Pre-flight (do this once)

```bash
cd /home/atgu/Projects/Ideas
```

Start Claude Code here. Confirm the new skills appear in the `/help` or in autocomplete:
- `/idea_init`
- `/idea_audit`
- `/idea_status`
- `/idea_triage` · `/idea_market` · `/idea_compete` · `/idea_customer` · `/idea_regulatory` · `/idea_technical` · `/idea_business` · `/idea_redteam` · `/idea_verdict`

If they don't appear, check `/home/atgu/Projects/Ideas/.claude/commands/` is populated and Claude Code's session is at this working directory.

## Scale modes (2026-05-25 patch — must validate)

The audit now supports three scale modes. Default is **L1 — replace-salary** (€50k-€500k ARR, bootstrap-only). Override with `--scale=L2` (indie) or `--scale=L3` (venture). Each invocation below specifies the scale explicitly so the smoke-test result is reproducible.

If the wizard asks you for scale at Step 0.5 (because `--scale` wasn't on the CLI), pick L1 unless the seed text obviously calls for a bigger outcome.

## B.0 — Validate that dispatch fires (the critical pre-condition)

Run **once** to confirm the Standard Step Driver pattern actually executes end-to-end:

```
/idea_init
```

Expected: bootstrap summary showing 11/11 agents, 13/13 skills, audits/ + _calibration.jsonl present, CLAUDE.md found. (Phase C added `funding-sourcing-analyst` + `/idea_funding`.)

Then:

```
/idea_audit "predictive crowd movement - tourist flow, protests, football games" --scale=L1 --depth=quick
```

The wizard will ask checkpoints between steps — proceed through all of them. Expected behavior:

- Step 1 (seed): creates `audits/2026-MM-DD_predictive-crowd-movement/` + `00_seed.md` + `state.yaml`
- Step 2 (clarify): `AskUserQuestion` prompts for customer/pain/mechanism/geo/build hypothesis; writes `01_clarification.md`
- Step 3 (falsify): invokes `/sci_falsify`; writes `01b_falsifier.md`
- Step 4 (triage): dispatches `red-team-analyst` mode:quick; writes `02_triage.md` with `TRIAGE VERDICT:` and `fatal_finding:` lines at top
- Step 5 (market): dispatches `market-size-analyst`; writes `03_market.md` with cited sources, TAM/SAM/SOM with bottom-up math, "why now" trigger, and the 5 closing blocks
- Step 12 (verdict, quick mode skips the middle): dispatches `verdict-synthesizer`; writes `10_verdict.md` with SCORECARD block + adversarial debate

After completion, inspect:

```
ls audits/2026-MM-DD_predictive-crowd-movement/
cat audits/2026-MM-DD_predictive-crowd-movement/state.yaml
cat audits/2026-MM-DD_predictive-crowd-movement/10_verdict.md  # look for SCORECARD as first content block
cat audits/_calibration.jsonl  # one line with wizard_version: phase-B
```

### If something is broken in B.0

Most likely failure modes (per the Phase B plan):

1. **WebFetch paywall cascade** — agent retries fail. Symptom: `[SOURCE-DISCIPLINE-FAILURE]` flags appear; some KPIs are `[ESTIMATE]` with confidence: low. **This is acceptable behavior** — the system is supposed to degrade gracefully to estimates with reasoning shown.
2. **Regex-audit retry loop** — wizard re-invokes the agent in an infinite loop. Symptom: same step runs repeatedly with no new artifact. Fix: the regex check needs the discrimination heuristic (numeric only auditable if in sentence with €/%/CAGR/customers/MRR/ARR). Check `idea_audit.md`'s Standard Step Driver §3.
3. **Cross-step numeric contradiction not flagged** — `08_business.md` Cross-agent reconciliation block shows agents disagreeing by >2× but no `[RECONCILE]` flag. Fix: verify wizard Step 10.B writes the reconciliation block from the sub-files.

## B.6 — Calibration runs on 3 seeds (each at L1 default; L3 contrast on Seed 2)

Run three audits with deliberate seed selection to test the synthesizer's discrimination:

### Seed 1 — Bad seed (expected NO_GO at ANY scale)

```
/idea_audit "AI for AI optimization, B2B2C, blockchain-enabled" --scale=L1 --depth=quick
```

**Acceptable verdict**: NO_GO (any confidence)
**Failure mode**: if the synthesizer issues PIVOT or DEFER, it's too lenient even at L1. Inspect the SCORECARD's KILLER FINDING — it should clearly identify "no real pain", "buzzword-soup", or similar. A bad seed should NO_GO at every scale_mode.

### Seed 2 — Strong-but-niche seed (expected GO at L1, PIVOT-or-NO_GO at L3)

This is the **scale-mode-discrimination test** — run the same seed at both L1 and L3 and check that the verdict actually changes.

```
/idea_audit "EU AI Act compliance audit tool for German SaaS, €5k/month subscription" --scale=L1 --depth=deep
```

**Acceptable L1 verdict**: GO (low or med confidence) — €5k/mo × ~20-30 customers = €100k-€180k ARR is achievable, MVP cash low, time-to-first-paying-customer plausibly <12 weeks.

Then re-run at L3 to validate scale-mode discrimination:

```
/idea_audit "EU AI Act compliance audit tool for German SaaS, €5k/month subscription" --scale=L3 --depth=deep
```

**Acceptable L3 verdict**: PIVOT or NO_GO (low or med confidence) — €100M+ outcome thesis weak (DE-only niche), defensibility-growth shallow (audit tools are commodity-prone), comparable EU exits sparse.

**Critical check**: the two SCORECARDs should show DIFFERENT verdicts on the same seed. If they're identical, the scale_mode logic isn't wired through. Inspect:
- `state.yaml.scale_mode` (should match the flag)
- The verdict file's `Active scale_mode:` line under VERDICT
- The CALIBRATION line (filtered to scale_mode, n=1 per side)
- The Tag re-evaluation log (some L3 [FATAL] tags should re-tag as L1 [ADVANTAGE] or be dropped)

This takes ~45–60 minutes per scale level interactively.

### Seed 3 — Ambiguous seed (re-run at L1)

```
/idea_audit --resume audits/2026-MM-DD_predictive-crowd-movement
```

Resume the B.0 audit to completion. The stub-overwrite policy means Steps 4, 6–11 (originally stub-skipped if you ran in quick mode) will be re-run with the real agents. The audit's `state.yaml.scale_mode` was set in B.0 (should be L1).

**Acceptable L1 verdict**: PIVOT, DEFER, or NO_GO-low
**Failure mode**: GO at any confidence = motivated reasoning failure — the L1 GO gate requires fast-revenue (<6 weeks to first paying customer; <9 mo to €10k MRR), and B2G procurement at 12-24 months violates that floor. If the synthesizer GOs this, the L1 fast-revenue gate isn't binding.

## B.7 — Phase C funding-research smoke test

This test validates the new Step 13 funding-research dispatch. Run after Seed 2 (the L1 GO compliance-audit case from B.6) has completed Step 12 with verdict ∈ {GO, PIVOT}.

### B.7.A — Auto-dispatch flow on GO/PIVOT

When B.6 Seed 2 finishes Step 12 with a GO verdict at L1, the wizard should automatically print the SCORECARD and then prompt:

```
Question: "Verdict: GO at scale L1. Run deep funding research now?
(~8–18 WebFetches; produces 11_funding.md with 4 sections of named entities — grants, angels, VCs, anchor-procurement contracts.)"
Options:
  1. Run now — recommended/default
  2. Defer — exit cleanly; user can run `/idea_funding <slug>` later in a fresh session
  3. Skip permanently — mark Step 13 status: skipped (--resume won't re-prompt)
  4. Other (free-text)
```

**Pick option 1.** The wizard dispatches `funding-sourcing-analyst` and produces `11_funding.md`.

**Acceptable**: `11_funding.md` exists with all 4 sections (§1 grants · §2 angels · §3 VCs · §4 anchor procurement), each non-empty (or explicitly `[NONE]` with reasoning).
**Failure mode**: §4 is empty AND `08b_gtm.md`'s LOI/paid-pilot column had named candidates — the funding-sourcing-analyst is failing to read upstream artifacts.

### B.7.B — Standalone `/idea_funding <slug>` on an existing GO/PIVOT audit

In a fresh Claude Code session:

```
/idea_funding 2026-MM-DD_compliance-audit-de
```

**Acceptable**: skill reads state.yaml, confirms verdict ∈ {GO, PIVOT}, dispatches funding-sourcing-analyst, produces or overwrites `11_funding.md`. If file already exists from B.7.A and is fresh (< 180d), skill asks via AskUserQuestion before re-running.
**Failure mode**: skill produces a new file without prompting → staleness check is broken.

### B.7.C — `--anchor-only` mode on a NO_GO audit (consulting-pivot exploration)

In a fresh Claude Code session, on Seed 1 (the bad seed, NO_GO):

```
/idea_funding 2026-MM-DD_ai-for-ai-optimization --anchor-only
```

**Acceptable**: skill produces `11_funding.md` with `mode: anchor_only` in frontmatter. §1/§2/§3 contain placeholder lines (`[ANCHOR-ONLY MODE — section skipped]`). §4 has real entries with `consulting-shaped: yes/no` annotations.
**Failure mode**: skill produces full 4-section output → `--anchor-only` flag isn't being respected.

### B.7.D — geo=global refusal

Edit a test audit's `state.yaml` to set `geo: global`, then:

```
/idea_funding <slug>
```

**Acceptable**: skill refuses with message naming supported geos and AskUserQuestion to pick a primary geo (EU27 / DE / FR / IT / ES / NL / RO / +US / +UK).
**Failure mode**: skill proceeds with `geo: global` → jurisdiction-bound funding sources cannot be enumerated; output will be padded with off-fit programs.

### B.7.E — Staleness threshold

Hand-edit `11_funding.md`'s `funding_data_as_of` frontmatter to a date > 180 days ago. Then:

```
/idea_audit --resume <slug>
```

**Acceptable**: wizard detects staleness on Step 13 entry, prompts user to re-run funding research before exit.
**Failure mode**: wizard exits cleanly without prompting → staleness resume hook isn't wired.

### B.7.F — Named-entity public-access-path enforcement

Open the produced `11_funding.md`. Spot-check:

- Every named angel has a public access path (Twitter @handle / AngelList URL / public newsletter) — **never personal email**.
- Every VC firm has a public partner name + public access path.
- Every grant program has a deadline in ISO format and a specific URL.
- Every anchor procurement entry has First-contact action filled (no `[TBD]`).

**Failure mode**: any personal email appears in the artifact → `[BANNED-CONTACT-INFO]` regex audit didn't fire.

### B.7.G — Cross-section reconciliation

Spot-check that §3's named investors intersect with `08c_capital_investor_fit.md`'s comparable-rounds named investors. Some overlap is expected (lead investors of comparable rounds = strong §3 candidates).

**Failure mode**: zero overlap AND `08c` had named comparable-rounds investors → funding-sourcing-analyst is not reading upstream artifacts.

## What to inspect after the 3 runs (object-level, not the prior)

Per the workspace contract, **do not update the calibration prior at n=3** — sampling variance dominates. Instead, check:

1. **Rubric trigger matches the verdict reason**: open each `10_verdict.md` SCORECARD → does the "RUBRIC TRIGGER" line match a human-readable explanation in the KILLER FINDING?
2. **Top-10 load-bearing KPIs are decisive**: the SCORECARD's top-10 should clearly drive the verdict; if half are noise, the synthesizer is mis-ranking.
3. **Regex-audit caught real Source Protocol violations**: search the artifacts for `[SOURCE-DISCIPLINE-FAILURE]` flags. If never present across 3 audits, either the agents are flawless (unlikely) or the audit is too lax — tighten the regex.
4. **Cross-step numeric reconciliation fired**: check `08_business.md`'s Cross-agent reconciliation block in each audit. `[RECONCILE]` flags should appear in at least one of the three, and the verdict-synthesizer should explain them.
5. **Self-RAG retrieve-critique-requery actually ran**: each artifact's "Verification log (CoVe + Self-RAG)" section should show real re-fetches with confirmation/revision marks. If always just "confirmed" with no revisions, the agents are skipping critique-of-span.
6. **Sentence-level grounding flagged ≥1 numeric claim as weak**: PRM-style grounding should catch some weak citations across the 3 audits.
7. **Scale-mode logic actually changed Seed 2's verdict**: this is the discrimination test. The L1 SCORECARD and L3 SCORECARD on the same compliance-audit seed MUST differ — verdict, top-10 KPIs, RUBRIC TRIGGER, and Tag re-evaluation log should all reflect the scale difference. If they're identical, the scale_mode field isn't flowing through state.yaml → agent briefs → synthesizer.
8. **L1 default applied where flag absent**: any audit run without `--scale` should have `scale_mode: L1` in state.yaml (either from the Step 0.5 AskUserQuestion or from the default).
9. **Calibration JSONL has scale_mode field**: each line in `audits/_calibration.jsonl` should have `"scale_mode":"L1|L2|L3"`. Missing field = bug.
10. **Phase C — Step 13 auto-prompt fired on GO/PIVOT**: in the Seed 2 L1 audit (and any other GO/PIVOT verdict), the wizard should have shown the 4-option `AskUserQuestion` for "Run funding research now?". If absent → Step 13 dispatch logic isn't wired in `idea_audit.md`.
11. **Phase C — `11_funding.md` 4-section completeness**: §1 grants · §2 angels · §3 VCs · §4 anchor procurement. Each section either has named entries OR an explicit `[NONE]` with `What I couldn't find` block explaining why. Empty silent section = regex audit didn't fire.
12. **Phase C — frontmatter freshness fields**: `11_funding.md` has `funding_data_as_of` and `staleness_warning_after` (data + 180d). Missing = the agent skipped freshness frontmatter; resume staleness hook will fail.
13. **Phase C — no personal emails in `11_funding.md`**: scan for `\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b`. Any hit on an individual (angel/partner) row → `[BANNED-CONTACT-INFO]` regex audit failed.
14. **Phase C — state.yaml.steps[13] entry present**: every audit (regardless of verdict) should have a Step 13 entry with status `pending|skipped|done`. Missing entry = `state.yaml` init template wasn't updated.

## What to send back if something is off

If any of the failure modes above appears, the most useful debugging information:

- The full `state.yaml` of the affected audit
- The first 100 lines of the agent's artifact that failed
- The wizard's output for that step (the printed checkpoint block)

## Once B.6 passes

The system is calibrated to the point where audits 4+ can be done with confidence. After n=10 Phase-B audits, the synthesizer will start using the running distribution as the calibration prior instead of the tentative anchor — per CLAUDE.md.

## Reference

- Workspace contract: `/home/atgu/Projects/Ideas/CLAUDE.md`
- Plan (architectural): `/home/atgu/.claude/plans/i-want-to-create-fuzzy-goblet.md`
- Calibration ledger: `/home/atgu/Projects/Ideas/audits/_calibration.jsonl`
