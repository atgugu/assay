---
description: Standalone regulatory analysis via regulatory-compliance-analyst — EU AI Act classification (with machine-readable EU_AI_ACT_CLASS line), GDPR exposure, sector certifications (MDR/IVDR/MiFID/NIS2/DSA/DMA/SOC2/ISO27001), national variation, data residency, time-to-clearance, global pivot.
argument-hint: "<slug-or-seed>  [--geo=EU27|<cc>|+US|global]  [--standalone-out=<path>]"
allowed-tools: Read, Write, Bash(ls:*), Bash(test:*), Bash(date:*), Bash(mkdir:*), Bash(grep:*), Bash(cat:*), Agent, AskUserQuestion, WebSearch, WebFetch
model: claude-opus-4-7
---

## Context

- Today: !`date +%Y-%m-%d`

## Task

Run regulatory analysis for **$ARGUMENTS**.

## Step 0 — Resolve target (same logic as /idea_market)

## Step 1 — Prepare brief

```
audit_dir: <path>
slug: <slug>
geo: <geo>

Clarified problem: <quote 01_clarification.md>
Technical context: <quote 07_technical.md if exists — needed for AI Act applicability>

Your structured task:
Produce 06_regulatory.md per "Output schema — 06_regulatory.md".
- EU AI Act classification with machine-readable `EU_AI_ACT_CLASS:` line
  (minimal | limited | high-risk | unacceptable | not-in-scope)
- Quote specific Article/Annex text via Self-RAG (EUR-Lex Reg. 2024/1689)
- GDPR exposure (low/med/high) + DPIA required (yes/no, citing Art. 35)
- Sector-specific certifications needed
- Compliance cost € to launch + €/yr ongoing
- Time-to-regulatory-clearance months on critical path
- Data residency requirement
- National variation across EU27 if --geo=EU27
- Global pivot if --geo=+US or global

Source Protocol §§1–8, Self-RAG, 5 closing blocks.

[USER-STATED CONTEXT — apply skeptical lens — if any]:
```

## Step 2 — Dispatch + audit

Agent `regulatory-compliance-analyst`. **Critical audit**: the regex `^EU_AI_ACT_CLASS: (minimal|limited|high-risk|unacceptable|not-in-scope)$` MUST match a line near the top of `06_regulatory.md`. If absent, re-invoke with feedback.

## Step 3 — Auto-skip check (UPDATE mode only)

If running inside `/idea_audit` UPDATE mode AND `EU_AI_ACT_CLASS: unacceptable` (Art. 5 prohibition): print warning + trigger auto-skip to Step 12 with NO_GO verdict citing the Art. 5 prohibition. (Standalone mode does not auto-skip.)

## Step 4 — Update state + summary

UPDATE state.yaml step 8 → done. Summary:

```
─── /idea_regulatory summary ──────────────────────────────────
Slug:                <slug>
EU_AI_ACT_CLASS:     <minimal|limited|high-risk|unacceptable|not-in-scope>
                     · [<TAG>] · Article cited: <Art. X>
GDPR exposure:       <low|med|high>  DPIA required: <yes|no>
Sector certs needed: <named list>
Compliance € launch: <€X>
Compliance €/yr:     <€Y>
Time-to-clearance:   <months>  (critical-path blocker for first revenue?)
Data residency:      <EU-only|in-country|global>

Tag tally: FATAL: x  BLOCKER: y  RISK: z  ADVANTAGE: w

Next: /idea_technical (Step 9) → /idea_business (Step 10)
─────────────────────────────────────────────────────────────────
```

## Avoid

- Emitting `EU_AI_ACT_CLASS:` without quoting the specific Article/Annex text
- Conflating "uses AI" with "in scope for AI Act"
- Paraphrasing regulation from training-data memory — WebFetch the current EUR-Lex text
- Citing "the AI Act says X" without article number

## Related

- `/idea_audit` — wires this as Step 8 (auto-skips on `unacceptable`)
- `/idea_technical` — provides tech-stack context for AI Act applicability
