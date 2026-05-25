---
description: Standalone 5-minute kill/keep triage gate via the red-team-analyst agent in quick-mode. Runs the three cheap kill-checks (regulatory blocker, already-commodity, demand-existence) + /sci_sanity_check on numeric claims in the seed. Emits TRIAGE VERDICT: PROCEED | KILL | REFRAME.
argument-hint: "<slug-or-seed>  [--geo=EU27|<cc>]  [--standalone-out=<path>]"
allowed-tools: Read, Write, Bash(ls:*), Bash(test:*), Bash(date:*), Bash(mkdir:*), Bash(grep:*), Bash(cat:*), Agent, AskUserQuestion, WebSearch, WebFetch
model: claude-opus-4-7
---

## Context

- Today: !`date +%Y-%m-%d`
- CLAUDE.md present: !`test -f /home/atgu/Projects/Ideas/CLAUDE.md && echo YES || echo "NO — run /idea_init"`

## Task

Run a 5-minute triage gate for **$ARGUMENTS**.

## Step 0 — Resolve target (UPDATE existing slug vs STANDALONE seed)

Same logic as `/idea_market`. Parse `--geo` (default EU27).

## Step 1 — Prepare the brief

Follow the Standard Step Driver. Critical brief content:

```
mode: quick

audit_dir: <resolved path>
slug: <slug>
geo: <geo>

Clarified problem (from 01_clarification.md if exists; else from raw seed):
<quote>

Your structured task:
Produce 02_triage.md per your file's "Output schema — 02_triage.md (quick-mode)" section.
- Run the 3 cheap kill-checks (regulatory blocker, already-commodity, demand-existence)
- Call /sci_sanity_check on any numeric claims in the seed
- Emit `TRIAGE VERDICT: <PROCEED|KILL|REFRAME>` at the top
- Emit `fatal_finding: <true|false>` at the top
- 5 closing blocks (compressed for quick-mode)

Output path: audits/<slug>/02_triage.md (or --standalone-out)

[USER-STATED CONTEXT — apply skeptical lens — if any]:
<any free-text>
```

## Step 2 — Dispatch + audit

Agent tool with `subagent_type: red-team-analyst`. Regex-audit checks: TRIAGE VERDICT line present, fatal_finding line present, ≥1 cited source per kill-check, 5 closing blocks present (compressed form OK).

## Step 3 — Update state.yaml (UPDATE mode)

Mark step 4 (triage) as `done`. Update `kill_signal` from the `fatal_finding` line.

## Step 4 — Print summary

```
─── /idea_triage summary ──────────────────────────────────────
Slug:                <slug>
TRIAGE VERDICT:      <PROCEED | KILL | REFRAME>
fatal_finding:       <true | false>

Kill-check 1 — Regulatory:        <finding · tag>
Kill-check 2 — Already-commodity: <finding · tag>
Kill-check 3 — Demand existence:  <finding · tag>
sci_sanity_check pass-through:    <pass | fail | n/a>

Tag tally: FATAL: x  BLOCKER: y  RISK: z  ADVANTAGE: w

Next suggested action:
  - PROCEED + UPDATE mode: continue /idea_audit --resume <slug> to Step 5
  - KILL: full /idea_audit will short-circuit on fatal_finding; consider /idea_verdict --pivot
  - REFRAME: refine the seed in ideas.md, then start fresh
─────────────────────────────────────────────────────────────────
```

## Avoid

- Treating triage as a full audit — it's a 5-min gate using surface evidence only
- Setting `fatal_finding: true` without citing a regulatory/market/economic blocker (not just "I have a bad feeling")
- Skipping `/sci_sanity_check` when the seed contains numeric claims

## Related

- `/idea_audit` — wires this as Step 4
- `/idea_market`, `/idea_compete`, `/idea_customer` — the deeper stages that follow PROCEED
- `/sci_sanity_check` — invoked here for numeric pre-filter
