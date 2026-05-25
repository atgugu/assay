---
description: Standalone red-team via red-team-analyst in BOTH modes (DA + premortem) serially, then wizard-merges into 09_redteam.md with the Cross-mode synthesis block (criticisms matching trajectories = highest-priority risks; trajectories not in DA = blind spots).
argument-hint: "<slug-or-seed>  [--only=DA|premortem]  [--standalone-out=<path>]"
allowed-tools: Read, Write, Bash(ls:*), Bash(test:*), Bash(date:*), Bash(mkdir:*), Bash(grep:*), Bash(cat:*), Agent, AskUserQuestion, WebSearch, WebFetch
model: claude-opus-4-7
---

## Context

- Today: !`date +%Y-%m-%d`

## Task

Run red-team analysis (both modes by default) for **$ARGUMENTS**.

## Step 0 — Resolve target + mode

Same UPDATE/STANDALONE logic as `/idea_market`. Parse `--only`:
- Default: dispatch DA mode + premortem mode (serially)
- `--only=DA`: dispatch only DA-mode → `09a_da.md`
- `--only=premortem`: dispatch only premortem-mode → `09b_premortem.md`

## Step 1.A — DA-mode dispatch

```
Brief for red-team-analyst:

mode: DA

audit_dir: <path>
slug: <slug>

All prior artifacts as quoted context (especially 04_competition.md, 05_customer.md, 06_regulatory.md, 07_technical.md, 08_business.md).

Your structured task:
Produce 09a_da.md per "Output schema — 09a_da.md (DA-mode)".
- Target restated (1 paragraph)
- Steel-man (3-5 sentences citing ADVANTAGEs from prior artifacts — MANDATORY before any criticism)
- 2-4 strongest criticisms across DISTINCT categories
  Each: severity tag + specific evidence + refutation condition + cost to address
- Incumbent-response table (NAMED companies + predicted move + timeline + recent precedent)
- 1-sentence verdict on direction (continue / modify / pivot)
- Self-check: am I the wrong critic (named bias / blind spot)?

Source Protocol §§1–8, Self-RAG, 5 closing blocks.
```

Dispatch + regex-audit (steel-man present before any criticism; 2-4 criticisms; named incumbents).

## Step 1.B — Premortem-mode dispatch

```
Brief for red-team-analyst:

mode: premortem

audit_dir: <path>
slug: <slug>

All prior artifacts as quoted context.

Your structured task:
Produce 09b_premortem.md per "Output schema — 09b_premortem.md".
- Scene: "It is <today + 3 years>. The company failed."
- 3-5 failure trajectories across DISTINCT mechanisms (PMF / burn / incumbent / regulation / founder / technical / timing / distribution)
  Each: probability (l/m/h calibrated, not pessimistic) + consequence + LEADING INDICATOR VISIBLE TODAY + cheapest mitigation
- Rank by P × consequence
- Single action this week — what would the founder do RIGHT NOW if they took this seriously?

Source Protocol §§1–8, Self-RAG, 5 closing blocks.
```

Dispatch + regex-audit (3-5 trajectories; each with named leading indicator visible TODAY; ranked by P × consequence).

## Step 2 — Wizard-merge into `09_redteam.md`

```markdown
# 09 — Red team

## Index
- §09a Devil's Advocate
- §09b Premortem

## Cross-mode synthesis (wizard-written)

### High-priority risks (criticisms in 09a matching trajectories in 09b)
| 09a criticism | 09b trajectory | Combined severity |

### DA-only criticisms (covered but not surfaced as trajectory)
<list — usually present-tense problems vs future-tense failure modes>

### Premortem-only trajectories (potential blind spots)
<list — these are failure modes the DA didn't surface as criticism>

---
[concatenated 09a content]
---
[concatenated 09b content]
```

## Step 3 — Update state + summary

UPDATE state.yaml step 11 → done. Summary:

```
─── /idea_redteam summary ─────────────────────────────────────
Slug:               <slug>

DA-mode (09a):
  Steel-man written:  <yes/no>
  Top criticisms:     <N> [F:x  S:y  M:z]
  Verdict on dir.:    continue | modify | pivot

Premortem-mode (09b):
  Failure trajectories: <N>
  Top trajectory:       <named, P×C ranked>
  Single action this week: <quote>

Cross-mode overlap:    <K matched (high-priority risks)>
Blind-spot trajectories: <M>

Tag tally: FATAL: x  BLOCKER: y  RISK: z  ADVANTAGE: w

Next: /idea_verdict (Step 12)
─────────────────────────────────────────────────────────────────
```

## Avoid

- Letting DA-mode attack without writing the steel-man first
- Letting premortem produce trajectories without a leading indicator visible TODAY (unfalsifiable doom)
- Skipping the named-companies requirement in DA-mode incumbent table
- Skipping the wizard-merged Cross-mode synthesis — that's where the signal lives
- Skipping `--only=DA` standalone runs from the workspace contract's discipline rules

## Related

- `/idea_audit` — wires this as Step 11
- `/sci_devils_advocate`, `/sci_pre_mortem` — research-toolkit analogs (conceptually parallel, instantiated separately)
- `/idea_verdict` — consumes both sub-files
