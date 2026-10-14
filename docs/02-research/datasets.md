# Datasets

> Researched 2026-10-15. **Conclusion: no public dataset has behaviour + device + transaction + scam context together. We train on a calibrated synthetic generator, and use public datasets to sanity-check the transaction/device parts.**

## Candidates
| Dataset | What's in it | Size / fraud rate | Use for us | Limits |
|---|---|---|---|---|
| **IEEE-CIS Fraud Detection** (Vesta, Kaggle 2019) | Card-not-present txns + an identity table (DeviceType, DeviceInfo, masked `id_*` fields) | 590,540 txns, 431 features, **3.5% fraud** | Benchmark the transaction + device model; feature ideas | Feature names masked, so it's hard to explain. No behaviour data. US e-commerce |
| **PaySim** (Lopez-Rojas et al., 2016) | Simulated mobile-money logs (TRANSFER, CASH_OUT, …) calibrated on a real African mobile-money service | ~6.36 M rows, ~8.2k fraud (~0.13%); fraud only in TRANSFER/CASH_OUT | Closest to UPI P2P transfers: drain-the-account and transfer→cash-out patterns | No device/behaviour. Known simulation quirks (balance columns) |
| **Bank Account Fraud (BAF)** (Feedzai, NeurIPS 2022) | Account-opening applications with device/session fields (device OS, session length, velocity, device fraud count, foreign request) | 6 datasets × 1 M rows, ~1% fraud | Realistic priors for device/session feature distributions | Account opening, not payment authentication |
| ULB Credit Card Fraud (Kaggle) | 284,807 European card txns, PCA features V1–V28 | 492 fraud (0.17%) | Imbalance baseline only | PCA features can't be explained, which defeats our purpose |
| CMU Keystroke Dynamics benchmark | 51 users × 400 typings of one password | n/a | Calibrate typing-cadence distributions | Lab data, desktop keyboards |

## Our plan: synthetic generator (`scripts/generate_data.py`)
1. **Users (~5,000).** Each has a home city, 1–2 known devices, a log-normal spending profile (median ₹300–₹5,000), active hours, typing-cadence mean/std (CMU-like), age band (10% are 60+).
2. **Normal sessions (~200k txns over 30 days).** Merchant payments and P2P to a known payee list, with honest noise: travel, a new phone, a big monthly rent payment, festival shopping. **Hard negatives matter**, or the model learns "new device = fraud".
3. **Injected attack scenarios (~2–3% of txns)**, each with its own *signature*:
   - **IMP / account takeover / SIM swap:** new device, SIM change < 48h, new city/VPN, fast login→pay, typing mismatch, often a new payee.
   - **SCAM / APP (digital arrest, investment):** *known* device and home location, but on a call or screen-sharing, first-time payee, amount 5–50× median, round amount, long confirm dwell, risky payee. **The device looks clean, which is the point.**
   - **BOT / card testing:** emulator/headless, many small amounts in minutes, near-zero dwell.
   - **MULE receive-side:** new payee account with high fan-in.
4. **Labels:** `is_fraud` plus `fraud_type`, so we can report recall per attack type.
5. Calibration targets: overall fraud rate a few %, as in IEEE-CIS (3.5%), so training is stable. We report metrics by type, and say clearly that it's synthetic.

## Why this is honest
We say on the slides that the data is synthetic and explain why (privacy, no public behavioural payment data). We validate the transaction-feature model on IEEE-CIS/PaySim as a reality check. Real deployment would train on the bank's labelled history.

## Links
- IEEE-CIS: https://www.kaggle.com/c/ieee-fraud-detection (summary: https://physics.paperswithcode.com/dataset/ieee-cis-fraud-detection-1)
- PaySim paper (EMSS 2016): https://msc-les.org/proceedings/emss/emss2016/emss2016_249.html · Kaggle: https://www.kaggle.com/datasets/ealaxi/paysim1
- BAF: https://github.com/feedzai/bank-account-fraud · paper https://arxiv.org/abs/2211.13358
- CMU keystroke: https://www.cs.cmu.edu/~keystroke/
