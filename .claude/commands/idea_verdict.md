---
description: Standalone verdict synthesis via verdict-synthesizer — reads all audit artifacts, applies the controlled-vocabulary rubric deterministically, runs cross-step numeric reconciliation (Step C.5), Multi-Agent Reflexion (Step F.5), pro-GO/anti-GO adversarial debate, calibration check (filtered to phase-B), and produces 10_verdict.md with SCORECARD + decision frame + cheapest experiment + VC narrative draft (for GO/PIVOT). Supports `--pivot` (regenerate 3-5 adjacent ideas for a NO_GO/PIVOT) and `--partial` (verdict from incomplete evidence with low confidence).
argument-hint: "<slug>  [--pivot]  [--partial]  [--regret]"
allowed-tools: Read, Write, Edit, Bash(ls:*), Bash(test:*), Bash(date:*), Bash(grep:*), Bash(cat:*), Bash(wc:*), Bash(awk:*), Bash(tail:*), Bash(jq:*), Agent, AskUserQuestion
model: claude-opus-4-7
---

## Context

- Today: !`date +%Y-%m-%d`
- audits/ dir: !`ls /home/atgu/Projects/Ideas/audits/ 2>/dev/null | grep -v '^_\|^\\.' | wc -l | xargs -I{} echo "{} existing audits"`
- _calibration.jsonl entries: !`wc -l < /home/atgu/Projects/Ideas/audits/_calibration.jsonl 2>/dev/null || echo 0`

## Task

Run verdict synthesis for **$ARGUMENTS**.

## Step 0 — Resolve mode

Parse args:
- `<slug>` only → REGENERATE verdict from existing artifacts
- `<slug> --pivot` → PIVOT mode: read existing `10_verdict.md`, generate 3–5 adjacent ideas
- `<slug> --partial` → PARTIAL mode: produce verdict from whatever artifacts exist (low confidence by default)
- `<slug> --regret` → REGRET mode: mark a past audit in `_calibration.jsonl` as `"reversed": true` with reason

## Step 1 — REGENERATE mode (default)

### Step 1.A — Pre-flight check

Read `audits/<slug>/state.yaml`. Verify expected artifacts exist:
- `00_seed.md`, `01_clarification.md`, `02_triage.md`, `03_market.md`, `04_competition.md`, `05_customer.md`, `06_regulatory.md`, `07_technical.md`, `08_business.md`, `09_redteam.md`, `sources.md`
- Optional: `01b_falsifier.md`, sub-files `08a/08b/08c/09a/09b`

If artifacts are missing, AskUserQuestion: "Missing: <list>. Proceed in --partial mode? Yes / Run /idea_audit --resume first / Cancel."

### Step 1.B — Prepare brief for verdict-synthesizer

```
Brief for verdict-synthesizer:

audit_dir: /home/atgu/Projects/Ideas/audits/<slug>/
slug: <slug>
geo: <from state.yaml>
depth: <from state.yaml>
wizard_version: <from state.yaml>

Read all artifacts in the audit dir in order (see your file's "How you operate" Step A).

Apply your workflow in full:
- Step A — Read every artifact
- Step B — Extract tagged findings into flat table
- Step C — Check pre-registered kill criteria (01b_falsifier.md)
- Step C.5 — Cross-step numeric reconciliation (build the comparison table)
- Step D — Pro-GO / anti-GO adversarial debate (in writing)
- Step E — Apply Verdict Optimization Target gate (speed-to-revenue + investor-attractiveness + defensibility growth path)
- Step F — Assign verdict + confidence per the rubric
- Step F.5 — Multi-Agent Reflexion check (read last 5–10 entries of _calibration.jsonl; check for "reversed" flags with similar tag-tally signature)
- Step G — Calibration check (FILTER _calibration.jsonl to wizard_version: phase-B before computing running distribution; state "n < 10; prior unchanged" if applicable)
- Step H — Write 10_verdict.md with SCORECARD as headline, then adversarial debate block, then VC narrative draft (if verdict ∈ {GO, PIVOT})
- Step I — Append one line to _calibration.jsonl with full schema (date, slug, verdict, confidence, geo, depth, wizard_version, steps_completed, reconciliation_flags)

[USER-STATED CONTEXT — apply skeptical lens — if any]:
```

### Step 1.C — Dispatch + audit

Dispatch via Agent tool with `subagent_type: verdict-synthesizer`. Audit specific: SCORECARD block is the first content (no preamble); VERDICT line ∈ {GO, PIVOT, NO_GO, DEFER}; Confidence ∈ {high, med, low}; adversarial debate block present (both pro-GO and anti-GO cases written); for GO/PIVOT: VC narrative draft present; `_calibration.jsonl` has one new line.

### Step 1.D — Print to user

Print the SCORECARD block (between the first and second `═══════` lines). Then print full path to `10_verdict.md`, next-action suggestion.

## Step 2 — PIVOT mode (--pivot flag)

Read existing `10_verdict.md`. Read the killer findings (the `KILLER FINDING` section + any `[FATAL|BLOCKER]` tags). Brief verdict-synthesizer in PIVOT mode:

```
PIVOT-mode brief:

audit_dir: <path>
slug: <slug>

Killer findings from 10_verdict.md:
<quote KILLER FINDING + top BLOCKER/FATAL tags>

Adjacent context to suggest 3-5 pivot directions:
- Customer pain still applies in 05_customer.md
- Different customer segment with same pain
- Different sales motion that fixes the GTM/CAC issue
- Different geography where regulatory burden is lower
- B2B pivot of B2C idea (or vice versa)
- Different price point that fixes LTV/CAC

Your task:
Generate 3-5 ADJACENT SEEDS that might evade the killer findings.
Each: one-line description + which killer it evades + which new killer it might introduce + confidence (high/med/low) + recommended next step (re-audit / explore / skip).

Write to audits/<slug>/10b_pivots.md.
```

Dispatch. Print 3-5 pivot seeds.

## Step 3 — PARTIAL mode (--partial flag)

Brief synthesizer with note that this is partial evidence. Confidence is `low` unless all 3 optimization-target gates are present. SCORECARD lists missing steps explicitly. Cheapest discriminating experiment addresses the largest unknown.

## Step 4 — REGRET mode (--regret flag)

Read `_calibration.jsonl`. Find the line matching `<slug>`. Append `"reversed": true, "reversed_at": "<today>", "reason": "<user-supplied>"`. AskUserQuestion to capture the reason.

This marks the past audit for the Multi-Agent Reflexion check (Step F.5) — future synthesizer runs will read this as guidance.

## Step 5 — Update state.yaml (REGENERATE mode)

Mark step 12 → done with timestamp. Set `final_verdict`, `final_confidence`.

## Avoid

- Issuing verdict without reading every available artifact (Step A)
- Skipping the adversarial debate block (Step D — the anti-bias step)
- Issuing GO without the Verdict Optimization Target gate (Step E) passing (speed + investor-attractive + defensibility growth)
- Skipping cross-step numeric reconciliation (Step C.5)
- Using unfiltered `_calibration.jsonl` for the running distribution (must filter to wizard_version: phase-B)
- Updating the calibration prior at n < 10 (sampling variance dominates)
- Hedging the verdict ("it depends") — must commit or explicitly DEFER with named trigger

## Related

- `/idea_audit` — wires this as Step 12
- `/idea_status <slug>` — read-only status before/after running verdict
- `/sci_falsify` — pre-registers kill criteria that this verdict checks
- `/sci_ledger` — analogous append-only verdict ledger for the science toolkit
