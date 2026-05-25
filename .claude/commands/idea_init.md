---
description: Bootstrap the Ideas workspace — idempotently create audits/ dir, _calibration.jsonl ledger, validate CLAUDE.md workspace contract, print summary of installed skills + agents. Safe to run multiple times.
argument-hint: "[--force]  (re-create _calibration.jsonl if it exists; use rarely)"
allowed-tools: Read, Write, Bash(mkdir:*), Bash(touch:*), Bash(ls:*), Bash(test:*), Bash(stat:*), Bash(wc:*), Bash(cat:*), Bash(pwd:*), Bash(date:*), Bash(realpath:*)
model: claude-opus-4-7
---

## Context

- Working directory: !`pwd`
- Today: !`date +%Y-%m-%d`
- Project root presence: !`test -f /home/atgu/Projects/Ideas/CLAUDE.md && echo "CLAUDE.md FOUND" || echo "CLAUDE.md MISSING"`
- audits/ dir: !`test -d /home/atgu/Projects/Ideas/audits && ls /home/atgu/Projects/Ideas/audits/ | wc -l | xargs -I{} echo "EXISTS, {} entries" || echo "MISSING"`
- _calibration.jsonl: !`test -f /home/atgu/Projects/Ideas/audits/_calibration.jsonl && wc -l < /home/atgu/Projects/Ideas/audits/_calibration.jsonl | xargs -I{} echo "EXISTS, {} verdicts logged" || echo "MISSING"`
- .claude/commands/: !`ls /home/atgu/Projects/Ideas/.claude/commands/ 2>/dev/null | grep -c '^idea_' | xargs -I{} echo "{} idea_* skills installed"`
- .claude/agents/: !`ls /home/atgu/Projects/Ideas/.claude/agents/ 2>/dev/null | wc -l | xargs -I{} echo "{} agents installed"`

## Task

Idempotently initialize the Ideas workspace at `/home/atgu/Projects/Ideas/`. Argument: **$ARGUMENTS** (`--force` re-creates `_calibration.jsonl` even if non-empty; otherwise everything is non-destructive).

## Step 1 — Verify or create the workspace skeleton

Check each of these and create only if missing:

```bash
mkdir -p /home/atgu/Projects/Ideas/audits
mkdir -p /home/atgu/Projects/Ideas/.claude/commands
mkdir -p /home/atgu/Projects/Ideas/.claude/agents
```

`mkdir -p` is idempotent; safe to run unconditionally.

## Step 2 — Verify CLAUDE.md exists

The workspace contract at `/home/atgu/Projects/Ideas/CLAUDE.md` is the authoritative document inherited by every skill and agent. If it is missing, **stop and surface the failure** — do not silently proceed. Tell the user:

> ⚠️ `Ideas/CLAUDE.md` is missing. The Ideas workspace cannot operate without the workspace contract. Re-create it from `/home/atgu/.claude/plans/i-want-to-create-fuzzy-goblet.md` or re-run the project bootstrap.

If present, briefly read the first 30 lines and confirm it mentions:
- Capability profile (elite solo founder)
- Verdict optimization target
- Source Protocol
- Controlled-vocabulary tags `[FATAL|BLOCKER|RISK|ADVANTAGE]`

If any of these are missing → flag a contract-drift warning.

## Step 3 — Initialize `_calibration.jsonl`

If the file does not exist OR `--force` was passed:

```bash
touch /home/atgu/Projects/Ideas/audits/_calibration.jsonl
```

If `--force` is passed AND the file already has content, ask the user to confirm via `AskUserQuestion` before truncating — this destroys verdict history.

Also touch `/home/atgu/Projects/Ideas/audits/.gitkeep` if absent (no-op if present).

## Step 4 — Inventory installed skills + agents

Verify which `idea_*` skills are present in `/home/atgu/Projects/Ideas/.claude/commands/`:

Expected eventually (Phase A subset marked ✱):
- ✱ `idea_init.md`
- ✱ `idea_audit.md`
- `idea_status.md`
- `idea_triage.md`
- `idea_market.md`
- `idea_compete.md`
- `idea_customer.md`
- `idea_regulatory.md`
- `idea_technical.md`
- `idea_business.md`
- `idea_redteam.md`
- `idea_verdict.md`

Verify agents present in `/home/atgu/Projects/Ideas/.claude/agents/`:

Expected eventually (Phase A subset marked ✱):
- ✱ `market-size-analyst.md`
- ✱ `verdict-synthesizer.md`
- `competitive-landscape-analyst.md`
- `customer-segment-analyst.md`
- `regulatory-compliance-analyst.md`
- `technical-feasibility-engineer.md`
- `unit-economics-analyst.md`
- `gtm-channel-analyst.md`
- `capital-and-investor-fit-analyst.md`
- `red-team-analyst.md`

Report which are present, which are missing, what phase the workspace is in (Phase A: only ✱ files; Phase B: all files).

## Step 5 — Print the summary block

Print to the user:

```
─── Ideas workspace status ──────────────────────────────────────
Root:              /home/atgu/Projects/Ideas
CLAUDE.md:         <found / MISSING>
audits/:           <N> existing audit dirs
_calibration.jsonl: <N> verdicts logged · running distribution (if N≥3): GO X% · PIVOT Y% · NO_GO Z% · DEFER W%
Skills:            <K>/12 installed (Phase <A|B>)
Agents:            <M>/10 installed (Phase <A|B>)

Defaults (from CLAUDE.md):
  --geo=EU27
  --depth=deep
  Pre-register kill criteria: ON in deep mode (auto-invokes /sci_falsify)
  Calibration prior: GO 10–15% · PIVOT 25–35% · NO_GO 35–45% · DEFER 10–20%

Next suggested action:
  - /idea_audit "<seed>"   to run the full wizard on a new idea
  - /idea_status <slug>    to inspect an existing audit
  - /idea_resume <slug>    (alias: /idea_audit --resume <slug>) to continue
─────────────────────────────────────────────────────────────────
```

If running distribution is computable (n ≥ 3), parse `_calibration.jsonl` and compute it. Otherwise show "insufficient history."

## Step 6 — Sanity-check the workspace

Confirm:
- `/home/atgu/Projects/Ideas/ideas.md` exists (seed list) — if absent, suggest creating it
- `/home/atgu/Projects/Ideas/.claude/commands/` is reachable from this command
- The user can invoke `/idea_audit` from this point

If any check fails, report the specific failure with the fix command.

## Avoid

- **Never** truncate `_calibration.jsonl` without explicit user confirmation (verdict history is irreplaceable evidence)
- **Never** overwrite `CLAUDE.md` — if missing, ask the user to restore it
- **Never** delete existing audit dirs as part of init
- **Never** silently "fix" a missing file beyond the idempotent dir/touch operations above

## Related

- `/idea_audit` — run the full wizard on a new seed
- `/idea_status <slug>` — read-only inspection of an audit's progress
- `/sci_init` — the analogous bootstrap for the scientific research toolkit (separate workspace contract)
