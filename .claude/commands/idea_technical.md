---
description: Standalone technical feasibility via technical-feasibility-engineer under the Capability Profile (elite AI-augmented solo founder; no team-hiring in MVP-phase). Time-to-MVP (founder weeks), MVP cash cost € (excl. founder time), time-to-revenue, vendor risk, data availability, infra cost/MAU, certifications cost, "out-of-reach" check (physical/economic constraints only).
argument-hint: "<slug-or-seed>  [--standalone-out=<path>]"
allowed-tools: Read, Write, Bash(ls:*), Bash(test:*), Bash(date:*), Bash(mkdir:*), Bash(grep:*), Bash(cat:*), Agent, AskUserQuestion, WebSearch, WebFetch
model: claude-opus-4-7
---

## Context

- Today: !`date +%Y-%m-%d`

## Task

Run technical feasibility analysis for **$ARGUMENTS** under the Capability Profile.

## Step 0 — Resolve target (same logic as /idea_market)

## Step 1 — Prepare brief

```
audit_dir: <path>
slug: <slug>

Clarified problem: <quote 01_clarification.md — especially "Build hypothesis (8-week MVP)">
Market/customer context: <quote scale assumptions from 03_market.md if relevant>

Your structured task:
Produce 07_technical.md per "Output schema — 07_technical.md".
- Capability Profile assumed: elite AI-augmented solo founder; no team-hiring in MVP-phase
- Decompose into 5–10 capability blocks (each with founder weeks + cash €)
- Time-to-MVP (founder weeks; sum of blocks)
- MVP cash cost € EXCLUDING founder time (tools, infra, data, contracted help)
- Time-to-revenue (months from project start to first paid customer)
- Tech stack vendor risk per material dependency + migration path
- Data availability + acquisition time
- Infra cost/MAU at 10k/100k/1M scale
- Latency/reliability/certification requirements (SOC2/ISO27001/HIPAA — € + months on critical path)
- "Out-of-reach" check: physical OR economic constraints only — "ML is hard" does NOT qualify
- Capability Profile guardrails section (what is NOT a hard problem)

Source Protocol §§1–8, Self-RAG, 5 closing blocks.

[USER-STATED CONTEXT — apply skeptical lens — if any]:
```

## Step 2 — Dispatch + audit

Agent `technical-feasibility-engineer`. Audit specific: capability blocks itemized (5–10); MVP cash explicitly EXCLUDES founder time; "Out-of-reach" section present with explicit physical/economic constraint OR "none under Capability Profile" + reasoning; "Capability Profile guardrails" section present.

## Step 3 — Update state + summary

UPDATE state.yaml step 9 → done. Summary:

```
─── /idea_technical summary ───────────────────────────────────
Slug:               <slug>
Time-to-MVP:        <X> founder weeks · [<TAG>]
MVP cash cost:      €<Y> (excl. founder time) · [<TAG>]
Time-to-revenue:    <Z> months · [<TAG>]
Vendor risk:        <low|med|high — top dep: <name>>
Data availability:  <named source + acquisition time>
Infra cost/MAU @1M: €<W>
Cert cost / months: <SOC2: €X+Ymo, ISO27001: ...>
"Out-of-reach":     <none under Capability Profile | named physical/economic constraint>

Tag tally: FATAL: x  BLOCKER: y  RISK: z  ADVANTAGE: w

Next: /idea_business (Step 10) → /idea_redteam (Step 11)
─────────────────────────────────────────────────────────────────
```

## Avoid

- Tagging "frontier ML" or "complex software" as `[BLOCKER]` under Capability Profile
- Including founder time in MVP cash cost
- Stating time-to-MVP without the per-block breakdown
- Confusing time-to-MVP with time-to-revenue
- Skipping the "Out-of-reach" check or the "Capability Profile guardrails" section

## Related

- `/idea_audit` — wires this as Step 9
- `/idea_business` — uses MVP cash + time-to-revenue as inputs
- `/idea_regulatory` — sector certifications cost feeds back here
