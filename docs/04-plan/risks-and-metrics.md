# Risks, limitations & success metrics (feeds deck slide 5)

## What we will realistically build during the hack
A deployed cloud API (`/v1/authenticate`) that scores a payment in milliseconds and returns allow / challenge(type) / block with reasons. Also: a demo UPI-style payment app with a behaviour SDK, a live dashboard, and a synthetic dataset with 4 labelled attack types. **Not built:** a real bank/NPCI integration, a real mobile SDK (on-call/screen-share are toggles), real FRI/MuleHunter feeds (mocked).

## Genuine risks / limitations
| # | Risk | Why it's real | Mitigation |
|---|---|---|---|
| 1 | **Data realism**: the model learns our generator, not real fraud | No public behaviour+payment dataset exists | Hard negatives (travel, new phone, big rent); report metrics per fraud type; sanity-check on IEEE-CIS/PaySim; a real pilot would retrain on the bank's labelled history |
| 2 | **Signal availability / adoption**: on-call & screen-share need OS permissions and app integration | A browser can't see them; apps must adopt an SDK | Missing = "unknown", never "safe"; the model still works on txn + device signals; precedent: Google's screen-share alerts already in GPay/Paytm/Navi |
| 3 | **False positives hurt real people**: delaying a genuine urgent payment | Friction drives users away; blocking is worst | High fixed block threshold (0.90); challenge budget ≤ 5%; cancel/whitelist; feedback loop |
| 4 | **Adversaries adapt**: scammers tell victims to hang up, or to wait out the hold | Social engineering is adaptive | No single signal decides; trusted-contact approval; retrain on feedback |
| 5 | **Privacy (DPDP Act)**: behavioural data is personal data; consent rules apply from 13 Nov 2026 | Legal | Derived features only, hashed IDs, retention window, audit log |
| 6 | **Latency at UPI scale** (~9,300 txns/s average) | Shared 15 s UPI timeout | In-memory profiles, GBDT < 1 ms, fast-path rules, 150 ms fail-safe to standard 2FA |

## Success metrics (prototype, measured on held-out synthetic data + load test)
1. **Scam catch rate at low friction:** ≥ 80% of SCAM-type fraud challenged or blocked while ≤ 5% of legit payments are challenged. OTP-only stops ~0% of these, because the victim enters it.
2. **Friction saved vs blanket rules:** ≥ 90% of legit ≥ ₹10k transfers pass **without** delay (the RBI-proposed blanket rule would delay 100%).
3. **Speed:** p95 server latency < 50 ms (hard deadline 150 ms).
These are *targets*. We'll show the measured numbers live on the dashboard.
