---
description: "Deep, actionable funding research for an idea that has reached a threshold verdict (GO or PIVOT at Step 12). Dispatches `funding-sourcing-analyst` to produce `11_funding.md` with 4 sections of named entities: §1 EU/national grants (deadlines + ticket sizes), §2 angel investors (public access paths), §3 VC firms (thesis-matched, named partners), §4 anchor procurement / development-funded contracts (the discriminator: pays before delivery exists?). Scale-mode-aware emphasis: L1 → §4 primary; L2 → balanced; L3 → §3 primary. Standalone usage on an existing audit dir, or auto-dispatched from `/idea_audit` Step 13 when verdict ∈ {GO, PIVOT}. Refuses `geo=global` (jurisdiction-bound funding). NO_GO audits require `--anchor-only` flag for §4-only consulting-pivot exploration."
argument-hint: "<slug>  [--anchor-only]  [--refresh]  [--no-fetch-budget-override]"
allowed-tools: Read, Write, Edit, Bash(ls:*), Bash(test:*), Bash(date:*), Bash(grep:*), Bash(cat:*), Bash(wc:*), Bash(stat:*), Bash(awk:*), Bash(sed:*), Bash(tail:*), Agent, AskUserQuestion, WebSearch, WebFetch
model: claude-opus-4-7
---

## Context

- Today: !`date +%Y-%m-%d`
- audits/ dir: !`ls /home/atgu/Projects/Ideas/audits/ 2>/dev/null | grep -v '^_\|^\\.' | wc -l | xargs -I{} echo "{} existing audits"`
- _calibration.jsonl entries: !`wc -l < /home/atgu/Projects/Ideas/audits/_calibration.jsonl 2>/dev/null || echo 0`

## Task

Run funding-sourcing research for **$ARGUMENTS**.

This is **Phase C Step 13** of the idea audit pipeline: produce a named-entity funding registry as `11_funding.md` in the audit dir. Triggered conditionally on verdict ∈ {GO, PIVOT} via `/idea_audit` Step 13, or invoked standalone here.

## Step 0 — Parse arguments and resolve mode

Parse args:
- `<slug>` only → DEFAULT mode: full 4-section registry for the audit
- `<slug> --anchor-only` → ANCHOR-ONLY mode: §4 only (consulting-pivot path for NO_GO verdicts)
- `<slug> --refresh` → REFRESH mode: re-run if `11_funding.md` exists and is past `staleness_warning_after`
- `<slug> --no-fetch-budget-override` → EXTEND fetch budget by 50% above scale_mode cap

If multiple flags, combine: `--anchor-only --refresh` is valid.

## Step 1 — Pre-flight

### Step 1.A — Resolve the audit directory

If `<slug>` looks like a path (`audits/<date>_<slug>` or absolute path), use it directly. Otherwise, look up the audit dir from the most recent matching entry in `audits/`:

```bash
ls -td /home/atgu/Projects/Ideas/audits/*_<slug> 2>/dev/null | head -1
```

If no match → `AskUserQuestion`: "No audit dir found for slug '<slug>'. Run `/idea_audit \"<seed>\"` first, or supply the full dir path."

### Step 1.B — Read state.yaml

Extract these fields from `audits/<slug>/state.yaml`:
- `scale_mode` (L1 / L2 / L3)
- `geo` (EU27 / DE / FR / IT / ES / NL / RO / +US / +UK / global)
- `final_verdict` (GO / PIVOT / NO_GO / DEFER) — set by Step 12
- `final_confidence` (high / med / low)
- `steps[13]` if present (status: pending / skipped / done from a prior Step 13 run)

If any required field is missing (`scale_mode` not set; `final_verdict` not set), refuse: "state.yaml is incomplete — Step 12 must complete before Step 13."

### Step 1.C — Refusal checks

**Refusal 1: `geo == global`.** Funding sources are jurisdiction-bound. Emit:

```
Funding research cannot run with geo=global because funding programs are jurisdiction-bound (EXIST=DE, EIC=EU, SBIR=US, BPI=FR, YC=US/global, etc.).
```

Then `AskUserQuestion`:

```
Question: "Which primary geo should the funding research target?"
Options:
  1. EU27 — pan-EU sources (EIC Accelerator, Horizon Europe, EU PCP)
  2. DE — Germany (EXIST, KfW, BMVg)
  3. FR — France (BPI, French Tech grants)
  4. Other (free-text: IT/ES/NL/RO/+US/+UK)
```

Update `state.yaml.geo` to the resolved value (with user permission), then proceed.

**Refusal 2: `final_verdict ∈ {NO_GO, DEFER}` without `--anchor-only`.** Emit:

```
Verdict was <verdict>. Default funding research is disabled because:
- NO_GO: the audit found the idea unviable as a product. Funding for a product company is premature.
- DEFER: the audit named a trigger to wait for. Funding research before that trigger is premature.

Two options:
  1. /idea_funding <slug> --anchor-only
       Explore §4 only: anchor procurement / development-funded contracts that could fund this as a SERVICES play (consulting / paid POC / public RFP).
  2. /idea_verdict --pivot <slug>
       Generate 3–5 adjacent ideas that might evade the killer findings.
```

Then `AskUserQuestion`: pick (1) anchor-only / (2) pivot mode / (3) cancel.

**Refusal 3: `08c_capital_investor_fit.md` missing or stub-marked.** Emit:

```
Funding research depends on 08c_capital_investor_fit.md (named acquirers + comparable rounds as seeds for §3 VCs and §4 anchor list).
That artifact is missing or stub-marked.
Run /idea_audit --resume <slug> to complete Step 10 (Business) first.
```

Exit.

### Step 1.D — Staleness check

If `audits/<slug>/11_funding.md` exists:
- Read frontmatter `funding_data_as_of` and `staleness_warning_after`.
- If today > `staleness_warning_after` AND `--refresh` flag absent: emit warning + `AskUserQuestion`:

```
11_funding.md exists from <funding_data_as_of>. Staleness threshold (180 days) was crossed on <staleness_warning_after>.
Options:
  1. Re-run from scratch (recommended) — equivalent to passing --refresh
  2. Read existing file as-is — return existing data
  3. Cancel
```

If `--refresh` was passed: skip the question, run fresh.

If today ≤ `staleness_warning_after`: print "11_funding.md is current (data_as_of=<date>, fresh)" and exit unless `--refresh`.

## Step 2 — Prepare the funding-sourcing-analyst brief

```
Brief for funding-sourcing-analyst:

audit_dir: /home/atgu/Projects/Ideas/audits/<slug>/
slug: <slug>
scale_mode: <L1|L2|L3>
geo: <EU27|DE|FR|IT|ES|NL|RO|+US|+UK>
mode: <full|anchor_only>
final_verdict: <GO|PIVOT|NO_GO with --anchor-only>
final_confidence: <high|med|low>

Read all artifacts in the audit dir in order (per your file's "How you operate" Step A):
  state.yaml, 01_clarification.md, 08c_capital_investor_fit.md (REQUIRED — seed list extraction),
  08b_gtm.md (REQUIRED — first-50-customer named-companies for §4 candidates),
  06_regulatory.md, 10_verdict.md.

Apply your workflow in full:
  - Step A — Read upstream context (refuse if 08c missing)
  - Step B — Pre-fetch refusal checks (geo=global already filtered by skill; NO_GO without --anchor-only already filtered)
  - Step C — Agentic Retrieval Loop (Self-RAG) per claim
  - Step D — Fetch budget cap: L1=5-8 / L2=8-12 / L3=12-18 (extended +50% iff --no-fetch-budget-override was passed)
  - Step E — §1 Grants (scale_mode-weighted: L1 micro only / L2 mid-tier / L3 Series-A-relevant)
  - Step F — §2 Angels (scale_mode-weighted: L1 3-5 micro / L2 10-15 mid / L3 5-10 lead)
  - Step G — §3 VCs (scale_mode-weighted: L1 1-2 perfunctory / L2 3-5 light / L3 15+ named)
  - Step H — §4 Anchor procurement (discriminator: pays before delivery? L1 PRIMARY 5-8 / L2 4-6 / L3 3-5 strategic-LOI)
  - Step I — Cross-section consistency check
  - Step J — Write 11_funding.md with output schema (frontmatter includes funding_data_as_of + staleness_warning_after = today + 180d)
  - Step K — Append all URLs to sources.md

Mode-specific:
  - mode=anchor_only: emit §4 only. §1/§2/§3 sections become single-line "[ANCHOR-ONLY MODE — section skipped]" placeholders.
  - --no-fetch-budget-override: agent may extend fetch budget by 50% (L1: up to 12 / L2: up to 18 / L3: up to 27)

Output path: audits/<slug>/11_funding.md

Regex audit will check:
  - Every named entity has First-contact action (no [TBD])
  - Every named entity has public access path (no personal emails, no `name@firm.com` guesses)
  - Every cited URL was WebFetch-verified within the artifact (access date present)
  - 5 closing blocks present (negative results, named analogs, inverse falsifier, confidence diary, CoVe verification log)
  - fetch_count ≤ scale_mode cap (unless --no-fetch-budget-override)
  - cross-section consistency with 08c (named investors / acquirers) and 08b (named companies) — flag [RECONCILE] on divergence

[USER-STATED CONTEXT — apply skeptical lens — if any]:
  <free-text from user (e.g., "include angel X"); agent treats as [USER-NAMED CANDIDATE] and independently verifies via public primary source; unverifiable → [USER-NAMED-ENTITY-UNVERIFIABLE] flag>
```

## Step 3 — Dispatch via Agent tool

Use the Agent tool with `subagent_type: funding-sourcing-analyst`. Wait for completion.

## Step 4 — Regex audit the artifact

Read `audits/<slug>/11_funding.md`. Apply these checks:

1. **Frontmatter completeness**: `funding_data_as_of`, `staleness_warning_after`, `fetch_count`, `fetch_budget_cap`, `mode`, `verdict_at_time_of_funding_research` all present.
2. **Mode-section consistency**: if `mode: anchor_only`, only §4 contains real entries; §1/§2/§3 are placeholder lines.
3. **First-contact actions**: every table row in active sections has a non-`[TBD]` First-contact action.
4. **Public access paths**: scan for personal-email patterns (`\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b`). If a personal email appears AND the entity is an individual (angel / partner) → `[BANNED-CONTACT-INFO]` flag. Re-invoke with feedback.
5. **Fetch budget**: `fetch_count` ≤ `fetch_budget_cap` (or +50% iff override flag passed).
6. **5 closing blocks**: present and non-empty.
7. **Cross-section consistency**: §3 named investors intersect with `08c` comparable-rounds investors (some overlap expected); divergence flagged in artifact.

If audit fails: re-invoke `funding-sourcing-analyst` ONCE with feedback ("regex audit found N issues: [list]"). If second invocation still fails, commit with `[SOURCE-DISCIPLINE-FAILURE]` flag added to `state.yaml.steps[13]`.

## Step 5 — Update state.yaml

After successful artifact + audit, update `audits/<slug>/state.yaml`:
- Add or update Step 13 entry: `{ n: 13, name: funding, status: done, at: <ISO timestamp>, mode: <full|anchor_only> }`
- `last_updated: <ISO timestamp>`
- Do NOT touch `final_verdict` / `final_confidence` (Step 13 doesn't change the verdict)
- Do NOT modify `_calibration.jsonl` (funding presence is checked via filesystem, per CLAUDE.md decision)

## Step 6 — Print to user

Print a compact summary:

```
─ Step 13 (Funding) complete ─────────────────────────────────
Artifact: audits/<slug>/11_funding.md
Mode: <full|anchor_only>
Fetch count: <N> / <cap> (within budget | exceeded)
Sections populated:
  §1 Grants: <K> entries (deadlines confirmed: <K_fresh>)
  §2 Angels: <K> entries
  §3 VCs: <K> entries
  §4 Anchor procurement: <K> entries (public RFP: <K_public>, private design-partner: <K_private>)
Freshness: data_as_of=<date>, staleness warning after <date+180d>
Closing blocks: 5/5 present
Cross-section reconciliation: <agree | [RECONCILE-N] flags>
```

Suggest next action based on scale_mode + verdict:
- **L1 GO** → "Top 3 first-contact actions for the next 7 days: §4 row 1 (<entity>), §4 row 2 (<entity>), §1 row 1 (<grant>). Re-read 11_funding.md."
- **L2 GO** → "Build a contact-tracker spreadsheet from §1 + §2 + §4. Top 5 contacts to schedule this month: <list>."
- **L3 GO/PIVOT** → "Prioritize §3 partners with active 2026 thesis posts in the space. Build warm-intro paths via the named portfolio CEOs in column 7."
- **NO_GO + --anchor-only** → "Treat §4 entries as a consulting pipeline. Top 3 to qualify this week: <list>. Decision rule: 2+ signed pilots in 90 days = re-audit as services play."

## Step 7 — Stale-data resume hook (for /idea_audit --resume)

If invoked from `/idea_audit --resume <slug>` and the existing `11_funding.md` is past `staleness_warning_after`, the orchestrator already prompted re-run. This skill receives `--refresh` automatically in that case.

## --anchor-only mode specifics

When `--anchor-only` is passed:

- Only §4 is populated with real entries. §1/§2/§3 contain a single line: *"[ANCHOR-ONLY MODE — section skipped. Re-run /idea_funding <slug> without --anchor-only after verdict pivot.]"*
- Scale-mode caps apply ONLY to §4 (so the full fetch budget can be spent on §4 named-entity research).
- §4 entries explicitly named as **consulting-suitable** (i.e., the buyer pays for a services-shaped delivery, not a product subscription). Mark each entry with `consulting-shaped: yes/no`.
- The frontmatter `mode: anchor_only` is required.

## Refresh mode specifics

When `--refresh` is passed:

- Existing `11_funding.md` is **overwritten** (after `AskUserQuestion` confirms; the prior file is moved to `11_funding.md.bak-<YYYY-MM-DD>` for audit-trail).
- All sources are re-fetched (don't rely on prior file's cited values).
- `funding_data_as_of` is set to today.
- Used by founders who need to re-check the funding landscape every 6 months (the staleness threshold).

## Avoid

- Running with verdict ∈ {NO_GO, DEFER} without `--anchor-only` (refusal logic in Step 1.C is mandatory)
- Running with `geo == global` (refusal logic in Step 1.C is mandatory)
- Dispatching without `08c_capital_investor_fit.md` available (refusal logic in Step 1.C is mandatory)
- Overwriting an existing `11_funding.md` without `--refresh` flag + user confirmation
- Modifying `_calibration.jsonl` (decision: funding presence is filesystem-checked, not ledger-tracked)
- Skipping the regex audit (the public-access-path enforcement only works if it actually runs)
- Letting the agent fetch past the scale_mode cap without `--no-fetch-budget-override`
- Generating personal-email contact info — public access paths only
- Treating user-named entities as authoritative — they are `[USER-NAMED CANDIDATE]` and require independent public-source verification

## Related

- `/idea_audit` — wires this as Step 13 (conditional on GO/PIVOT verdict at Step 12)
- `/idea_verdict <slug>` — produces the verdict that gates Step 13
- `/idea_verdict --pivot <slug>` — alternative for NO_GO ideas (adjacent-idea generation, not funding research)
- `/idea_status <slug>` — read-only inspection (will surface Step 13 status)
- `funding-sourcing-analyst` agent — the underlying agent dispatched here

## What "passes some thresholds" means (verdict-to-trigger mapping)

| Verdict at Step 12 | Default `/idea_funding` behavior | `--anchor-only` behavior |
|---|---|---|
| GO | runs full 4-section | runs §4 only |
| PIVOT | runs full 4-section | runs §4 only |
| NO_GO | REFUSES (suggests /idea_verdict --pivot) | runs §4 only (consulting-pivot exploration) |
| DEFER | REFUSES (suggests waiting for trigger) | runs §4 only with warning |

This is what fulfills the founder's intent: actionable funding leads appear **only when the audit's own evidence supports pursuing the idea** — preventing the system from producing a tempting funding list for a verdict-killed idea.
