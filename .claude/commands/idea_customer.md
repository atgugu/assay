---
description: Standalone customer-segment analysis via customer-segment-analyst — pain severity 1-10 evidence-backed, pain frequency, current cost of problem €/yr, WTP €/yr anchored to named analog ARPU/ACV, time-to-value, buyer ≠ user influence map for B2B. Real customer voices quote-attributed (G2/Reddit/forums/surveys).
argument-hint: "<slug-or-seed>  [--geo=EU27|<cc>]  [--standalone-out=<path>]"
allowed-tools: Read, Write, Bash(ls:*), Bash(test:*), Bash(date:*), Bash(mkdir:*), Bash(grep:*), Bash(cat:*), Agent, AskUserQuestion, WebSearch, WebFetch
model: claude-opus-4-7
---

## Context

- Today: !`date +%Y-%m-%d`

## Task

Run customer-segment analysis for **$ARGUMENTS**.

## Step 0 — Resolve target (same logic as /idea_market)

## Step 1 — Prepare brief

```
audit_dir: <path>
slug: <slug>
geo: <geo>

Clarified problem: <quote 01_clarification.md>
Market context: <quote relevant from 03_market.md>

Your structured task:
Produce 05_customer.md per "Output schema — 05_customer.md".
- ≥5 real customer voices quote-attributed (G2, Reddit, sector forums, surveys)
- Pain severity 1–10 EVIDENCE-BACKED (not adjective-based)
- Pain frequency (daily/weekly/monthly/yearly)
- Current cost of problem €/yr per customer
- WTP €/yr anchored to ≥2 named analog companies' ARPU/ACV
- Time-to-value days
- B2B: buyer ≠ user influence map

Source Protocol §§1–8, Self-RAG, 5 closing blocks.

[USER-STATED CONTEXT — apply skeptical lens — if any]:
```

## Step 2 — Dispatch + audit

Agent `customer-segment-analyst`. Audit specific: ≥5 quote-attributed voices; WTP anchored to named analogs; B2B has influence map.

## Step 3 — Update state + summary

UPDATE state.yaml step 7 → done. Summary:

```
─── /idea_customer summary ────────────────────────────────────
Slug:                  <slug>
Pain severity:         <X>/10 · [<TAG>]
Pain frequency:        <daily|weekly|monthly|yearly>
Current cost €/yr:     €<Y>
WTP estimate:          €<Z>/yr  (anchored to <named analogs>)
Time-to-value:         <days>
Buyer ≠ user mapped:   <yes/no/n/a>
Quote-attributed pain: <N> distinct sources

Tag tally: FATAL: x  BLOCKER: y  RISK: z  ADVANTAGE: w

Next: /idea_regulatory (Step 8) → /idea_technical (Step 9)
─────────────────────────────────────────────────────────────────
```

## Avoid

- Founder-paraphrased pain treated as customer voice → `[UNVALIDATED-PAIN]`
- WTP without ≥2 named analog ARPU/ACV citations
- Skipping the buyer ≠ user map on B2B audits (`[BLOCKER]`)

## Related

- `/idea_audit` — wires this as Step 7
- `/idea_market` — sized the segment
- `/idea_business` — uses WTP for unit economics
