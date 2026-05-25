# 01 — Clarification

**Auditor note:** User picked "All three (composite platform)" as market framing but "Dashboard + forecast API for 1 city" as MVP, and "Not sure — let auditor probe" on pain. This is an internal tension: a composite-platform TAM headline cannot co-exist with a single-vertical wedge MVP at audit-grade confidence. Both are recorded; the auditor will treat the wedge as load-bearing and the composite framing as the **growth narrative** (Step 12's VC story), not as the addressable market in the first 18 months.

The pain answer was deferred to the auditor, so this artifact carries a `[CLARIFICATION-INSUFFICIENT]` flag on the Pain dimension. Step 12's confidence will be downgraded accordingly.

---

## Customer

**Composite-platform framing (long-term, Step 12 VC narrative)**: B2G public-sector buyers (city police, transit authorities, tourism boards) + B2B venue/event/insurer + B2B retail/real-estate analytics.

**Wedge (load-bearing for MVP and Steps 5/9)**: ONE customer city's public-safety / mobility office.
- Sub-segment: a mid-to-large EU city (population 300k–2M) with a top-flight football club, a tourism flow > 1M overnight stays/yr, and an in-house GIS or "smart city" unit that already commissions data products.
- Named exemplar candidates (NOT YET CONTACTED): Munich, Hamburg, Cologne (DE Bundesliga); Madrid, Barcelona, Seville (ES La Liga); Milan, Naples (IT Serie A); Lisbon, Porto (PT Primeira). Romania candidates: Bucharest, Cluj-Napoca.
- The buyer is a public-sector official or smart-city PMO — slow procurement, high reference-value, low churn once landed.

## Pain (severity hypothesis) — `[CLARIFICATION-INSUFFICIENT]`

**Working hypothesis (auditor's best guess, NOT validated):** Cities cannot quantitatively predict where dangerous pedestrian density will build up during football match-days, demonstrations, and tourism peaks. Current practice is briefing-room intuition + radio dispatch. After Itaewon (2022, 159 dead) and Astroworld (2021, 10 dead), liability for high-density events has shifted toward "did you have a quantitative forecast on file?" This is the strongest pain narrative consistent with the user's MVP choice.

Alternative pain framings that the user chose NOT to commit to:
- Retail siting (dead-store CAPEX) — orthogonal to the MVP; ignore in Phase A
- Overtourism political backlash — adjacent, weaker urgency (politicians can delay; police can't)

**Pain severity confidence: LOW** — Step 7 (Customer) would normally validate via 5+ buyer interviews; Phase A skips Step 7. The verdict-synthesizer will treat the pain narrative as unconfirmed and downgrade to DEFER unless market and technical signal compensate.

## Mechanism (1 sentence)

A real-time ingestion + forecasting service that fuses mobile-network signaling data, anonymized telco aggregates, ticketed-event schedules, weather, public-transit GTFS feeds, and historic crowd flows into a graph-neural-network density forecast at 100m grid × 15-minute granularity, delivered via dashboard + API to municipal operations centers.

## Geography (initial)

**EU27**, with one customer city as the launch beachhead (selected at Step 7 in Phase B; Phase A will market-size the EU27 envelope and a Germany/Spain/Italy sub-band because tourism + football density concentrate there).

## Build hypothesis (8-week founder-MVP)

**In scope:**
- One city, one stadium, one tourism district, one protest-prone square.
- Ingestion of: (a) one operator's telco aggregate or a commercial mobility-data feed (Veraset / Spectus / Tamoco / Cuebiq successor), (b) public events calendar, (c) weather, (d) GTFS transit feed, (e) ticket-sales data if the venue partners.
- Spatio-temporal model — start with a graph-conv + temporal-attention baseline; benchmark vs. naive prior-week-average and vs. published crowd-flow papers (e.g., DeepCrowd, STResNet variants).
- Dashboard: heatmap + 15-min forecast horizon up to 72h ahead, with alerting on density thresholds.
- API: REST endpoint returning grid-level forecast for downstream operational systems (CAD/transit-management).

**Out of scope (MVP):**
- Retail / siting product (would re-emerge in year 2 of the composite narrative).
- Multi-city deployment (single-city pilot → reference customer → replication).
- Consumer-facing app (different product, different unit economics).
- Real-time CCTV / camera-based density (very different data + regulatory profile — falls under EU AI Act high-risk biometric category).

## Differentiation hypothesis

The crowded adjacency (Placer.ai, Huq, Geoblink, Telefónica/Vodafone analytics, CrowdVision, Inrix) is mostly:
- **Steady-state, monthly resolution, retail-focused** — not real-time, not event-driven, not city-operations focused.
- **OR** stadium-only computer-vision systems (CrowdVision, WaitTime) — venue-internal, not city-scale.

The hypothesized differentiator is **city-scale + event-driven + sub-hour forecast horizon for B2G public-safety buyers**. Whether this is a real white-space or already occupied by a stealth incumbent is exactly what Step 5 (Market) and Step 6 (Competition, Phase B) must establish.

"AI-powered" is **not** the differentiation. The differentiation is data exclusivity (telco partnership), event-domain modeling, and a B2G procurement-defensible compliance posture.

## Why now (initial hypothesis)

Three converging triggers (each to be verified at Step 5 with cited sources):

1. **Liability shift post-Itaewon (2022) and Astroworld (2021)** — cities and event organizers face documented expectation of quantitative density forecasts in safety plans.
2. **EU overtourism + Cities Mission funding (Horizon Europe, "100 Climate-Neutral and Smart Cities by 2030")** — funded budget pool for predictive urban-data products.
3. **Telco mobility-data productization maturing** — Deutsche Telekom Motionlogic, Orange Smart Mobility, Telefónica LUCA all expanded API access 2023–2025; previously raw-only and lawyer-gated.

The "why now" is plausible but each leg needs a cited primary source before it survives Step 5.

---

**Open dimensions flagged for Step 5/6 (Phase B would resolve these):**
- Is the EU public-safety budget for predictive crowd analytics > €100M/yr?
- Has Placer.ai or Telefónica already filed a city-scale crowd-safety product?
- Does GDPR + EU AI Act treat telco-aggregate forecasts as high-risk?
- What's the realistic pilot ACV for a Tier-2 EU city ops contract (€30k / €60k / €150k)?
- Time-to-first-paying-pilot: < 6 months or > 12 months?
