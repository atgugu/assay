---
description: Standalone business analysis — bundles 3 agents in serial dispatch (unit-economics + GTM + capital-and-investor-fit), then wizard-merges into 08_business.md with the Cross-agent reconciliation block (CAC across agents, ARPU consistency, build-cost consistency). The €100M+ outcome thesis is REQUIRED for any GO verdict.
argument-hint: "<slug-or-seed>  [--only=unit-econ|gtm|capital]  [--standalone-out=<path>]"
allowed-tools: Read, Write, Bash(ls:*), Bash(test:*), Bash(date:*), Bash(mkdir:*), Bash(grep:*), Bash(cat:*), Agent, AskUserQuestion, WebSearch, WebFetch
model: claude-opus-4-7
---

## Context

- Today: !`date +%Y-%m-%d`

## Task

Run business analysis (3-agent bundle by default) for **$ARGUMENTS**.

## Step 0 — Resolve target + mode

Same UPDATE/STANDALONE logic as `/idea_market`. Parse `--only=<one of unit-econ|gtm|capital>`:
- Default: dispatch all 3 agents (serial), merge into `08_business.md`
- `--only=unit-econ`: dispatch only `unit-economics-analyst` → `08a_unit_economics.md`
- `--only=gtm`: dispatch only `gtm-channel-analyst` → `08b_gtm.md`
- `--only=capital`: dispatch only `capital-and-investor-fit-analyst` → `08c_capital_investor_fit.md`

## Step 1 — Serial dispatch of 3 agents (default)

Order matters because `gtm-channel-analyst` and `capital-and-investor-fit-analyst` reference earlier sub-files.

### Step 1.A — unit-economics-analyst

```
Brief for unit-economics-analyst:

audit_dir: <path>
slug: <slug>

Clarified problem: <quote 01_clarification.md>
Market: <quote 03_market.md>
Customer: <quote 05_customer.md — especially WTP>
Competition: <quote 04_competition.md — for differentiation pricing premium>

Your structured task:
Produce 08a_unit_economics.md per "Output schema — 08a_unit_economics.md".
- Speed-to-revenue KPIs as FIRST-CLASS lead block (time to first paying customer / €10k MRR / €100k ARR / ramen profitability)
- CAC anchored to named channel analogs (will be reconciled with GTM agent)
- LTV with named retention analog
- LTV/CAC, payback, gross margin, NRR, burn multiple, Rule of 40, capital efficiency

Source Protocol §§1–8, Self-RAG, 5 closing blocks.
```

Dispatch via Agent. Regex-audit per Standard Step Driver.

### Step 1.B — gtm-channel-analyst

```
Brief for gtm-channel-analyst:

audit_dir: <path>
slug: <slug>

Clarified problem: <quote>
Customer: <quote 05_customer.md>
Unit economics (read for CAC reconciliation): <quote 08a_unit_economics.md>

Your structured task:
Produce 08b_gtm.md per "Output schema — 08b_gtm.md".
- ACV + sales-motion fit (named analog)
- Sales cycle length matched to ACV
- Win-rate benchmark
- Top-3 channels with NAMED entry paths (NOT "content marketing" generic)
- Channel concentration risk
- First-50-customer plan with NAMED ENTITIES (companies, communities, conferences, individuals, newsletters)
- CAC reconciliation with 08a_unit_economics.md (must show explicit reconciliation paragraph)

Source Protocol §§1–8, Self-RAG, 5 closing blocks.
```

Dispatch + audit.

### Step 1.C — capital-and-investor-fit-analyst

```
Brief for capital-and-investor-fit-analyst:

audit_dir: <path>
slug: <slug>

All prior artifacts as quoted context.

Your structured task:
Produce 08c_capital_investor_fit.md per "Output schema — 08c_capital_investor_fit.md".
- Cash to first paying customer (from 07/08a)
- Pre-seed / seed / Series A capital required (anchored to named EU comparable rounds)
- Total capital to break-even
- Capital path classification: bootstrap-revenue | angel | pre-seed-VC | seed-VC | deep-tech-grant | hybrid | unfundable
- **REQUIRED for GO**: Plausible €100M+ outcome thesis (one paragraph + ≥3 named comparable exits/rounds with cited values)
- Comparable funding rounds last 12mo (hot/cold classification)
- ≥3 named plausible acquirers with rationale
- Defensibility growth path (the moat as it develops across €100k → €10M → €100M ARR)
- Distribution thesis (how 10x growth without burning all capital)
- Capital efficiency target
- Hype-risk check
- Active EU grants if material (EIC, Horizon, national)

Source Protocol §§1–8, Self-RAG, 5 closing blocks.
```

Dispatch + audit.

## Step 2 — Wizard-merge into `08_business.md`

After all three sub-files exist, write `08_business.md`:

```markdown
# 08 — Business (unit economics + GTM + capital + investor fit)

## Index
- §08a Unit economics — by unit-economics-analyst
- §08b GTM — by gtm-channel-analyst
- §08c Capital & investor fit — by capital-and-investor-fit-analyst

## Cross-agent reconciliation (wizard-written)

| Numeric | 08a value | Other-source value | Verdict |
| **CAC** | €<X> | 08b: €<Y> | <agree | [RECONCILE]> |
| **ARPU/ACV** | €<X> | 03 (market): €<Z> ; 05 (customer WTP): €<W> | <agree | [RECONCILE]> |
| **Build cost** | 08c: €<X> | 07 (technical): €<Y> | <agree | [RECONCILE]> |
| **Time-to-revenue** | 08a: <X mo> | 07: <Y mo> | <agree | [RECONCILE]> |

Any `[RECONCILE]` flags feed verdict-synthesizer's Step C.5.

---
[concatenated 08a content]
---
[concatenated 08b content]
---
[concatenated 08c content]
```

## Step 3 — Update state + summary

UPDATE state.yaml step 10 → done. Summary:

```
─── /idea_business summary ────────────────────────────────────
Slug:                  <slug>

Unit economics (08a):
  Time to first paying customer: <weeks> · [<TAG>]
  Time to €10k MRR:              <months>
  LTV/CAC:                       <ratio> · [<TAG>]
  Gross margin:                  <%>

GTM (08b):
  Sales motion:        <PLG|sales-led|channel|partner>
  ACV:                 €<X>
  Top channel:         <named>  CAC: €<Y>
  First-50 plan:       <N named entities>

Capital + investor fit (08c):
  Capital path:        <bootstrap-revenue|angel|pre-seed-VC|seed-VC|...>
  €100M+ thesis:       <present | ABSENT — BLOCKS GO>
  Comparable exits:    <N> deals
  Hot/cold:            <hot|warming|steady|cold|cooling>
  Named acquirers:     <N>

Cross-agent reconciliation: <K [RECONCILE] flags>

Tag tally: FATAL: x  BLOCKER: y  RISK: z  ADVANTAGE: w

Next: /idea_redteam (Step 11) → /idea_verdict (Step 12)
─────────────────────────────────────────────────────────────────
```

## Avoid

- Skipping serial order — race conditions on `sources.md` writes
- Allowing GTM agent's CAC and unit-econ agent's CAC to differ without explicit reconciliation paragraph
- Letting capital-investor agent omit the €100M+ thesis (required for any GO)
- Treating named acquirers as "Google, Microsoft" without strategic-rationale + recent-precedent

## Related

- `/idea_audit` — wires this as Step 10 (3-agent bundled)
- `/idea_customer`, `/idea_market`, `/idea_compete`, `/idea_technical` — upstream
- `/idea_verdict` — downstream consumer of the cross-agent reconciliation
