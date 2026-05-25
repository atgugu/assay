# 00 — Seed

**Original**: predictive crowd movement - tourist flow, protests, football games, business opportunities for shops stores etc pedestrian movement prediction

**Source**: CLI arg to `/idea_audit` (also tracked in `/home/atgu/Projects/Ideas/ideas.md` as a truncated line)

**Invocation**: `/idea_audit "predictive crowd movement - tourist flow, protests, football games, business opportunities for shops stores etc pedestrian movement prediction" --depth=deep --geo=EU27`

**Slug**: predictive-crowd-movement

**Audit dir**: audits/2026-05-25_predictive-crowd-movement/

**Created**: 2026-05-25T12:46:56+02:00

**Wizard version**: phase-A

## Initial reading of the seed (not yet validated)

The seed mixes three distinct customer/value propositions in one phrase:

1. **Crowd movement prediction as a forecasting product** — predicting where pedestrians/crowds will be at time T (model + data).
2. **Use cases named**: tourist flow (city-level, B2G or B2B tourism), protests (B2G public-safety, B2B media/insurance), football games (B2G policing + B2B venue/transport ops).
3. **B2B retail "where should I open my shop / staff up today"** — fundamentally a different product (location intelligence / footfall analytics) than (1).

These are NOT the same product. (1) is an event-driven anomaly forecaster; (3) is a steady-state location-intelligence SaaS. Clarification (Step 2) must pick **one primary** — the seed as written is multi-product and will fail bottom-up sizing.

**Existing players in adjacent space** (to be verified at Step 5, do not cite yet):
- Footfall/location intelligence: Placer.ai (US), Huq Industries (UK), Geoblink (ES), Dalia/Veraset, Spaceti, Locomizer.
- City-scale crowd/tourist flow: Skyhook, Carto, Mapbox Movement, BeMobile, Vodafone Analytics, Telefónica Smart Steps (now wound down), Mediamobile.
- Event-day crowd safety: WaitTime, CrowdVision, Inrix, Movement Strategies.

This makes the space **crowded but fragmented** — a clarification-first audit, not a market-discovery one.
