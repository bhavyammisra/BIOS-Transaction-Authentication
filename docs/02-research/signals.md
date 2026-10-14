# Signal catalogue

> Priority: **P0** = MVP must-have, **P1** = nice to have, **P2** = stretch.

## Behaviour (session)
| Signal | Why it matters | Priority |
|---|---|---|
| Time from login to payment | Bots/ATO move unnaturally fast | P0 |
| Transaction velocity (count in last 1h/24h) | Card-testing, account takeover | P0 |
| Failed auth attempts recently | Credential stuffing | P0 |
| Typing / click cadence | Human vs bot; user's own rhythm | P1 |
| Navigation path (skipped steps) | Scripted flows | P2 |

## Device
| Signal | Why it matters | Priority |
|---|---|---|
| New device for this user | Classic ATO indicator | P0 |
| IP geo vs user's usual location / impossible travel | Stolen credentials | P0 |
| VPN / proxy / TOR | Hiding origin | P1 |
| Emulator / rooted / headless browser | Fraud tooling | P1 |
| Many users on one device | Fraud farm | P1 |

## Transaction
| Signal | Why it matters | Priority |
|---|---|---|
| Amount vs user's median (z-score / ratio) | Out-of-pattern spend | P0 |
| New merchant / category for user | Novelty | P0 |
| Unusual hour for this user | Behavioural mismatch | P1 |
| New beneficiary + high amount (transfers) | Mule / scam payments | P1 |
| Round amounts / just-under-limit amounts | Limit probing | P2 |
