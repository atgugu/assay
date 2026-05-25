---
description: Read-only status report for an existing audit — prints the SCORECARD-so-far + step progress + running tag tally + missing-step list. No agent dispatches, no writes. Useful between sessions to recall where an audit stands.
argument-hint: "<slug-or-audit-path>  e.g. predictive-crowd-movement | audits/2026-05-25_predictive-crowd-movement"
allowed-tools: Read, Bash(ls:*), Bash(cat:*), Bash(grep:*), Bash(wc:*), Bash(test:*), Bash(date:*), Bash(awk:*), Bash(sort:*), Bash(head:*), Bash(tail:*)
model: claude-opus-4-7
---

## Context

- Working directory: !`pwd`
- Today: !`date +%Y-%m-%d`
- audits/ dir: !`ls /home/atgu/Projects/Ideas/audits/ 2>/dev/null | grep -v '^_\|^\\.' | wc -l | xargs -I{} echo "{} existing audits"`

## Task

Print a read-only status block for audit **$ARGUMENTS**. No agent calls, no file writes.

## Step 1 — Resolve target audit

Accept either:
- A slug (e.g., `predictive-crowd-movement`) — find by listing `audits/` for matching slug
- An audit path (e.g., `audits/2026-05-25_predictive-crowd-movement`)
- An absolute path

If multiple audits match a slug (different dates), present the user with `AskUserQuestion` to pick one. If no match, list the 5 most recent audits and exit.

## Step 2 — Read state.yaml + artifacts

Read `audits/<slug>/state.yaml`. Extract:
- created / last_updated
- geo, depth, wizard_version
- For each step (1–12): status (pending / done / stub-skipped / aborted), timestamp
- running_tags counts
- provisional_verdict + provisional_confidence
- final_verdict + final_confidence (if Step 12 done)
- user_context_injected (if any)

## Step 3 — Print the status block

Format:

```
─── Audit status: <slug> ────────────────────────────────────────
Path:            audits/<YYYY-MM-DD>_<slug>/
Created:         <ISO>          Last updated: <ISO>
Geo:             <EU27|...>     Depth: <quick|deep|paranoid>
Wizard version:  <phase-A|phase-B>

Step progress:
  Step  1 (seed):         done (<timestamp>)
  Step  2 (clarify):      done
  Step  3 (falsify):      done | skipped (--no-pre-register)
  Step  4 (triage):       done — TRIAGE VERDICT: <...>, fatal_finding: <...>
  Step  5 (market):       done | pending | stub-skipped
  Step  6 (competition):  ...
  Step  7 (customer):     ...
  Step  8 (regulatory):   done — EU_AI_ACT_CLASS: <...>
  Step  9 (technical):    ...
  Step 10 (business):     ...
  Step 11 (redteam):      ...
  Step 12 (verdict):      done — VERDICT: <...>, Confidence: <...>

Running tag tally:    FATAL: x   BLOCKER: y   RISK: z   ADVANTAGE: w
Provisional verdict:  <...> (<confidence>) [if Step 12 not yet done]
Final verdict:        <...> (<confidence>) [if Step 12 done]

Source quality:
  - Total cited sources: <N> (parsed from sources.md)
  - Primary: <P>   Secondary: <S>   Unverified: <U>
  - WebFetch-OK: <yes / N failures>

Missing/incomplete artifacts:
  <list of files expected but not present>

User context injected:
  <list of injections from state.yaml>

Reconciliation flags (if Step 12 done): <count>

Next suggested action:
  - If pending steps remain: `/idea_audit --resume <slug>` to continue
  - If final verdict written: read audits/<slug>/10_verdict.md for the scorecard
  - If verdict is NO_GO/PIVOT: `/idea_verdict --pivot <slug>` for adjacent ideas
─────────────────────────────────────────────────────────────────
```

## Step 4 — Print the SCORECARD if it exists

If `audits/<slug>/10_verdict.md` exists, print its SCORECARD block (everything between the first and second `═══════` lines).

## Avoid

- Dispatching any agent (this is read-only)
- Writing any file (no exceptions — even fixing parsing errors in `state.yaml` should be reported, not silently fixed)
- Confirming user-injected context as "validated" — it's just whatever the user typed

## Related

- `/idea_audit --resume <slug>` — continue an incomplete audit
- `/idea_verdict <slug>` — regenerate verdict from existing artifacts
- `/idea_verdict --pivot <slug>` — generate adjacent ideas from a NO_GO/PIVOT
