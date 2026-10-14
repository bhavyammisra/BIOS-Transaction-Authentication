# Scope & hackathon logistics

## Logistics (fill in from the official rules)
| Item | Value |
|---|---|
| Hackathon | BIOS, Thapar Institute |
| Screening/submission deadline | 2026-10-15, night (deck + video) |
| Final round dates | _TBD_ |
| Submission format | Screening: 5-slide deck in the official `BIOS_V2_CORE_FRONTIER_Screening_Template.pptx` (kept locally, not in git) + a video |
| Judging criteria | Not published to us. The template says "we are screening builders, not Shark Tank pitches" and calls slide 4 (Technical Approach) "the most important CORE slide" |
| Team size / members | see `../04-plan/team.md` |

## In scope (MVP)
- `/v1/authenticate` API returning decision, score and reasons
- Signals from all three families: behaviour, device and transaction
- Explainability: top contributing signals in plain English
- Demo dashboard and a scripted fraud-vs-legit scenario
- Latency measurement

- Typed challenges: biometric step-up (impostor) vs cooling-off / trusted contact (scam). See `../03-design/risk-engine.md`

## Stretch
- Step-up challenge flow (mock OTP) for "challenge" decisions
- Feedback loop (analyst marks a case as fraud or legit, and that adjusts thresholds)
- Model drift / monitoring view

## Out of scope
- Real payment-network integration
- Real PII or real card data. We use synthetic data only.
