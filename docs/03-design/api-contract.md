# API contract (draft v0)

## `POST /v1/authenticate`

### Request
```json
{
  "transaction": { "id": "txn_123", "user_id": "u_42", "amount": 18999.0, "currency": "INR",
                   "merchant_id": "m_9", "merchant_category": "electronics", "timestamp": "2026-10-14T23:10:00+05:30",
                   "type": "card|upi|transfer", "beneficiary_id": null },
  "device":      { "device_id": "fp_abc", "ip": "203.0.113.5", "user_agent": "...",
                   "is_emulator": false, "is_vpn": false },
  "behaviour":   { "session_age_ms": 4000, "login_to_pay_ms": 3800, "failed_logins_24h": 0,
                   "keystroke_avg_ms": 120 }
}
```

### Response
```json
{
  "transaction_id": "txn_123",
  "decision": "allow | challenge | block",
  "risk_score": 0.62,
  "reasons": [
    { "signal": "new_device", "contribution": 0.25, "message": "First time this device is used by this user" },
    { "signal": "amount_ratio", "contribution": 0.20, "message": "Amount is 8.1x the user's median" }
  ],
  "challenge": { "type": "otp" },
  "latency_ms": 23,
  "model_version": "v0-rules"
}
```

### Errors
`400` invalid payload · `500` internal error. Fail-safe policy: _TBD_ (fail-open as allow, or fail-closed as challenge?) → decisions.md.
