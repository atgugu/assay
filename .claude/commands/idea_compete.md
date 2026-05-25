---
description: Standalone competitive landscape via the competitive-landscape-analyst agent — direct + indirect + adjacent competitors, funding/HC/revenue per competitor, top-3 concentration, named moat type, incumbent response forecast, M&A activity 24mo.
argument-hint: "<slug-or-seed>  [--geo=EU27|<cc>|global]  [--standalone-out=<path>]"
allowed-tools: Read, Write, Bash(ls:*), Bash(test:*), Bash(date:*), Bash(mkdir:*), Bash(grep:*), Bash(cat:*), Agent, AskUserQuestion, WebSearch, WebFetch
model: claude-opus-4-7
---

## Context

- Today: !`date +%Y-%m-%d`
- CLAUDE.md present: !`test -f /home/atgu/Projects/Ideas/CLAUDE.md && echo YES || echo "NO — run /idea_init"`

## Task

Run competitive landscape analysis for **$ARGUMENTS**.

## Step 0 — Resolve target

Same UPDATE/STANDALONE logic as `/idea_market`. Parse `--geo`.

## Step 1 — Prepare brief

```
audit_dir: <resolved path>
slug: <slug>
geo: <geo>

Clarified problem (from 01_clarification.md):
<quote>

Market context (from 03_market.md if exists — for SAM / growth):
<quote relevant sections>

Your structured task:
Produce 04_competition.md per your file's "Output schema — 04_competition.md" section.
- ≥3 direct competitors with funding/HC/revenue/positioning (Crunchbase / S-1 / LinkedIn cited)
- Indirect competitors (status-quo workarounds named)
- 2–5 adjacent threats from BigCo with bundling prediction + timeline
- Top-3 concentration %
- Switching cost analysis
- Named moat type (NOT "AI-powered" — that's FATAL)
- Incumbent response forecast table
- M&A activity 24mo

Output path: audits/<slug>/04_competition.md (or --standalone-out)

Source Protocol §§1–8, Self-RAG, 5 closing blocks.

[USER-STATED CONTEXT — apply skeptical lens — if any]:
```

## Step 2 — Dispatch + audit

Agent `competitive-landscape-analyst`. Audit: ≥3 competitors with cited funding/HC; named moat type that is not "AI"; incumbent table with named companies.

## Step 3 — Update state + summary

UPDATE state.yaml step 6 → done. Summary:

```
─── /idea_compete summary ─────────────────────────────────────
Slug:                <slug>
Direct competitors:  <N> ([list top 3 with funding])
Indirect/status quo: <named>
BigCo threats:       <named>
Top-3 concentration: <%>
Switching cost:      <low/med/high>
Named moat type:     <type> · [<TAG>]
Incumbent response:  <fastest predicted move>
M&A 24mo:            <count> deals, median multiple <X>x

Tag tally: FATAL: x  BLOCKER: y  RISK: z  ADVANTAGE: w

Next suggested action:
  - In wizard: continue /idea_audit Step 7 (Customer)
  - Standalone: /idea_customer for the same slug
─────────────────────────────────────────────────────────────────
```

## Avoid

- "No competitors found" without showing the 5–10 search angles attempted
- Citing competitor revenue/funding/HC without WebFetch + access date
- "AI-powered" or vague moat accepted (`[FATAL]` per workspace contract)

## Related

- `/idea_audit` — wires this as Step 6
- `/idea_market` — provides SAM context
- `/idea_customer` — next stage
