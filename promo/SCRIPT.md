# Pramaan · 60 s promo: voiceover script

Video: `Pramaan_Promo_60s.mp4` (1080p, 60 fps, silent). About **120 words**, around 2 words per second, so the read is relaxed and leaves pauses for the visuals.
Start each line at its **cue**. The amounts and labels are already on screen, so the voice doesn't repeat them.

| Cue | Window | On screen | Voiceover | Words |
|---|---|---|---|---|
| **0:01** | 0:00–0:08 | Fake CBI call → PIN typed → *Approved* → turns red | "Asha is seventy-two. A fake CBI officer pressures her to pay. She enters her own PIN… *(beat)* approved." | 16 |
| **0:08.5** | 0:08–0:17 | Counter to ₹22,495 crore → "A PIN checks who you are…" | "In 2025, Indians lost over twenty-two thousand crore rupees to cyber fraud. *(beat)* A PIN checks *who* you are. Nobody checks *what's happening*." | 22 |
| **0:17.5** | 0:17–0:21 | Pramaan logo reveal | "Pramaan checks the situation before every payment." | 7 |
| **0:21.5** | 0:21–0:27 | ① Allow | "Usual payee, own phone, normal typing? It goes through instantly." | 10 |
| **0:27.5** | 0:27–0:33 | ② Challenge · biometric | "New phone, fresh SIM, new city? Only the owner's fingerprint can approve it." | 13 |
| **0:34** | 0:33–0:41 | ③ Hold + trusted contact; son taps *Cancel* | "On a call, paying someone new? We pause the payment, *(beat)* and her son can cancel it." | 15 |
| **0:41.5** | 0:41–0:47 | ④ Block | "A bot making fifteen attempts in ten minutes? Blocked." | 9 |
| **0:47.5** | 0:47–0:53 | Analyst console, "why" bars | "Every decision comes with a clear reason, and feedback keeps the model learning." | 13 |
| **0:54** | 0:53–1:00 | "Honest payments stay instant…" → logo | "Honest payments stay instant. Risky ones get stopped. *(beat)* We're Caffeinated Nerds, and this is Pramaan." | 15 |

## Read it as one piece
> Asha is seventy-two. A fake CBI officer pressures her to pay. She enters her own PIN… approved.
> In 2025, Indians lost over twenty-two thousand crore rupees to cyber fraud. A PIN checks who you are. Nobody checks what's happening.
> Pramaan checks the situation before every payment.
> Usual payee, own phone, normal typing? It goes through instantly.
> New phone, fresh SIM, new city? Only the owner's fingerprint can approve it.
> On a call, paying someone new? We pause the payment, and her son can cancel it.
> A bot making fifteen attempts in ten minutes? Blocked.
> Every decision comes with a clear reason, and feedback keeps the model learning.
> Honest payments stay instant. Risky ones get stopped. We're Caffeinated Nerds, and this is Pramaan.

## Delivery
- **Tone:** start quiet and serious for Asha, turn confident at "Pramaan", and keep it warm at the end.
- **Questions:** the four situations are questions followed by an answer. Lift the voice on the question, pause briefly, then give the answer.
- **Stress:** *approved* (ironic), *who* / *what's happening*, *instantly*, *Blocked*, *Pramaan*.
- **Timing:** finish each line before its window ends. If you run late, shift the next line rather than speeding up. Leave about 1 s of silence at the end.

## Adding the voiceover
- In any editor (CapCut, Clipchamp, DaVinci, Premiere): record the lines, then drag each one to its cue.
- With one VO file: `ffmpeg -i Pramaan_Promo_60s.mp4 -i vo.m4a -c:v copy -c:a aac -shortest Pramaan_Promo_VO.mp4`
- Optional: a soft music bed at around −24 dB under the voice.

Source for ₹22,495 crore: MHA via ThePrint (`docs/02-research/problem-evidence.md` [1]). The scores and latencies on screen are demo values.
