# Scope & hackathon logistics

## Logistics (fill in from the official rules)
| Item | Value |
|---|---|
| Hackathon | BIOS, Thapar Institute |
| Screening/submission deadline | _TBD_ |
| Final round dates | _TBD_ |
| Submission format | _TBD_ (repo? video? deck? deployed link?) |
| Judging criteria | _TBD_ |
| Team size / members | see `../04-plan/team.md` |

## In scope (MVP)
- `/v1/authenticate` API returning decision, score and reasons
- Signals from all three families: behaviour, device and transaction
- Explainability: top contributing signals in plain English
- Demo dashboard and a scripted fraud-vs-legit scenario
- Latency measurement

## Stretch
- Step-up challenge flow (mock OTP) for "challenge" decisions
- Feedback loop (analyst marks a case as fraud or legit, and that adjusts thresholds)
- Model drift / monitoring view

## Out of scope
- Real payment-network integration
- Real PII or real card data. We use synthetic data only.
