---
description: Standalone market sizing — TAM/SAM/SOM with bottom-up math, growth, "why now" trigger, demand signals — via the market-size-analyst agent. Use against an existing audit slug to (re-)produce 03_market.md, or with a fresh seed to produce a one-off market analysis.
argument-hint: "<slug-or-seed>  [--geo=EU27|<cc>|+US|global]  [--standalone-out=<path>]  e.g. predictive-crowd-movement | \"AI compliance tool for German SaaS\""
allowed-tools: Read, Write, Bash(ls:*), Bash(test:*), Bash(date:*), Bash(mkdir:*), Bash(pwd:*), Bash(grep:*), Bash(cat:*), Agent, AskUserQuestion, WebSearch, WebFetch
model: claude-opus-4-7
---

## Context

- Working directory: !`pwd`
- Today: !`date +%Y-%m-%d`
- CLAUDE.md present: !`test -f /home/atgu/Projects/Ideas/CLAUDE.md && echo YES || echo "NO — run /idea_init"`
- audits/ dir: !`ls /home/atgu/Projects/Ideas/audits/ 2>/dev/null | grep -v '^_\|^\\.' | wc -l | xargs -I{} echo "{} existing audits"`

## Task

Run the market-sizing analysis standalone for **$ARGUMENTS**. Defaults: `--geo=EU27`.

## Step 0 — Parse args + resolve target

Determine mode:

| Pattern | Mode | Action |
|---|---|---|
| First arg is an existing audit slug | UPDATE | Re-produce `audits/<slug>/03_market.md`, possibly overwriting a stub |
| First arg is a seed (quoted text or short phrase) | STANDALONE | Create temporary audit dir or use `--standalone-out` path |
| `--standalone-out=<path>` flag | STANDALONE-FIXED | Write to specified path |

Parse `--geo` (default `EU27`).

If UPDATE mode and `03_market.md` already exists, AskUserQuestion: "Overwrite existing market artifact? Yes / No / Diff first / Cancel".

## Step 1 — Resolve dependencies (UPDATE mode only)

For UPDATE mode, market-size-analyst's brief benefits from `01_clarification.md`. Check it exists; if not, suggest running `/idea_audit` first (Steps 1–2) to produce it, OR proceed with the slug as the only context.

## Step 2 — Prepare the sanitized brief

Follow the **Standard Step Driver** pattern from `idea_audit.md`'s "Standard Step Driver" section:

```
Brief for market-size-analyst:

audit_dir: <resolved path>
slug: <slug>
geo: <geo>
depth: standalone (not the same as deep/quick/paranoid wizard depths)

Clarified problem (from 01_clarification.md, OR from the seed text):
<quote>

Pre-registered kill criteria (from 01b_falsifier.md if exists):
<quote any market-relevant ones>

Your structured task:
Produce 03_market.md following your file's "Output schema" section. Apply the
Source Protocol, Self-RAG (Agentic Retrieval Loop), the 5 anti-confirmation-bias
closing blocks, and tag every load-bearing KPI with [FATAL|BLOCKER|RISK|ADVANTAGE].

Output:
  path: audits/<slug>/03_market.md  (UPDATE) or <--standalone-out>  (STANDALONE)
  schema: see your "Output schema — 03_market.md" section

Regex audit will check Source Protocol §§1–8, 5 closing blocks, banned-language, tag extractability.

[USER-STATED CONTEXT — apply skeptical lens — if any]:
<any free-text from user, optional>
```

## Step 3 — MAST pre-dispatch check

Validate required fields in the brief (audit_dir, slug, geo, structured_question, output_path). Refuse to dispatch if any are missing.

## Step 4 — Dispatch + audit

Dispatch via Agent tool with `subagent_type: market-size-analyst`. After return, regex-audit per Standard Step Driver §3. Re-invoke once on failure; commit with `[SOURCE-DISCIPLINE-FAILURE]` on second failure.

## Step 5 — Extract + update state.yaml (UPDATE mode)

Parse `[FATAL|BLOCKER|RISK|ADVANTAGE]` from `03_market.md`. Update `state.yaml`:
- Mark step 5 (market) as `done` with timestamp
- Update `running_tags`
- Update `provisional_verdict` via simplified rubric

(For STANDALONE mode, no state.yaml exists; skip this step.)

## Step 6 — Print summary

Compact summary block:

```
─── /idea_market summary ──────────────────────────────────────
Slug:       <slug>
Geo:        <geo>
Artifact:   <path>

Top KPIs:
  TAM:               €<X> · <confidence>
  SAM:               €<X>
  SOM (yr3):         €<X> · [<TAG>]
  Growth CAGR 3yr:   <%>  · [<TAG>]
  "Why now":         <trigger> · [<TAG>]
  Quote-attributed demand signals: <count> sources

Tag tally this artifact: FATAL: x  BLOCKER: y  RISK: z  ADVANTAGE: w

Source quality:
  Primary: <P>   Secondary: <S>   Unverified-fetch: <U>
  Self-RAG re-queries triggered: <N>
  [SOURCE-DISCIPLINE-FAILURE]: <yes/no>

Agent flagged for your attention:
  - "<quote of any negative-results note>"

Next suggested action:
  - In a wizard run: continue to /idea_audit Step 6 (Competition)
  - Standalone: review the artifact + /idea_compete for the same slug
─────────────────────────────────────────────────────────────────
```

## Avoid

- Skipping the regex audit (the Source Protocol enforcement only works if it runs)
- Letting the agent receive the user's prior conversation — only the sanitized brief
- Editing `03_market.md` after the agent writes it; if the artifact needs change, re-invoke the agent with refinement
- Pretending an estimate is a fact — `[ESTIMATE]` flag must remain visible

## Related

- `/idea_audit` — the full wizard (Step 5 dispatches this same agent)
- `/idea_compete` — competitive landscape, complementary to market sizing
- `/idea_customer` — customer-segment analysis, complementary
- `/idea_verdict <slug>` — once all stages are done, generate the verdict
