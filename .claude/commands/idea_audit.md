---
description: Wizard orchestrator for end-to-end idea-feasibility audit. Runs 12 steps with AskUserQuestion checkpoints between every step (default — one step per turn, NOT all-at-once). Produces a categorical verdict (GO/PIVOT/NO_GO/DEFER) backed by a tagged-evidence scorecard. Inherits Source Protocol, Agentic Retrieval Loop, anti-confirmation-bias requirements, Capability Profile, and MAST defenses from `CLAUDE.md`. Phase B: all 12 steps wired with real agents.
argument-hint: "[seed-text]  |  start <seed>  |  --resume <slug>  |  --pivot <slug>  |  --partial <slug>   ·   flags: --depth=quick|deep|paranoid  --geo=EU27|<cc>|+US|global  --no-checkpoints  --no-pre-register  --no-gates  --from-file=PATH"
allowed-tools: Read, Write, Edit, Bash(mkdir:*), Bash(touch:*), Bash(ls:*), Bash(test:*), Bash(date:*), Bash(stat:*), Bash(wc:*), Bash(cat:*), Bash(pwd:*), Bash(realpath:*), Bash(basename:*), Bash(grep:*), Bash(sort:*), Bash(awk:*), Bash(tr:*), Bash(sed:*), Bash(find:*), Agent, AskUserQuestion, WebSearch, WebFetch
model: claude-opus-4-7
---

## Context

- Working directory: !`pwd`
- Today: !`date +%Y-%m-%d`
- CLAUDE.md present: !`test -f /home/atgu/Projects/Ideas/CLAUDE.md && echo YES || echo "NO — run /idea_init first"`
- audits/ dir: !`test -d /home/atgu/Projects/Ideas/audits && ls /home/atgu/Projects/Ideas/audits/ | grep -v '^_\|^\\.' | wc -l | xargs -I{} echo "{} existing audits"`
- _calibration.jsonl: !`test -f /home/atgu/Projects/Ideas/audits/_calibration.jsonl && wc -l < /home/atgu/Projects/Ideas/audits/_calibration.jsonl | xargs -I{} echo "{} verdicts logged"`
- ideas.md seeds: !`test -f /home/atgu/Projects/Ideas/ideas.md && wc -l < /home/atgu/Projects/Ideas/ideas.md | xargs -I{} echo "{} lines"`

## Task

Run the idea-feasibility wizard on **$ARGUMENTS**. Defaults: `--depth=deep`, `--geo=EU27`, pre-registration ON, checkpoints between steps ON.

The pipeline is the **wizard pattern**: one step per turn, AskUserQuestion checkpoint after every step, user always sees provisional state before paying for the next stage. **Default is NOT one-shot.** `--no-checkpoints` removes the pauses for power users who trust the pipeline.

Phase B: all 12 steps are wired with real agents via the Standard Step Driver. Steps 10 and 11 use sub-files with wizard-merged synthesis blocks (08a/b/c and 09a/b).

## Step 0 — Parse arguments and resolve mode

Identify which mode this invocation is in:

| Detected pattern | Mode | Action |
|---|---|---|
| `--resume <slug>` | RESUME | Read existing `state.yaml`, identify next pending step, jump there |
| `--pivot <slug>` | PIVOT-ONLY | Skip the wizard, run only `/idea_verdict --pivot <slug>` logic |
| `--partial <slug>` | PARTIAL | Skip the wizard, run only `/idea_verdict --partial <slug>` logic |
| `--from-file=PATH` | NEW from file | Read seed from `PATH` (default `ideas.md` line N) |
| `start <seed>` or bare seed | NEW | Start a fresh audit on the given seed |
| (no args) | INTERACTIVE | AskUserQuestion: "Which seed?" — present last 3 lines of `ideas.md` as options |

Parse the flags:
- `--scale=L1|L2|L3` (default `L1` — see CLAUDE.md "Verdict optimization target". Default is L1 (replace-salary) because VC-mode thresholds false-negative indie-scale ideas. If absent from CLI, ask the user via AskUserQuestion at Step 0.5 with L1 as the recommended option.)
- `--depth=quick|deep|paranoid` (default `deep`)
- `--geo=EU27|DE|FR|IT|ES|NL|RO|+US|global` (default `EU27`)
- `--no-checkpoints` (default off)
- `--no-pre-register` (default off — pre-reg is ON in deep mode)
- `--no-gates` (default off — auto-skip on fatal is ON)
- `--no-funding` (default off — Phase C Step 13 runs when verdict ∈ {GO, PIVOT}; this flag disables Step 13 entirely)

Print to user: "Audit mode: NEW · seed='<...>' · scale=<L1|L2|L3> · geo=EU27 · depth=deep · checkpoints=ON · pre-register=ON"

## Step 0.5 — Resolve scale mode (if not on CLI)

If `--scale` was NOT provided on the command line, ask the user via `AskUserQuestion` BEFORE Step 1 (state.yaml init) — the scale_mode field is required at init.

Question: "Which scale level should the audit optimize for? See CLAUDE.md → 'Verdict optimization target' for the full definitions."

Options:
- **L1 — replace-salary (Recommended)** · "€50k–€500k ARR in 24mo, bootstrap-only, founder ≈ senior dev salary. Default: maximizes verdict surface for indie-SaaS-scale wins; prevents false-negatives on solo-founder ideas."
- **L2 — indie** · "€500k–€5M ARR in 36mo, bootstrap or small angel (<€200k), founder + 0–3 contractors."
- **L3 — venture** · "€5M–€100M+ ARR in 5y, VC-fundable. Requires €100M+ outcome thesis + defensibility growth path for any GO verdict."
- Other (free-text override)

Header: "Scale mode" · multiSelect: false.

Store the resolved value as `scale_mode` for use in Step 1's state.yaml init. Print: "Resolved scale_mode: <L1|L2|L3>."

The pre-registered kill criteria in Step 3 (sci_falsify) MUST be calibrated to this scale_mode — passing it through is a Step-3 brief responsibility.

## Standard Step Driver (referenced by Steps 4, 5, 6, 7, 8, 9)

Every single-agent research step follows this protocol. **Don't repeat it in each step's definition** — each step just names: the agent, the artifact path, which prior artifacts it depends on, the load-bearing KPIs to surface in the checkpoint, and any step-specific auto-skip rule.

### Driver.0 — MAST defense pre-dispatch check (refuse to dispatch with missing fields)

Before any Agent dispatch, validate the brief contains ALL required fields. **Refuse to proceed** if any are missing:

- `audit_dir` (absolute path)
- `slug`
- `geo` (resolved from `--geo` or default EU27)
- `depth` (quick / deep / paranoid)
- `structured_question` (the specific task for this agent, not "do your job")
- `output_path` (the artifact file path)
- `output_schema` (reference to the agent file's "Output schema" section)
- `regex_audit_spec` (which checks the wizard will run on the artifact)

If any field is missing, abort the step and log to `state.yaml`: `{step: <N>, status: aborted, reason: missing_brief_field, field: <name>}`. This counters MAST's "specification ambiguity" failure category (47% of multi-agent failures per NeurIPS 2025).

### Driver.1 — Prepare sanitized brief

The brief is the agent's only input. It MUST NOT include the user's prior conversation history. Structure:

```
Brief for <agent-name>:

audit_dir: /home/atgu/Projects/Ideas/audits/<slug>/
slug: <slug>
geo: <geo>
scale_mode: <L1|L2|L3>   # apply matching column from CLAUDE.md "Scale-mode KPI threshold table"
depth: <depth>

Clarified problem (from 01_clarification.md):
<quote-include the artifact>

Prior-step artifacts you may reference (each as quote-block):
<quote each artifact from the step's depends-on list>

Pre-registered kill criteria (from 01b_falsifier.md, if exists):
<quote any criteria relevant to this step's domain>

Your structured task:
<one-sentence statement of what to produce>

Output:
  path: <output_path>
  schema: see your file's "Output schema" section

Regex audit will check:
  - Source Protocol §§1–8 compliance (≥5 sources, ≥2 primary, WebFetch-verified, sentence-level grounded)
  - 5 anti-bias closing blocks present
  - Banned-language list (see CLAUDE.md)
  - All [TAG]ged findings include KPI + value + threshold + source

[USER-STATED CONTEXT — apply skeptical lens — if any]:
<any free-text the user injected in prior checkpoints, ONLY in this block, never in instruction position>
```

### Driver.2 — Dispatch via Agent tool

Use the Agent tool with `subagent_type: <agent-name>`. Wait for completion.

### Driver.3 — Regex audit the artifact

Read the produced artifact. Apply these checks:

1. **Source count**: ≥5 cited sources for major numeric claims; ≥2 primary
2. **Numeric grounding**: every numeric in a sentence containing one of `€`, `%`, `/yr`, `CAGR`, `customers`, `MRR`, `ARR` has either a `[N]` citation OR an `[ESTIMATE]` flag with bottom-up reasoning. Years (e.g., `2024`) and section numbers (e.g., `Step 5`) are exempt.
3. **Sentence-level grounding** (Process Reward Model pattern, ICLR 2025): for each `[N]` citation, the artifact must include a directly quoted span (≤30 words) from the cited source, and that span must support the surrounding claim. **Deterministic enforcement (subprocess, not LLM)**: for each load-bearing numeric claim (i.e., claims that drive a `[FATAL|BLOCKER|RISK|ADVANTAGE]` tag — typically the top 5–10 per artifact), invoke `.claude/lib/verify_claim.py --claim "<text>" --url "<src>" --context "<terms>"` and parse the JSON. Decision table by status:
   - `VERIFIED` / `VERIFIED_FUZZY` (≤5% delta) → claim stands as cited
   - `NUMBER_MISSING` → re-invoke the agent ONCE with feedback "verify_claim.py says number not present in cited span; either fix the cite or convert to [ESTIMATE]"
   - `FETCH_FAILED` / `PAYWALLED` / `JS_REQUIRED` → auto-tag the claim `[ESTIMATE]` (with the failure reason in a parenthetical) and downgrade the source from primary to secondary in `sources.md`
   - `NO_CLAIM_NUMBER` → claim has no numeric value to ground; skip
The LLM grades nothing here — the regex engine does. This closes the verification-gap category (MAST §3, 21% of multi-agent failures). If the script is missing or import-errors, log `[GROUNDING-VERIFIER-UNAVAILABLE]` in `state.yaml.steps[N]` and fall back to the LLM-graded check (degrades to prior behavior, never blocks).
4. **5 closing blocks present**: negative results, named analogs, inverse falsifier, confidence diary, CoVe verification log. Each must be non-empty.
5. **Banned-language scan**: zero occurrences of the banned phrases from `CLAUDE.md` "Banned language" section.
6. **Tag extractability**: regex `/\[(FATAL|BLOCKER|RISK|ADVANTAGE)\]/` returns the expected count; every tag has KPI + value + threshold + source on the same line or in the immediately preceding line.

### Driver.4 — Retry on failure (bounded)

If audit fails, re-invoke ONCE with feedback ("regex audit found N issues: [list of specific violations]"). If second invocation still fails, commit the artifact with a `[SOURCE-DISCIPLINE-FAILURE]` flag added to `state.yaml`'s per-step record — the synthesizer will read this and downgrade overall confidence.

### Driver.5 — Extract tags and update state

Parse the artifact for `[FATAL|BLOCKER|RISK|ADVANTAGE]` occurrences. Update `state.yaml`:

- Mark step `<N>` `status: done` with timestamp
- Add tags to `running_tags`
- Update `provisional_verdict` via simplified rubric (≥1 FATAL → NO_GO leaning; ≥2 BLOCKER → PIVOT leaning; else proceeding)

### Driver.6 — Print checkpoint + AskUserQuestion

Print the structured "Checkpoint format" block (defined later in this file) showing this step's findings, the running tally, and the provisional verdict. Then ask the user via `AskUserQuestion` with the 4 standard options.

### Driver.7 — `--depth=paranoid` self-consistency layer

If `--depth=paranoid`, for each load-bearing KPI claim in the artifact, re-dispatch the agent with a brief variant ("re-derive this single KPI from a different starting assumption") two more times (N=3 total samples). Compare the resulting values:

- Divergence < 10% → confirm; no change
- Divergence 10–30% → flag `[CALIBRATION-MODERATE]` and downgrade KPI confidence by one tier
- Divergence > 30% → flag `[CALIBRATION-UNSTABLE]` and mark the KPI `[ESTIMATE]` with bounds shown

This is calibrated reasoning via self-consistency (arXiv:2506.03723). Expensive — only fires in paranoid mode. Skip in quick/deep modes.

## Step 1 — Seed + slug (Phase A: WIRED)

For NEW mode:

1. Capture the seed text. If from `ideas.md`, also record the line number and full original line.
2. **Generate a slug** — 3-5 lowercase kebab-case words capturing the essence. Examples:
   - "predictive crowd movement - tourist flow, protests, football games" → `predictive-crowd-movement`
   - "AI compliance auditing tool for German Mittelstand" → `compliance-audit-de-mittelstand`
   - "Tool for analyzing theory of mind aspects in LLMs" → `tom-llm-analyzer`
3. Form the audit-dir name: `<YYYY-MM-DD>_<slug>` (use today's date from the Context block).
4. Check if the audit dir already exists:

   ```bash
   test -d /home/atgu/Projects/Ideas/audits/<YYYY-MM-DD>_<slug>
   ```

   If yes, AskUserQuestion (4 options):
   - **Resume** (default) — read `state.yaml`, continue from next pending step
   - **New version** — append `_v2` to slug
   - **Overwrite** — destructive; ask again to confirm
   - Other (free-text)

5. Create the audit dir: `mkdir -p /home/atgu/Projects/Ideas/audits/<YYYY-MM-DD>_<slug>`
6. Write `00_seed.md`:

   ```markdown
   # 00 — Seed

   **Original**: <full seed text as user provided>
   **Source**: <CLI arg | ideas.md line N | other>
   **Invocation**: `/idea_audit "<...>" --depth=<...> --geo=<...>`
   **Slug**: <slug>
   **Audit dir**: audits/<YYYY-MM-DD>_<slug>/
   **Created**: <ISO timestamp>
   **Wizard version**: phase-B
   ```

7. Initialize `state.yaml`:

   ```yaml
   slug: <slug>
   geo: <geo>
   scale_mode: <L1|L2|L3>   # from --scale flag or Step 0.5 AskUserQuestion; default L1
   depth: <depth>
   created: <ISO timestamp>
   last_updated: <ISO timestamp>
   wizard_version: phase-B
   checkpoints: <on|off>
   pre_register: <on|off>
   steps:
     - { n: 1, name: seed, status: done, at: <ISO> }
     - { n: 2, name: clarify, status: pending }
     - { n: 3, name: falsify, status: pending }
     - { n: 4, name: triage, status: pending }
     - { n: 5, name: market, status: pending }
     - { n: 6, name: competition, status: pending }
     - { n: 7, name: customer, status: pending }
     - { n: 8, name: regulatory, status: pending }
     - { n: 9, name: technical, status: pending }
     - { n: 10, name: business, status: pending }
     - { n: 11, name: redteam, status: pending }
     - { n: 12, name: verdict, status: pending }
     - { n: 13, name: funding, status: pending }   # Phase C — runs only if verdict ∈ {GO, PIVOT} AND --no-funding flag absent AND geo != global
   running_tags: { FATAL: 0, BLOCKER: 0, RISK: 0, ADVANTAGE: 0 }
   provisional_verdict: null
   provisional_confidence: null
   user_context_injected: []
   ```

8. Print the post-step block (see "Checkpoint format" section).
9. Run the checkpoint (see "Checkpoint format" — proceed to Step 2 default).

## Step 2 — Clarify (Phase A: WIRED, main-thread + AskUserQuestion)

Goal: turn the vague seed into a well-formed problem statement with explicit customer, pain, mechanism, geo, and build hypothesis.

1. Read `00_seed.md` and analyze the seed for missing dimensions. The 5 dimensions that MUST be locked before proceeding:
   - **Customer**: who specifically pays? (B2C / B2B / B2G — with named segment)
   - **Pain**: what's the core pain in their own words? Quantify if possible.
   - **Mechanism**: how does the solution work in 1 sentence?
   - **Initial geography**: where do you launch?
   - **Build hypothesis**: what does the MVP do; what's explicitly out of scope?

2. **Ask the user (one AskUserQuestion call, multiSelect: false per question or one combined free-text)** — only ask about the dimensions that are unclear in the seed. Typical questions:

   - "Who is the primary customer for this product?" — options: B2C consumers / B2B SMB / B2B enterprise / B2G public sector / Other
   - "Which geography do we evaluate first?" — options: EU27 / Germany (DE) / France (FR) / Romania (RO) / Other
   - "What's the core pain you believe this addresses?" — Other (free-text expected)
   - "What's the most ambitious version of this you'd build in 8 weeks?" — Other (free-text)

   Ask 2–4 of these, focused on the actual ambiguity in the seed.

3. **Refuse to proceed if the clarification is too vague.** Specifically, refuse if any of these are present:
   - "We'll figure out the customer later"
   - "It's for everyone"
   - "TBD" on Pain or Mechanism
   - "Just AI" or similar non-mechanistic answer on Mechanism

   If the answers are too vague, push back ONCE with a more pointed question. If still vague, mark the audit `[CLARIFICATION-INSUFFICIENT]` and proceed with low-confidence flag.

4. Write `01_clarification.md`:

   ```markdown
   # 01 — Clarification

   ## Customer
   <named segment, B2C/B2B/B2G, sub-segment>

   ## Pain (severity hypothesis)
   <one paragraph in customer's words; quantify if possible>

   ## Mechanism (1 sentence)
   <how the product works>

   ## Geography (initial)
   <EU27 / DE / FR / ... — explicit>

   ## Build hypothesis (8-week MVP)
   <what's in; what's explicitly out>

   ## Differentiation hypothesis (1 paragraph)
   <what makes this not commodity — moat hypothesis, NOT 'AI-powered' alone>

   ## Why now (initial hypothesis)
   <the trigger that makes this opportunity exist in 2026>
   ```

5. Update `state.yaml`: mark step 2 as done.

6. Post-step block + checkpoint.

## Step 3 — Pre-register kill criteria (Phase A: WIRED via /sci_falsify)

Conditions: `--depth=deep` AND not `--no-pre-register`. Skip otherwise.

1. Print: "Invoking `/sci_falsify` to pre-register what would kill this idea before any market research begins. This counters post-hoc rationalization."

2. Invoke `/sci_falsify` via the orchestration pattern (the existing `sci_*` skill is available). Pass the clarified problem statement from `01_clarification.md` as the hypothesis to falsify. The expected output is a `*falsifier*.md` file with pre-registered kill conditions.

3. Copy or symlink the resulting falsifier file into the audit dir as `01b_falsifier.md`. If `/sci_falsify` returns inline (no file), capture its output and write `01b_falsifier.md` with the kill conditions structured as:

   ```markdown
   # 01b — Pre-registered kill criteria (sci_falsify)

   These kill conditions were pre-registered BEFORE market research began. They cannot be retroactively softened.

   ## Kill condition 1
   IF <observable measurement> <comparison> <threshold> THEN this idea is NO_GO regardless of other findings.
   Severity: <FATAL|BLOCKER>

   ## Kill condition 2
   ...

   (3–7 conditions, each falsifiable with a named metric and threshold)
   ```

4. Update `state.yaml`: mark step 3 as done.

5. Post-step block + checkpoint.

If `/sci_falsify` is unavailable or fails, log to state.yaml `{ falsify_unavailable: true }` and continue without the falsifier — note this in the verdict-synthesizer's brief so it knows pre-registration was skipped.

## Step 4 — Triage (WIRED via red-team-analyst quick-mode)

Follow the **Standard Step Driver** with these specifics:

- **Agent**: `red-team-analyst`
- **Artifact path**: `audits/<slug>/02_triage.md`
- **Depends-on**: `01_clarification.md` (+ `01b_falsifier.md` if exists)
- **Brief mode line** (first line of the brief): `mode: quick`
- **Brief structured task**: "Produce a 5-minute kill/keep gate for this seed. Run the three cheap kill-checks (regulatory blocker, already-commodity, demand-existence). Call /sci_sanity_check on any numeric claims in the seed. Emit a `TRIAGE VERDICT: <PROCEED|KILL|REFRAME>` line and a `fatal_finding: <true|false>` line at the top of the artifact."
- **Load-bearing KPIs to surface in checkpoint**: TRIAGE VERDICT (PROCEED/KILL/REFRAME), fatal_finding (true/false), and the single most-important kill-check finding
- **Step-specific auto-skip rule**: if the artifact contains `fatal_finding: true`, the wizard jumps to Step 12 with a brief NO_GO verdict, citing the triage finding. (Override with `--no-gates`.)

After dispatch + audit + extract: if `fatal_finding: true`, skip remaining steps and go to Step 12. Otherwise checkpoint and continue.

## Step 5 — Market (Phase A: WIRED via market-size-analyst agent)

1. Prepare the agent brief. The brief MUST be sanitized (no user-conversation context — only the artifacts so far + the structured question):

   ```
   Brief for market-size-analyst:

   Audit slug: <slug>
   Audit dir: /home/atgu/Projects/Ideas/audits/<slug>/
   Geography: <geo>
   Depth: <depth>

   Clarified problem (from 01_clarification.md):
   <quote the full clarification artifact>

   Pre-registered kill criteria (from 01b_falsifier.md, if exists):
   <quote any market-related kill conditions>

   Your task:
   Produce 03_market.md following your output schema. Apply the full Source Protocol,
   the 5 anti-confirmation-bias closing blocks (negative results, named analogs,
   inverse falsifier, confidence diary, CoVe verification log), and tag every
   load-bearing KPI with [FATAL|BLOCKER|RISK|ADVANTAGE].

   Write your output to /home/atgu/Projects/Ideas/audits/<slug>/03_market.md.
   Append every cited URL to /home/atgu/Projects/Ideas/audits/<slug>/sources.md.

   [USER-STATED CONTEXT — apply skeptical lens — if any]:
   <any free-text the user injected in prior checkpoints>
   ```

2. Dispatch the `market-size-analyst` agent via the Agent tool with `subagent_type: market-size-analyst`.

3. After the agent returns, **read** `03_market.md` and **regex-audit** it for Source Protocol compliance:
   - Are there ≥5 sources cited in claims?
   - Do all numerics have either a `[N]` citation or `[ESTIMATE: ...]` flag?
   - Are bottom-up arithmetic chains shown for TAM/SAM/SOM?
   - Are the 5 closing blocks present and non-empty?
   - Banned-phrase check (use the list from `CLAUDE.md`)

   If audit fails:
   - Re-invoke the agent ONCE with feedback ("regex audit found N issues: [list]")
   - If second invocation still fails, commit with `[SOURCE-DISCIPLINE-FAILURE]` flag in state.yaml

4. **Extract the tag tally** from `03_market.md`:
   - Count `[FATAL]`, `[BLOCKER]`, `[RISK]`, `[ADVANTAGE]` occurrences
   - Update `state.yaml` `running_tags`
   - Update `state.yaml` `provisional_verdict` using a simplified rubric (≥1 FATAL → NO_GO leaning; ≥2 BLOCKER → PIVOT leaning; else PROVISIONAL)

5. Post-step block + checkpoint.

## Step 6 — Competition (WIRED via competitive-landscape-analyst)

Follow the **Standard Step Driver** with these specifics:

- **Agent**: `competitive-landscape-analyst`
- **Artifact path**: `audits/<slug>/04_competition.md`
- **Depends-on**: `01_clarification.md`, `03_market.md` (for SAM context + market growth signal)
- **Brief structured task**: "Produce a competitive landscape — ≥3 direct competitors with funding/HC/revenue/positioning, indirect competitors (status quo workarounds), 2–5 adjacent threats from BigCo with predicted bundling moves, top-3 concentration, switching cost analysis, named moat type (not 'AI'), incumbent response forecast table, M&A activity 24mo."
- **Load-bearing KPIs to surface in checkpoint**: # direct competitors, largest competitor funding, top-3 concentration, named moat type, M&A 24mo count
- **Step-specific auto-skip rule**: none

## Step 7 — Customer (WIRED via customer-segment-analyst)

Follow the **Standard Step Driver** with these specifics:

- **Agent**: `customer-segment-analyst`
- **Artifact path**: `audits/<slug>/05_customer.md`
- **Depends-on**: `01_clarification.md`, `03_market.md` (for segment context)
- **Brief structured task**: "Produce a customer-segment analysis with quote-attributed pain (≥5 distinct real customer voices from G2/Reddit/forums/surveys), pain severity 1–10 evidence-backed, pain frequency, current cost of the problem €/yr, WTP €/yr anchored to ≥2 named analog companies, time-to-value, buyer-≠-user influence map for B2B."
- **Load-bearing KPIs**: pain severity, WTP estimate, time-to-value, buyer ≠ user mapped (B2B), quote-attributed pain count
- **Step-specific auto-skip rule**: none

## Step 8 — Regulatory (WIRED via regulatory-compliance-analyst)

Follow the **Standard Step Driver** with these specifics:

- **Agent**: `regulatory-compliance-analyst`
- **Artifact path**: `audits/<slug>/06_regulatory.md`
- **Depends-on**: `01_clarification.md`, `07_technical.md` (if exists, for tech-stack context)
- **Brief structured task**: "Produce regulatory analysis — EU AI Act classification with the machine-readable line `EU_AI_ACT_CLASS: <minimal|limited|high-risk|unacceptable|not-in-scope>`, GDPR exposure + DPIA-required determination, sector certifications needed (MDR/MiFID/NIS2/etc.), compliance cost € to launch + €/yr ongoing, time-to-clearance months on critical path, data residency. If --geo=+US or global, extend to US sector regs."
- **Load-bearing KPIs**: EU AI Act class, GDPR exposure, compliance cost € to launch, time-to-clearance, sector certs needed
- **Step-specific auto-skip rule**: after the audit, regex-parse `EU_AI_ACT_CLASS:` line from `06_regulatory.md`. If value is `unacceptable`, jump to Step 12 with NO_GO verdict citing the Art. 5 prohibition. (Override with `--no-gates`.)

## Step 9 — Technical (WIRED via technical-feasibility-engineer)

Follow the **Standard Step Driver** with these specifics:

- **Agent**: `technical-feasibility-engineer`
- **Artifact path**: `audits/<slug>/07_technical.md`
- **Depends-on**: `01_clarification.md`
- **Brief structured task**: "Produce a technical feasibility analysis under the Capability Profile (elite AI-augmented solo founder; no team-hiring in MVP-phase) — decompose into 5–10 capability blocks with founder weeks + cash €, time-to-MVP, MVP cash cost (excl. founder time), time-to-revenue, tech stack vendor risk + migration paths, data availability + acquisition time, infra cost/MAU at 10k/100k/1M scale, latency/reliability/certification requirements. Include explicit 'out-of-reach' check (only physical/economic constraints qualify — not 'ML is hard') and Capability Profile guardrails section."
- **Load-bearing KPIs**: time-to-MVP (founder weeks), MVP cash cost €, time-to-revenue (months), tech stack vendor risk, "out-of-reach" check
- **Step-specific auto-skip rule**: none

## Step 10 — Business (WIRED via 3-agent bundle into sub-files)

This step bundles three agents writing to **sub-files** that the wizard then merges into `08_business.md`.

### Step 10.A — Serial dispatch of three agents

To avoid `sources.md` write races, dispatch the three agents **serially** in this order:

1. **`unit-economics-analyst`** → writes `audits/<slug>/08a_unit_economics.md`
   - Brief structured task: "Produce unit economics — speed-to-revenue KPIs as first-class (time to first paying customer / €10k MRR / €100k ARR / ramen profitability), CAC anchored to named channel analogs, LTV with named retention analog, LTV/CAC, payback, gross margin, NRR, burn multiple at €1M ARR, Rule of 40, capital efficiency."
   - Depends-on: `01_clarification.md`, `03_market.md`, `05_customer.md`, `04_competition.md`

2. **`gtm-channel-analyst`** → writes `audits/<slug>/08b_gtm.md`
   - Brief structured task: "Produce GTM analysis — ACV + sales-motion fit with named analog, sales cycle length, win rate, top-3 channels with NAMED entry paths, channel concentration risk, first-50-customer plan with NAMED ENTITIES (companies/communities/conferences/individuals/newsletters). Reconcile CAC estimate with unit-economics-analyst."
   - Depends-on: `01_clarification.md`, `05_customer.md`, `08a_unit_economics.md`

3. **`capital-and-investor-fit-analyst`** → writes `audits/<slug>/08c_capital_investor_fit.md`
   - Brief structured task: "Produce capital path + investor attractiveness — cash to first paying customer, pre-seed/seed/A capital required, capital path classification, plausible €100M+ outcome thesis with ≥3 named comparable exits/rounds (REQUIRED for any GO verdict), comparable funding rounds 12mo, hot/cold classification, named plausible acquirers, defensibility growth path, distribution thesis, capital efficiency target, hype-risk check, active EU grants."
   - Depends-on: all prior artifacts

### Step 10.B — Wizard merges into `08_business.md`

After all three sub-files exist, the wizard writes `08_business.md` with this structure:

```markdown
# 08 — Business (unit economics + GTM + capital + investor fit)

## Index
- §08a Unit economics — by unit-economics-analyst
- §08b GTM — by gtm-channel-analyst
- §08c Capital & investor fit — by capital-and-investor-fit-analyst

## Cross-agent reconciliation (wizard-written)
- **CAC**: 08a reports €<X>; 08b reports €<Y>. <Agreement | [RECONCILE] if >2× divergence>.
- **ARPU/ACV**: 08a reports €<X>; 03 (market analyst) reports €<Z>. <Agreement | [RECONCILE]>.
- **Build cost**: 08a/08c reports €<X>; 07_technical.md reports €<W>. <Agreement | [RECONCILE]>.
- **Time-to-revenue**: 08a reports <X mo>; 07 reports <Y mo>. <Agreement | [RECONCILE]>.

---
[concatenated 08a content]
---
[concatenated 08b content]
---
[concatenated 08c content]
```

Any `[RECONCILE]` flags feed verdict-synthesizer's Step C.5.

### Step 10.C — Single checkpoint

Print ONE checkpoint block after all three sub-files + the merged `08_business.md` are written. Surface the top KPIs across all three: LTV/CAC, time to first paying customer, capital-path classification, €100M+ thesis present/absent.

## Step 11 — Red-team (WIRED via red-team-analyst dual-mode)

Similar mechanism to Step 10 — same agent (`red-team-analyst`) invoked twice with different mode briefs.

### Step 11.A — Two invocations

1. **`red-team-analyst` mode: DA** → writes `audits/<slug>/09a_da.md`
   - Brief first line: `mode: DA`
   - Brief structured task: "Devil's advocate critique — steel-man the idea in 3-5 sentences citing ADVANTAGEs from prior artifacts, then 2-4 strongest criticisms across distinct categories with severity + evidence + refutation condition + cost to address. Include incumbent-response table with NAMED companies. End with 1-sentence verdict on direction (continue/modify/pivot) and self-check for shared-bias failure."
   - Depends-on: all prior artifacts (especially `04_competition.md`, `05_customer.md`, `06_regulatory.md`, `07_technical.md`, `08_business.md`)

2. **`red-team-analyst` mode: premortem** → writes `audits/<slug>/09b_premortem.md`
   - Brief first line: `mode: premortem`
   - Brief structured task: "Premortem — it is 3 years from today, the company failed. Generate 3-5 failure trajectories across distinct mechanisms (PMF / burn / incumbent / regulation / founder / technical / timing / distribution). Each with probability + consequence + leading indicator visible TODAY + cheapest mitigation. Rank by P × consequence. Recommend single action this week."
   - Depends-on: all prior artifacts

### Step 11.B — Wizard merges into `09_redteam.md`

```markdown
# 09 — Red team

## Index
- §09a Devil's Advocate
- §09b Premortem

## Cross-mode synthesis (wizard-written)
- Criticisms in 09a that match trajectories in 09b: <list — these are the highest-priority risks>
- Failure trajectories in 09b not covered by 09a: <list — these are blind spots>

---
[concatenated 09a content]
---
[concatenated 09b content]
```

### Step 11.C — Single checkpoint

Print ONE checkpoint block after both sub-files + merged file are written. Surface: top 3 criticisms (DA), top 3 failure trajectories (premortem), the cross-mode overlap.

## Step 12 — Verdict (Phase A: WIRED via verdict-synthesizer agent)

1. Print: "All research stages complete (with Phase A stubs noted). Invoking verdict-synthesizer to produce the final ruling."

2. Prepare the brief (sanitized — only artifacts, no user conversation):

   ```
   Brief for verdict-synthesizer:

   Audit slug: <slug>
   Audit dir: /home/atgu/Projects/Ideas/audits/<slug>/
   Geography: <geo>
   Depth: <depth>
   Wizard version: phase-B (all 12 steps wired with real agents)

   Read all artifacts in the audit dir in order:
   00_seed.md, 01_clarification.md, 01b_falsifier.md (if exists),
   02_triage.md, 03_market.md, 04_competition.md, 05_customer.md,
   06_regulatory.md, 07_technical.md, 08_business.md (including the
   wizard-written Cross-agent reconciliation block + sub-files 08a/08b/08c),
   09_redteam.md (including the wizard-written Cross-mode synthesis block
   + sub-files 09a/09b), sources.md, and
   /home/atgu/Projects/Ideas/audits/_calibration.jsonl for the running
   distribution (FILTER to wizard_version: phase-B).

   Apply the controlled-vocabulary rubric (Step B → tag tally).
   Check pre-registered kill criteria (Step C — `01b_falsifier.md`).
   Run cross-step numeric reconciliation (Step C.5 — see your file).
   Run the pro-GO / anti-GO adversarial debate (Step D) in writing.
   Apply the Verdict Optimization Target gate (Step E — speed-to-revenue +
   investor-attractiveness + defensibility growth path; NO GO without all three).
   Assign verdict + confidence (Step F).
   Multi-Agent Reflexion check on similar past audits (Step F.5).
   Calibration check (Step G, FILTERED to phase-B).
   Write 10_verdict.md with SCORECARD as the headline, then adversarial debate
   block, then VC narrative draft (GO/PIVOT only).
   Append one line to /home/atgu/Projects/Ideas/audits/_calibration.jsonl
   with the full schema: date, slug, verdict, confidence, geo, depth,
   wizard_version=phase-B, steps_completed=[1..12], reconciliation_flags=<count>.

   [USER-STATED CONTEXT — apply skeptical lens — if any]:
   <any free-text injections>
   ```

3. Dispatch `verdict-synthesizer` via the Agent tool with `subagent_type: verdict-synthesizer`.

4. After the agent returns, read `10_verdict.md` and verify:
   - SCORECARD block is the first content (no preamble narrative)
   - VERDICT line is one of GO / PIVOT / NO_GO / DEFER
   - Confidence is one of high / med / low
   - Adversarial debate block is present (both pro-GO and anti-GO cases written)
   - For GO/PIVOT: VC narrative draft is present
   - `_calibration.jsonl` has one new line appended

5. Update `state.yaml`:
   - Mark step 12 as done with timestamp
   - Set `final_verdict`, `final_confidence`
   - Append the calibration line locally for fast access

6. **Print the SCORECARD block to stdout** so the user sees the headline immediately. Then print:

   ```
   Full verdict: audits/<slug>/10_verdict.md
   Sources: audits/<slug>/sources.md
   State: audits/<slug>/state.yaml
   Calibration ledger: audits/_calibration.jsonl
   ```

7. Suggest next action based on verdict:
   - **GO** → "Run the cheapest discriminating experiment: <quoted from verdict>. Re-audit on completion."
   - **PIVOT** → "Consider `/idea_audit <pivot-direction>` on the suggested pivot. Or re-audit this slug after refining the problem statement."
   - **NO_GO** → "Don't pursue as a product company. Consider `/idea_verdict --pivot <slug>` to generate 3–5 adjacent ideas. OR if a single anchor procurement contract ≥€100k/yr could fund development as a services play, run `/idea_funding --anchor-only <slug>` to surface §4 named buyers."
   - **DEFER** → "Wait for trigger: <quoted>. Re-audit on/after <date>."

## Step 13 — Funding research (Phase C, conditional on GO/PIVOT)

**Trigger**: Step 12 completed and `state.yaml.final_verdict` ∈ {GO, PIVOT}. Otherwise skip to wizard exit.

**Skip conditions** (any one fires → skip Step 13 silently and exit cleanly):

- `--no-funding` flag was passed at audit start
- `--partial` mode was used to generate the verdict (funding research is premature on incomplete evidence)
- `state.yaml.geo == global` (funding sources are jurisdiction-bound; the skill will refuse — surface this proactively)
- `state.yaml.final_verdict ∈ {NO_GO, DEFER}` (off-ramp: user can still run `/idea_funding --anchor-only <slug>` standalone — already surfaced in Step 12.7 NO_GO prose)

**Silent-skip state update** (when any of the above fires): BEFORE wizard exit, write to `state.yaml`:

```yaml
steps:
  - { n: 13, name: funding, status: skipped, skip_reason: <verdict_not_GO_or_PIVOT | no_funding_flag | partial_mode | geo_global>, at: <ISO timestamp> }
last_updated: <ISO timestamp>
```

Map the `skip_reason` value:
- `final_verdict ∈ {NO_GO, DEFER}` → `verdict_not_GO_or_PIVOT`
- `--no-funding` flag → `no_funding_flag`
- `--partial` mode → `partial_mode`
- `geo == global` → `geo_global`

This keeps `/idea_status <slug>` honest (Step 13 shows as `skipped` with reason, not stuck `pending`) and prevents `--resume` from re-evaluating the gate on every resume. The B.7.E staleness resume hook can then check both `done` and `skipped` states cleanly.

### Step 13.A — Skip-check + AskUserQuestion (unless `--no-checkpoints`)

When `final_verdict ∈ {GO, PIVOT}` AND no skip condition fires:

- If `--no-checkpoints` is on: auto-fire (proceed to Step 13.B).
- Otherwise, ask via `AskUserQuestion`:

```
Question: "Verdict: <GO|PIVOT> at scale <L1|L2|L3>. Run deep funding research now?
(~8–18 WebFetches; produces 11_funding.md with 4 sections of named entities — grants, angels, VCs, anchor-procurement contracts.)"
Options:
  1. Run now — recommended/default
  2. Defer — exit cleanly; user can run `/idea_funding <slug>` later in a fresh session
  3. Skip permanently — mark Step 13 status: skipped (--resume won't re-prompt)
  4. Other (free-text)
```

Routing:
- Option 1 (Run now) → Step 13.B.
- Option 2 (Defer) → set `state.yaml.steps[13].status: pending`; print "Step 13 deferred. Run `/idea_funding <slug>` in a fresh session when ready (recommended within 90 days of verdict)." Exit cleanly.
- Option 3 (Skip permanently) → set `state.yaml.steps[13].status: skipped`; print "Step 13 skipped permanently. `--resume` will not re-prompt." Exit cleanly.
- Option 4 (Other) → parse free-text: "skip"/"never" = option 3; "later"/"defer" = option 2; anything else = option 1 with the free-text appended to brief as `[USER-STATED CONTEXT — apply skeptical lens]`.

### Step 13.B — Dispatch via `funding-sourcing-analyst`

Effectively delegate to `/idea_funding <slug>` (the standalone skill), or dispatch the agent directly with the same brief. Either keeps the dispatch contract single-sourced via `idea_funding.md` Step 2.

Brief MUST include (Standard Step Driver §0 MAST-defense check applies):

```
Brief for funding-sourcing-analyst:

audit_dir: /home/atgu/Projects/Ideas/audits/<slug>/
slug: <slug>
scale_mode: <L1|L2|L3>  # from state.yaml
geo: <EU27|DE|FR|IT|ES|NL|RO|+US|+UK>  # state.yaml; geo=global already filtered as skip condition
mode: full              # default for GO/PIVOT; --anchor-only flag would set mode: anchor_only
final_verdict: <GO|PIVOT>
final_confidence: <high|med|low>

(Standard Step Driver Driver.1 brief structure applies — sanitized, structured task, prior-step artifacts as quote-blocks. Per idea_funding.md Step 2 for the canonical brief.)

[USER-STATED CONTEXT — apply skeptical lens — if any]:
<any free-text from Step 13.A Option 4>
```

### Step 13.C — Regex audit (per Standard Step Driver Driver.3) — funding-specific checks

In addition to the universal regex audit, apply Step 13-specific checks:
- Frontmatter `funding_data_as_of`, `staleness_warning_after`, `fetch_count`, `fetch_budget_cap`, `mode` all present
- Every named entity has a non-`[TBD]` First-contact action
- No personal emails appear (regex scan; `[BANNED-CONTACT-INFO]` flag → re-invoke)
- `fetch_count` ≤ `fetch_budget_cap` (unless override flag passed)
- 5 closing blocks present
- Cross-section reconciliation with `08c_capital_investor_fit.md` named investors

Retry once on failure (Driver.4). If second invocation fails, commit with `[SOURCE-DISCIPLINE-FAILURE]` flag on `state.yaml.steps[13]`.

### Step 13.D — Update `state.yaml`

- `steps[13].status: done` with timestamp
- `steps[13].mode: full|anchor_only`
- `last_updated: <ISO timestamp>`
- Do **NOT** touch `final_verdict` / `final_confidence` (Step 13 is informational, doesn't change the verdict)
- Do **NOT** modify `_calibration.jsonl` (decision: Step-13 presence is filesystem-checked via `11_funding.md` existence; no ledger schema bump — per Phase C architectural decision #11)

### Step 13.E — Print summary + exit

Print:

```
─ Step 13 (Funding) complete ─────────────────────────────────
Artifact: audits/<slug>/11_funding.md
Mode: <full|anchor_only>
Fetch count: <N> / <cap>
Sections populated:
  §1 Grants:           <K> named programs (deadlines confirmed: <K_fresh>)
  §2 Angels:           <K> named investors
  §3 VC firms:         <K> firms with thesis match
  §4 Anchor proc.:     <K> entries (public RFP: <K_pub>, private design-partner: <K_priv>)
Freshness:  data_as_of=<date>  ·  staleness warning after <date+180d>
Closing blocks: 5/5 present
Cross-section reconcile: <agree | [RECONCILE-N] flags>
```

Suggest next action based on `scale_mode` + verdict:
- **L1 GO** → "Top 3 first-contact actions for the next 7 days: <quote from §4 row 1, §4 row 2, §1 row 1>. Re-read 11_funding.md."
- **L2 GO** → "Build a contact-tracker spreadsheet from §1 + §2 + §4. Top 5 contacts to schedule this month: <quote>."
- **L3 GO/PIVOT** → "Prioritize §3 partners with active 2026 thesis posts in the space. Build warm-intro paths via the named portfolio CEOs in column 7."

For PIVOT verdicts at any scale, append: "Note: the verdict was PIVOT — re-audit the suggested pivot direction before pursuing this funding list. Some funding entries may not apply to the pivot scope."

Then print full path summary:

```
Full audit trail:
  audits/<slug>/state.yaml
  audits/<slug>/10_verdict.md  (verdict + SCORECARD + scale-mode plan)
  audits/<slug>/11_funding.md  (funding registry)
  audits/<slug>/sources.md
  audits/_calibration.jsonl
```

## Checkpoint format (after every wired step, except where noted)

After completing a step, print:

```
─ Step <N> of 12: <name> ─────────────────────────────────────
Artifact: audits/<slug>/<file>.md
Findings this step:
  <KPI 1>  <value>  <benchmark>  [<TAG>]  §<file>#<anchor>
  <KPI 2>  ...
  (3–5 lines, the load-bearing findings)

Running tally:  FATAL: x   BLOCKER: y   RISK: z   ADVANTAGE: w
Provisional verdict if we stopped here:  <verdict> (<confidence>)

Source quality:  <K> primary, <M> secondary, <L> unverified · all WebFetch-OK | <flag>
Agent flagged for your attention:
  - "<quote of any inverse-falsifier or 'I couldn't find' note from the agent>"
```

Then **always** ask the user via `AskUserQuestion` — exactly 4 options (the 5th is auto-"Other"):

```
Question: "Step <N> complete. How do you want to proceed?"
Options:
  1. Continue to Step <N+1> (<name>) — recommended/default
  2. Add context for next step — free-text injection
  3. Re-run this step with refined brief — free-text refinement
  4. Write verdict now from partial evidence — skips to Step 12 with --partial flag
```

If user picks 2: capture the free-text, append to `state.yaml.user_context_injected`, then re-ask the question.
If user picks 3: capture the refinement, re-invoke the same agent with the refinement appended to the brief, then re-show the checkpoint.
If user picks 4: jump to Step 12 with `partial=true`.
If user picks Other: parse the free-text:
- "stop", "exit", "pause" — write state and exit cleanly; user can `/idea_audit --resume <slug>` later
- "fast-forward to N" or "skip to N" — suppress checkpoints until step N
- anything else — interpret as additional context and treat as option 2

## Auto-skip rules (Phase A: disabled because Steps 4 and 8 are stubs)

In Phase B, two auto-skips bypass the user checkpoint:
- Step 4 (Triage) → `fatal_finding=true` → jump to Step 12 NO_GO
- Step 8 (Regulatory) → EU AI Act class `unacceptable` → jump to Step 12 NO_GO

In Phase A, both are stubs, so no auto-skips fire. State this in the post-Step-4 stub notice.

## --no-checkpoints mode

If `--no-checkpoints` is passed, skip every AskUserQuestion checkpoint after each step. Run through all 12 steps in sequence. Still write `state.yaml` at each step. Still apply auto-skip rules (Phase B). Recommend against this for the user's first 3 audits while they calibrate trust.

## --resume mode

If `--resume <slug>` is passed:

1. Read `audits/<slug>/state.yaml`
2. **Stub-overwrite policy** (per `CLAUDE.md`): treat `status: stub-skipped` as equivalent to `status: pending`. Identify the first step with `status` ∈ {`pending`, `stub-skipped`}.
3. Print: "Resuming audit <slug> at Step <N> (<name>). Last update: <timestamp>. <K> stub steps will be re-run with real agents."
4. Continue from that step. Inherit `geo`, `depth`, `checkpoints`, `pre_register` from `state.yaml`.
5. When overwriting a stub artifact (file first line matches `^# .* — .* \(NOT YET IMPLEMENTED`), prepend `[OVERWRITES PRIOR STUB on <ISO timestamp>]` as the first line of the new artifact for audit-trail purposes.

If all steps are `done`, print "Audit <slug> is complete — see audits/<slug>/10_verdict.md" and exit.

## --depth=paranoid mode (extra rigor for high-stakes audits)

If `--depth=paranoid` is passed, the wizard additionally applies the **Self-consistency calibration layer** (per Standard Step Driver §7) to each load-bearing KPI claim in each research agent's artifact. Each load-bearing KPI is re-derived N=3 times via separate Agent invocations with re-framed briefs; numeric divergence > 30% across samples is flagged `[CALIBRATION-UNSTABLE]` and the KPI is marked `[ESTIMATE]` with bounds.

Paranoid mode roughly triples the per-step compute cost of single-agent steps. Use only when the verdict will drive a € decision > €50k or when the seed touches a high-uncertainty category (frontier-AI applications, new regulatory categories, etc.).

## Avoid

- Auto-advancing through steps in `--no-checkpoints` mode without writing `state.yaml` after each step (the resume contract requires per-step persistence)
- Allowing an agent to "read the user's conversation" — every agent brief is sanitized; only artifacts + structured question + labeled user-context
- Skipping the regex audit on agent output (the Source Protocol enforcement only works if it actually runs)
- Letting Step 12 issue a GO when only market evidence (Phase A) is available — Phase A should yield DEFER or low-confidence PIVOT by design
- Truncating `_calibration.jsonl` — verdict history is irreplaceable; append-only
- Editing `00_seed.md` after the audit starts — the original seed is immutable evidence

## Output expectations

By the end of a Phase B+C wired pass on a new seed, the audit dir contains:
- `state.yaml` with all 12 steps marked `done` (plus Step 13 `done|skipped|pending` per the GO/PIVOT-gated dispatch)
- `00_seed.md`, `01_clarification.md`, `01b_falsifier.md` (if deep mode)
- `02_triage.md` (red-team-analyst quick-mode)
- `03_market.md` (market-size-analyst)
- `04_competition.md` (competitive-landscape-analyst)
- `05_customer.md` (customer-segment-analyst)
- `06_regulatory.md` (regulatory-compliance-analyst) — with regex-parseable `EU_AI_ACT_CLASS:` line
- `07_technical.md` (technical-feasibility-engineer)
- `08a_unit_economics.md` + `08b_gtm.md` + `08c_capital_investor_fit.md` (sub-files)
- `08_business.md` (wizard-merged with Cross-agent reconciliation block)
- `09a_da.md` + `09b_premortem.md` (sub-files)
- `09_redteam.md` (wizard-merged with Cross-mode synthesis block)
- `10_verdict.md` (verdict-synthesizer output with SCORECARD + adversarial debate + scale-mode plan)
- `11_funding.md` (Phase C — produced only if Step 13 ran; 4-section funding registry of named entities)
- `sources.md` (all URLs from all agents with claim + access date + primary/secondary tag)
- One new line in `audits/_calibration.jsonl` with full Phase-B schema (Step 13 presence is filesystem-checked, not ledger-tracked)

## Related

- `/idea_init` — bootstrap the workspace (run before first audit)
- `/idea_status <slug>` — read-only inspection of an existing audit
- `/idea_market <seed-or-slug>` — standalone market sizing (Phase B)
- `/idea_verdict <slug>` — regenerate verdict for an existing audit
- `/idea_funding <slug>` — Phase C — standalone funding research (also auto-dispatched from Step 13 when verdict ∈ {GO, PIVOT})
- `/sci_falsify` — invoked by Step 3 in deep mode for kill-criteria pre-registration
- `/sci_brainstorm triage` — upstream complement: compare 3–5 seeds before picking one to audit
