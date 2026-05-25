# 01b — Pre-registered kill criteria (sci_falsify discipline)

**Pre-registered on:** 2026-05-25T12:50:00+02:00
**Pre-registered BEFORE:** Step 5 (Market), Step 6 (Competition), Step 8 (Regulatory), Step 9 (Technical), Step 10 (Business).
**Discipline:** These kill conditions cannot be retroactively softened. If any FATAL condition fires during research, the audit must produce NO_GO unless the red-team artifact (Step 11) explicitly refutes in writing with cited evidence.

**Why pre-register?** Crowd-flow / location-intelligence is a "warm and exciting" idea — high risk of confirmation bias. Pre-locked thresholds force the auditor to honor the negative evidence when it appears, not to relax them after seeing the market sizing.

---

## Kill condition 1 — Market size (FATAL)

**IF** the bottom-up SAM for B2G + B2B venue/event crowd-forecasting in EU27 < **€80M/yr** at 2026 prices, with primary-source backing,
**THEN** NO_GO — the market is too small to support a €100M-outcome thesis (the verdict optimization target requires VC-fundability).

Operationalization (the math chain Step 5 must show):
- N(EU cities with population > 300k AND top-flight football club AND tourism > 1M overnight stays) × realistic_ACV_per_year × adoption_within_5_yr ≥ €80M.
- Adjacent demand: N(EU stadia hosting matches with > 30k attendance) × realistic_ACV ≥ €15M.

Source bar: must cite Eurostat, UEFA financial reports, and at least one regulator/transport-authority RFP value to validate ACV.

---

## Kill condition 2 — Competitive moat (FATAL)

**IF** a named incumbent (Placer.ai, Telefónica LUCA, Huq Industries, CrowdVision, Inrix, Carto, or a Big-4 telco mobility unit) has shipped a city-scale event-driven crowd-density forecasting product to ≥3 paying EU cities by 2026,
**THEN** NO_GO — the white-space is already occupied; founder is late.

Operationalization: Step 6 (Phase B) must produce evidence of (a) live city case study, (b) press release of contract win, or (c) procurement portal entry.

Phase A fallback: Step 5 (Market) agent must include a competitor-presence screen. If ≥3 of the named players show city-safety case studies during fetch, this fires as **BLOCKER** (not FATAL) due to incomplete Step 6.

---

## Kill condition 3 — Regulatory (FATAL)

**IF** the EU AI Act classifies real-time pedestrian-density forecasting from telco aggregate data + GTFS as **"high-risk biometric identification"** or **"prohibited"** when deployed for law-enforcement public-safety use,
**THEN** NO_GO — the B2G public-safety wedge is regulatorily forbidden; pivot to private B2B-only.

Operationalization: read Annex III of the AI Act + 2024–2026 EU Commission guidance on "crowd analytics" and "remote biometric identification". If ambiguous, fires as **BLOCKER** (not FATAL).

Adjacent regulatory risk: GDPR Article 5/6 lawful-basis test for the telco aggregate. If anonymization standard fails (e.g., k-anonymity < 5 at 100m × 15-min grid), this is a **BLOCKER** for the entire data layer.

---

## Kill condition 4 — Time-to-first-revenue (BLOCKER)

**IF** realistic time from contract signing to first €30k pilot revenue for a Tier-2 EU city > **9 months** (B2G procurement cycle),
**THEN** PIVOT — violates the Workspace Contract's speed-to-revenue gate ("first paying customer in < 3 months; €10k MRR in < 6 months").

Operationalization: Step 10 (Business, Phase B stub) would cite 3 named EU smart-city procurement timelines (e.g., Barcelona Sentilo, Hamburg Smart City, Vienna DigitalCity). Phase A: the market-size-analyst is asked to flag any procurement-timeline evidence encountered.

This is BLOCKER because there are credible mitigations: stadium/venue B2B procurement (faster), insurance/reinsurance partnership channels, EU R&D grants as bridge revenue.

---

## Kill condition 5 — Data dependency (BLOCKER)

**IF** the only viable mobility-data source is a single telco's commercial aggregate AND no contract or pilot agreement is achievable within 6 months at < **€100k/yr** for one-city scope,
**THEN** PIVOT — the data dependency creates an unfundable cost structure and supplier-power risk.

Operationalization: Step 9 (Technical, Phase B stub) would price one quote each from Deutsche Telekom Motionlogic, Orange Smart Mobility, Telefónica LUCA, Vodafone Analytics, and one alternative data broker (Veraset / Spectus / SafeGraph EU). Phase A: market-size-analyst is asked to surface any public pricing or RFP value.

---

## Kill condition 6 — Model accuracy floor (RISK)

**IF** a naive baseline (prior-week average + event-calendar override) achieves > **85% of the GNN's RMSE reduction** on a published benchmark (e.g., NYC-Taxi flow, Beijing-Bike density),
**THEN** the technical differentiation is weak; verdict is downgraded to PIVOT (toward UX/data/integration moat rather than model moat).

Operationalization: Step 9 (stub in Phase A). Carried forward as a flagged hypothesis.

---

## Kill condition 7 — Funding climate / VC narrative (RISK)

**IF** there are < **3 named European seed/Series-A rounds in 2024–2026** to companies pitching "urban mobility / crowd analytics / city operating system" with > €5M raised,
**THEN** the VC narrative collapses; verdict downgrades to DEFER pending climate change.

Operationalization: Step 8 (Capital & Investor Fit, Phase B stub) would screen Crunchbase / Sifted / EU-Startups. Phase A: deferred; market-size-analyst may surface evidence opportunistically.

---

## Summary table for the verdict-synthesizer

| # | Condition | Severity | Resolved by Phase | Status post-Step-5 |
|---|---|---|---|---|
| 1 | SAM < €80M/yr | FATAL | Step 5 | TBD |
| 2 | Incumbent ships city-scale safety forecast to ≥3 EU cities | FATAL (BLOCKER in Phase A) | Step 6 (5 in Phase A) | TBD |
| 3 | EU AI Act high-risk / prohibited classification | FATAL (BLOCKER if ambiguous) | Step 8 | DEFERRED (stub) |
| 4 | Time-to-pilot-revenue > 9 months | BLOCKER | Step 10 | DEFERRED (stub) |
| 5 | No data partnership < €100k for 1-city scope in 6 months | BLOCKER | Step 9 | DEFERRED (stub) |
| 6 | Naive baseline ≥ 85% of GNN performance | RISK | Step 9 | DEFERRED (stub) |
| 7 | < 3 EU seed/Series-A comparables 2024–2026 | RISK | Step 8 | DEFERRED (stub) |

**Inverse falsifier (what would make me MORE confident in GO):**
- Public RFP > €500k from any EU Tier-1 city explicitly for "predictive crowd analytics" in 2025–2026.
- A signed letter-of-intent from a Bundesliga or La Liga club for a pilot.
- Telefónica LUCA or DT Motionlogic publicly retreating from crowd-safety vertical.
- An EU Horizon Europe call funded specifically for predictive urban crowd-management products > €10M.

These would push toward GO regardless of TAM headline because they would prove demand + diminished competition + funded budget pool simultaneously.
