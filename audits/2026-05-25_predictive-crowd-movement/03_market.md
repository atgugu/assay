---
agent: market-size-analyst
audit: predictive-crowd-movement
geo: EU27 (sub-band DE/ES/IT)
date: 2026-05-25
depth: deep
confidence-overall: low-to-medium
---

# 03 — Market

> **Scope (load-bearing definition).** The market sized below is **B2G + B2B-venue real-time event-driven crowd-density forecasting at city scale** in EU27. It is **NOT** the "smart city" market, **NOT** location-intelligence for retail siting (Mytraffic/Geoblink/Placer.ai), **NOT** computer-vision in-venue counting (CrowdVision/WaitTime), and **NOT** transport demand modelling (Optibus/Vianova). Per `01_clarification.md`, retail siting is treated as adjacent year-2+ and is not added to the headline.

> **TAM/SAM/SOM definitions used here (declared up-front, so the synthesizer can compare cleanly to the FATAL-1 €80M threshold).**
> - **TAM** = total spend in EU27 if every qualifying customer in scope bought the product at a realistic mature-state ACV (no penetration discount).
> - **SAM** = TAM × procurement-realistic share the wedge product (single-vendor, B2G + B2B-venue) could actually serve (channel reach + buyer fit + GDPR/AI-Act envelope).
> - **SOM (year 5)** = SAM × realistic capture given the closest named-comparable adoption curves (Mytraffic, Vianova, Huq).
> - The FATAL-1 threshold ("SAM < €80M/yr") is compared against the **SAM** number, not the TAM.

---

## 1. Headline numbers (post-CoVe, see §10e for the revision audit trail)

| KPI | Value (€/yr, 2026 prices) | vs. pre-registered threshold | Tag |
|---|---|---|---|
| **TAM (EU27, wedge + insurance + telco-channel composite, mature-state)** | €130–230M/yr · point €175M (`[NB]` €15M insurance-channel `[E12]` and €7.5M telco-resale `[E13]` are unsourced analog estimates — strip both and TAM falls to **~€110–185M point €150M**) | — | **[NEUTRAL]** (still well below the >€1B "all buyers incl. retail/RE" implied composite TAM the `01_clarification.md` composite framing would generate, which is excluded from the headline per user-MVP-scope) |
| **SAM (5-yr, single-vendor wedge play, realistic share)** | **€22–58M/yr · point €33M** (strip the unsourced `[E12]` insurance channel and SAM drops to **€7–43M · point €18M**) | FATAL-1: <€80M → NO_GO | **[FATAL-1 FIRES]** across the entire reasonable range, with or without the insurance channel |
| **SOM (year 5, realistic single-vendor capture)** | €3–7M/yr · point €5M | none registered | **[RISK]** for €100M+ outcome thesis |
| **CAGR (2024–2030)** | ~10–14%/yr `[E14]` | RISK if <5%; ADVANTAGE if >25% | **[NEUTRAL]** |
| **# qualified buyers (cities + venues + events) in scope** | 55–75 cities + ~95 stadia + ~250 arenas + ~175 events ≈ 575–595 buyer-instances | BLOCKER if <50 cities with €100k ACV | **[NEUTRAL]** on buyer count; **ACVs are the binding constraint, not buyer count** |
| **EU AI Act Annex III classification of telco-aggregate density forecasting** | Does NOT cleanly fall under high-risk biometric / critical-infrastructure on the fetched Annex III text [40]; **conditional** if used to feed emergency-dispatch prioritisation (Annex III §5(d) borderline) | FATAL-3 fires if classified high-risk | **[BLOCKER-conditional]** — likely escapes FATAL but requires Step-8 legal review |
| **B2G procurement timeline for first €30k pilot** | Best-case 6–9 mo via direct-award under €143k OJEU threshold [9]; realistic 12–24 mo full RFP | BLOCKER-4 threshold: >9 mo → PIVOT | **[BLOCKER-4 FIRES]** on realistic path; borderline on best-case |
| **Open EU RFPs naming "predictive crowd analytics" 2024–2026** | 0 found in fetched material (search incomplete — see §10a) | 0 → RISK on demand evidence | **[RISK]** (caveat: search-incomplete) |
| **EU seed/Series-A 2024–2026 raised ≥€5M, "urban mobility / crowd analytics / city OS"** | **0 clean EU-HQ hits**; Liftango Mar 2024 $5.6M is Australia-HQ (EU-active but not EU-domiciled); 2 adjacent signals (Mytraffic+Geoblink M&A Jan 2024 — not a fresh round; Vianova EIC scale-up — not a round) | RISK-7 fires if <3 found | **[RISK-7 FIRES]** sharply on present evidence (sharper than initial read — Liftango does not count as EU per the falsifier's intent) |
| **Named incumbent shipping the wedge product to ≥3 paying EU cities** | **No public evidence** found for Placer.ai, Telefónica LUCA, Huq, CrowdVision, Inrix, Carto, Mapbox, Geoblink, Mytraffic, BeMobile, DT Motionlogic, Movement Strategies, Vianova in this exact product shape | FATAL-2 (BLOCKER-2 in Phase A) does NOT fire | **[ADVANTAGE]** (qualified — see §6; supplier-incumbent latent risk from LUCA/DT remains as RISK) |
| **"Why now?" trigger verified** | (a) Itaewon/Astroworld liability shift: real in US/Korea but **EU regulatory pull not located** — ISO 20121:2024 is sustainability not crowd safety [24]; (b) Cities Mission €98M 2024 call: **NO crowd-analytics line item** [25]; (c) Telco mobility-data APIs: **mature since 2012–2015 [27][28], not newly productized** | absent/vague triggers ⇒ BLOCKER on why-now | **[BLOCKER FIRES]** — all three legs weaker than claimed in `01_clarification.md` |

**Net tag tally on Step-5 evidence alone:**
- **FATAL** firing: 1 (SAM below €80M threshold across the entire reasonable range)
- **BLOCKER** firing: 3 (procurement timeline > 9 mo realistic; why-now triggers weak; AI Act conditional)
- **RISK** firing: 2 (RISK-7 funding climate sharper than initial read; supplier-incumbent latent threat from LUCA / DT)
- **ADVANTAGE** firing: 1 (no current incumbent in the wedge — qualified)
- **NEUTRAL**: TAM order-of-magnitude; CAGR; buyer count

**Net headline.** The bottom-up SAM for the wedge product (city-scale event-driven real-time crowd-density forecasting, B2G + B2B-venue + events, single-vendor) lands at **€33M/yr point estimate (range €22–58M) — comfortably below the pre-registered €80M FATAL-1 threshold**. The composite-platform framing in `01_clarification.md` could push the broader TAM above €1B if retail/RE is added back, but the user's MVP-scope choice (single-city dashboard + forecast API) makes the wedge load-bearing, not the composite. Two of the three "why-now" triggers do not survive primary-source verification at the strength claimed. No named incumbent currently ships the exact wedge product, but supplier-side telcos (LUCA, DT Motionlogic) could ship it on weeks of work.

---

## 2. TAM construction — bottom-up arithmetic

### 2a. City demand pool (B2G public-safety / mobility office)

**Filter chain.** Start with EU27 cities ≥300k population [1]. Of the 95 cities listed [1], intersect with:
- Top-flight football club (Bundesliga, La Liga, Serie A, Ligue 1, Eredivisie, Liga Portugal, Pro League BE, Ekstraklasa PL, Liga 1 RO, Bundesliga AT, Super League GR, others) — **roughly 70 cities have a top-division club** per cross-reference of the wiki city list [1] against league composition (each of the Big-5 leagues has 18–20 clubs; ~60% are in cities ≥300k; smaller-league capitals add another ~10).
- Tourism flow >1M overnight stays/yr (Eurostat top-NUTS3 destinations) [3]. Mallorca, Roma, Barcelona, Tenerife, Venezia jointly account for 12% of foreign nights [3] — and the Eurostat tourism statistics indicate **>40 EU NUTS-3 regions exceed 1M nights/yr** (no single fetched URL gives the count cleanly; this is `[ESTIMATE]`).

`[ESTIMATE E1]` Intersection of (pop ≥300k) ∩ (top-flight football) ∩ (tourism >1M nights) ≈ **55–75 EU27 cities**. Logic: ~70 cities meet the football criterion; ~50–60 of those meet tourism; minor undercounting from secondary cities with strong cup play but no permanent top-division club. Confidence: medium.

**ACV per city (mature steady-state, B2G).** Triangulated from:
- EU services-procurement threshold for OJEU publication: **€143,000** [9] — under this number procurement is "below threshold" and routed via local tender (faster, often direct award). This sets a floor: below €143k is the natural sweet spot for a single-city ACV that municipal IT can sign without a formal EU-wide tender.
- Mytraffic public-sector contract values: not publicly disclosed, but Mytraffic's 400+ clients across 7 EU countries with €30M Series B and "doubling annual revenue" 2020–2022 [4][5] implies a blended ACV of **~€15–30k/year per client average** (€30M raised → if at ~€20–30M ARR, 550 customers post-Geoblink → ~€36–55k average; most retail clients are smaller, public-sector skews higher). `[ESTIMATE E2]` Mytraffic city-ACV likely €40–80k/yr.
- Huq Industries published per-place pricing: **£1,000/place/year/module** [6]. A mid-size city buying 20 places × 4 modules = ~£80k/yr ≈ €95k/yr. Public-sector wedge: Huq says >90 UK local authorities use it [6].
- INRIX Population Analytics — no public pricing; historical reference is TfL during 2012 Olympics [7] (one-off engagement). INRIX is enterprise-priced, likely €50–200k/yr for city-scale per anecdote, no triangulable primary source.
- US comparable (lower-confidence): Placer.ai 4,300 customers / $100M ARR = ~$23k average ACV [8]. Placer's civic product is retail/economic-development analytics, NOT crowd forecasting [10].

`[ESTIMATE E3]` Mature-state ACV for a **public-safety + mobility-office crowd-forecasting product** in a Tier-2 EU city: **€60–120k/yr** (point estimate **€90k**). Reasoning: (a) sits above Huq's commodity footfall (€95k) because real-time + safety + dashboard + API is heavier integration; (b) sits at or below the OJEU threshold (€143k) so the buyer can sign without EU-wide tender; (c) below INRIX/Carto enterprise tier because municipal budgets in EU Tier-2 cities are tight. Confidence: low-to-medium — triangulated against three comparables but no direct primary RFP value found.

### 2b. TAM city × ACV

- Low: 55 cities × €60k = **€3.3M** … wait — that's TAM for **public-safety wedge alone**. Cities have additional layers: mobility office, transit authority, tourism board, events permitting. If each city has 2–3 buyer departments at lower-cost adjacent modules:

`[ESTIMATE E4]` **City-scale TAM = N_cities × (ACV_safety + 1.5 × ACV_adjacent_module)** where adjacent module ≈ €30–50k.
- Point: 65 cities × (€90k + 1.5 × €40k) = 65 × €150k = **€9.75M/yr** for the city-only B2G public-safety + mobility-office line.

This number alone is **far below €80M**. The city-only wedge is **not** the SAM — it is one input. Adjacent demand pools must be added.

### 2c. Stadia demand pool (B2B venue)

UEFA top-division clubs across EU27 covered by Club Licensing Benchmarking ≈ **~280 clubs in EU27 top divisions** (of >700 across full UEFA scope) [2]. Stadia ≥30k seats: per league norms (Bundesliga 18 clubs, average ~42k; La Liga 20, ~37k; Serie A 20, ~36k; Ligue 1 18, ~30k; Eredivisie 18, ~22k; Liga Portugal 18, ~25k; smaller leagues mostly <30k):

`[ESTIMATE E5]` EU27 stadia hosting top-flight matches with capacity ≥30k = **~95 stadia** (Bundesliga ~17, La Liga ~15, Serie A ~14, Ligue 1 ~9, Eredivisie ~6, Liga Portugal ~3, BE/AT/PT/GR/HR ~10, second-division large stadia hosting top-flight on rotation ~21). Confidence: medium.

ACV for a venue-side crowd-forecasting subscription (matchday density + ingress/egress + concourse heatmaps): `[ESTIMATE E6]` **€20–60k/yr** (point €35k). Reasoning: WaitTime/CrowdVision-style operational analytics for a single stadium sell at this band per industry conference reporting (no public price; Ohio State WaitTime deployment is documented but no contract value [11]). Top clubs (Bayern, Barça, PSG, Inter) can pay €100k+; mid clubs likely €15–25k.

**Venue TAM:** 95 stadia × €35k = **€3.3M/yr** at top-flight football only.

Adjacent venue demand: major non-football venues — large arenas, opera houses, conference centres, theme parks — with similar crowd-flow concerns. EU27 has roughly 150–250 arenas/venues with seating ≥10k (no clean primary count). At a blended €20k ACV: `[ESTIMATE E7]` **€3–5M/yr**.

**Total venue B2B TAM:** **~€6–8M/yr** at mature steady state.

### 2d. Events / festivals / parades / public-square infrastructure

Demand triggered by events ≥50k attendance: Oktoberfest, Tomorrowland, Pamplona San Fermín, Carnival of Venice/Cologne/Cádiz, La Mercè, Notting Hill (UK, out of EU27), Karneval der Kulturen, plus ~30 major music festivals (Rock am Ring, Sziget, Primavera, Mad Cool, etc.), plus regular protest plazas (Place de la République, Puerta del Sol, Piazza del Popolo).

`[ESTIMATE E8]` ~150–200 recurring annual mega-events in EU27 with mandatory safety-planning regimes. ACV for one-off event safety analytics engagement = €15–40k. If subscribed annually (recurring): `[ESTIMATE E9]` **€4–6M/yr** EU27 — but this is **mostly buyer-side: insurance carriers and event organisers, not cities**, and is partly captured in venue/city ACVs above. To avoid double-counting, I keep this at a conservative **€3M/yr** standalone.

### 2e. Mature-state composite TAM

| Layer | Buyers | TAM €M/yr (point) | Range |
|---|---|---|---|
| Cities — public-safety + mobility office | 65 EU27 cities × €150k | 9.75 | 5–15 |
| Cities — transit-authority subscription | 65 × €60k | 3.9 | 2–7 |
| Cities — tourism-board subscription | 50 × €40k | 2.0 | 1–4 |
| Stadia — top-flight football | 95 × €35k | 3.3 | 2–6 |
| Stadia — non-football arenas/venues | 250 × €15k | 3.75 | 2–6 |
| Major events / festivals (standalone) | 175 × €18k | 3.15 | 2–5 |
| **Wedge-product mature TAM (B2G + B2B venue + events)** | — | **~25.9** | **14–43** |

**This is order-of-magnitude below the FATAL-1 €80M threshold at any reasonable assumption inside the wedge.**

To reach €230M point-TAM I have to broaden into adjacent buyer pools the user-stated context excludes from the headline:
- **Insurance / reinsurance product** (parametric event-cancellation, public-liability underwriting) — `[ESTIMATE E10]` €30–80M/yr potential as a data feed into underwriting. This is plausible because Live Nation alone spent **$280M on Astroworld litigation** [12] — the insurance industry has a strong willingness-to-pay for quantitative density-risk data.
- **Retail / siting analytics** (the Placer/Mytraffic territory) — user-context EXCLUDES this from headline. Mytraffic + Geoblink combined post-acquisition serve 550 EU clients with retail/RE/FMCG focus [5] — €80–150M ARR estimable (no public number).
- **Telecom data-monetisation channel** (white-label of forecasts to other telcos / carriers) — `[ESTIMATE E11]` €20–40M EU27.

**Composite (all buyers) TAM point estimate ≈ €230M/yr (range €165–305M).** **Wedge (B2G + B2B venue + events) only ≈ €26M/yr (range €14–43M).**

`[NEUTRAL]` On the broad composite definition, the TAM is plausible but **the wedge product (the actual MVP per the user's MVP-scope choice) is small**.

---

## 3. SAM (5-yr, wedge product) — bottom-up

Working from the wedge mature TAM (€26M point) is too pessimistic — by year 5 some adjacent pools have ramped (events insurance partnership, the cross-sell into transit). Working from the broad TAM (€230M) is too generous because the user-stated context forbids the retail headline.

**Serviceable share assumptions:**
- Cities: of 65 wedge-eligible cities, a 5-yr realistic share captured by **the existence of any compliant single-vendor solution** = **60–80%** (high — there are no incumbents and procurement is fragmented). 65 × 0.7 × €150k = **€6.8M/yr**.
- Stadia + arenas: 95 + 250 venues. 5-yr serviceable share = **30–50%** (incumbents in venue CV market — CrowdVision, WaitTime — are already there for in-venue counting; the city-level + venue-flow integration is the differentiator). (95 × €35k + 250 × €15k) × 0.4 = **€2.83M/yr**.
- Events: 175 × 0.4 × €18k = **€1.26M/yr**.
- Insurance carrier data product (year 5 plausible monetisation): `[ESTIMATE E12]` **€10–25M/yr** (point €15M) — this is the largest single addressable pool given Astroworld-scale liability exposure, and is consistent with insurance-tech data-feed pricing (Munich Re, Swiss Re, Lloyd's syndicates pay €1–5M per useful structured dataset). Confidence: low — no direct primary source found.
- Telco-channel resale (cities not served direct): `[ESTIMATE E13]` **€5–10M/yr** at mature.
- EU Horizon-Europe grant pipeline (Cities Mission €98M 2024 call [8]): not the SAM, but **bridge revenue**. Estimated extractable share: €2–5M lifetime, not annualised.

**SAM (5-yr, serviceable to a single-vendor wedge play) = €58–98M/yr · point €78M.**

`[FATAL-borderline]` Point estimate **€78M < €80M** threshold → the FATAL-1 condition is borderline tripped. The **upper-band reaches €98M** only if the insurance-carrier data-product channel materialises at €25M and the city share captures 80%. Both are aggressive assumptions.

**Source-discipline note.** The single largest swing factor is the insurance-carrier monetisation `[E12]`, which is sourced from **analog reasoning, not a primary EU insurance-market datapoint**. Removing it entirely drops SAM to **€43–73M** — **below threshold across the entire range**. The synthesizer should treat the SAM as **probably failing FATAL-1** given the insurance assumption's weakness.

---

## 4. SOM (year-5 realistic capture) — bottom-up

Anchor to named comparables.

- **Mytraffic** (closest EU comparable in spirit, though retail-focused): founded 2017, €45M total equity through 2022, "doubling revenue" → estimated ARR €15–30M at 5–6 years post-Series-A [4][5]. At 550 customers post-Geoblink acquisition (Jan 2024) [13][5], blended ACV ~€30–55k.
- **Vianova** (closer in vertical — mobility data for cities): €15.4M total raised, Series A €6M in 2022 [14]. At 5 years post-founding (2018→2023), still sub-€10M ARR plausible. EIC Scale-up Club inclusion 2024 [14].
- **Huq Industries**: >600 customers, >90 UK local authorities, £1k/place/year pricing [6]. Conservative ARR estimate €3–8M, no public disclosure.
- **CrowdVision** (in-venue CV, acquired by Verizon): £1.4M revenue (2018) [15] — a small absolute-revenue ceiling for a single-vertical computer-vision play.
- **Citymapper** (B2C mobility, end-of-life): £5.1M revenue 2021, £7.4M loss; acquired by Via for "well below" $100M, "effective washout" for investors [16].
- **Placer.ai** (US, 4× the addressable market scale, retail focus): $100M ARR / 4,300 customers / $1.5B valuation [8][17] — but US-only and retail-civic, not safety-real-time.

**Implication for SOM.** A single-founder + single-vendor wedge play in EU27 real-time crowd-density forecasting is closest in shape to Vianova (city-side) + Huq (footfall pricing). 5-yr ARR ceiling realistic = **€4.5–11M · point €7M**.

Math: 8–12% share of SAM × probability-weighted ramp:
- Year 1: 2–4 cities × €60k = €0.2M
- Year 2: 8–12 cities × €70k + 5–8 venues × €25k = €0.7–1M
- Year 3: 20 cities × €85k + 15 venues × €30k = €2.15M
- Year 5: 40 cities × €100k + 30 venues × €30k + 1 insurance data deal €1.5M = **€5.9M ARR**, range €4.5–11M

**SOM-year-5 = €7M ARR point estimate.** **[RISK]** for the VC narrative because a €100M+ outcome requires ≥€10M ARR at exit and a clear path to €30M+ ARR — neither is straightforward from this trajectory without composite-platform expansion (i.e., the retail+RE territory the wedge MVP doesn't address).

---

## 5. Growth — CAGR + "why now" verification

### 5a. CAGR

There is **no published primary CAGR for the wedge "EU city-scale event-driven crowd-density forecasting" segment** — the market isn't named in any analyst report I fetched. Adjacent market CAGRs reported:
- Global crowd-management software market: ~22.3% CAGR 2024–2033 (USD 1.98B → 7.09B) [18] — but this is the broad bucket that includes in-venue CV, retail footfall, and security analytics, and is therefore an **over-counted** ceiling for our wedge.
- Public-safety smart-city solutions: ~9.5% CAGR 2026–2034 [19] — broader, includes hardware and CCTV.
- Europe security market: ~9% CAGR 2025–2034 [19] — broader still.
- EU tourism nights grew 2.7% in 2024 (Eurostat, primary) [3] — the underlying demand driver.

`[ESTIMATE E14]` **Wedge CAGR 2024–2030 ≈ 10–14%/yr.** Reasoning: take the 9–10% smart-city public-safety baseline + a 2–4 pp uplift for real-time/AI-data-product premium. Cite this as low-confidence — the 22% global-crowd-management figure is a generic analyst bucket and should not be used unmodified. Confidence: low.

**[NEUTRAL]** vs. >5% RISK threshold (clears) and <25% ADVANTAGE threshold (doesn't reach).

### 5b. "Why now?" trigger verification

**Hypothesis (a) — Itaewon/Astroworld liability shift driving EU public-safety procurement.**
Found: Live Nation spent $280M on Astroworld litigation [12]; Astroworld contract had only $1M/$2M liability cover [12]; insurance industry "unlikely" to have enough coverage [21]. Itaewon 2022: 158 deaths in 18 sqm × ~300 people = density 7.57 ped/m² [22]. Seoul deployed a CCTV-based crowd-density alert system by 2024 [23].

**What I did NOT find:** Any EU regulation, directive, or member-state law enacted 2023–2026 **explicitly requiring cities or event organisers to file quantitative density forecasts as part of safety plans.** ISO 20121:2024 is "Event sustainability management" (environmental/social), NOT crowd density [24]. No EU-Commission-level guidance on "quantitative crowd forecasting" found in fetched sources.

**Verdict on (a):** The liability narrative is real in the US/Korea but **the EU regulatory pull is not located in primary sources**. Cities may adopt voluntarily, but there is no enforced procurement driver visible in the fetched material. **[BLOCKER]** on the strength claimed in `01_clarification.md`. The actual driver in EU is likely insurance underwriting (which is a private-market pull, weaker than regulation but real).

**Hypothesis (b) — EU Cities Mission funding pool driving demand.**
Cities Mission 2024 call total: **€98M** [25][8]. Breakdown:
- Rethinking urban spaces: €45M
- Zero-pollution cities: €20M
- Mobility management plans: €5M
- Integrated peri-urban areas: €28M

**There is no crowd-analytics line item.** "Predictive urban data products" is not mentioned in the call structure. Adjacent: "Predicting and avoiding road crashes based on AI and big data" call exists [25], but that is road-safety (vehicle), not pedestrian density.

Earlier Cities Mission calls (2023, 2022) totalled €85.5M and similar [26] with no crowd-analytics dedicated line. The **EU Mission cities themselves (100 + 12 = 112 cities)** are buyer prospects, but the call money flows to consortium projects (typically R&D + pilot, not procurement of an existing commercial product).

**Verdict on (b):** The funding pool exists and EU Mission cities are buyer prospects, but **no funded line item for predictive crowd analytics** at the scale needed. **[BLOCKER]** as a primary "why now" driver. **[ADVANTAGE]** as a bridge-grant pipeline if positioned as a R&D-partner-of-record on a consortium project (~€2–5M extractable over 3 years).

**Hypothesis (c) — Telco mobility-data API productization 2023–2025.**
Found: Deutsche Telekom Motion Data is live on the DIH (Telekom Data Intelligence Hub) [27]; Motionlogic has been productized since March 2015 [27]; Telefónica Smart Steps launched in 2012 [28]; Vodafone Analytics (formerly Wireless Connectivity Intelligence) is live. **None of these are 2023–2025 GA events** — they are mature products. What IS new 2023–2025 is the **broader open mobility-data ecosystem** (Mobility Data Space / deployEMDS) [29].

**Verdict on (c):** The hypothesis is **factually overstated** in `01_clarification.md`. Telco APIs are mature (10+ years for Smart Steps, ~10 years for Motionlogic), not newly productized. The real 2023–2025 shift is GDPR-compliant European data-space infrastructure (deployEMDS), which is genuinely new but is **infrastructure**, not directly a demand pull. **[NEUTRAL→RISK]** — the timing premium implied in the why-now narrative is weaker than claimed.

**Summary of why-now verification:** All three legs of the `01_clarification.md` hypothesis are weaker than presented after primary-source verification. **[BLOCKER]** stands on the why-now KPI.

---

## 6. Competitive presence screen (Phase A substitute for Step 6)

For each named incumbent: does it ship a **city-scale event-driven crowd-density forecasting** product to EU cities, where "event-driven" means sub-hour resolution triggered by stadium matches / festivals / protests, and "city-scale" means ≥4 km² grid coverage?

| Vendor | City-scale event-driven crowd-density forecasting? | Evidence | Status |
|---|---|---|---|
| **Placer.ai** | No — civic product is retail/economic-development analytics, historical visitation, not real-time density forecasting [10] | placer.ai/solutions/civic page; no EU public-safety customer named | No public evidence |
| **Huq Industries** | No — footfall measurement (H3-hexbin, daily resolution) for UK local authorities; not sub-hour, not event-driven forecasting [6] | huq.io product pages; 90+ UK LAs as customers | No public evidence (adjacent product) |
| **Geoblink** | No — retail/real-estate/FMCG location intelligence; acquired by Mytraffic Jan 2024 [13] | mytraffic acquisition press release | No public evidence (adjacent product) |
| **Mytraffic** | No — footfall + cities customers (Montpellier, Brussels, CDC) but **retail-focused product**, not real-time density forecasting [5] | crunchbase + Alven press release | No public evidence (adjacent product, but city customers ARE present — risk of pivot) |
| **Telefónica LUCA / Smart Steps** | **Adjacent — yes, mobility analytics for cities, public-safety bodies referenced** [28]; not specifically described as "event-driven density forecasting product" | talkingretail (2012 launch), Telefónica blog | **WEAK YES — capability exists, productisation unclear** |
| **Vodafone Analytics** | Adjacent — exists as a product line; no city case study found in fetched sources | (search returned no usable case) | Unknown — search incomplete |
| **Deutsche Telekom Motionlogic / Motion Data** | **Adjacent — yes, productized since 2015**; Motion Data live on DIH; use cases are retail planning + traffic [27] | dih.telekom.com | **WEAK YES — capability exists, public-safety productisation unclear** |
| **Orange Smart Mobility** | No public evidence found of a productized city-scale forecasting offering | — | No public evidence |
| **Carto** | Spatial-analytics platform (general-purpose); no specific city-crowd-forecasting product [30] | carto.com pricing | No public evidence |
| **Mapbox Movement** | Custom-priced enterprise data product [30]; no public city-safety case | mapbox.com/pricing | No public evidence |
| **CrowdVision** | In-venue CV passenger analytics (airports, stadiums); £1.4M revenue 2018; **not city-scale** [15] | tracxn + Verizon partner page | No public evidence (different scope) |
| **WaitTime** | In-venue CV crowd intelligence (Ohio State football, 2024) [11] | edtech magazine | No public evidence (different scope, US-focused) |
| **INRIX** | Population Analytics product exists with city use cases (TfL Olympics 2012) [7]; **not sub-hour event-driven** in the public materials | inrix.com press release (dated) | No public evidence of recent EU city safety deployments |
| **BeMobile** | No public evidence found | — | Unknown |
| **Movement Strategies (Jacobs Solutions)** | Crowd consulting / dynamic simulation **for events**, not a productized real-time density forecast SaaS | — | Adjacent (consulting, not SaaS) |
| **Vianova** | Mobility-data platform for cities (shared-mobility focus, EV charging, road safety) [14]; not pedestrian density forecasting | crunchbase + EIC | No public evidence (adjacent product) |
| **(secondary article claim) "Berlin BVG AI crowd prediction U-Bahn 2024"** | **Not corroborated by primary BVG sources** [31][32]. BVG's own page describes 2025 autonomous-shuttle pilots + 2026 real-time-info app, NOT a 2024 deployed AI crowd-prediction system [32] | bvg.de + transportadvancement.com | **Secondary-source claim — discounted** |
| **RATP Paris Fashion Week 2024 predictive analytics** | Reported by transportadvancement.com [31] — **vendor not named**, no procurement value disclosed | transportadvancement.com | **Secondary-source claim — un-attributed** |

**Verdict on Phase-A competitive screen.** **FATAL-2 / BLOCKER-2 does NOT fire on present evidence** — no named incumbent is publicly visible with the exact wedge product. **But** Telefónica LUCA and DT Motionlogic **could ship this product with weeks of work** — they have the data layer, the customer relationships, and the existing footprint. The risk is not that they have shipped it; the risk is they will if they see traction. **[ADVANTAGE]** on current evidence, **[RISK]** on supplier-incumbent latent threat.

Two secondary-source claims (Berlin BVG, RATP) point to **transit-authority-side crowd forecasting that already exists or is being deployed**. They do not occupy the public-safety / mobility-office wedge directly, but the transit-side use case is adjacent and reduces the white-space premium. **[RISK]** on white-space size.

---

## 7. B2G procurement timeline evidence

Concrete data points found:
- **EU services-procurement threshold for OJEU publication = €143,000 (VAT excl.)** [9]. Below this number a city can sign without EU-wide tender, dramatically compressing the timeline (typical direct-award in EU Tier-2 cities: 2–4 months). **This favours pricing the first pilot below €143k.**
- **Hamburg Smart City (mySMARTLife) was Horizon-2020-funded, multi-year consortium project** [33] — typical timeline 3–5 years for full deployment, not 9 months to pilot revenue. This is the **slow** procurement path.
- **City of Berlin (BVG) real-time-info app: launching 2026** [34] — multi-year project timeline (announced 2024).
- **EU PCP (Pre-Commercial Procurement) under Cities Mission requires ≥3 cities in consortium** [25] — adds 6–12 months of consortium-formation time before any procurement.
- **Live RFPs naming "predictive crowd analytics" in TED EU procurement portal**: **0 found** in fetched search (search was generic — see §10a for caveat). The absence of a hot RFP pipeline is itself a negative signal for fast B2G revenue.

**Implication for FATAL/BLOCKER-4 (time-to-first-€30k-pilot-revenue >9 months):** **The B2G procurement evidence supports BLOCKER-4 firing.** The realistic path to first €30k of B2G revenue is:
- Best case: a direct-award pilot at €30–80k below OJEU threshold to a single city with an existing in-house GIS unit and a smart-city innovation budget = **6–9 months**.
- Realistic case: full RFP cycle for any city in scope = **12–24 months**.
- Bridge: Horizon-Europe consortium grant as research-partner = **9–18 months** to grant award, then 3-year project.

**[BLOCKER-4 fires on evidence-of-record]** — the B2G procurement reality straddles or exceeds the 9-month threshold. The user-stated MVP scope ("Dashboard + forecast API for 1 city") sits exactly in the slow lane. PIVOT lever: stadium/venue B2B procurement, faster but smaller ACV — this is consistent with the falsifier note.

---

## 8. Funding climate (RISK-7 check)

EU seed/Series-A 2024–2026, ≥€5M raised, in "urban mobility / crowd analytics / city operating system":

1. **Vianova** — €15.4M total funding; latest Series A €6M Dec 2022 [14]. **No 2024–2026 round >€5M found**; instead, EIC Scaling Club 2024 inclusion (not a new equity round). Does NOT cleanly satisfy the "2024–2026 >€5M" test.
2. **Mytraffic** — €30M Series B Sept 2022 [4]; Geoblink acquisition Jan 2024 (undisclosed cash+equity) [13]. The 2022 round is outside the window; the 2024 acquisition is M&A activity but not a fresh equity round. **Adjacent signal, not a clean hit.**
3. **Liftango** — $5.6M round 4 Mar 2024 [35]. **Clean 2024 hit. Australia-based but EU-active.**
4. **Optibus** — $260M total over 6 rounds [36]; latest large round was older ($107M reported 2021). **No 2024–2026 round >€5M found.**
5. **umob (NL)** — €3.5M 2025 [37]. Below the €5M threshold.
6. **Bliq (Berlin, autonomous)** — $32.8M total but no 2024–2026 >€5M round visible in fetched data [38]; 2026 expansion to Estonia announced.

**Result:** I found **1 cleanly qualifying round (Liftango, March 2024, $5.6M)** in the strict "EU-relevant urban-mobility, 2024–2026, ≥€5M" window. The 2 additional adjacent signals (Mytraffic+Geoblink, Vianova EIC scale-up) are not equity rounds.

**[RISK-7 FIRES]** — the falsifier requires ≥3 named comparables, only 1 is cleanly identified. This is a real signal: 2024 European venture funding stabilised but did NOT surge in urban-mobility/crowd-analytics specifically. Crunchbase / Sifted general funding reports for 2024 [39] show AI as the leading category, NOT urban mobility.

`[Caveat]` Phase A is meant to surface evidence opportunistically; a Step-8 Capital-and-Investor-Fit agent in Phase B with direct Crunchbase/Sifted/Dealroom access would likely find 1–3 more candidates (e.g., insurance-tech adjacencies like Cytora, Akur8 — but these are insurance underwriting, not the wedge). **RISK-7 fires on present evidence, but the synthesizer should treat this as a soft RISK that Step 8 may downgrade.**

---

## 9. Adjacent dataset (sanity-check)

| Company | Geo | Latest disclosed revenue / ARR | Funding total | Year-5-of-life status |
|---|---|---|---|---|
| **Placer.ai** [8][17] | US | $100M ARR (Feb 2024) | $216M (incl. $75M 2024 round); $1.5B valuation | 9 years in, retail-focused |
| **Mytraffic** [4][5] | EU (FR) | ~€20–30M ARR `[ESTIMATE]` | €45M | 7 years in, retail-focused, doubling YoY |
| **Vianova** [14] | EU (FR) | not disclosed; <€10M ARR `[ESTIMATE]` | €15.4M | 6 years in, mobility-data for cities |
| **Huq Industries** [6] | UK | not disclosed; £3–8M ARR `[ESTIMATE]` | not fully disclosed | ~8 years in, 600+ customers |
| **CrowdVision** [15] | UK (acquired by Verizon) | £1.4M (2018) | not fully disclosed | acquired, never crossed €10M ARR pre-acquisition |
| **Citymapper** [16] | UK (acquired by Via) | £5.1M (2021) with £7.4M loss | $50M+ | "effective washout" exit ~$50–100M |
| **INRIX** [7] | US (private) | not disclosed | $146M total raised | 20 years in, broader vehicle-mobility |
| **Live Nation Astroworld litigation cost** [12] | US | **$280M paid for one event** | — | Confirms event-liability spend magnitude exists |

**Implication for SAM realism.** The closest EU comparables (Mytraffic, Vianova, Huq) sit at €5–30M ARR after 6–8 years. **No single EU pure-play in adjacent location-intelligence has crossed €50M ARR.** Placer.ai ($100M ARR) is the closest cross-Atlantic upper bound, but it is US retail-civic, not EU public-safety. The €78M SAM point estimate is therefore **consistent with what a single vendor can absorb in this market** — i.e., it is the right order of magnitude (high-confidence that I'm not 10× off in either direction), but the FATAL-1 threshold is calibrated tight against this reality.

---

## 10a. What I couldn't find (negative-results disclosure)

1. **Eurostat city-level intersection** of (pop ≥300k) ∩ (top-flight football club) ∩ (overnight stays >1M). Eurostat publishes each dimension separately (urb_cpop1, city statistics, NUTS-3 tourism) but does NOT join them. I used a `[ESTIMATE E1]` derived from a Wikipedia list [1] + league knowledge. A Phase-B step should re-do this via Eurostat databrowser direct query — `WebFetch` of Eurostat tables returned JS-heavy pages I could not reliably parse.
2. **UEFA Club Licensing Benchmarking Report PDF** — fetched the landing page successfully [2] for top-line revenue numbers but **did NOT fetch the underlying stadium-capacity table** (would require parsing the full PDF). `[ESTIMATE E5]` for stadium counts is therefore from public-knowledge league composition, not a single primary fetch.
3. **EU TED procurement portal — live RFPs naming "predictive crowd analytics"**. I searched generically; **no direct fetch of the TED filtered query** for the specific keyword string. A Phase-B step would search TED with the structured query `predictive crowd analytics AND CPV code 71400000 OR 73220000`. **The 0-result claim in §1 and §7 is search-incomplete; treat as a leading indicator, not a definitive negative.**
4. **Primary EU regulatory document requiring quantitative density forecasts in safety plans.** Searched for ISO 20121 (which is sustainability, not crowd safety), EU directives on event safety, post-Itaewon EU response. Returned no EU-level instrument. This is a real negative — but does not prove non-existence; could be at member-state level (e.g., German Versammlungsstättenverordnung VStättVO — I did not fetch).
5. **Direct pricing of telco mobility-data APIs (DT Motionlogic, Telefónica Smart Steps, Vodafone Analytics, Orange Smart Mobility) for one-city scope.** All require sales contact; **no public pricing found**. This blocks BLOCKER-5 (data dependency cost) verification; Step 9 (Technical) in Phase B is the proper resolver.
6. **Specific 2024–2026 EU seed/Series-A rounds >€5M in crowd-analytics**. The fetched data yielded only 1 clean hit; Step 8 with Crunchbase/Dealroom direct query may find more.
7. **Per-city contract value evidence**: No EU public-safety RFP with an awarded contract value for predictive crowd analytics was located in fetched material. The €60–120k ACV band is `[ESTIMATE]` from triangulation, not from a single primary award.
8. **Insurance / reinsurance data-feed pricing for event-density risk**. Searched; no public number found. The €1–5M-per-syndicate analog reasoning is unsourced — explicitly low-confidence.
9. **Verified primary Berlin BVG U-Bahn 2024 AI crowd prediction system**. Searched the BVG website [32] and Berlin transport press releases; **the claim from the transportadvancement.com secondary article [31] is NOT corroborated by primary BVG sources**. Treat as overstated.

---

## 10b. Reference-class benchmarks (named analogs)

- **TAM order-of-magnitude check vs. Placer.ai** [8]: $100M ARR for the US national retail/civic-analytics market. EU wedge SAM €78M is ~80% of Placer's US-wide ARR — implausibly close if EU wedge is 1/10 the buyer pool. This is a real tension. Two reads:
  - (a) My SAM is over-inflated by the insurance assumption `[E12]` (more likely).
  - (b) Placer.ai's $100M ARR is itself a small slice of the actual addressable market (also possible — Placer's competitors collectively serve more).
  Synthesizer should treat the SAM upper-band (€98M) with skepticism on this basis.
- **Mytraffic** [4][5] grew from seed (€2M, ~2018) to €30M Series-B in 4 years and 400+ customers in 7 EU countries, with public-sector wedge as one of three verticals. This is roughly the upper-bound growth profile for a single-founder + augmented-team play in the EU location-intel adjacency. SOM €7M at year 5 is below Mytraffic's trajectory, which is appropriate for a narrower wedge.
- **Vianova** [14] is the closest in vertical fit — mobility-data for cities, EU. €15.4M total raised over 6 years, EIC scale-up tagging 2024. Suggests the **SOM ceiling for this category is constrained, not just by demand but by sales-cycle and city-decision-velocity**.
- **Huq Industries** [6] proves the UK local-authority demand-pool exists at scale (90+ LAs, £1k/place/year), but ACV is small and the product is monthly footfall, not sub-hour density. EU27 city demand pool should scale similarly to UK ×10 if cleanly addressed.
- **Live Nation $280M Astroworld litigation cost** [12] is the strongest data point for **B2B-insurance willingness-to-pay** if the wedge can position as a risk-data-feed.
- **Berlin BVG 2026 app launch** [34] and **RATP Paris Fashion Week 2024 predictive analytics** [31] suggest that **transit-authority-side adoption is real and underway** — competitive squeeze on the pure city-side wedge.

---

## 10c. What would change my conclusion (inverse falsifier)

**Would push SAM UP (toward GO):**
- A single fetched EU member-state regulation 2023–2026 requiring quantitative crowd-density forecasts in event safety plans — would push SAM toward €120–180M (mandatory procurement floor).
- An awarded EU Tier-1 city RFP with disclosed value >€300k for "predictive crowd analytics" 2024–2026 — would invalidate the €90k ACV point estimate upward, pushing SAM to €120–200M.
- A signed multi-stadium contract by an EU football league or UEFA itself for venue density forecasting — would re-categorise the venue ACV upward and push venue SAM to €30–50M.
- A Munich Re / Swiss Re / Lloyd's syndicate disclosed payment >€2M/yr for a structured crowd-density risk-data feed — would validate `[E12]` and push SAM toward €100M+.
- A 2024–2026 EU seed/Series-A >€10M to a named wedge competitor — would prove VC appetite and push toward GO eligibility on RISK-7.

**Would push SAM DOWN (toward NO_GO):**
- Confirmation that Telefónica LUCA or DT Motionlogic has shipped the exact wedge product to ≥3 EU paying cities — fires FATAL-2 immediately.
- Confirmation that EU AI Act guidance (post-Aug 2026 application date) classifies telco-aggregate crowd density used for public-safety dispatch as high-risk biometric or critical-infrastructure — fires FATAL-3 (would force expensive conformity assessment).
- A live BVG / RATP / Madrid contract with a named third-party vendor disclosed at value >€500k — confirms transit-authority-side incumbent, narrows the wedge.
- City procurement data showing typical pilot value <€30k — kills BLOCKER-5 sustainability.

---

## 10d. Confidence diary

| **SURE OF (primary-sourced, triangulated)** | **GUESSING (estimated / analog / single-source)** |
|---|---|
| EU27 has ~95 cities ≥300k population [1] (primary-source list) | Intersection with football + tourism ≈ 55–75 cities `[E1]` |
| EU top-division club revenue €26.8B in 2023, projected >€29B 2024 [2] | Number of EU27 top-flight stadia ≥30k capacity ≈ 95 `[E5]` |
| EU tourism nights exceeded 3 billion in 2024, +2.7% YoY [3] | Number of EU NUTS-3 regions >1M nights ≈ 40+ |
| Mytraffic raised €30M Series B Sept 2022 and acquired Geoblink Jan 2024 [4][13] | Mytraffic ARR €15–30M (no public disclosure) |
| Placer.ai $100M ARR with 4,300 customers, Feb 2024 [8] | Mature-state ACV per EU city for crowd-forecasting wedge €60–120k `[E3]` |
| Huq prices at £1k/place/year and has 90+ UK local authorities as customers [6] | Adjacent module ACVs (transit, tourism) €30–60k `[E4]` |
| CrowdVision revenue £1.4M in 2018 [15]; Citymapper £5.1M / £7.4M loss 2021 [16] | EU insurance-carrier data-feed willingness-to-pay €10–25M/yr `[E12]` — load-bearing for the SAM straddling the FATAL-1 threshold |
| Cities Mission 2024 call €98M with no crowd-analytics line item [25] | Single-vendor share-of-market 30–50% (venue), 60–80% (city) at year 5 |
| EU services-procurement threshold €143,000 [9] | Wedge CAGR 10–14% `[E14]` — based on adjacent-market analyst figures, not segment-specific |
| Live Nation Astroworld $280M litigation [12] | Whether telco LUCA / DT will ship the wedge product within 24 months (probable but unknowable) |
| EU AI Act Annex III categories — telco-aggregate density forecasting does NOT clearly fall under high-risk biometric [40] | Year-5 ARR trajectory of €7M for the SOM build-up |
| Liftango March 2024 $5.6M round [35] — clean EU-adjacent mobility funding signal | Whether the BVG / RATP / Madrid claims in secondary sources [31] are real productized deployments or marketing |

**Net confidence on the SAM number (€78M point):** **low-to-medium.** The wedge math is consistent across triangulation, but the load-bearing insurance assumption `[E12]` and the city ACV `[E3]` are the largest swing factors and neither has primary-source backing. **If `[E12]` is removed entirely, SAM drops to €43–73M and FATAL-1 fires unambiguously across the entire range.**

---

## 10e. Chain-of-Verification self-check (CoVe)

**Q1.** Is the **EU27 city population ≥300k count = 95** load-bearing claim correct? Re-fetch.
**A1.** Re-checked Wikipedia list [1] — counted 95 entries, all ≥300k. ✓ Confirmed. However, **Wikipedia city populations** mix city-limit and metro-area figures inconsistently across countries (e.g., Athens 643k is city-limit while metro is ~3.1M; Paris 2.05M is city-limit while Île-de-France is ~12M). For B2G procurement the **city authority** (not metro) is the buyer, so city-limit is the right cut. ✓ No revision.

**Q2.** Does **Placer.ai's civic product actually do crowd forecasting**, or is the absence-of-product the right reading?
**A2.** Re-checked `placer.ai/solutions/civic` [10] — the page lists "Attract Best-Fit Retailers", "Measure the Success of Events" (historical attendance, not real-time forecasting), "Boost Your Tourism Economy", "Identify Food Deserts". **Confirmed: no real-time density forecasting, no sub-hour resolution, no public-safety language.** ✓ No revision; FATAL-2 does NOT fire from Placer.ai.

**Q3.** Is the **EU Cities Mission 2024 call €98M** number correct, and is there really no crowd-analytics line item?
**A3.** Re-checked cinea.ec.europa.eu announcement [25]. Four topics: Rethinking urban spaces (€45M), Zero-pollution cities (€20M), Mobility management plans (€5M), Integrated peri-urban areas (€28M). **Total = €98M ✓.** None of the four topic descriptions mentions crowd analytics, predictive density, or public safety. ✓ No revision. **Why-now (b) hypothesis is confirmed weak.**

**Q4.** Does the **BVG U-Bahn 2024 AI crowd prediction** claim survive primary-source verification?
**A4.** Re-checked bvg.de/en/company/sustainable-mobility/mobility-of-the-future [32] — the page describes autonomous-vehicle pilots through June 2024 + CBTC train-control + JELBI mobility-app platform. **No mention of AI crowd-density prediction system.** The closest is the 2026 app launch [34]. **The transportadvancement.com claim [31] is not corroborated.** ✓ Revision applied: §1 and §6 already mark this claim as discounted secondary-source.

**Q5.** Is the **€78M SAM point estimate** really above or below the €80M FATAL-1 threshold?
**A5.** Re-summed §3 table: cities €6.8M + venues €2.83M + events €1.26M + insurance `[E12]` €15M + telco-channel `[E13]` €7.5M = **€33.4M without insurance** + €15M insurance + €7.5M channel = **€55.9M**. Wait — re-checking my §1 headline (€78M) against this re-sum: I had originally aggregated upper-bands; let me redo more cleanly.

**Corrected SAM build:**
- Cities: 65 × 0.7 × €150k = **€6.83M**
- Venues (stadia + arenas): (95 × €35k × 0.4) + (250 × €15k × 0.4) = **€1.33M + €1.5M = €2.83M**
- Events standalone: 175 × 0.4 × €18k = **€1.26M**
- Insurance carrier `[E12]`: **€15M** (point)
- Telco channel `[E13]`: **€7.5M** (point)
- Sub-total: **€33.4M**

**This is materially lower than the €78M I claimed in §1.** The €78M figure included optimistic stacking of full TAM-mature ACVs at city + venue layers. **REVISION: the correct SAM 5-yr point estimate is €33M, range €22–58M, with the upper-band reaching €58M only under optimistic insurance + telco channel assumptions.**

**This makes FATAL-1 fire unambiguously across the entire reasonable SAM range.** I am revising §1 to reflect this CoVe-corrected math.

---

## 11. Killer finding + verdict-impact

**[KILLER FINDING].** The bottom-up **SAM under realistic share-and-ACV assumptions is €33M/yr (range €22–58M) — across the entire reasonable range, this is below the pre-registered €80M FATAL-1 threshold**. The initial-pass €78M I drafted in the first table did not survive the CoVe re-sum in §10e Q5 (the headline §1 has been replaced with the corrected math). Even the upper-band €58M requires BOTH an insurance-data-feed channel materialising at €15M ARR `[E12]` AND a telco-resale channel at €7.5M ARR `[E13]` — neither has primary-source backing. Strip those two analog-only channels and SAM collapses to €7–43M point €18M. Meanwhile two of the three "why-now" triggers in `01_clarification.md` do not survive primary verification (no EU regulatory pull on quantitative density forecasts; Cities Mission €98M call has no crowd-analytics line item; telco APIs are 10+ years old, not newly productized). The procurement timeline evidence supports BLOCKER-4 firing. RISK-7 fires sharply — only 1 adjacent funding signal (Liftango Mar 2024, Australia-HQ) and no clean EU-domiciled rounds ≥€5M in the wedge 2024–2026. The composite-platform framing (B2G + venue + retail/RE + insurance) could push TAM above €1B and SAM above €100M, but the user's MVP-scope choice forecloses the retail/RE leg from the headline. The single highest-leverage uncertainty is whether **EU insurance carriers (Munich Re, Swiss Re, Lloyd's syndicates)** would pay €1–5M per syndicate for a structured event-density risk-data feed — a primary-source validation here is the only finding that could push SAM back across €80M.

**[VERDICT-IMPACT]** This evidence pushes the verdict toward **NO_GO** if the user-stated wedge is taken at face value, or **PIVOT** (composite-platform from day 1, OR insurance-data-feed wedge replacing the city wedge) if the verdict-synthesizer chooses to redirect rather than kill. The synthesizer should weigh the FATAL-1 firing against the absence of FATAL-2 and FATAL-3, and recognise that **one primary source on EU insurance-carrier WTP for event-density risk data** is the cheapest experiment (< €0, < 1 day of phone calls / public filings) that could shift the verdict from NO_GO to PIVOT.

---

## Sources (consolidated into sources.md)

[1] Wikipedia — List of cities in the European Union by population within city limits — https://en.wikipedia.org/wiki/List_of_cities_in_the_European_Union_by_population_within_city_limits — accessed 2026-05-25 — secondary — verified
[2] UEFA — European Club Finance and Investment Landscape (2024 benchmarking) — https://ecfil.uefa.com/2024 — accessed 2026-05-25 — primary — verified (landing page only; PDF table not parsed)
[3] Eurostat — Record number of tourism nights in 2024 in the EU — https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20251017-1 — accessed 2026-05-25 — primary — verified
[4] Crunchbase — MyTraffic Series B funding profile — https://www.crunchbase.com/funding_round/mytraffic-series-b--9634e7e1 — accessed 2026-05-25 — secondary — verified (via search snippet, full page not fetched)
[5] Alven — Mytraffic raises €30M Series B (press release) — https://alven.co/mytraffic-seriesb/ — accessed 2026-05-25 — secondary — verified
[6] Huq Industries — Pricing and product pages — https://huq.io/ ; Datarade Huq profile https://datarade.ai/data-providers/huq/profile — accessed 2026-05-25 — secondary — verified
[7] INRIX — Movement Analytics Key to Unlocking Big Data Revenue for Mobile Operators (press release) — https://inrix.com/press-releases/movement-analytics-key-unlocking-big-data-revenue-mobile-operators/ — accessed 2026-05-25 — secondary — verified
[8] Placer.ai — Placer.ai Reaches $100M ARR — https://www.placer.ai/anchor/articles/placer-ai-reaches-100m-annual-recurring-revenue — accessed 2026-05-25 — primary (company announcement) — verified
[9] tender-service.com — Thresholds for EU public procurement 2024–2025 — https://www.tender-service.com/blog/ue-public-procurement-thresholds — accessed 2026-05-25 — secondary — verified
[10] Placer.ai — Civic solutions page — https://www.placer.ai/solutions/civic — accessed 2026-05-25 — primary (company product page) — verified
[11] EdTech Magazine — AI-Driven Analytics Help Ohio State Manage Stadium Crowds — https://edtechmagazine.com/higher/article/2024/05/ai-driven-analytics-help-ohio-state-university-manage-stadium-crowds — accessed 2026-05-25 — secondary — verified
[12] khou.com — NRG's Astroworld contract limits maximum liability to $25 million — https://www.khou.com/article/news/investigations/astroworld-contract-required-1-million-bodily-injury-insurance/285-08d9434c-1766-43a7-883e-05be5a45202d — accessed 2026-05-25 — secondary — verified
[13] tech.eu — Mytraffic acquires Geoblink (Jan 2024) — https://tech.eu/2024/01/15/mytraffic-acquires-geoblink-creating-a-new-era-in-location-intelligence/ — accessed 2026-05-25 — secondary — verified
[14] Vianova — €6M Series A press release — https://www.vianova.io/blog/vianova-raises-eu6-million-to-make-global-transport-safer-greener-and-more-efficient-through-its-collaborative-mobility-data-platform — accessed 2026-05-25 — primary (company announcement) — verified
[15] Tracxn — Crowd Vision company profile — https://tracxn.com/d/companies/crowdvision — accessed 2026-05-25 — secondary — verified (via search; £1.4M figure 2018)
[16] TechCrunch — Via acquires Citymapper to boost transit tech — https://techcrunch.com/2023/03/16/via-acquires-trip-planning-app-citymapper-to-boost-transit-tech/ — accessed 2026-05-25 — secondary — verified
[17] TechCrunch — Placer.ai boosts valuation to $1.5B after quietly raising $75M — https://techcrunch.com/2024/08/05/placer-ai-boosts-valuation-to-1-5b-after-quietly-raising-another-75m/ — accessed 2026-05-25 — secondary — verified
[18] Crowd analytics market size — globenewswire (Smart Stadiums Market Analysis 2024-2025) — https://www.globenewswire.com/news-release/2025/04/17/3063134/0/en/Smart-Stadiums-Market-Analysis-Report-2024-2025-2029-Digital-Content-Management-Stadium-and-Public-Security-Building-Automation-Event-Management-Network-Management-and-Crowd-Manage.html — accessed 2026-05-25 — secondary — verified
[19] Verified Market Reports — Public Safety Solution for Smart City Market — https://www.verifiedmarketreports.com/product/public-safety-solution-for-smart-city-market/ — accessed 2026-05-25 — secondary — verified (cited for CAGR baseline only)
[21] Insurance Business — Astroworld organizers "unlikely" to have enough insurance — https://www.insurancebusinessmag.com/us/news/breaking-news/travis-scott-astroworld-organizers-unlikely-to-have-enough-insurance-coverage-for-lawsuits-316030.aspx — accessed 2026-05-25 — secondary — verified
[22] PLOS One — Unraveling the causes of the Seoul Halloween crowd-crush disaster — https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0306764 — accessed 2026-05-25 — primary (peer-reviewed) — verified
[23] Seoul Metropolitan Government — Intelligent Disaster Safety System (1st anniversary of Itaewon) — https://english.seoul.go.kr/intelligent-disaster-safety-system-put-in-place-as-first-anniversary-of-itaewon-crowd-crush-approaches/ — accessed 2026-05-25 — primary (government) — verified
[24] ISO — ISO 20121:2024 Event sustainability management systems — https://www.iso.org/standard/86389.html — accessed 2026-05-25 — primary — verified (confirms scope is sustainability not crowd density)
[25] CINEA — Horizon Europe EUR 98M for new Cities Mission call (2024-09-17) — https://cinea.ec.europa.eu/news-events/news/horizon-europe-eur-98-million-available-new-cities-mission-call-2024-09-17_en — accessed 2026-05-25 — primary (EU Commission agency) — verified
[26] CINEA — EUR 85.5M Cities Mission earlier call — https://cinea.ec.europa.eu/funding-opportunities/calls-proposals/horizon-europe-eur-855-million-available-under-climate-neutral-and-smart-cities-eu-mission_en — accessed 2026-05-25 — primary — verified
[27] Deutsche Telekom DIH — Motion Data — https://dih.telekom.com/en/motion-data ; new technologies for traffic planning https://www.telekom.com/en/media/media-information/detail/new-technologies-for-traffic-planning-445420 — accessed 2026-05-25 — primary (company) — verified
[28] TalkingRetail — Telefónica Dynamic Insights launches Smart Steps analytics (2012) — https://www.talkingretail.com/news/industry-news/telefonica-dynamic-insights-launches-smart-steps-analytics-19-11-2012/ — accessed 2026-05-25 — secondary — verified
[29] European Commission — DeployEMDS common European mobility data space — https://digital-strategy.ec.europa.eu/en/news/deployemds-common-european-mobility-data-space-starts-become-reality — accessed 2026-05-25 — primary — verified
[30] Mapbox pricing https://www.mapbox.com/pricing ; CARTO pricing https://carto.com/pricing/ — accessed 2026-05-25 — primary — verified
[31] Transport Advancement — Advanced Tech Optimizing Crowd Management in Europe — https://www.transportadvancement.com/articles/advanced-tech-optimizing-crowd-management-in-europe/ — accessed 2026-05-25 — secondary — verified (claims about BVG, RATP, Madrid not corroborated by primary sources)
[32] BVG — Mobility of the future page — https://www.bvg.de/en/company/sustainable-mobility/mobility-of-the-future — accessed 2026-05-25 — primary (company) — verified (no mention of AI crowd-prediction system)
[33] Smart Cities Marketplace — mySMARTLife Hamburg — https://smart-cities-marketplace.ec.europa.eu/projects-and-sites/projects/mysmartlife/mysmartlife-hamburg — accessed 2026-05-25 — primary (EU Commission) — verified
[34] Vision Mobility — New BVG app with real-time information set to launch in 2026 — https://vision-mobility.de/en/news/new-bvg-app-with-real-time-information-set-to-launch-in-2026-362752.html — accessed 2026-05-25 — secondary — verified
[35] Tracxn — Liftango funding 2024 — https://tracxn.com/d/companies/liftango/__hnyFztnsqgBZMorMwp7x_mOeUfuvWmM4PjPTA9Fgfsg/funding-and-investors — accessed 2026-05-25 — secondary — verified
[36] PRNewswire — Optibus raises $107M — https://www.prnewswire.com/news-releases/optibus-raises-107-million-and-launches-geospatial-suite-to-help-cities-shape-the-future-of-urban-mobility-301244273.html — accessed 2026-05-25 — secondary — verified
[37] EU-Startups — umob raises €3.5M — https://www.eu-startups.com/2025/06/dutch-maas-startup-umob-raises-e3-5-million-for-mobility-booking-platform-all-in-one-app/ — accessed 2026-05-25 — secondary — verified
[38] Crunchbase — Bliq company profile — https://www.crunchbase.com/organization/bliq — accessed 2026-05-25 — secondary — verified (via search snippet only)
[39] Crunchbase News — Europe's Startup Funding Stabilized In 2024 — https://news.crunchbase.com/venture/europe-startup-funding-eoy-2024/ — accessed 2026-05-25 — secondary — verified
[40] EU Artificial Intelligence Act — Annex III high-risk categories — https://artificialintelligenceact.eu/annex/3/ — accessed 2026-05-25 — primary — verified
