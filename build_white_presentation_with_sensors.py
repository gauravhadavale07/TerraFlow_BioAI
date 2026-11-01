"""
TerraFlow BioAI - Major Project Official Presentation Generator
Clean White / Light-Canvas Academic Style matching TerraFlow_BioAI_Final_Presentation.pptx
Includes Dedicated Multi-Modal Sensor Suite Slide (NEO-6M GPS, Float Switch, etc.)
and Native Detailed Multi-Tier System Architecture Diagram.

Academic Year: 2026-2027
Department of Electronics & Telecommunication Engineering, SPIT Mumbai
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# ── Color Palette (Clean White / Light-Slate Academic Deck) ───────────────────
BG_CANVAS      = RGBColor(248, 250, 252)   # #F8FAFC Crisp Slate Canvas
CARD_BG        = RGBColor(255, 255, 255)   # #FFFFFF Pure White Card
CARD_BORDER    = RGBColor(226, 232, 240)   # #E2E8F0 Subtle Clean Border
CARD_HOVER     = RGBColor(241, 245, 249)   # #F1F5F9 Slate Tint
TEXT_HEAD      = RGBColor(15, 23, 42)      # #0F172A Deep Navy / Slate 900
TEXT_BODY      = RGBColor(51, 65, 85)      # #334155 Slate 700 (Very readable)
TEXT_MUTED     = RGBColor(100, 116, 139)   # #64748B Slate 500
ACCENT_BLUE    = RGBColor(2, 132, 199)     # #0284C7 Sky/Royal Blue
ACCENT_NAVY    = RGBColor(30, 58, 138)     # #1E3A8A Classic Academic Navy
ACCENT_GREEN   = RGBColor(16, 185, 129)    # #10B981 Emerald Green
ACCENT_AMBER   = RGBColor(217, 119, 6)     # #D97706 Warm Amber
ACCENT_RED     = RGBColor(225, 29, 72)     # #E11D48 Rose Red
ACCENT_PURPLE  = RGBColor(124, 58, 237)    # #7C3AED Royal Purple
TAG_BG_BLUE    = RGBColor(224, 242, 254)   # #E0F2FE Light blue badge
TAG_BG_GREEN   = RGBColor(209, 250, 229)   # #D1FAE5 Light green badge

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPIT_LOGO_PATH = os.path.join(BASE_DIR, "extracted_assets", "spit_logo_0.png")


def set_canvas_bg(slide):
    """Sets a clean, modern off-white canvas background."""
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_CANVAS
    bg.line.fill.background()
    return bg


def add_slide_header(slide, slide_num, category, title, subtitle):
    """Adds a human-designed, crystal clear header with large readable fonts."""
    # Top Category Pill / Tracker
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.32), Inches(4.2), Inches(0.32))
    badge.fill.solid()
    badge.fill.fore_color.rgb = TAG_BG_BLUE
    badge.line.fill.background()

    tf_b = badge.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0
    p_b = tf_b.paragraphs[0]
    num_str = f"0{slide_num}" if slide_num < 10 else f"{slide_num}"
    p_b.text = f"SLIDE {num_str}  •  {category.upper()}"
    p_b.font.name = "Segoe UI"
    p_b.font.size = Pt(9.5)
    p_b.font.bold = True
    p_b.font.color.rgb = ACCENT_NAVY
    p_b.alignment = PP_ALIGN.CENTER

    # Title
    t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(10.5), Inches(0.55))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title
    p_t.font.name = "Segoe UI"
    p_t.font.size = Pt(23)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_HEAD

    # Subtitle
    s_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.24), Inches(10.5), Inches(0.35))
    tf_s = s_box.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = 0
    p_s = tf_s.paragraphs[0]
    p_s.text = subtitle
    p_s.font.name = "Segoe UI"
    p_s.font.size = Pt(12)
    p_s.font.color.rgb = TEXT_MUTED

    # Header Divider Line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.65), Inches(11.733), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = CARD_BORDER
    line.line.fill.background()

    # Small SPIT Logo on top-right
    if os.path.exists(SPIT_LOGO_PATH):
        try:
            slide.shapes.add_picture(SPIT_LOGO_PATH, Inches(11.8), Inches(0.32), height=Inches(0.95))
        except Exception:
            pass


def create_white_card(slide, left, top, width, height, top_accent=None, border_color=CARD_BORDER):
    """Creates a clean white card container with high visual depth and readability."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = border_color
    card.line.width = Pt(1.5)

    if top_accent:
        stripe = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(0.06))
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = top_accent
        stripe.line.fill.background()

    return card


def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Grand SPIT Academic Presentation)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s1)

    # Top Accent Ribbon
    ribbon = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    ribbon.fill.solid()
    ribbon.fill.fore_color.rgb = ACCENT_NAVY
    ribbon.line.fill.background()

    # SPIT Official Maroon Logo - Prominent on Title Page
    if os.path.exists(SPIT_LOGO_PATH):
        try:
            s1.shapes.add_picture(SPIT_LOGO_PATH, Inches(0.8), Inches(0.55), height=Inches(1.35))
        except Exception as e:
            print(f"Error loading logo: {e}")

    # College Header
    col_box = s1.shapes.add_textbox(Inches(2.4), Inches(0.55), Inches(10.0), Inches(1.3))
    tf_c = col_box.text_frame
    tf_c.word_wrap = True

    p_c1 = tf_c.paragraphs[0]
    p_c1.text = "BHARATIYA VIDYA BHAVAN'S SARDAR PATEL INSTITUTE OF TECHNOLOGY"
    p_c1.font.name = "Segoe UI"
    p_c1.font.size = Pt(13.5)
    p_c1.font.bold = True
    p_c1.font.color.rgb = ACCENT_NAVY

    p_c2 = tf_c.add_paragraph()
    p_c2.text = "Autonomous Institute Affiliated to University of Mumbai  |  Dept. of Electronics & Telecommunication Eng."
    p_c2.font.name = "Segoe UI"
    p_c2.font.size = Pt(11)
    p_c2.font.color.rgb = TEXT_MUTED

    p_c3 = tf_c.add_paragraph()
    p_c3.text = "B.Tech Final Major Project Presentation  •  Academic Year 2026–2027"
    p_c3.font.name = "Segoe UI"
    p_c3.font.size = Pt(11)
    p_c3.font.bold = True
    p_c3.font.color.rgb = ACCENT_BLUE

    # Hero Card for Project Title
    create_white_card(s1, Inches(0.8), Inches(2.1), Inches(11.733), Inches(2.6), top_accent=ACCENT_NAVY)

    hb = s1.shapes.add_textbox(Inches(1.1), Inches(2.25), Inches(11.1), Inches(2.3))
    tf_h = hb.text_frame
    tf_h.word_wrap = True

    p_tag = tf_h.paragraphs[0]
    p_tag.text = "CYBER-PHYSICAL EDGE-IOT  •  PRECISION IRRIGATION  •  DECISION SUPPORT"
    p_tag.font.name = "Segoe UI"
    p_tag.font.size = Pt(11)
    p_tag.font.bold = True
    p_tag.font.color.rgb = ACCENT_BLUE

    p_main = tf_h.add_paragraph()
    p_main.text = "TerraFlow BioAI: A Zone-Aware Edge-IoT Architecture\nfor Closed-Loop Precision Irrigation & Agro-Advisory"
    p_main.font.name = "Segoe UI"
    p_main.font.size = Pt(25)
    p_main.font.bold = True
    p_main.font.color.rgb = TEXT_HEAD
    p_main.space_before = Pt(6)

    p_subt = tf_h.add_paragraph()
    p_subt.text = "Deterministic Edge Safety (STM32 + ESP32), Volumetric Pulse-Flow Actuation & Evidence-Driven Machine Learning"
    p_subt.font.name = "Segoe UI"
    p_subt.font.size = Pt(13)
    p_subt.font.color.rgb = TEXT_BODY
    p_subt.space_before = Pt(8)

    # Team Members Card (Left)
    create_white_card(s1, Inches(0.8), Inches(4.95), Inches(7.6), Inches(2.05), top_accent=ACCENT_BLUE)

    t_box = s1.shapes.add_textbox(Inches(1.05), Inches(5.1), Inches(7.1), Inches(1.8))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True

    p_th = tf_t.paragraphs[0]
    p_th.text = "PROJECT TEAM MEMBERS (EXTC DEPT.)"
    p_th.font.name = "Segoe UI"
    p_th.font.size = Pt(11)
    p_th.font.bold = True
    p_th.font.color.rgb = ACCENT_BLUE

    team = [
        ("Shreyash A Jadhav", "2023200055", "Safety Interlocks, Embedded Control & Hardware Testing"),
        ("Gaurav Hadavale", "2023200054", "ML Pipeline, Firmware Architecture & Sensor Integration"),
        ("Atharv Bodake", "2023200028", "IoT Gateway, Cloud Telemetry & React Dashboard UI")
    ]
    for name, uid, work in team:
        p_tm = tf_t.add_paragraph()
        p_tm.text = f"•  {name}  —  UID: {uid}   ({work})"
        p_tm.font.name = "Segoe UI"
        p_tm.font.size = Pt(11)
        p_tm.font.bold = True
        p_tm.font.color.rgb = TEXT_HEAD
        p_tm.space_before = Pt(5)

    # Faculty Mentor Card (Right)
    create_white_card(s1, Inches(8.65), Inches(4.95), Inches(3.88), Inches(2.05), top_accent=ACCENT_NAVY)

    g_box = s1.shapes.add_textbox(Inches(8.9), Inches(5.1), Inches(3.4), Inches(1.8))
    tf_g = g_box.text_frame
    tf_g.word_wrap = True

    p_gh = tf_g.paragraphs[0]
    p_gh.text = "PROJECT MENTOR"
    p_gh.font.name = "Segoe UI"
    p_gh.font.size = Pt(11)
    p_gh.font.bold = True
    p_gh.font.color.rgb = ACCENT_NAVY

    p_gn = tf_g.add_paragraph()
    p_gn.text = "Prof. Milind Paraye"
    p_gn.font.name = "Segoe UI"
    p_gn.font.size = Pt(16)
    p_gn.font.bold = True
    p_gn.font.color.rgb = TEXT_HEAD
    p_gn.space_before = Pt(4)

    p_gd = tf_g.add_paragraph()
    p_gd.text = "Assistant Professor\nDept. of Electronics & Telecommunication Eng.\nSardar Patel Institute of Technology (SPIT)"
    p_gd.font.name = "Segoe UI"
    p_gd.font.size = Pt(11)
    p_gd.font.color.rgb = TEXT_MUTED
    p_gd.space_before = Pt(4)

    # =========================================================================
    # SLIDE 2: THE PROBLEM (What Farmers Face in the Field)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s2)
    add_slide_header(s2, 2, "Problem Statement",
                     "The Problem: What Farmers Face in the Field",
                     "Real-world challenges in irrigation scheduling, soil visibility, hardcoded thresholds, and field usability")

    # 4 Problem Cards (2x2 Grid)
    c_w = Inches(5.72)
    c_h = Inches(2.30)
    x1 = Inches(0.8)
    x2 = Inches(6.81)
    y1 = Inches(1.85)
    y2 = Inches(4.35)

    problems = [
        (x1, y1, "Schedule-Based Irrigation", ACCENT_BLUE,
         "Farmers water crops on fixed schedules or blind timers, not on actual soil demand — leading to overwatering or drought stress, root hypoxia, and immense groundwater waste."),

        (x2, y1, "No Real-Time Soil & Water Data", ACCENT_AMBER,
         "Zero visibility into root-zone soil moisture, temperature, or water salinity (TDS). Farming decisions rely purely on guesswork, surface feel, and manual trial-and-error."),

        (x1, y2, "Rigid Hardcoded Calibration Flaws", ACCENT_RED,
         "Existing IoT setups rely on fragile, hardcoded sensor thresholds (e.g. 'if ADC < 300: pump ON') that drift and fail across different soil textures. Farmers need an adaptive ML model that learns soil dynamics, not manual recalibration values."),

        (x2, y2, "Targeting Hardcore Farmers", ACCENT_GREEN,
         "Smallholder farmers in the field need a set-and-forget, autonomous closed-loop system. It must run deterministically on the edge without complex manual setup, app bloat, or dependence on continuous internet connectivity.")
    ]

    for px, py, ptitle, pcol, pdesc in problems:
        create_white_card(s2, px, py, c_w, c_h, top_accent=pcol)

        tb_p = s2.shapes.add_textbox(px + Inches(0.3), py + Inches(0.18), c_w - Inches(0.6), c_h - Inches(0.3))
        tf_p = tb_p.text_frame
        tf_p.word_wrap = True

        p_pt = tf_p.paragraphs[0]
        p_pt.text = ptitle
        p_pt.font.name = "Segoe UI"
        p_pt.font.size = Pt(16)
        p_pt.font.bold = True
        p_pt.font.color.rgb = pcol

        p_pd = tf_p.add_paragraph()
        p_pd.text = pdesc
        p_pd.font.name = "Segoe UI"
        p_pd.font.size = Pt(11.5)
        p_pd.font.color.rgb = TEXT_BODY
        p_pd.space_before = Pt(8)

    # Bottom Core Objective Summary
    bot_card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.75), Inches(11.733), Inches(0.55))
    bot_card.fill.solid()
    bot_card.fill.fore_color.rgb = TAG_BG_GREEN
    bot_card.line.fill.background()

    tb_b = s2.shapes.add_textbox(Inches(1.0), Inches(6.78), Inches(11.3), Inches(0.5))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True
    p_b = tf_b.paragraphs[0]
    p_b.text = "CORE TAKEAWAY: TerraFlow BioAI solves these challenges through deterministic bare-metal edge safety, volumetric pulse-flow control, and sensor-aligned machine learning tailored for real-world farming conditions."
    p_b.font.name = "Segoe UI"
    p_b.font.size = Pt(11)
    p_b.font.bold = True
    p_b.font.color.rgb = RGBColor(6, 95, 70)

    # =========================================================================
    # SLIDE 3: DETAILED SYSTEM ARCHITECTURE (The Master 12-Module Multi-Tier Diagram)
    # Rendered natively in clean white style!
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s3)
    add_slide_header(s3, 3, "System Architecture",
                     "TerraFlow BioAI: System Architecture & Control Flow",
                     "Closed-loop precision irrigation, multi-parametric agro-advisory, and deterministic edge safety (Zone Z01 | Node TF01)")

    # ── SECTION 1: PHASE 1-2 (FIELD SENSING, EMBEDDED CONTROL & CLOUD DATA) ───
    sec1_y = Inches(1.72)
    sec1_h = Inches(1.68)

    s1_cards = [
        (Inches(0.60), Inches(2.28), "1. FIELD SENSORS (TF01)", ACCENT_BLUE, [
            "• Soil Moisture: Capacitive (0–3.3V)",
            "• Soil Temp: DS18B20 (-55°C to 125°C)",
            "• Water Quality: TDS (0–1000 ppm)",
            "• Climate: BME280 (Temp, RH, Press)",
            "• Flow Sensor: YF-S201 Pulse Meter"
        ]),
        (Inches(2.98), Inches(2.35), "2. STM32 SAFETY AUTHORITY", ACCENT_NAVY, [
            "• ARM Cortex-M3 @ 72 MHz (Bare-metal)",
            "• On-Chip Signal Filtering & ADC Sanity",
            "• 5-State FSM: IDLE→SENSE→EVAL→ACT",
            "• Watchdog (IWDG) + Max Runtime Guard",
            "• Sole Actuator: Direct MOSFET gate pin"
        ]),
        (Inches(5.43), Inches(2.15), "3. ESP32 CONNECTIVITY", ACCENT_BLUE, [
            "• UART2 Bidirectional link (115200 baud)",
            "• Wi-Fi 802.11 b/g/n + HTTPS POST",
            "• Auto-reconnect with exp. backoff",
            "• Telemetry buffer during network drop",
            "• NTP time sync & advisory forwarding"
        ]),
        (Inches(7.68), Inches(2.15), "4. NODE.JS BACKEND API", ACCENT_GREEN, [
            "• Ingestion API: validates device JSON",
            "• Computes live WSI, VPD, & DRI indices",
            "• Microservice bridge to Python ML API",
            "• Zone & crop profile management",
            "• Serves real-time telemetry to React"
        ]),
        (Inches(9.93), Inches(2.80), "5. SUPABASE DATA LAYER", ACCENT_PURPLE, [
            "• Operational DB: sensor series, pump logs, faults",
            "• Agronomic Knowledge Base: 80+ FAO-56 rules",
            "• 4 Soil Profiles: Field Capacity & PWP limits",
            "• Soil Health Cards: Ingested certified lab NPK",
            "• Calibration & threshold reference tables"
        ])
    ]

    for cl, cw, ct, col, cpts in s1_cards:
        create_white_card(s3, cl, sec1_y, cw, sec1_h, top_accent=col)

        tb = s3.shapes.add_textbox(cl + Inches(0.08), sec1_y + Inches(0.05), cw - Inches(0.16), sec1_h - Inches(0.10))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = ct
        p_t.font.name = "Segoe UI"
        p_t.font.size = Pt(9.2)
        p_t.font.bold = True
        p_t.font.color.rgb = col

        for pt in cpts:
            p_p = tf.add_paragraph()
            p_p.text = pt
            p_p.font.name = "Segoe UI"
            p_p.font.size = Pt(7.6)
            p_p.font.color.rgb = TEXT_BODY
            p_p.space_before = Pt(1.0)

    # Connecting Arrows between Phase 1-2 Cards
    arrow_xs = [Inches(2.89), Inches(5.34), Inches(7.59), Inches(9.84)]
    for ax in arrow_xs:
        arr = s3.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, ax, sec1_y + Inches(0.65), Inches(0.08), Inches(0.18))
        arr.fill.solid()
        arr.fill.fore_color.rgb = ACCENT_BLUE
        arr.line.fill.background()

    # ── SECTION 2: PHASE 3 (SOFTWARE & DECISION INTELLIGENCE) ─────────────────
    sec2_y = Inches(3.48)
    sec2_h = Inches(1.60)

    s2_cards = [
        (Inches(0.60), Inches(3.40), "6. WEATHER & MICROCLIMATE CONTEXT", ACCENT_BLUE, [
            "• External Weather API: Forecast rain %, temp, humidity, wind, and ET0.",
            "• Local Measurement (TF01, BME280): Real-time field temp, RH, and pressure.",
            "• Dual-Stream Isolation: Maintained as separate channels (never averaged) to distinguish regional climate from microclimate canopy stress."
        ]),
        (Inches(4.12), Inches(3.75), "7. ML SUPPORT LAYER (Decision Support Only)", ACCENT_PURPLE, [
            "• 4 Validated Models: XGBoost & Random Forest (90.8% - 100% Accuracy).",
            "• Calibrated Features: In-situ moisture, rainfall context, crop Kc, and Soil Health Card lab NPK (no fabricated sensor claims).",
            "• Output: Advisory decision + confidence % + transparent reason codes (e.g. RUN:MOISTURE_LOW, SKIP:RAIN_CONTEXT).",
            "• Architectural Rule: ML advises; never has direct pump control authority."
        ]),
        (Inches(7.99), Inches(4.74), "8. SOFTWARE DECISION ENGINES (Backend Logic)", ACCENT_AMBER, [
            "• A. Irrigation Engine: Soil deficit + Crop Kc + Weather → Target Volume (Liters) + Reason Code (RUN:MOISTURE_LOW).",
            "• B. Crop Suitability Engine: Soil type + pH/EC + Season → Top 5 ranked crop recommendations with suitability %.",
            "• C. Fertilizer Advisory Engine: Soil NPK test deficit + stage → Exact commercial fertilizer grade (Urea for low N, DAP for low P, 10-26-26)."
        ])
    ]

    for cl, cw, ct, col, cpts in s2_cards:
        create_white_card(s3, cl, sec2_y, cw, sec2_h, top_accent=col)

        tb = s3.shapes.add_textbox(cl + Inches(0.10), sec2_y + Inches(0.05), cw - Inches(0.20), sec2_h - Inches(0.10))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = ct
        p_t.font.name = "Segoe UI"
        p_t.font.size = Pt(9.2)
        p_t.font.bold = True
        p_t.font.color.rgb = col

        for pt in cpts:
            p_p = tf.add_paragraph()
            p_p.text = pt
            p_p.font.name = "Segoe UI"
            p_p.font.size = Pt(7.8)
            p_p.font.color.rgb = TEXT_BODY
            p_p.space_before = Pt(1.2)

    # Connecting Arrows Phase 3
    arr2_xs = [Inches(4.02), Inches(7.89)]
    for ax in arr2_xs:
        arr = s3.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, ax, sec2_y + Inches(0.65), Inches(0.08), Inches(0.18))
        arr.fill.solid()
        arr.fill.fore_color.rgb = ACCENT_PURPLE
        arr.line.fill.background()

    # ── SECTION 3: PHASE 4 (ACTUATION, MONITORING & VERIFICATION) ─────────────
    sec3_y = Inches(5.16)
    sec3_h = Inches(1.80)

    s3_cards = [
        (Inches(0.60), Inches(4.55), "9. STM32 CLOSED-LOOP CONTROL LOGIC (\"Cloud Advises, STM32 Decides\")", ACCENT_NAVY, [
            "1. Sense & Filter: Read ADC, apply 1-D noise smoothing, verify data validity.",
            "2. Safety Checks: Verify safe mode, watchdog status, and resting window.",
            "3. Trigger Evaluation: Calibrated moisture drops below threshold (<35%).",
            "4. Volumetric Budgeting: Set target liters from FAO-56 depletion: V = Δθ × A × Zr.",
            "5. Pulse-Flow Cutoff: Terminate pump actuation when pulse count reaches target liters.",
            "6. Verification: 3 min post-shutoff check confirms wetting front (Δθ ≥ +18%)."
        ]),
        (Inches(5.27), Inches(3.40), "10. FIELD ACTUATION CHAIN (Physical Hardware)", ACCENT_AMBER, [
            "• STM32 GPIO (PB0): 3.3V logic trigger output.",
            "• MOSFET Driver: IRLZ44N N-channel gate + 10kΩ pull-down resistor.",
            "• DC Pump: 12V DC water pump with 1N4007 flyback diode protection.",
            "• YF-S201 Flow Sensor: Measures delivered volume (L) in real time.",
            "• Closed-Loop Feedback: Water to soil → Moisture sensor verifies percolation."
        ]),
        (Inches(8.79), Inches(3.94), "11 & 12. REACT DASHBOARD & KEY OUTCOMES", ACCENT_GREEN, [
            "• React Console: Real-time gauges, WSI/VPD curves, ML prediction card, volumetric progress bar, and academic simulation mode.",
            "• Key Outcomes Achieved:",
            "  ✓ ~38% Water Conserved (FAO-56 volumetric vs timer)",
            "  ✓ 100% Fail-Safe Safety (Zero runaway pump risk)",
            "  ✓ Transparent Reason Codes on every decision",
            "  ✓ Complete Offline Autonomy on bare-metal STM32"
        ])
    ]

    for cl, cw, ct, col, cpts in s3_cards:
        create_white_card(s3, cl, sec3_y, cw, sec3_h, top_accent=col)

        tb = s3.shapes.add_textbox(cl + Inches(0.10), sec3_y + Inches(0.04), cw - Inches(0.20), sec3_h - Inches(0.08))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = ct
        p_t.font.name = "Segoe UI"
        p_t.font.size = Pt(9.2)
        p_t.font.bold = True
        p_t.font.color.rgb = col

        for pt in cpts:
            p_p = tf.add_paragraph()
            p_p.text = pt
            p_p.font.name = "Segoe UI"
            p_p.font.size = Pt(7.6)
            p_p.font.color.rgb = TEXT_BODY
            p_p.space_before = Pt(1.0)

    # ── BOTTOM LEGEND & DATA FLOW STRIPE ──────────────────────────────────────
    leg_y = Inches(7.04)
    leg_box = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.60), leg_y, Inches(12.133), Inches(0.25))
    leg_box.fill.solid()
    leg_box.fill.fore_color.rgb = TAG_BG_GREEN
    leg_box.line.fill.background()

    tf_leg = leg_box.text_frame
    tf_leg.word_wrap = True
    p_leg = tf_leg.paragraphs[0]
    p_leg.text = "DATA FLOW:  [1] Sensors → STM32 (ADC/I2C)  |  [2] Telemetry → ESP32 (UART2)  |  [3] Cloud → Backend & Supabase (HTTPS)  |  [4] Advice → STM32 Validates  |  [5] Feedback → Soil Infiltration"
    p_leg.font.name = "Segoe UI"
    p_leg.font.size = Pt(8.5)
    p_leg.font.bold = True
    p_leg.font.color.rgb = RGBColor(6, 95, 70)
    p_leg.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 4: DEDICATED SENSOR SUITE (User Explicitly Requested!)
    # Includes NEO-6M GPS, Float Switch Water Level, Capacitive Moisture, etc.
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s4)
    add_slide_header(s4, 4, "Sensor Architecture",
                     "Dedicated Multi-Modal Sensor Architecture",
                     "Physical transducer interfacing, measurement specifications, and agronomic roles across Zone Z01")

    # 7 Comprehensive Sensor Cards (4 on top row, 3 on bottom row)
    top_row_y = Inches(1.85)
    bot_row_y = Inches(4.35)
    card_w4 = Inches(2.78)
    card_h4 = Inches(2.30)
    card_w3 = Inches(3.75)
    card_h3 = Inches(2.35)

    top_sensors = [
        ("Capacitive Soil Moisture (v1.2)", "PA0 ADC1  •  0 to 3.3V Analog", ACCENT_BLUE,
         "Measures Soil Volumetric Water Content (0–100%). Capacitive design prevents electrolysis and galvanic corrosion, ensuring multi-season calibration stability. Primary closed-loop irrigation trigger."),

        ("DS18B20 Waterproof Temp", "PA4 GPIO  •  Dallas 1-Wire", ACCENT_NAVY,
         "Submersible stainless-steel probe measuring root-zone soil temperature (-55°C to +125°C, ±0.5°C). Provides thermal context for root metabolic activity and dynamic temperature compensation for the TDS sensor."),

        ("Analog Water TDS Sensor (v1.0)", "PA1 ADC2  •  0 to 2.3V Analog", ACCENT_AMBER,
         "Monitors Total Dissolved Solids (0–1000 ppm) in irrigation water. Evaluates salinity hazard to protect crop roots from osmotic shock. (Note: strictly monitors water quality, not soil NPK)."),

        ("BME280 Environmental Microclimate", "PB6/PB7  •  Hardware I2C Bus", ACCENT_GREEN,
         "3-in-1 sensor measuring Ambient Temperature (°C), Relative Humidity (%RH), and Barometric Pressure (hPa). Enables precise Vapor Pressure Deficit (VPD) and FAO-56 evapotranspiration modeling.")
    ]

    for idx, (sname, spin, scol, sdesc) in enumerate(top_sensors):
        sx = Inches(0.8 + idx * 2.98)
        create_white_card(s4, sx, top_row_y, card_w4, card_h4, top_accent=scol)

        tb = s4.shapes.add_textbox(sx + Inches(0.18), top_row_y + Inches(0.12), card_w4 - Inches(0.36), card_h4 - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True

        p_h = tf.paragraphs[0]
        p_h.text = sname
        p_h.font.name = "Segoe UI"
        p_h.font.size = Pt(12)
        p_h.font.bold = True
        p_h.font.color.rgb = scol

        p_pin = tf.add_paragraph()
        p_pin.text = spin
        p_pin.font.name = "Segoe UI"
        p_pin.font.size = Pt(9.5)
        p_pin.font.bold = True
        p_pin.font.color.rgb = TEXT_MUTED
        p_pin.space_before = Pt(2)

        p_d = tf.add_paragraph()
        p_d.text = sdesc
        p_d.font.name = "Segoe UI"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = TEXT_BODY
        p_d.space_before = Pt(6)

    bot_sensors = [
        ("YF-S201 Pulse Flow Meter", "PA2 EXTI  •  Hardware Interrupt", ACCENT_AMBER,
         "Hall-effect turbine sensor measuring delivered irrigation volume (1–30 L/min, 450 pulses/L). Replaces crude timers with exact volumetric dosing (V = Δθ × Area × Depth), enabling closed-loop water shutoff."),

        ("NEO-6M GPS Receiver Module", "USART3  •  9600 Baud Serial", ACCENT_BLUE,
         "Acquires field Latitude, Longitude, and Altitude. Automatically aligns farm plot coordinates with Open-Meteo regional weather forecasting, solar zenith angle modeling, and spatial multi-zone geo-tagging."),

        ("Magnetic Float Switch (Tank Level)", "PA3 GPIO  •  Digital Input (Pull-Up)", ACCENT_RED,
         "Rugged reed-switch float sensor monitoring water reservoir levels. Enforces a hardware safety gate: immediately inhibits pump firing when tank level drops below safe threshold, preventing dry-run pump burnout.")
    ]

    for idx, (sname, spin, scol, sdesc) in enumerate(bot_sensors):
        sx = Inches(0.8 + idx * 3.99)
        create_white_card(s4, sx, bot_row_y, card_w3, card_h3, top_accent=scol)

        tb = s4.shapes.add_textbox(sx + Inches(0.20), bot_row_y + Inches(0.12), card_w3 - Inches(0.40), card_h3 - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True

        p_h = tf.paragraphs[0]
        p_h.text = sname
        p_h.font.name = "Segoe UI"
        p_h.font.size = Pt(12.5)
        p_h.font.bold = True
        p_h.font.color.rgb = scol

        p_pin = tf.add_paragraph()
        p_pin.text = spin
        p_pin.font.name = "Segoe UI"
        p_pin.font.size = Pt(9.5)
        p_pin.font.bold = True
        p_pin.font.color.rgb = TEXT_MUTED
        p_pin.space_before = Pt(2)

        p_d = tf.add_paragraph()
        p_d.text = sdesc
        p_d.font.name = "Segoe UI"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = TEXT_BODY
        p_d.space_before = Pt(6)

    # Bottom Sensor Summary
    bot_s_card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.80), Inches(11.733), Inches(0.50))
    bot_s_card.fill.solid()
    bot_s_card.fill.fore_color.rgb = TAG_BG_BLUE
    bot_s_card.line.fill.background()

    tb_bs = s4.shapes.add_textbox(Inches(1.0), Inches(6.82), Inches(11.3), Inches(0.45))
    tf_bs = tb_bs.text_frame
    tf_bs.word_wrap = True
    p_bs = tf_bs.paragraphs[0]
    p_bs.text = "INTEGRATION HIGHLIGHT: All 7 transducers interface natively with the STM32F103C8T6 bare-metal firmware via isolated analog channels, I2C, 1-Wire, and hardware interrupts with zero inter-sensor bus cross-talk."
    p_bs.font.name = "Segoe UI"
    p_bs.font.size = Pt(10.5)
    p_bs.font.bold = True
    p_bs.font.color.rgb = ACCENT_NAVY

    # =========================================================================
    # SLIDE 5: MASTER SYSTEM ARCHITECTURE BLUEPRINT (The AI Architecture Diagram)
    # Added after Slide 4, with NO explanatory text on the side
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s5)
    add_slide_header(s5, 5, "System Architecture Blueprint",
                     "TerraFlow BioAI: End-to-End System Architecture",
                     "Master cyber-physical data pipelines, multi-parametric decision engines, and physical actuation loops")

    arch_img_path = os.path.join(BASE_DIR, "extracted_assets", "report_img250.jpg")
    if not os.path.exists(arch_img_path):
        arch_img_path = os.path.join(BASE_DIR, "AdobeExpressPhotos_a369f03e02f64518807f918bd2532900_CopyEdited.png")

    img_h = Inches(5.60)
    img_w = img_h * (1672.0 / 941.0)
    card_w = img_w + Inches(0.30)
    card_h = img_h + Inches(0.20)
    card_x = (Inches(13.333) - card_w) / 2
    card_y = Inches(1.48)

    create_white_card(s5, card_x, card_y, card_w, card_h, top_accent=ACCENT_NAVY)

    if os.path.exists(arch_img_path):
        s5.shapes.add_picture(arch_img_path, card_x + Inches(0.15), card_y + Inches(0.10), height=img_h)

    # =========================================================================
    # SLIDE 6: EMBEDDED HARDWARE DESIGN (STM32 & ESP32 Dual-Controller)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s6)
    add_slide_header(s6, 6, "Embedded Hardware Design",
                     "Dual-Controller Hardware Topology: STM32 & ESP32",
                     "Physical division of responsibilities: Bare-metal deterministic safety vs high-speed wireless connectivity")

    hw_w = Inches(5.72)
    hw_h = Inches(3.60)

    # Left Column: STM32 (Local Safety Authority)
    add_left = Inches(0.8)
    create_white_card(s6, add_left, Inches(1.85), hw_w, hw_h, top_accent=ACCENT_NAVY)

    tb_s6_1 = s6.shapes.add_textbox(add_left + Inches(0.3), Inches(1.95), hw_w - Inches(0.6), hw_h - Inches(0.2))
    tf_s6_1 = tb_s6_1.text_frame
    tf_s6_1.word_wrap = True

    p_stm_tag = tf_s6_1.paragraphs[0]
    p_stm_tag.text = "LOCAL SAFETY & ACTUATION AUTHORITY"
    p_stm_tag.font.name = "Segoe UI"
    p_stm_tag.font.size = Pt(11)
    p_stm_tag.font.bold = True
    p_stm_tag.font.color.rgb = ACCENT_NAVY

    p_stm_h = tf_s6_1.add_paragraph()
    p_stm_h.text = "STM32F103C8T6 (ARM Cortex-M3 @ 72 MHz)"
    p_stm_h.font.name = "Segoe UI"
    p_stm_h.font.size = Pt(15)
    p_stm_h.font.bold = True
    p_stm_h.font.color.rgb = TEXT_HEAD
    p_stm_h.space_before = Pt(2)

    stm_features = [
        ("Sole Pump Actuation Authority:", "Directly drives the IRLZ44N MOSFET pump gate. The cloud never has physical control of the pump pin."),
        ("Direct Sensor Acquisition:", "Reads BME280 via I2C (PB6/PB7), Soil Moisture on ADC1 (PA0), and TDS Sensor on ADC2 (PA1)."),
        ("On-Chip Signal Filtering:", "Lightweight noise smoothing in firmware eliminates electrical pump noise and air-pocket fluctuations."),
        ("Pulse-Flow Volumetric Integration:", "Hardware interrupt counts flow meter pulses; cuts off pump when target volume (Liters) is delivered."),
        ("Deterministic Safety Watchdog (IWDG):", "180s hard timeout and float switch interlock prevent dry-run damage and over-watering.")
    ]
    for lbl, desc in stm_features:
        p_pt = tf_s6_1.add_paragraph()
        p_pt.text = f"•  {lbl} "
        p_pt.font.name = "Segoe UI"
        p_pt.font.size = Pt(11)
        p_pt.font.bold = True
        p_pt.font.color.rgb = TEXT_HEAD
        p_pt.space_before = Pt(4)

        run = p_pt.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_BODY

    # Right Column: ESP32 (Wi-Fi & Cloud Gateway)
    esp_left = Inches(6.81)
    create_white_card(s6, esp_left, Inches(1.85), hw_w, hw_h, top_accent=ACCENT_BLUE)

    tb_s6_2 = s6.shapes.add_textbox(esp_left + Inches(0.3), Inches(1.95), hw_w - Inches(0.6), hw_h - Inches(0.2))
    tf_s6_2 = tb_s6_2.text_frame
    tf_s6_2.word_wrap = True

    p_esp_tag = tf_s6_2.paragraphs[0]
    p_esp_tag.text = "IOT TELEMETRY & CLOUD GATEWAY"
    p_esp_tag.font.name = "Segoe UI"
    p_esp_tag.font.size = Pt(11)
    p_esp_tag.font.bold = True
    p_esp_tag.font.color.rgb = ACCENT_BLUE

    p_esp_h = tf_s6_2.add_paragraph()
    p_esp_h.text = "ESP32 DevKit (Dual-Core Tensilica @ 240 MHz)"
    p_esp_h.font.name = "Segoe UI"
    p_esp_h.font.size = Pt(15)
    p_esp_h.font.bold = True
    p_esp_h.font.color.rgb = TEXT_HEAD
    p_esp_h.space_before = Pt(2)

    esp_features = [
        ("High-Speed UART2 Link:", "Receives preprocessed sensor packets from STM32 at 115200 baud with packet verification."),
        ("Wi-Fi Ingestion & Reconnect:", "Handles 802.11 b/g/n connectivity with automatic exponential backoff retry on dropouts."),
        ("REST Telemetry Dispatch:", "Packages sensor data into JSON and sends HTTPS POST requests to Supabase and Python ML server."),
        ("Advisory Packet Forwarding:", "Receives ML recommendations (decision, confidence, reason codes) and relays them to STM32."),
        ("Fail-Safe Offline Isolation:", "If Wi-Fi drops, ESP32 buffers data; the STM32 autonomously continues local irrigation safely.")
    ]
    for lbl, desc in esp_features:
        p_pt = tf_s6_2.add_paragraph()
        p_pt.text = f"•  {lbl} "
        p_pt.font.name = "Segoe UI"
        p_pt.font.size = Pt(11)
        p_pt.font.bold = True
        p_pt.font.color.rgb = TEXT_HEAD
        p_pt.space_before = Pt(4)

        run = p_pt.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_BODY

    # Bottom Full-Width Card: Power Architecture & MOSFET Circuit
    create_white_card(s6, Inches(0.8), Inches(5.60), Inches(11.733), Inches(1.50), top_accent=ACCENT_GREEN)

    tb_pa = s6.shapes.add_textbox(Inches(1.05), Inches(5.70), Inches(11.2), Inches(0.3))
    tf_pa = tb_pa.text_frame
    p_pah = tf_pa.paragraphs[0]
    p_pah.text = "POWER ARCHITECTURE & SOLID-STATE ACTUATION CIRCUIT"
    p_pah.font.name = "Segoe UI"
    p_pah.font.size = Pt(11)
    p_pah.font.bold = True
    p_pah.font.color.rgb = ACCENT_GREEN

    pw_stages = [
        ("5V 2A Main Supply", "Wall Adapter / Solar Battery", Inches(1.05)),
        ("LM2596 Step-Down", "High-efficiency DC-DC Buck", Inches(3.85)),
        ("3.3V Regulated Rail", "Powering STM32, ESP32 & Sensors", Inches(6.65)),
        ("IRLZ44N MOSFET Driver", "220Ω Gate + 1N4007 Diode + 12V Pump", Inches(9.45))
    ]
    for i, (ptext, psub, px) in enumerate(pw_stages):
        p_blk = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px, Inches(6.05), Inches(2.45), Inches(0.85))
        p_blk.fill.solid()
        p_blk.fill.fore_color.rgb = CARD_HOVER
        p_blk.line.color.rgb = CARD_BORDER

        tf_pb = p_blk.text_frame
        tf_pb.word_wrap = True
        p_ptx = tf_pb.paragraphs[0]
        p_ptx.text = ptext
        p_ptx.font.name = "Segoe UI"
        p_ptx.font.size = Pt(11)
        p_ptx.font.bold = True
        p_ptx.font.color.rgb = TEXT_HEAD
        p_ptx.alignment = PP_ALIGN.CENTER

        p_sub = tf_pb.add_paragraph()
        p_sub.text = psub
        p_sub.font.name = "Segoe UI"
        p_sub.font.size = Pt(9)
        p_sub.font.color.rgb = TEXT_MUTED
        p_sub.alignment = PP_ALIGN.CENTER
        p_sub.space_before = Pt(2)

        if i < 3:
            arr_px = px + Inches(2.50)
            arr_p = s6.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, arr_px, Inches(6.35), Inches(0.20), Inches(0.20))
            arr_p.fill.solid()
            arr_p.fill.fore_color.rgb = ACCENT_BLUE
            arr_p.line.fill.background()

    # =========================================================================
    # SLIDE 7: MACHINE LEARNING INTELLIGENCE
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s7)
    add_slide_header(s7, 7, "Machine Learning Decision Support",
                     "Sensor-Aligned Machine Learning Intelligence",
                     "4 specialized models trained on sensor-compatible feature vectors and evaluated with 5-fold cross-validation")

    m_w = Inches(5.72)
    m_h = Inches(2.15)

    ml_models = [
        ("MODEL 1: PRIMARY DECISION ENGINE", "Irrigation Prediction", "XGBoost Classifier",
         "90.80% Test Acc | 92.00% 5-Fold CV", ACCENT_NAVY,
         "Filtered moisture (23.7%), Rainfall context (33.3%), Soil type (16.2%), Crop Kc (9.9%), Temp & RH (6.4%).",
         "Actionable IRRIGATE / NO_IRRIGATION decision with transparent reason codes (e.g. RUN:MOISTURE_LOW, SKIP:RAIN_CONTEXT)."),

        ("MODEL 2: PRE-PLANTING ADVISORY", "Crop Suitability Recommendation", "Random Forest (200 Trees)",
         "99.32% Test Acc | 99.45% 5-Fold CV", ACCENT_BLUE,
         "Soil profile texture, BME280 temperature, relative humidity, rainfall context, and Soil Health Card NPK.",
         "Evaluates 22 candidate crops and ranks the Top 5 recommended crops with percentage suitability confidence bars."),

        ("MODEL 3: NUTRIENT CORRECTION", "Fertilizer Prescription", "XGBoost Classifier",
         "100.0% Test Acc | 99.90% 5-Fold CV", ACCENT_GREEN,
         "Soil-test N, P, K status, target crop type, growth stage, and current soil moisture level.",
         "Prescribes exact commercial fertilizer grade (Urea for low N, DAP for low P, 10-26-26, 14-35-14) to correct deficits."),

        ("MODEL 4: SOIL CHARACTERIZATION", "Soil Type Classification", "Random Forest Classifier",
         "84.50% Test Acc | 84.80% 5-Fold CV", ACCENT_PURPLE,
         "Moisture retention dynamics, ambient climate patterns, and baseline electrical conductivity.",
         "Classifies soil texture into Black (Vertisol), Red (Alfisol), Alluvial, Sandy, Clayey, or Loamy.")
    ]

    positions_s7 = [
        (Inches(0.8), Inches(1.85)),
        (Inches(6.81), Inches(1.85)),
        (Inches(0.8), Inches(4.25)),
        (Inches(6.81), Inches(4.25))
    ]

    for (pos, (tag, name, algo, metrics, col, feat, out)) in zip(positions_s7, ml_models):
        x, y = pos
        create_white_card(s7, x, y, m_w, m_h, top_accent=col)

        tb_m = s7.shapes.add_textbox(x + Inches(0.25), y + Inches(0.12), m_w - Inches(0.5), m_h - Inches(0.25))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True

        p_t = tf_m.paragraphs[0]
        p_t.text = f"{tag}  •  {algo}"
        p_t.font.name = "Segoe UI"
        p_t.font.size = Pt(10)
        p_t.font.bold = True
        p_t.font.color.rgb = col

        p_n = tf_m.add_paragraph()
        p_n.text = f"{name}  —  {metrics}"
        p_n.font.name = "Segoe UI"
        p_n.font.size = Pt(13)
        p_n.font.bold = True
        p_n.font.color.rgb = TEXT_HEAD
        p_n.space_before = Pt(2)

        p_f = tf_m.add_paragraph()
        p_f.text = "Key Features: "
        p_f.font.name = "Segoe UI"
        p_f.font.size = Pt(10.5)
        p_f.font.bold = True
        p_f.font.color.rgb = TEXT_HEAD
        p_f.space_before = Pt(4)
        run_f = p_f.add_run()
        run_f.text = feat
        run_f.font.bold = False
        run_f.font.color.rgb = TEXT_BODY

        p_o = tf_m.add_paragraph()
        p_o.text = "Actionable Output: "
        p_o.font.name = "Segoe UI"
        p_o.font.size = Pt(10.5)
        p_o.font.bold = True
        p_o.font.color.rgb = TEXT_HEAD
        p_o.space_before = Pt(2)
        run_o = p_o.add_run()
        run_o.text = out
        run_o.font.bold = False
        run_o.font.color.rgb = TEXT_BODY

    # Bottom Agronomic Honesty Badge
    hon_card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.60), Inches(11.733), Inches(0.65))
    hon_card.fill.solid()
    hon_card.fill.fore_color.rgb = TAG_BG_GREEN
    hon_card.line.fill.background()

    tb_h = s7.shapes.add_textbox(Inches(1.0), Inches(6.63), Inches(11.3), Inches(0.58))
    tf_h = tb_h.text_frame
    tf_h.word_wrap = True
    p_h = tf_h.paragraphs[0]
    p_h.text = "CRUCIAL VIVA DEFENSE POINT: Our TDS Meter V1.0 measures water dissolved solids (salinity), NOT soil NPK. Nitrogen, Phosphorus, Potassium, and pH are derived from accredited Soil Health Card lab tests stored in Supabase (with ICAR regional baseline autofill)."
    p_h.font.name = "Segoe UI"
    p_h.font.size = Pt(10.5)
    p_h.font.bold = True
    p_h.font.color.rgb = RGBColor(6, 95, 70)

    # =========================================================================
    # SLIDE 8: WEB APPLICATION & OPERATOR CONSOLE
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s8)
    add_slide_header(s8, 8, "Web Application & Control Console",
                     "Real-Time React Dashboard & Closed-Loop UI",
                     "Connected operator console with live sensor gauges, zone configuration, AI advisory cards, and historical trends")

    cols_dash = [
        ("01. Live Telemetry & Agro-Indices", ACCENT_NAVY, [
            ("Moisture Gauge:", "Displays both filtered soil moisture % and raw ADC readings with colored risk zones."),
            ("BME280 Climate Cards:", "Real-time Ambient Temperature (°C), Humidity (%RH), and Barometric Pressure (hPa)."),
            ("Water Quality (TDS):", "Total dissolved solids (ppm) in irrigation water to warn of salinity hazards."),
            ("VPD Drying Stress:", "Vapor Pressure Deficit calculated from temp & humidity to assess crop transpiration demand.")
        ]),
        ("02. Zone Settings & AI Advisory", ACCENT_BLUE, [
            ("Zone Z01 Configuration:", "Dropdowns for Crop (Rice, Wheat, Tomato, Maize), Soil (Black, Red, Sandy), and Growth Stage."),
            ("Soil Test / NPK Autofill:", "Allows manual entry of Soil Health Card numbers or one-click ICAR regional baseline autofill."),
            ("Irrigation Decision Card:", "Displays IRRIGATE / NO_IRRIGATION with confidence % and explainable reason codes."),
            ("Fertilizer & Crop Cards:", "Prescribes fertilizer grade and displays Top 5 ranked crop suitability scores.")
        ]),
        ("03. Closed-Loop Actuation & Trends", ACCENT_GREEN, [
            ("Pump Actuation Badge:", "Animated status (RUNNING / IDLE) reflecting the real hardware MOSFET state."),
            ("Volumetric Progress Bar:", "Tracks Target Volume (L) vs Delivered Volume (L) measured from pulse flow meter."),
            ("Recharts Time-Series Graph:", "Plots real-time moisture vs temperature to visually prove moisture rise after irrigation."),
            ("Simulation Mode Switch:", "Allows offline demonstration of all 5 academic viva scenarios without hardware.")
        ])
    ]

    card_dw = Inches(3.75)
    card_dh = Inches(5.15)

    for i, (col_title, accent, bullets) in enumerate(cols_dash):
        left = Inches(0.8 + i * 3.99)
        create_white_card(s8, left, Inches(1.85), card_dw, card_dh, top_accent=accent)

        tb_d = s8.shapes.add_textbox(left + Inches(0.25), Inches(2.0), card_dw - Inches(0.5), card_dh - Inches(0.3))
        tf_d = tb_d.text_frame
        tf_d.word_wrap = True

        p_dt = tf_d.paragraphs[0]
        p_dt.text = col_title
        p_dt.font.name = "Segoe UI"
        p_dt.font.size = Pt(15)
        p_dt.font.bold = True
        p_dt.font.color.rgb = TEXT_HEAD

        for lbl, dsc in bullets:
            p_b = tf_d.add_paragraph()
            p_b.text = f"•  {lbl} "
            p_b.font.name = "Segoe UI"
            p_b.font.size = Pt(11.5)
            p_b.font.bold = True
            p_b.font.color.rgb = TEXT_HEAD
            p_b.space_before = Pt(12)

            run = p_b.add_run()
            run.text = dsc
            run.font.bold = False
            run.font.color.rgb = TEXT_BODY

    # =========================================================================
    # SLIDE 9: CORE TECHNICALITIES & EXAMINER VIVA DEFENSE GUIDE
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s9)
    add_slide_header(s9, 9, "Core Technicalities & Academic Defense",
                     "Core Innovations, Viva Defense & Conclusion",
                     "Why TerraFlow BioAI represents a true cyber-physical closed loop and answers to key examiner questions")

    card_8w = Inches(5.72)
    card_8h = Inches(4.55)

    # Left Column: Core Technical Novelties
    create_white_card(s9, Inches(0.8), Inches(1.85), card_8w, card_8h, top_accent=ACCENT_NAVY)

    tb_nov = s9.shapes.add_textbox(Inches(1.05), Inches(1.95), card_8w - Inches(0.5), card_8h - Inches(0.25))
    tf_nov = tb_nov.text_frame
    tf_nov.word_wrap = True

    p_nth = tf_nov.paragraphs[0]
    p_nth.text = "CORE TECHNICAL NOVELTIES"
    p_nth.font.name = "Segoe UI"
    p_nth.font.size = Pt(11)
    p_nth.font.bold = True
    p_nth.font.color.rgb = ACCENT_NAVY

    p_ntm = tf_nov.add_paragraph()
    p_ntm.text = "What Makes TerraFlow Truly 'Closed-Loop'?"
    p_ntm.font.name = "Segoe UI"
    p_ntm.font.size = Pt(15.5)
    p_ntm.font.bold = True
    p_ntm.font.color.rgb = TEXT_HEAD
    p_ntm.space_before = Pt(2)

    novelties = [
        ("Volume-Based Delivery (No Fixed Timers):",
         "Target volume (L) is calculated from FAO-56 soil depletion: Volume = (Field Capacity - Current Moisture) × Area × Depth. Actuation stops based on pulse-flow meter volume integration, eliminating over/under-watering."),

        ("Post-Irrigation Moisture Verification:",
         "Re-reads soil moisture 3 minutes after watering to confirm the wetting front percolation (Δθ = +18% to +24%). If no rise is observed, flags FAULT: NO_RESPONSE and alerts the dashboard."),

        ("Deterministic Edge Isolation:",
         "The STM32 firmware guarantees fail-safe OFF behavior during Wi-Fi drops, server crashes, or sensor disconnects. Cloud advises; bare-metal controls."),

        ("Transparent Reason Codes:",
         "Replaces black-box switching with human-readable labels: RUN:MOISTURE_LOW, SKIP:RAIN_CONTEXT, RUN:WATER_DEFICIT backed by 80+ FAO-56/ICAR knowledge base rules.")
    ]

    for ntitle, ndesc in novelties:
        p_pt = tf_nov.add_paragraph()
        p_pt.text = f"•  {ntitle} "
        p_pt.font.name = "Segoe UI"
        p_pt.font.size = Pt(10.5)
        p_pt.font.bold = True
        p_pt.font.color.rgb = TEXT_HEAD
        p_pt.space_before = Pt(8)

        run = p_pt.add_run()
        run.text = ndesc
        run.font.bold = False
        run.font.color.rgb = TEXT_BODY

    # Right Column: Examiner Viva Defense Guide (The exact highlighted box!)
    create_white_card(s9, Inches(6.81), Inches(1.85), card_8w, card_8h, top_accent=ACCENT_BLUE)

    tb_viva = s9.shapes.add_textbox(Inches(7.06), Inches(1.95), card_8w - Inches(0.5), card_8h - Inches(0.25))
    tf_viva = tb_viva.text_frame
    tf_viva.word_wrap = True

    p_vh = tf_viva.paragraphs[0]
    p_vh.text = "EXAMINER VIVA DEFENSE GUIDE"
    p_vh.font.name = "Segoe UI"
    p_vh.font.size = Pt(11)
    p_vh.font.bold = True
    p_vh.font.color.rgb = ACCENT_BLUE

    p_vm = tf_viva.add_paragraph()
    p_vm.text = "Answers to Tough Professor Questions"
    p_vm.font.name = "Segoe UI"
    p_vm.font.size = Pt(15.5)
    p_vm.font.bold = True
    p_vm.font.color.rgb = TEXT_HEAD
    p_vm.space_before = Pt(2)

    viva_qa = [
        ("Q: Does your TDS sensor measure soil NPK?",
         "A: No, Sir. TDS measures dissolved salts in irrigation water. Claiming cheap sensors read soil NPK is chemically false; we use accredited Soil Health Card lab inputs in Supabase with ICAR regional baseline autofill."),

        ("Q: Why use two microcontrollers (STM32 + ESP32)?",
         "A: Reliability & Determinism. STM32 provides real-time deterministic safety, interrupt-driven pulse counting, and signal filtering that never crash; ESP32 handles Wi-Fi, telemetry, and cloud ML connectivity."),

        ("Q: What happens if Wi-Fi disconnects?",
         "A: The STM32 operates autonomously under local calibrated threshold rules. Actuation never stalls or hangs open."),

        ("Q: Publication & Future Scope?",
         "A: Formalized as an IEEE Conference Paper. Future scope includes LoRaWAN mesh expansion for multi-zone farm coverage (TF01 → TF0N) and solar battery power harvesting.")
    ]

    for q, a in viva_qa:
        p_q = tf_viva.add_paragraph()
        p_q.text = q
        p_q.font.name = "Segoe UI"
        p_q.font.size = Pt(10.5)
        p_q.font.bold = True
        p_q.font.color.rgb = ACCENT_NAVY
        p_q.space_before = Pt(7)

        p_a = tf_viva.add_paragraph()
        p_a.text = a
        p_a.font.name = "Segoe UI"
        p_a.font.size = Pt(9.8)
        p_a.font.color.rgb = TEXT_BODY
        p_a.space_before = Pt(2)

    # Bottom Stat Metrics Row (4 Prestigious Engineering Badges)
    stats = [
        ("~38% Water Conserved", "Volumetric Pulse-Flow vs Timer", ACCENT_NAVY),
        ("100% Fail-Safe Safety", "Zero Runaway Pump Execution", ACCENT_BLUE),
        ("90.8% - 100% ML Acc", "4 Models, 5-Fold Cross-Validated", ACCENT_GREEN),
        ("80+ Agronomic Rules", "FAO-56 & ICAR Knowledge Base", ACCENT_PURPLE)
    ]

    stat_w = Inches(2.78)
    stat_h = Inches(0.72)
    stat_top = Inches(6.52)

    for idx, (s_val, s_sub, s_col) in enumerate(stats):
        s_left = Inches(0.8 + idx * 2.98)
        card_s = create_white_card(s9, s_left, stat_top, stat_w, stat_h, top_accent=s_col)

        tb_s = s9.shapes.add_textbox(s_left + Inches(0.12), stat_top + Inches(0.08), stat_w - Inches(0.24), stat_h - Inches(0.12))
        tf_s = tb_s.text_frame
        tf_s.word_wrap = True

        p_sv = tf_s.paragraphs[0]
        p_sv.text = s_val
        p_sv.font.name = "Segoe UI"
        p_sv.font.size = Pt(12)
        p_sv.font.bold = True
        p_sv.font.color.rgb = s_col
        p_sv.alignment = PP_ALIGN.CENTER

        p_ss = tf_s.add_paragraph()
        p_ss.text = s_sub
        p_ss.font.name = "Segoe UI"
        p_ss.font.size = Pt(9.5)
        p_ss.font.color.rgb = TEXT_BODY
        p_ss.alignment = PP_ALIGN.CENTER
        p_ss.space_before = Pt(1)

    # =========================================================================
    # SLIDE 10: ACADEMIC REFERENCES & TECHNICAL DATASHEETS
    # Peer-reviewed literature, FAO/ICAR standards, and component datasheets
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s10)
    add_slide_header(s10, 10, "References & Technical Datasheets",
                     "Academic References & Component Datasheets",
                     "Peer-reviewed literature, FAO/ICAR agronomic standards, and manufacturer datasheets underpinning TerraFlow BioAI")

    card_9w = Inches(5.72)
    card_9h = Inches(4.55)

    # Left Column: Academic References & Agronomic Standards
    create_white_card(s10, Inches(0.8), Inches(1.85), card_9w, card_9h, top_accent=ACCENT_NAVY)

    tb_ref = s10.shapes.add_textbox(Inches(1.05), Inches(1.95), card_9w - Inches(0.5), card_9h - Inches(0.25))
    tf_ref = tb_ref.text_frame
    tf_ref.word_wrap = True

    p_rh = tf_ref.paragraphs[0]
    p_rh.text = "PEER-REVIEWED RESEARCH & STANDARDS"
    p_rh.font.name = "Segoe UI"
    p_rh.font.size = Pt(11)
    p_rh.font.bold = True
    p_rh.font.color.rgb = ACCENT_NAVY

    p_rm = tf_ref.add_paragraph()
    p_rm.text = "Key Academic & Agronomic Literature"
    p_rm.font.name = "Segoe UI"
    p_rm.font.size = Pt(15.5)
    p_rm.font.bold = True
    p_rm.font.color.rgb = TEXT_HEAD
    p_rm.space_before = Pt(2)

    academic_refs = [
        ("[1] FAO-56 Penman-Monteith (Allen et al., 1998):",
         "\"Crop evapotranspiration: Guidelines for computing crop water requirements\", FAO Irrig. & Drain. Paper 56, Rome — Primary standard for reference evapotranspiration (ET0) and single crop coefficient (Kc) curves."),

        ("[2] FAO-33 Water Deficit Standards (Doorenbos & Kassam):",
         "\"Yield response to water\", FAO Irrig. & Drain. Paper 33 — Yield response factor (Ky) and allowable soil depletion fractions (p) preventing crop stress."),

        ("[3] ICAR & Soil Health Card Protocols (Govt. of India):",
         "Scientific soil-test-based fertilizer recommendations (STCR) for NPK deficit correction and agro-climatic zone crop suitability guidelines."),

        ("[4] IoT & Sensor Review (Prakash et al., 2023):",
         "\"Advancements in smart farming: A comprehensive review of IoT, wireless communication, sensors, and hardware\", Sens. Actuators A: Phys., vol. 362."),

        ("[5] AIoT Precision Agriculture (Sharma et al., 2024):",
         "\"Integrating artificial intelligence and IoT for precision agriculture: Recent advances and future directions\", Smart Agric. Technol., vol. 7.")
    ]

    for rtitle, rdesc in academic_refs:
        p_pt = tf_ref.add_paragraph()
        p_pt.text = f"•  {rtitle} "
        p_pt.font.name = "Segoe UI"
        p_pt.font.size = Pt(10)
        p_pt.font.bold = True
        p_pt.font.color.rgb = TEXT_HEAD
        p_pt.space_before = Pt(6)

        run = p_pt.add_run()
        run.text = rdesc
        run.font.bold = False
        run.font.color.rgb = TEXT_BODY

    # Right Column: Component Datasheets & Hardware Standards
    create_white_card(s10, Inches(6.81), Inches(1.85), card_9w, card_9h, top_accent=ACCENT_BLUE)

    tb_ds = s10.shapes.add_textbox(Inches(7.06), Inches(1.95), card_9w - Inches(0.5), card_9h - Inches(0.25))
    tf_ds = tb_ds.text_frame
    tf_ds.word_wrap = True

    p_dh = tf_ds.paragraphs[0]
    p_dh.text = "MANUFACTURER COMPONENT DATASHEETS"
    p_dh.font.name = "Segoe UI"
    p_dh.font.size = Pt(11)
    p_dh.font.bold = True
    p_dh.font.color.rgb = ACCENT_BLUE

    p_dm = tf_ds.add_paragraph()
    p_dm.text = "Technical Specifications & Hardware Manuals"
    p_dm.font.name = "Segoe UI"
    p_dm.font.size = Pt(15.5)
    p_dm.font.bold = True
    p_dm.font.color.rgb = TEXT_HEAD
    p_dm.space_before = Pt(2)

    datasheets = [
        ("STMicroelectronics STM32F103x8/xB Reference Manual:",
         "ARM Cortex-M3 32-bit MCU @ 72 MHz (DocID RM0008, Rev. 21) — Direct register timer capture, independent watchdog (IWDG), and bare-metal safety logic."),

        ("Espressif Systems ESP32 Series Datasheet (v5.0, 2023):",
         "Dual-Core Tensilica Xtensa 32-bit LX6 @ 240 MHz — 802.11 b/g/n Wi-Fi stack, TLS/HTTPS REST telemetry dispatch, and offline JSON ring buffer."),

        ("Bosch Sensortec BME280 Datasheet (BST-BME280-DS002):",
         "Combined digital humidity, pressure, and temperature sensor via I2C interface — Primary input for Vapor Pressure Deficit (VPD) computation."),

        ("Maxim Integrated DS18B20 Digital Thermometer (Rev. 6):",
         "Programmable resolution 1-Wire digital temperature probe (±0.5°C) — Submersible stainless steel for root-zone thermal tracking & TDS compensation."),

        ("u-blox NEO-6M GPS Module Data Sheet (UBX-14004472):",
         "50-channel high-sensitivity positioning engine (9600 baud NMEA) — Provides latitude/longitude coordinates for agro-climatic geo-tagging."),

        ("Vishay IRLZ44N MOSFET & Sea YF-S201 Flow Sensor:",
         "Logic-level N-channel Power MOSFET (55V, 47A) & Hall-effect turbine pulse flow meter (450 pulses/L) for exact closed-loop volumetric shutoff.")
    ]

    for dtitle, ddesc in datasheets:
        p_pt = tf_ds.add_paragraph()
        p_pt.text = f"•  {dtitle} "
        p_pt.font.name = "Segoe UI"
        p_pt.font.size = Pt(10)
        p_pt.font.bold = True
        p_pt.font.color.rgb = ACCENT_NAVY
        p_pt.space_before = Pt(4.5)

        run = p_pt.add_run()
        run.text = ddesc
        run.font.bold = False
        run.font.color.rgb = TEXT_BODY

    # Bottom Full-Width Research Outcome Banner
    bot_ref_card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.52), Inches(11.733), Inches(0.72))
    bot_ref_card.fill.solid()
    bot_ref_card.fill.fore_color.rgb = TAG_BG_GREEN
    bot_ref_card.line.fill.background()

    tb_br = s10.shapes.add_textbox(Inches(1.0), Inches(6.56), Inches(11.3), Inches(0.65))
    tf_br = tb_br.text_frame
    tf_br.word_wrap = True
    p_br = tf_br.paragraphs[0]
    p_br.text = "RESEARCH OUTCOME & PUBLICATION: This cyber-physical architecture, empirical sensor validation, and volumetric closed loop have been formalized as an IEEE Conference Paper titled 'TerraFlow BioAI: A Zone-Aware Edge-IoT Architecture for Closed-Loop Precision Irrigation & Agro-Advisory'."
    p_br.font.name = "Segoe UI"
    p_br.font.size = Pt(11)
    p_br.font.bold = True
    p_br.font.color.rgb = RGBColor(6, 95, 70)

    # Save Outputs
    output_target0 = os.path.join(BASE_DIR, "TerraFlow_BioAI_Academic_Presentation.pptx")
    output_target1 = os.path.join(BASE_DIR, "TerraFlow_BioAI_White_Theme_Presentation.pptx")
    output_target2 = os.path.join(BASE_DIR, "TerraFlow_BioAI_Final_Presentation.pptx")
    output_target3 = os.path.join(BASE_DIR, "TerraFlow_BioAI_SPIT_Major_Project.pptx")

    saved_paths = []
    for tgt in [output_target0, output_target1, output_target2, output_target3]:
        try:
            prs.save(tgt)
            print(f"[OK] Saved: {tgt}")
            saved_paths.append(tgt)
        except PermissionError:
            print(f"[NOTE] {tgt} is currently locked by PowerPoint. Skipped.")

    return saved_paths[0] if saved_paths else output_target0


if __name__ == "__main__":
    build_deck()
