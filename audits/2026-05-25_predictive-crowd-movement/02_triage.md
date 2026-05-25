# 02 — Triage (NOT YET IMPLEMENTED in Phase A)

This step will run a fast kill/keep gate via the `red-team-analyst` agent in quick-mode. In Phase A, this step is skipped — the wizard will proceed directly to Market.

**No `fatal_signal` set.** The verdict-synthesizer will treat this audit as having no triage gate, and will adjust confidence downward to reflect the missing layer.

The auditor flags one concern that a real triage would have raised: the seed mixes ≥2 distinct products (event-day forecasting vs steady-state retail siting). The Step 2 clarification collapsed this to a single MVP wedge (event-day, 1 city) with the composite framing retained only as the long-term VC narrative. A real triage might have killed the audit here on "scope sprawl"; instead, this is carried forward as a `[RISK]` for Step 12 to weigh.
