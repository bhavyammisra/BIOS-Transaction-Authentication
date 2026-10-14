# Architecture (draft; nothing here is final until it's logged in `decisions.md`)

## Components
```
Client / merchant checkout
        │  POST /v1/authenticate  (txn + device + behaviour)
        ▼
┌──────────────┐   ┌─────────────────────┐   ┌──────────────────┐
│   API layer  │──▶│ Feature extraction  │──▶│  Scoring         │
│ (src/api)    │   │ (user history, device│   │ rules + model    │
└──────┬───────┘   │  profile lookups)   │   └────────┬─────────┘
       │           └──────────┬──────────┘            │
       │                      ▼                       ▼
       │              Profile store (user/device)   Decision + reasons
       │                                              │
       └──────────────◀───────────────────────────────┘
                       │
                       ▼
              Event log ──▶ Dashboard (src/dashboard)
```

## Request flow
1. The API validates the payload (`api-contract.md`).
2. Features are built: the user's history (median amount, known devices, usual geo) and the session's behaviour.
3. The risk engine produces a score in [0,1] and per-signal contributions (`risk-engine.md`).
4. Thresholds map the score to allow / challenge / block. Hard rules can override (e.g. block on a known-bad device).
5. The response is returned. The event is logged for the dashboard and the feedback loop.

## Latency budget (target p95 < 100 ms)
| Step | Budget |
|---|---|
| Validation + parsing | 5 ms |
| Profile lookups | 20 ms |
| Scoring + explanation | 30 ms |
| Network/overhead | remainder |

## Stack
_TBD: see decisions.md D-002._
