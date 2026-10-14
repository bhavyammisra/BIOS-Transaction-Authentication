# Timeline

| Date | Milestone | Status |
|---|---|---|
| 2026-10-14 | Problem finalised, repo set up | ✅ |
| 2026-10-15 | Research + design + build plan (docs) | ✅ |
| **2026-10-15 (night)** | **Screening submission: 5-slide deck (BIOS template) + video** | ⏳ |
| _TBD_ | Screening results | |
| _TBD_ | BIOS hack: build the prototype (plan below) | |

## Build plan for the hack (in hack-hours; assumes a ~24–36 h hack. Adjust once dates and duration are known)
| Hours | Milestone | Owner |
|---|---|---|
| H0–H2 | Repo scaffolding: FastAPI skeleton + `/health`, React app skeleton, Supabase table, Cloud Run deploy pipeline | Bhavyam |
| H0–H6 | Synthetic generator: users, normal traffic, 4 attack types, hard negatives | Gunagye |
| H2–H8 | Demo payment app + SDK capture + scenario toggles (on-call, screen-share, SIM change) | Abhijay |
| H6–H12 | Features + LightGBM + calibration + TreeSHAP + reason templates + policy (`config.yaml`) | Gunagye |
| H6–H12 | `/v1/authenticate` wired end-to-end with profiles, event log, fail-safe | Bhavyam |
| H8–H16 | Dashboard: live feed, "why" panel, latency chart, threshold sliders | Shefali |
| H12–H18 | Scenario tests (allow / impostor→biometric / scam→cooling-off / bot→block) + metrics + load test | Shefali + Gunagye |
| H18–H22 | Deploy, polish, rehearse the 3-minute demo | All |
| H22+ | Buffer / stretch: feedback loop, trusted-contact flow, IEEE-CIS sanity check | All |
