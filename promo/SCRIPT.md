# Pramaan · 60 s promo: voiceover script

Video: `Pramaan_Promo_60s.mp4` (1920×1080, 60 fps, **silent**). Record the voiceover over it.
Pace: ~150 words in 60 s, calm and confident. Each line is timed to a cut, so start each one when its scene starts.

| Time | On screen | Voiceover |
|---|---|---|
| **0:00–0:08** · Hook | Incoming call from a "CBI Officer"; Asha accepts, enters her UPI PIN; the phone says *Payment approved*, then turns red | "Asha is 72. A caller claiming to be from the CBI tells her to transfer eighty-five thousand rupees. Her own phone, her own PIN. Every check says: approved." |
| **0:08–0:17** · Problem | Counter climbs to **₹22,495 crore**; "A PIN checks *who* you are. Nobody checks *what's happening*." | "In 2025, Indians lost over twenty-two thousand crore rupees to cyber fraud, mostly through scams where victims make the payment themselves. A PIN checks who you are. Nobody checks what's happening." |
| **0:17–0:21** · Reveal | Pramaan logo draws in; "Same ₹85,000 payment. Four situations." | "Pramaan checks the situation before every payment, in milliseconds." |
| **0:21–0:27** · ① Allow | Usual payee, own phone, normal typing → risk 0.04 → **ALLOW**, 38 ms | "Usual payee, usual phone, normal typing? It goes through instantly." |
| **0:27–0:33** · ② Biometric | New phone, SIM swapped 20 h ago, Kolkata → 0.58 → **CHALLENGE · biometric**; fingerprint fails | "New phone, SIM swapped yesterday, new city? That looks like a thief, so only the owner's fingerprint gets through." |
| **0:33–0:41** · ③ Hold + family | On a call, pasted new UPI ID → 0.71 → **CHALLENGE · hold + trusted contact**; 30-min timer; son Rohan taps *Cancel* on Telegram; "₹85,000 is safe" | "Her own phone, but she's on a call, paying a new account? That's a scam. We pause it, warn her, and her son gets a Telegram message: approve or cancel." |
| **0:41–0:47** · ④ Block | Emulator + VPN, attempt counter to 15 → 0.97 → **BLOCK**, analyst alerted | "A bot firing fifteen attempts in ten minutes is stopped outright." |
| **0:47–0:53** · Explain | Analyst console: live feed, "why" bars, *Confirm scam* → "model retrains" | "Every decision comes with a reason, and analyst feedback makes the model smarter." |
| **0:53–1:00** · Close | "Honest payments stay instant. Only risky ones are stopped." → logo, "Fast. Secure. Explained." | "Honest payments stay instant. Only risky ones are stopped. We're Caffeinated Nerds, and this is Pramaan." |

**Word count:** ~150. If you run long, drop "in milliseconds" (0:17) and "and analyst feedback makes the model smarter" (0:47).

## Adding the voiceover
- Any editor (CapCut, Clipchamp, DaVinci Resolve, Premiere): drop the MP4 on the timeline, record or import the VO, and line each sentence up with its row above.
- Optional: soft ambient/tech music bed at around −24 dB under the voice, with a riser into 0:17 (logo) and a hit on each decision pill (0:24, 0:30, 0:36.5, 0:44).
- Command line, if the VO is one file: `ffmpeg -i Pramaan_Promo_60s.mp4 -i vo.m4a -c:v copy -c:a aac -shortest Pramaan_Promo_VO.mp4`

## Facts used (all from `docs/`)
- ₹22,495 crore lost to cyber fraud in 2025: MHA via ThePrint (`docs/02-research/problem-evidence.md` [1]).
- Four situations, decisions and reasons: `docs/05-pitch/README.md` demo script and slide 3.
- Risk scores, latencies and the console data are illustrative values for the demo.
