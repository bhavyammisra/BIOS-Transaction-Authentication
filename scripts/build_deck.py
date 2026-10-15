"""Fill the BIOS V2 screening template with Pramaan content. Usage: python build.py template.pptx out.pptx"""
import sys, copy
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree

NAVY = "1E2761"; ICE = "CADCFC"; PANEL = "EEF1FB"; TEXT = "222222"; MUTED = "5A6275"
GREEN = "2E7D32"; GREEN_T = "E8F5E9"; AMBER = "B25E00"; AMBER_T = "FFF3E0"; RED = "C62828"; RED_T = "FDECEA"
WHITE = "FFFFFF"; BODY = "Calibri"; HEAD = "Cambria"

def rgb(h): return RGBColor.from_string(h)

def remove(shape):
    el = shape._element; el.getparent().remove(el)

def set_run_text(shape, text, top=None, left=None, width=None, height=None):
    """Replace text while keeping the first run's formatting."""
    tf = shape.text_frame
    p = tf.paragraphs[0]
    runs = p.runs
    runs[0].text = text
    for r in runs[1:]:
        r._r.getparent().remove(r._r)
    for extra in tf.paragraphs[1:]:
        extra._p.getparent().remove(extra._p)
    if top is not None: shape.top = Inches(top)
    if left is not None: shape.left = Inches(left)
    if width is not None: shape.width = Inches(width)
    if height is not None: shape.height = Inches(height)

def _apply_font(run, size, bold=False, italic=False, color=TEXT, font=BODY):
    f = run.font
    f.size = Pt(size); f.bold = bold; f.italic = italic; f.name = font
    f.color.rgb = rgb(color)

def add_par(tf, runs, align=PP_ALIGN.LEFT, space_after=0, space_before=0, bullet=False, first=False, line_spacing=None):
    """runs: list of (text, size, bold, color[, italic[, font]])"""
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    if space_after: p.space_after = Pt(space_after)
    if space_before: p.space_before = Pt(space_before)
    if line_spacing: p.line_spacing = line_spacing
    if bullet:
        pPr = p._p.get_or_add_pPr()
        pPr.set("marL", str(Emu(Inches(0.17)))); pPr.set("indent", str(-Emu(Inches(0.15))))
        for tag in ("a:buNone", "a:buChar", "a:buAutoNum"):
            for e in pPr.findall(qn(tag)): pPr.remove(e)
        buClr = etree.SubElement(pPr, qn("a:buClr")); sc = etree.SubElement(buClr, qn("a:srgbClr")); sc.set("val", NAVY)
        bu = etree.SubElement(pPr, qn("a:buChar")); bu.set("char", "•")
    for r in runs:
        text, size, bold, color = r[0], r[1], r[2], r[3]
        italic = r[4] if len(r) > 4 else False
        font = r[5] if len(r) > 5 else BODY
        run = p.add_run(); run.text = text
        _apply_font(run, size, bold, italic, color, font)
    return p

def textbox(slide, x, y, w, h, name, anchor=MSO_ANCHOR.TOP, margin=0.0):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tb.name = name
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(margin); tf.margin_top = tf.margin_bottom = Inches(margin)
    tf.vertical_anchor = anchor
    return tb, tf

def box(slide, x, y, w, h, name, fill=PANEL, line=None, radius=0.06, anchor=MSO_ANCHOR.TOP, pad=0.12, shape=MSO_SHAPE.ROUNDED_RECTANGLE):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    s.name = name
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    if fill: s.fill.solid(); s.fill.fore_color.rgb = rgb(fill)
    else: s.fill.background()
    if line: s.line.color.rgb = rgb(line); s.line.width = Pt(1)
    else: s.line.fill.background()
    s.shadow.inherit = False
    tf = s.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(pad); tf.margin_top = tf.margin_bottom = Inches(pad * 0.7)
    tf.vertical_anchor = anchor
    return s, tf

def pill(slide, x, y, w, h, name, text, fill, size=11):
    s, tf = box(slide, x, y, w, h, name, fill=fill, radius=0.5, anchor=MSO_ANCHOR.MIDDLE, pad=0.05)
    add_par(tf, [(text, size, True, WHITE)], align=PP_ALIGN.CENTER, first=True)
    return s

def arrow(slide, x1, y1, x2, y2, name, color=NAVY, width=1.75, dashed=False):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.name = name
    c.line.color.rgb = rgb(color); c.line.width = Pt(width)
    ln = c.line._get_or_add_ln()
    if dashed:
        d = etree.SubElement(ln, qn("a:prstDash")); d.set("val", "dash")
    te = etree.SubElement(ln, qn("a:tailEnd")); te.set("type", "triangle"); te.set("w", "med"); te.set("len", "med")
    return c

def label(tf, text, color=NAVY, size=11, first=False, space_before=0):
    return add_par(tf, [(text, size, True, color)], first=first, space_after=2, space_before=space_before)

def strip_instructions(slide):
    for sh in list(slide.shapes):
        if sh.name in ("Text 5", "Text 6", "Shape 7", "Text 8", "Text 9"):
            remove(sh)

def heading(slide, title_y=1.58, sub_y=2.13, headline=None):
    for sh in slide.shapes:
        if sh.name == "Text 2":
            sh.top = Inches(title_y); sh.left = Inches(0.5); sh.width = Inches(8.0)
        if sh.name == "Text 4":
            set_run_text(sh, headline, top=sub_y, left=0.5, width=12.35, height=0.5)

def sources(slide, text, y=7.12):
    tb, tf = textbox(slide, 0.5, y, 12.35, 0.3, "Sources")
    add_par(tf, [(text, 9, False, MUTED, True)], first=True)

def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text

# ---------------------------------------------------------------- slide 1
def slide1(s):
    strip_instructions(s)
    heading(s, headline="> Fraud has moved past OTPs: victims now approve the payment themselves")

    # team strip (top right, beside the logo)
    st, tf = box(s, 4.15, 0.66, 8.7, 0.9, "Team strip", fill=PANEL, radius=0.12, pad=0.12)
    add_par(tf, [("Team Caffeinated Nerds", 11.5, True, NAVY), ("   ·   Challenge: ", 11, False, NAVY), ("Frontier · PS-04", 11, True, NAVY), (" · Fast and Secure Online Transaction Authentication", 11, False, NAVY)], first=True)
    for i, (name, roll) in enumerate([("Bhavyam Misra", "1024030535"), ("Gunagye Jain", "1024030019"),
                                      ("Abhijay Nagal", "______________"), ("Shefali Sharma", "1024030284")]):
        tb, ttf = textbox(s, 4.27 + i * 2.13, 1.01, 2.05, 0.45, f"Member {i+1}")
        add_par(ttf, [(name, 10.5, True, TEXT)], first=True)
        add_par(ttf, [("Roll No: " + roll, 10, False, MUTED)])

    # left column: problem / stakeholder / why
    tb, tf = textbox(s, 0.5, 2.82, 6.75, 3.6, "Problem text")
    label(tf, "PROBLEM", first=True)
    add_par(tf, [("Every online payment gets the same static PIN/OTP check. It proves ", 13, False, TEXT),
                 ("who holds the credential", 13, True, TEXT), (", not whether ", 13, False, TEXT),
                 ("this payment is normal for this person, right now", 13, True, TEXT),
                 (". Scam victims type their own OTP while a fraudster coaches them; SIM-swappers intercept it.", 13, False, TEXT)], space_after=10)
    label(tf, "TARGET STAKEHOLDER")
    add_par(tf, [("Banks, UPI apps & payment gateways", 13, True, TEXT),
                 (" that must allow / challenge / block within UPI's 15-second window, on behalf of everyday users, especially ", 13, False, TEXT),
                 ("seniors and first-time digital payers", 13, True, TEXT), (".", 13, False, TEXT)], space_after=10)
    label(tf, "WHY IT IS WORTH SOLVING")
    add_par(tf, [("Losses tripled from 2023 to 2024. RBI's proposed fix is a ", 13, False, TEXT),
                 ("blanket 1-hour delay on every ₹10k+ transfer", 13, True, TEXT),
                 (", adding friction for all honest users. A precise, explainable risk check stops the scam and keeps honest payments instant. RBI's 2025 rules already allow risk-based extra checks.", 13, False, TEXT)])

    # right column: evidence stats
    tb, tf = textbox(s, 7.55, 2.82, 5.3, 0.3, "Evidence label")
    label(tf, "EVIDENCE", first=True)
    stats = [("₹22,495 cr", "lost to cyber fraud in 2025: 28 lakh complaints, +24% year on year (MHA / NCRP)"),
             ("~85%", "of 2025 losses came from investment & “digital arrest” scams, where the victim pays (MHA)"),
             ("98.5%", "of fraud value is in payments above ₹10,000. RBI: account takeover is “now negligible”, most fraud is authorised push payment (RBI, Apr 2026)")]
    y = 3.12
    for i, (big, small) in enumerate(stats):
        b, tf = box(s, 7.55, y, 5.3, 1.0, f"Stat {i+1}", fill=PANEL, radius=0.1, pad=0.14, anchor=MSO_ANCHOR.MIDDLE)
        p = add_par(tf, [(big, 24, True, NAVY, False, HEAD)], first=True)
        add_par(tf, [(small, 11, False, TEXT)])
        y += 1.1

    # SDG row
    sdgs = [("00689D", "PRIMARY · SDG 16", "16.4: cut illicit financial flows & organised crime"),
            ("A21942", "SUPPORTING · SDG 8", "8.10: access to financial services for all"),
            ("DD5A1F", "SUPPORTING · SDG 9", "9.1: reliable, resilient (digital) infrastructure")]
    x = 0.5
    for i, (col, head, body) in enumerate(sdgs):
        b, tf = box(s, x, 6.48, 4.0, 0.6, f"SDG {i+1}", fill=col, radius=0.18, pad=0.12, anchor=MSO_ANCHOR.MIDDLE)
        add_par(tf, [(head, 10.5, True, WHITE)], first=True)
        add_par(tf, [(body, 10.5, False, WHITE)])
        x += 4.175
    sources(s, "Sources: MHA/NCRP data via Parliament replies (2024, 2025); RBI Discussion Paper on safeguards in digital payments, 9 Apr 2026; RBI Authentication Directions, 25 Sep 2025. Links: repo › docs/02-research/problem-evidence.md")
    notes(s, "We're team Caffeinated Nerds, on the Frontier challenge: Fast and Secure Online Transaction Authentication. "
             "Today every online payment in India gets the same check, a PIN or an OTP. That proves who holds the credential, but not whether this payment makes sense right now. "
             "And fraud has moved. In April 2026 the RBI said account-takeover fraud is now negligible. Most fraud is authorised push payment: the real user, on their own phone, types their own OTP while a scammer coaches them. "
             "Indians lost about 22,500 crore rupees to cyber fraud in 2025, and around 85 percent of that came from investment and digital-arrest scams. "
             "Our stakeholders are banks, UPI apps and payment gateways, who must decide in milliseconds, on behalf of everyday users, especially seniors. "
             "The obvious fix, delaying every big transfer, punishes every honest user, so we want precision instead. "
             "Primary SDG 16.4, supported by 8.10 and 9.1.")

# ---------------------------------------------------------------- slide 2
def slide2(s):
    strip_instructions(s)
    heading(s, headline="> Today's defences check the credential or the receiver, never the moment")
    cards = [
        ("1 · Static two-factor auth", "UPI PIN · SMS OTP · 3-D Secure",
         "Device binding + PIN/OTP on every payment. RBI keeps 2FA as the minimum from April 2026.",
         "Checks the credential, not the context. Coached victims type it in; SIM-swap steals it. Same friction for a ₹50 tea and a ₹2 lakh transfer."),
        ("2 · Commercial risk engines", "Stripe Radar · Sift · BioCatch · 3DS-2 issuer engines",
         "ML score over hundreds of signals → block / review / ask for 3DS. BioCatch adds behavioural biometrics.",
         "Proprietary, priced for large players, sold as separate products. Gives analysts a score, not the customer a reason. The challenge is a generic OTP whatever the risk."),
        ("3 · India's ecosystem tools", "NPCI FRM · DoT FRI · RBI MuleHunter.AI · DPIP (pilot)",
         "Shared intelligence on risky numbers and mule accounts; alerts to banks. RBI also proposes blanket delays & trusted-person approval.",
         "Reputation after the fact: a number must be reported first, and scam numbers live only days. Scores the receiver, not this session. Blanket rules add friction for everyone."),
    ]
    x = 0.5
    for i, (title, sub, does, gap) in enumerate(cards):
        b, tf = box(s, x, 2.8, 3.97, 3.12, f"Approach {i+1}", fill=PANEL, radius=0.06, pad=0.16)
        add_par(tf, [(title, 15, True, NAVY, False, HEAD)], first=True)
        add_par(tf, [(sub, 10.5, False, MUTED, True)], space_after=8)
        add_par(tf, [("What it does", 11, True, NAVY)], space_after=1)
        add_par(tf, [(does, 13, False, TEXT)], space_after=10)
        add_par(tf, [("What's still missing", 11, True, RED)], space_after=1)
        add_par(tf, [(gap, 13, False, TEXT)])
        x += 4.19
    b, tf = box(s, 0.5, 6.05, 12.35, 0.95, "Gap statement", fill=NAVY, radius=0.12, pad=0.2, anchor=MSO_ANCHOR.MIDDLE)
    add_par(tf, [("The gap we are addressing is: ", 14, True, ICE, False, HEAD),
                 ("no lightweight, real-time service fuses behaviour + device + transaction context into an explained allow / challenge / block decision that also picks the ", 13.5, False, WHITE),
                 ("right kind", 13.5, True, WHITE), (" of challenge. Coached victims get stopped; honest payments stay instant.", 13.5, False, WHITE)], first=True)
    sources(s, "Sources: RBI press release 25 Sep 2025 & Discussion Paper 9 Apr 2026; Stripe Radar docs (risk evaluation); Sift; BioCatch (remote-access scams; India 2024 report); NPCI FRM; DoT FRI (May 2025); IBTimes on IDPIC/MuleHunter (Sep 2026). Links: repo › docs/02-research/prior-art.md")
    notes(s, "Three families of solutions exist today. "
             "First, static two-factor auth: PIN, OTP, 3-D Secure. It's mandatory and it's the floor, but it checks the credential, not the context. A coached victim simply types it in. "
             "Second, commercial risk engines like Stripe Radar, Sift and BioCatch. They're powerful, but proprietary and expensive, the output is a score for an analyst, and the challenge is a generic OTP regardless of what kind of risk it is. "
             "Third, India's ecosystem tools: NPCI's fraud monitoring, DoT's Fraud Risk Indicator, RBI's MuleHunter. They're great reputation lists, but they work after the fact: a number has to be reported first, and they score the receiver, not this session. "
             "So the gap is a lightweight real-time service that fuses all three signal families into an explained decision and picks the right kind of challenge.")

# ---------------------------------------------------------------- slide 3
def slide3(s):
    strip_instructions(s)
    heading(s, headline="> Pramaan: OTP checks the person. We check the situation.")
    tb, tf = textbox(s, 0.5, 2.8, 5.75, 4.3, "Solution text")
    label(tf, "WHAT WE BUILD", first=True)
    add_par(tf, [("A cloud risk API that banks and UPI apps call ", 13, False, TEXT), ("before", 13, True, TEXT),
                 (" PIN/OTP. It returns ", 13, False, TEXT), ("allow / challenge / block", 13, True, TEXT),
                 (" in milliseconds, with plain-language reasons. It adds to mandated 2FA; it never replaces it.", 13, False, TEXT)], space_after=9)
    label(tf, "CORE FUNCTIONALITY")
    for t in [("20+ signals", " (behaviour, device, transaction, receiver) scored against each user's own history"),
              ("Hybrid engine:", " policy rules + gradient-boosted model, with each signal's contribution explained"),
              ("Amount-aware:", " a ₹40 tea is never stopped; an ₹85k first-time transfer is checked closely"),
              ("4 levels of response:", " allow · fingerprint for a likely impostor · pause + family approval for a likely scam victim · block")]:
        add_par(tf, [(t[0], 12.5, True, TEXT), (t[1], 12.5, False, TEXT)], bullet=True, space_after=3)
    label(tf, "WHY THIS CLOSES THE GAP", space_before=6)
    add_par(tf, [("An OTP can't stop someone who is being coached. A pause and a family member who can cancel can. We use them ", 12.5, False, TEXT),
                 ("only", 12.5, True, TEXT), (" when the context is risky, unlike RBI's proposed blanket 1-hour delay. Built on free, open tools: ", 12.5, False, TEXT),
                 ("₹0 running cost", 12.5, True, TEXT), (".", 12.5, False, TEXT)])

    # right: user interaction table
    tb, tf = textbox(s, 6.55, 2.8, 6.3, 0.3, "Scenarios label")
    label(tf, "USER INTERACTION: 4 levels · the same ₹85,000 payment, four situations", first=True)
    rows = [("Usual payee, own phone, normal typing", "① ALLOW", GREEN, GREEN_T, "No extra step. Pays instantly."),
            ("New phone, SIM swapped 20 h ago, new city", "② FINGERPRINT", AMBER, AMBER_T, "Impostor risk: owner's passkey biometric needed."),
            ("On a call, new UPI ID pasted, own phone", "③ PAUSE + FAMILY", AMBER, AMBER_T, "Scam risk: held; son taps Cancel on Telegram"),
            ("Emulator + VPN, 15 attempts in 10 minutes", "④ BLOCK", RED, RED_T, "Bot / card-testing: stopped, analyst alerted.")]
    y = 3.13
    for i, (ctx, dec, col, tint, why) in enumerate(rows):
        b, tf = box(s, 6.55, y, 6.3, 0.78, f"Scenario {i+1}", fill=tint, radius=0.1, pad=0.13, anchor=MSO_ANCHOR.MIDDLE)
        tf.margin_right = Inches(2.72)
        add_par(tf, [(ctx, 12, True, TEXT)], first=True)
        add_par(tf, [(why, 11, False, MUTED)])
        pill(s, 10.25, y + 0.16, 2.5, 0.46, f"Decision {i+1}", dec, col, size=11.5)
        y += 0.87
    b, tf = box(s, 6.55, y + 0.03, 6.3, 0.45, "Analyst note", fill=PANEL, radius=0.15, pad=0.13, anchor=MSO_ANCHOR.MIDDLE)
    add_par(tf, [("Analysts", 11.5, True, NAVY), (" see every decision live with its “why”; their feedback retrains the model.", 11.5, False, TEXT)], first=True)
    notes(s, "Our solution is Pramaan, which means proof. It's a cloud risk API that a bank or UPI app calls just before the PIN or OTP step. "
             "It scores more than 20 signals against the user's own history and returns allow, challenge or block in milliseconds, with reasons in plain language. "
             "Two things make it different. First, thresholds depend on the amount: a 40-rupee tea is never stopped, an 85,000-rupee first-time transfer is checked closely. "
             "Second, the challenge depends on the kind of risk. Look at the same 85,000-rupee payment in four situations. Usual payee, own phone: allowed. "
             "New phone and a SIM swap yesterday: that's an impostor, so we ask for the owner's fingerprint. "
             "Own phone at home, but on a call and pasting a new UPI ID: that's a coached victim. An OTP won't help, so we pause it and her son gets an Approve or Cancel message on Telegram. "
             "An emulator firing 15 attempts: blocked.")

# ---------------------------------------------------------------- slide 4
def slide4(s):
    strip_instructions(s)
    heading(s, headline="> One API call: context in, an explained decision out, in milliseconds")
    top = 2.78; H = 2.22
    # 1 input
    b, tf = box(s, 0.5, top, 2.0, H, "D1 Input", fill=PANEL, line=ICE, radius=0.08, pad=0.12)
    add_par(tf, [("1 · INPUT", 10.5, True, MUTED)], first=True, space_after=2)
    add_par(tf, [("Payment app + Pramaan SDK", 12.5, True, NAVY)], space_after=4)
    add_par(tf, [("transaction · device · session behaviour: typing rhythm, dwell, paste, login→pay time, on-call*, screen-share*", 10.5, False, TEXT)])
    # 2 api
    b, tf = box(s, 2.83, top, 1.8, H, "D2 API", fill=PANEL, line=ICE, radius=0.08, pad=0.12)
    add_par(tf, [("2 · API", 10.5, True, MUTED)], first=True, space_after=2)
    add_par(tf, [("POST /v1/authenticate", 12, True, NAVY)], space_after=4)
    add_par(tf, [("FastAPI on Render (free tier): validate, start timer. Over 150 ms → falls back to standard 2FA", 10.5, False, TEXT)])
    # 3 features
    b, tf = box(s, 4.96, top, 2.0, 1.32, "D3 Features", fill=PANEL, line=ICE, radius=0.08, pad=0.12)
    add_par(tf, [("3 · FEATURES", 10.5, True, MUTED)], first=True, space_after=2)
    add_par(tf, [("20+ features vs the user's own baseline", 11.5, True, NAVY)], space_after=2)
    add_par(tf, [("“8× usual amount”, new payee, new device…", 10.5, False, TEXT)])
    b, tf = box(s, 4.96, top + 1.62, 2.0, 0.6, "D3b Profile store", fill=WHITE, line=NAVY, radius=0.15, pad=0.08, anchor=MSO_ANCHOR.MIDDLE)
    add_par(tf, [("Profile store (in-memory)", 10.5, True, NAVY)], first=True, align=PP_ALIGN.CENTER)
    add_par(tf, [("habits · devices · payees · receiver risk", 9.5, False, TEXT)], align=PP_ALIGN.CENTER)
    # 4 engine
    ex = 7.29; ew = 3.15
    b, tf = box(s, ex, top, ew, H, "D4 Engine", fill=NAVY, radius=0.06, pad=0.12)
    add_par(tf, [("4 · RISK ENGINE", 10.5, True, ICE)], first=True)
    steps = [("a", "Rules: hard policy + fast-path allow"), ("b", "LightGBM → fraud probability p"),
             ("c", "TreeSHAP → each signal's contribution"), ("d", "Risk type: impostor · scam · bot · mule"),
             ("e", "Cost policy → decision + challenge type")]
    sy = top + 0.36
    for k, t in steps:
        sb, stf = box(s, ex + 0.12, sy, ew - 0.24, 0.33, f"Engine step {k}", fill="2C3A86", radius=0.2, pad=0.08, anchor=MSO_ANCHOR.MIDDLE)
        add_par(stf, [(k + "  ", 10.5, True, ICE), (t, 10.5, False, WHITE)], first=True)
        sy += 0.365
    # 5 output
    b, tf = box(s, 10.77, top, 2.08, H, "D5 Output", fill=PANEL, line=ICE, radius=0.08, pad=0.12)
    add_par(tf, [("5 · OUTPUT", 10.5, True, MUTED)], first=True, space_after=4)
    for txt, col in (("ALLOW", GREEN), ("CHALLENGE (type)", AMBER), ("BLOCK", RED)):
        add_par(tf, [(txt, 11.5, True, col)], space_after=1)
    add_par(tf, [("+ score, top-3 reasons, latency", 10.5, False, TEXT)], space_before=4)
    add_par(tf, [("Holds → n8n → family on Telegram", 10.5, True, NAVY)], space_before=3)
    # arrows main flow
    mid = top + 0.75
    arrow(s, 2.5, mid, 2.83, mid, "A1"); arrow(s, 4.63, mid, 4.96, mid, "A2")
    arrow(s, 6.96, mid, 7.29, mid, "A3"); arrow(s, 10.44, mid, 10.77, mid, "A4")
    arrow(s, 5.96, top + 1.32, 5.96, top + 1.62, "A5 profile", width=1.25)

    # what's built strip
    b, tf = box(s, 0.5, 5.12, 12.35, 0.42, "Built strip", fill=GREEN_T, radius=0.3, pad=0.14, anchor=MSO_ANCHOR.MIDDLE)
    add_par(tf, [("Built during the hack: ", 11, True, GREEN),
                 ("SDK + demo app, API, risk engine, passkey fingerprint, n8n + Telegram family loop, replay simulator, live dashboard, deploy.   ", 11, False, TEXT),
                 ("Mocked: ", 11, True, AMBER), ("bank/NPCI rails, FRI & mule feeds, *phone call-state.", 11, False, TEXT)], first=True)

    # bottom panels
    panels = [
        ("STACK (all free, ₹0 running cost)", [("Python · FastAPI · LightGBM · SHAP on Render (no card) · React on Vercel · Supabase free tier", False),
                   ("n8n (self-hosted) + Telegram Bot API: hold → family Approve/Cancel → timeout → label", False),
                   ("WebAuthn passkeys for fingerprint · replay simulator: our policy vs RBI's blanket delay", False)]),
        ("DATA", [("No public dataset has all three signal families → synthetic generator: 5k users, 30 days, 4 labelled attack types + hard negatives (travel, new phone, rent)", False),
                  ("Sanity-checked on IEEE-CIS (590k txns) & PaySim · *call state: mobile SDK, toggles in demo", False)]),
        ("DECISION RULE", [("Block if p ≥ 0.90 or a hard rule fires", False),
                           ("Challenge if p ≥ clip(₹500 ÷ amount, 0.05, 0.60): stricter as the amount grows", False),
                           ("Challenge type = lowest friction + p × amount × (1 − effectiveness vs this risk type)", False)]),
    ]
    x = 0.5; w = 4.0
    for i, (head, lines) in enumerate(panels):
        b, tf = box(s, x, 5.68, w, 1.55, f"Panel {head}", fill=PANEL, radius=0.07, pad=0.13)
        add_par(tf, [(head, 10.5, True, NAVY)], first=True, space_after=2)
        for t, _ in lines:
            add_par(tf, [(t, 10.5, False, TEXT)], bullet=True, space_after=2)
        x += w + 0.175
    notes(s, "Here's how it works. One: the payment app, with our small SDK, sends the transaction, device info and session behaviour, like typing rhythm, time on the confirm screen, a pasted payee, and on mobile whether a call or screen-share is active. "
             "Two: our FastAPI service, on Render's free tier, validates it and starts a timer. "
             "Three: we build 20-plus features against this user's own history from an in-memory profile store. "
             "Four, the risk engine: hard rules first, then a LightGBM model gives a fraud probability, TreeSHAP tells us each signal's contribution, the strongest family tells us the risk type, and a cost policy picks the decision. "
             "The thresholds tighten as the amount grows, and the challenge type is whichever costs least for that risk type. "
             "Five: allow, challenge or block, plus reasons and latency. If we ever take longer than 150 milliseconds we fall back to standard 2FA, so we never fail open. "
             "For a likely scam, the hold goes to an n8n workflow that messages a family member on Telegram to approve or cancel; for a likely impostor, a passkey fingerprint check. Everything is free and open, so running cost is zero. Our training data is synthetic, and we say so: no public dataset has these signals together.")

# ---------------------------------------------------------------- slide 5
def slide5(s):
    strip_instructions(s)
    heading(s, headline="> A deployed, working prototype in the hack, honest about its limits")
    cols = [("1 · WHAT WE WOULD BUILD", 0.5), ("2 · RISKS & LIMITATIONS", 4.69), ("3 · EXPECTED IMPACT", 8.88)]
    for i, (h, x) in enumerate(cols):
        b, tf = box(s, x, 2.8, 3.97, 0.42, f"Col head {i+1}", fill=NAVY, radius=0.3, pad=0.12, anchor=MSO_ANCHOR.MIDDLE)
        add_par(tf, [(h, 12, True, WHITE)], first=True)
    # col 1
    b, tf = box(s, 0.5, 3.32, 3.97, 3.9, "Build body", fill=PANEL, radius=0.05, pad=0.15)
    add_par(tf, [("A working prototype by the end of the hack:", 11.5, True, NAVY)], first=True, space_after=3)
    for t in ["Live /v1/authenticate (Render, free) with fail-safe",
              "Risk engine: rules + LightGBM + TreeSHAP + cost policy",
              "4 levels live: passkey fingerprint, n8n + Telegram family loop",
              "Demo UPI app + SDK; dashboard with “why” panel",
              "Replay simulator vs RBI's blanket delay; synthetic data"]:
        add_par(tf, [(t, 12, False, TEXT)], bullet=True, space_after=3)
    add_par(tf, [("Plan (hack hours)", 11.5, True, NAVY)], space_before=8, space_after=1)
    add_par(tf, [("H0–6 data + scaffolding · H6–12 engine + API · H8–16 app, passkeys, n8n loop · H12–18 dashboard, simulator, tests · H18+ deploy + rehearse", 11, False, TEXT)], space_after=6)
    add_par(tf, [("Cost: ", 11, True, NAVY), ("₹0, free tiers + open source, no paid APIs.", 11, False, TEXT)])
    # col 2
    b, tf = box(s, 4.69, 3.32, 3.97, 3.9, "Risks body", fill=PANEL, radius=0.05, pad=0.15)
    risks = [("Data realism.", " Synthetic ≠ real fraud.", " → hard negatives, per-type metrics, IEEE-CIS/PaySim check; retrain on bank history in a pilot."),
             ("Signal access.", " Call/screen-share state needs a mobile SDK + app adoption.", " → missing = “unknown”, never “safe”; Google is already piloting screen-share alerts in GPay/Paytm."),
             ("False positives.", " Delaying a genuine urgent payment hurts.", " → block only at p ≥ 0.9, ≤ 5% challenge budget, cancel/whitelist, feedback loop."),
             ("Privacy & adaptation.", " DPDP consent rules (from 13 Nov 2026); scammers adapt.", " → derived features only, hashed IDs; no single signal decides; retraining.")]
    first = True
    for a, b_, c in risks:
        add_par(tf, [(a, 12, True, RED), (b_, 12, False, TEXT), (c, 11, False, MUTED, True)], first=first, space_after=9)
        first = False
    # col 3
    b, tf = box(s, 8.88, 3.32, 3.97, 0.78, "Impact lead", fill=PANEL, radius=0.08, pad=0.15, anchor=MSO_ANCHOR.MIDDLE)
    add_par(tf, [("For banks & UPI apps: ", 11.5, True, NAVY), ("stop the scams OTP can't, without slowing down honest users.", 11.5, False, TEXT)], first=True)
    mets = [("≥ 80%", "of scam-type fraud caught while ≤ 5% of legit payments are challenged (OTP-only: ~0%)"),
            ("≥ 90%", "of legit ₹10k+ transfers pass with no delay (a blanket 1-hour rule delays 100%)"),
            ("< 50 ms", "p95 decision latency, well inside UPI's 15 s window")]
    y = 4.2
    for i, (big, small) in enumerate(mets):
        b, tf = box(s, 8.88, y, 3.97, 0.8, f"Metric {i+1}", fill=WHITE, line=ICE, radius=0.1, pad=0.12, anchor=MSO_ANCHOR.MIDDLE)
        tf.margin_left = Inches(1.3)
        add_par(tf, [(small, 10.5, False, TEXT)], first=True)
        tb, ttf = textbox(s, 8.98, y, 1.2, 0.8, f"Metric {i+1} value", anchor=MSO_ANCHOR.MIDDLE)
        add_par(ttf, [(big, 20, True, GREEN, False, HEAD)], first=True, align=PP_ALIGN.CENTER)
        y += 0.88
    tb, tf = textbox(s, 8.88, 6.85, 3.97, 0.35, "Metric note")
    add_par(tf, [("Targets, measured live on the dashboard against held-out synthetic data.", 10, False, MUTED, True)], first=True)
    notes(s, "What we'll actually build in the hack: a live authenticate API on a free host, the full risk engine, all four response levels working, including a real passkey fingerprint check and an n8n plus Telegram loop where a family member can cancel a held payment, a dashboard, and a replay simulator comparing us with RBI's blanket delay. All on free tools, zero running cost. "
             "We're honest about the risks. Our data is synthetic, so we add hard negatives, report metrics per attack type and sanity-check on public datasets. "
             "Call and screen-share state needs a mobile SDK, so missing signals count as unknown, never safe. "
             "False positives hurt real people, so we only block at very high confidence and keep challenges under five percent. "
             "And there's privacy: we store derived features only, under the DPDP Act. "
             "Success means catching at least 80 percent of scam-type fraud while challenging at most 5 percent of honest payments, letting 90 percent of honest big transfers through with no delay, and deciding in under 50 milliseconds.")

def main(src, out):
    prs = Presentation(src)
    sl = list(prs.slides)
    slide1(sl[0]); slide2(sl[1]); slide3(sl[2]); slide4(sl[3]); slide5(sl[4])
    # tidy "SLIDE X OF 5" box so it stays on the canvas
    for s in sl:
        for sh in s.shapes:
            if sh.name == "Text 1":
                sh.left = Inches(11.3); sh.width = Inches(1.55)
                sh.text_frame.paragraphs[0].alignment = PP_ALIGN.RIGHT
    prs.save(out)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
