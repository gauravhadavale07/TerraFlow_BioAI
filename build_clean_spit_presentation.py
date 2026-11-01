"""
TerraFlow BioAI - Major Project Official Presentation Generator
Designed for SPIT Mumbai B.Tech Final Presentation (Academic Year 2026-2027)

Design Principles:
- 16:9 Widescreen (13.333" x 7.5")
- Clean, human-designed academic style (crisp white background, deep navy text, royal blue and emerald green accents)
- Big, readable typography (12-14pt body, 16-18pt section headers, 24-26pt slide titles)
- Bold lead-in phrases for fast professor comprehension
- Official SPIT transparent logo on title slide and top-right header of all slides
- High-res architecture diagram integrated cleanly on Slide 3
- Exactly 7 slides covering the required flow
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# ── Color Palette (Human-Designed Academic Deck) ───────────────────────────
BG_CANVAS      = RGBColor(248, 250, 252)   # #F8FAFC Crisp Slate Canvas
CARD_BG        = RGBColor(255, 255, 255)   # #FFFFFF Pure White Card
CARD_BORDER    = RGBColor(226, 232, 240)   # #E2E8F0 Subtle Clean Border
TEXT_HEAD      = RGBColor(15, 23, 42)      # #0F172A Deep Navy / Slate 900
TEXT_BODY      = RGBColor(51, 65, 85)      # #334155 Slate 700 (Very readable)
TEXT_MUTED     = RGBColor(100, 116, 139)   # #64748B Slate 500
ACCENT_BLUE    = RGBColor(2, 132, 199)     # #0284C7 Sky/Royal Blue
ACCENT_NAVY    = RGBColor(30, 58, 138)     # #1E3A8A Classic Academic Navy
ACCENT_GREEN   = RGBColor(16, 185, 129)    # #10B981 Emerald Green
ACCENT_AMBER   = RGBColor(217, 119, 6)     # #D97706 Warm Amber
ACCENT_RED     = RGBColor(225, 29, 72)     # #E11D48 Rose Red
TAG_BG_BLUE    = RGBColor(224, 242, 254)   # #E0F2FE Light blue badge
TAG_BG_GREEN   = RGBColor(209, 250, 229)   # #D1FAE5 Light green badge

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPIT_LOGO_PATH = os.path.join(BASE_DIR, "extracted_assets", "spit_logo_0.png")
ARCH_IMG_PATH  = os.path.join(BASE_DIR, "extracted_assets", "report_img250.jpg")


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
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.32), Inches(3.4), Inches(0.32))
    badge.fill.solid()
    badge.fill.fore_color.rgb = TAG_BG_BLUE
    badge.line.fill.background()

    tf_b = badge.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0
    p_b = tf_b.paragraphs[0]
    p_b.text = f"SLIDE 0{slide_num}  •  {category.upper()}"
    p_b.font.name = "Segoe UI"
    p_b.font.size = Pt(10)
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
    p_s.font.size = Pt(12.5)
    p_s.font.color.rgb = TEXT_MUTED

    # Header Divider Line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.68), Inches(11.733), Inches(0.02))
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
    # SLIDE 1: TITLE SLIDE (Clean, Official, Grand)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s1)

    # Top Accent Ribbon
    ribbon = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    ribbon.fill.solid()
    ribbon.fill.fore_color.rgb = ACCENT_NAVY
    ribbon.line.fill.background()

    # SPIT Logo - Prominent on Title Page
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
    # SLIDE 2: LITERATURE SURVEY & TECHNICAL GAPS
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s2)
    add_slide_header(s2, 2, "Literature Survey & Motivation",
                     "Technical Gaps in Existing Smart Irrigation Systems",
                     "Why commercial timer schedules and cloud-only IoT switches fail in real-world agricultural conditions")

    # 3 Big Distinct Gap Cards (Easily readable, big text)
    gaps = [
        ("01", "Galvanic Probe Drift & Raw Noise",
         ACCENT_RED,
         [("The Problem:", "Resistive soil probes suffer rapid galvanic corrosion in moist soil, drifting calibration within 2–3 weeks."),
          ("Raw ADC Flaws:", "Air pockets and electrical pump noise cause false ADC spikes, triggering erratic relay chattering."),
          ("Our Solution:", "Capacitive corrosion-resistant probes with lightweight on-chip noise smoothing before decisions run.")]),

        ("02", "Cloud-Only Actuation Latency & Risk",
         ACCENT_AMBER,
         [("The Problem:", "Standard IoT systems stream raw data to cloud servers (ThingsBoard/AWS), which directly switch pump relays."),
          ("Network Outages:", "A Wi-Fi drop or server stall leaves high-power pumps running indefinitely, flooding crops and burning motors."),
          ("Our Solution:", "Strict separation of concerns: Bare-metal STM32 retains 100% pump safety authority. Cloud only advises.")]),

        ("03", "Fixed Timers vs Agronomic Hydrology",
         ACCENT_BLUE,
         [("The Problem:", "Hard-coded rules ('pump ON for 10 mins') completely ignore soil water holding capacity and crop growth stage."),
          ("Over-Irrigation:", "10 minutes floods Sandy soil (causing root rot), but starves Clay soil. Wastes critical water resources."),
          ("Our Solution:", "Target water volume calculated using FAO-56 Penman-Monteith equations, metered via pulse-flow sensor.")])
    ]

    c_w = Inches(3.75)
    c_h = Inches(4.55)
    c_top = Inches(1.95)

    for i, (num, title, accent, points) in enumerate(gaps):
        left = Inches(0.8 + i * 3.99)
        create_white_card(s2, left, c_top, c_w, c_h, top_accent=accent)

        tb = s2.shapes.add_textbox(left + Inches(0.25), c_top + Inches(0.2), c_w - Inches(0.5), c_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p_n = tf.paragraphs[0]
        p_n.text = f"TECHNICAL GAP {num}"
        p_n.font.name = "Segoe UI"
        p_n.font.size = Pt(11)
        p_n.font.bold = True
        p_n.font.color.rgb = accent

        p_t = tf.add_paragraph()
        p_t.text = title
        p_t.font.name = "Segoe UI"
        p_t.font.size = Pt(16)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_HEAD
        p_t.space_before = Pt(4)

        for label, desc in points:
            p_p = tf.add_paragraph()
            p_p.text = f"{label} "
            p_p.font.name = "Segoe UI"
            p_p.font.size = Pt(12)
            p_p.font.bold = True
            p_p.font.color.rgb = TEXT_HEAD
            p_p.space_before = Pt(10)

            run = p_p.add_run()
            run.text = desc
            run.font.bold = False
            run.font.color.rgb = TEXT_BODY

    # Bottom Core Objective Summary
    bot_card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.65), Inches(11.733), Inches(0.6))
    bot_card.fill.solid()
    bot_card.fill.fore_color.rgb = TAG_BG_GREEN
    bot_card.line.fill.background()

    tb_b = s2.shapes.add_textbox(Inches(1.0), Inches(6.68), Inches(11.3), Inches(0.5))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True
    p_b = tf_b.paragraphs[0]
    p_b.text = "CORE TAKEAWAY: TerraFlow BioAI bridges these gaps by combining bare-metal deterministic safety on STM32 with explainable FAO-56 volumetric water budgeting and evidence-driven ML advisory."
    p_b.font.name = "Segoe UI"
    p_b.font.size = Pt(11)
    p_b.font.bold = True
    p_b.font.color.rgb = RGBColor(6, 95, 70)

    # =========================================================================
    # SLIDE 3: SYSTEM ARCHITECTURE (High-Res Master Diagram)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s3)
    add_slide_header(s3, 3, "System Architecture",
                     "End-to-End System Architecture (The 5 Layers)",
                     "Physical closed-loop sensing, edge processing, dual-MCU topology, and cloud agro-advisory")

    # Left: Master High-Res Architecture Diagram Card
    img_left = Inches(0.8)
    img_top = Inches(1.95)
    img_w = Inches(7.0)
    img_h = Inches(5.25)
    create_white_card(s3, img_left, img_top, img_w, img_h, top_accent=ACCENT_NAVY)

    if os.path.exists(ARCH_IMG_PATH):
        try:
            s3.shapes.add_picture(ARCH_IMG_PATH, img_left + Inches(0.15), img_top + Inches(0.25), width=img_w - Inches(0.3))
        except Exception as e:
            print(f"Error loading arch img: {e}")

    # Right: The 5 Layers Breakdown inside one unified, clean card
    r_left = Inches(8.05)
    r_w = Inches(4.48)
    r_h = Inches(5.25)
    create_white_card(s3, r_left, img_top, r_w, r_h, top_accent=ACCENT_BLUE)

    tb_r = s3.shapes.add_textbox(r_left + Inches(0.25), img_top + Inches(0.15), r_w - Inches(0.5), r_h - Inches(0.3))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p_rt = tf_r.paragraphs[0]
    p_rt.text = "THE 5 ARCHITECTURAL LAYERS"
    p_rt.font.name = "Segoe UI"
    p_rt.font.size = Pt(11)
    p_rt.font.bold = True
    p_rt.font.color.rgb = ACCENT_BLUE

    layers = [
        ("Layer 1: Field Sensing (Zone Z01)",
         "BME280 (I2C), FC-28 capacitive soil moisture (ADC1), TDS water quality (ADC2), and pulse-flow sensor on pump discharge line.",
         ACCENT_NAVY),
        ("Layer 2: STM32 Edge Safety Authority",
         "On-chip noise smoothing, 5-state safety FSM, hardware flow pulse counting, and IRLZ44N MOSFET gate drive.",
         ACCENT_BLUE),
        ("Layer 3: ESP32 Gateway & Telemetry",
         "Receives data over UART2 (115200 baud); transmits JSON over Wi-Fi; buffers telemetry safely during network outages.",
         ACCENT_GREEN),
        ("Layer 4: Agronomic Cloud & ML Intelligence",
         "Supabase stores 80+ FAO-56 crop rules; Python REST ML microservice evaluates irrigation, crop, and fertilizer models.",
         ACCENT_AMBER),
        ("Layer 5: Closed-Loop Operator Console",
         "React dashboard displays live sensor trends, WSI/VPD drying stress, reason codes, volumetric progress, and pump state.",
         RGBColor(109, 40, 217))
    ]

    for ltitle, ldesc, col in layers:
        p_lt = tf_r.add_paragraph()
        p_lt.text = f"•  {ltitle}"
        p_lt.font.name = "Segoe UI"
        p_lt.font.size = Pt(12)
        p_lt.font.bold = True
        p_lt.font.color.rgb = col
        p_lt.space_before = Pt(10)

        p_ld = tf_r.add_paragraph()
        p_ld.text = f"   {ldesc}"
        p_ld.font.name = "Segoe UI"
        p_ld.font.size = Pt(11)
        p_ld.font.color.rgb = TEXT_BODY
        p_ld.space_before = Pt(2)

    # =========================================================================
    # SLIDE 4: HARDWARE IMPLEMENTATION (STM32 & ESP32)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s4)
    add_slide_header(s4, 4, "Embedded Hardware Design",
                     "Dual-Controller Hardware Topology: STM32 & ESP32",
                     "Physical division of responsibilities: Bare-metal deterministic safety vs high-speed wireless connectivity")

    hw_w = Inches(5.72)
    hw_h = Inches(5.25)

    # Left Column: STM32 (Local Safety Authority)
    add_left = Inches(0.8)
    create_white_card(s4, add_left, Inches(1.95), hw_w, hw_h, top_accent=ACCENT_NAVY)

    tb_s4_1 = s4.shapes.add_textbox(add_left + Inches(0.3), Inches(2.1), hw_w - Inches(0.6), hw_h - Inches(0.4))
    tf_s4_1 = tb_s4_1.text_frame
    tf_s4_1.word_wrap = True

    p_stm_tag = tf_s4_1.paragraphs[0]
    p_stm_tag.text = "LOCAL SAFETY & ACTUATION AUTHORITY"
    p_stm_tag.font.name = "Segoe UI"
    p_stm_tag.font.size = Pt(11)
    p_stm_tag.font.bold = True
    p_stm_tag.font.color.rgb = ACCENT_NAVY

    p_stm_h = tf_s4_1.add_paragraph()
    p_stm_h.text = "STM32F103C8T6 (ARM Cortex-M3 @ 72 MHz)"
    p_stm_h.font.name = "Segoe UI"
    p_stm_h.font.size = Pt(16)
    p_stm_h.font.bold = True
    p_stm_h.font.color.rgb = TEXT_HEAD
    p_stm_h.space_before = Pt(2)

    stm_features = [
        ("Sole Pump Actuation Authority:", "Directly drives the IRLZ44N MOSFET pump gate. The cloud never has physical control of the pump pin."),
        ("Sensor Acquisition:", "Reads BME280 via I2C (PB6/PB7), Soil Moisture on ADC1 (PA0), and TDS Sensor on ADC2 (PA1)."),
        ("On-Chip Signal Filtering:", "Lightweight noise smoothing in firmware eliminates electrical pump noise and air-pocket fluctuations."),
        ("Pulse-Flow Volumetric Integration:", "Accumulates pulses from flow sensor via hardware interrupt; cuts off pump when target volume (Liters) is delivered."),
        ("Hardware Watchdog (IWDG):", "180-second hard safety timeout cuts pump automatically if flow stalls or line blocks.")
    ]
    for lbl, desc in stm_features:
        p_pt = tf_s4_1.add_paragraph()
        p_pt.text = f"•  {lbl} "
        p_pt.font.name = "Segoe UI"
        p_pt.font.size = Pt(12)
        p_pt.font.bold = True
        p_pt.font.color.rgb = TEXT_HEAD
        p_pt.space_before = Pt(8)

        run = p_pt.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_BODY

    # Right Column: ESP32 (Wi-Fi & Cloud Gateway)
    esp_left = Inches(6.81)
    create_white_card(s4, esp_left, Inches(1.95), hw_w, hw_h, top_accent=ACCENT_BLUE)

    tb_s4_2 = s4.shapes.add_textbox(esp_left + Inches(0.3), Inches(2.1), hw_w - Inches(0.6), hw_h - Inches(0.4))
    tf_s4_2 = tb_s4_2.text_frame
    tf_s4_2.word_wrap = True

    p_esp_tag = tf_s4_2.paragraphs[0]
    p_esp_tag.text = "IOT TELEMETRY & CLOUD GATEWAY"
    p_esp_tag.font.name = "Segoe UI"
    p_esp_tag.font.size = Pt(11)
    p_esp_tag.font.bold = True
    p_esp_tag.font.color.rgb = ACCENT_BLUE

    p_esp_h = tf_s4_2.add_paragraph()
    p_esp_h.text = "ESP32 DevKit (Dual-Core Tensilica @ 240 MHz)"
    p_esp_h.font.name = "Segoe UI"
    p_esp_h.font.size = Pt(16)
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
        p_pt = tf_s4_2.add_paragraph()
        p_pt.text = f"•  {lbl} "
        p_pt.font.name = "Segoe UI"
        p_pt.font.size = Pt(12)
        p_pt.font.bold = True
        p_pt.font.color.rgb = TEXT_HEAD
        p_pt.space_before = Pt(8)

        run = p_pt.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_BODY

    # =========================================================================
    # SLIDE 5: MACHINE LEARNING DECISION SUPPORT
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s5)
    add_slide_header(s5, 5, "Machine Learning Decision Support",
                     "Sensor-Aligned Machine Learning Intelligence",
                     "4 specialized models trained on sensor-compatible feature vectors and evaluated with 5-fold cross-validation")

    # 4 Model Cards Grid (2x2)
    m_w = Inches(5.72)
    m_h = Inches(2.1)

    ml_models = [
        ("MODEL 1: PRIMARY DECISION ENGINE", "Irrigation Prediction", "XGBoost Classifier",
         "90.80% Test Acc | 92.00% 5-Fold CV", ACCENT_NAVY,
         "Filtered moisture (23.7%), Rainfall context (33.3%), Soil type (16.2%), Crop Kc (9.9%), Temp & RH (6.4%).",
         "Actionable IRRIGATE / NO_IRRIGATION decision with transparent reason codes (e.g., RUN:MOISTURE_LOW, SKIP:RAIN_CONTEXT)."),

        ("MODEL 2: PRE-PLANTING ADVISORY", "Crop Suitability Recommendation", "Random Forest (200 Trees)",
         "99.32% Test Acc | 99.45% 5-Fold CV", ACCENT_BLUE,
         "Soil profile texture, BME280 temperature, relative humidity, rainfall context, and Soil Health Card NPK.",
         "Evaluates 22 candidate crops and ranks the Top 5 recommended crops with percentage suitability confidence bars."),

        ("MODEL 3: NUTRIENT CORRECTION", "Fertilizer Prescription", "XGBoost Classifier",
         "100.0% Test Acc | 99.90% 5-Fold CV", ACCENT_GREEN,
         "Soil-test N, P, K status, target crop type, growth stage, and current soil moisture level.",
         "Prescribes exact commercial fertilizer grade (Urea for low N, DAP for low P, 10-26-26, 14-35-14) to correct deficits."),

        ("MODEL 4: SOIL CHARACTERIZATION", "Soil Type Classification", "Random Forest Classifier",
         "84.50% Test Acc | 84.80% 5-Fold CV", RGBColor(124, 58, 237),
         "Moisture retention dynamics, ambient climate patterns, and baseline electrical conductivity.",
         "Classifies soil texture into Black (Vertisol), Red (Alfisol), Alluvial, Sandy, Clayey, or Loamy.")
    ]

    positions_s5 = [
        (Inches(0.8), Inches(1.95)),
        (Inches(6.81), Inches(1.95)),
        (Inches(0.8), Inches(4.25)),
        (Inches(6.81), Inches(4.25))
    ]

    for (pos, (tag, name, algo, metrics, col, feat, out)) in zip(positions_s5, ml_models):
        x, y = pos
        create_white_card(s5, x, y, m_w, m_h, top_accent=col)

        tb_m = s5.shapes.add_textbox(x + Inches(0.25), y + Inches(0.12), m_w - Inches(0.5), m_h - Inches(0.25))
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
        p_n.font.size = Pt(13.5)
        p_n.font.bold = True
        p_n.font.color.rgb = TEXT_HEAD
        p_n.space_before = Pt(2)

        p_f = tf_m.add_paragraph()
        p_f.text = "Key Features: "
        p_f.font.name = "Segoe UI"
        p_f.font.size = Pt(11)
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
        p_o.font.size = Pt(11)
        p_o.font.bold = True
        p_o.font.color.rgb = TEXT_HEAD
        p_o.space_before = Pt(3)
        run_o = p_o.add_run()
        run_o.text = out
        run_o.font.bold = False
        run_o.font.color.rgb = TEXT_BODY

    # Bottom Agronomic Honesty Badge
    hon_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.55), Inches(11.733), Inches(0.68))
    hon_card.fill.solid()
    hon_card.fill.fore_color.rgb = TAG_BG_GREEN
    hon_card.line.fill.background()

    tb_h = s5.shapes.add_textbox(Inches(1.0), Inches(6.58), Inches(11.3), Inches(0.6))
    tf_h = tb_h.text_frame
    tf_h.word_wrap = True
    p_h = tf_h.paragraphs[0]
    p_h.text = "CRUCIAL VIVA DEFENSE POINT: Our TDS Meter V1.0 measures water dissolved solids (salinity), NOT soil NPK. Nitrogen, Phosphorus, Potassium, and pH are derived from accredited Soil Health Card lab tests stored in Supabase (with ICAR regional baseline autofill)."
    p_h.font.name = "Segoe UI"
    p_h.font.size = Pt(10.5)
    p_h.font.bold = True
    p_h.font.color.rgb = RGBColor(6, 95, 70)

    # =========================================================================
    # SLIDE 6: WEB DASHBOARD & USER INTERFACE
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s6)
    add_slide_header(s6, 6, "Web Application & Control Console",
                     "Real-Time React Dashboard & Closed-Loop UI",
                     "Connected operator console with live sensor gauges, zone configuration, AI advisory cards, and historical trends")

    # 3 Main Feature Columns
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
        create_white_card(s6, left, Inches(1.95), card_dw, card_dh, top_accent=accent)

        tb_d = s6.shapes.add_textbox(left + Inches(0.25), Inches(2.1), card_dw - Inches(0.5), card_dh - Inches(0.4))
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
            p_b.font.size = Pt(12)
            p_b.font.bold = True
            p_b.font.color.rgb = TEXT_HEAD
            p_b.space_before = Pt(12)

            run = p_b.add_run()
            run.text = dsc
            run.font.bold = False
            run.font.color.rgb = TEXT_BODY

    # =========================================================================
    # SLIDE 7: CORE TECHNICALITIES, DEFENSE & CONCLUSION
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s7)
    add_slide_header(s7, 7, "Core Technicalities & Academic Defense",
                     "Core Innovations, Viva Defense & Conclusion",
                     "Why TerraFlow BioAI represents a true cyber-physical closed loop and answers to key examiner questions")

    # Left Column: Core Technical Innovations
    i_left = Inches(0.8)
    i_w = Inches(5.72)
    i_h = Inches(5.25)
    create_white_card(s7, i_left, Inches(1.95), i_w, i_h, top_accent=ACCENT_NAVY)

    tb_i = s7.shapes.add_textbox(i_left + Inches(0.3), Inches(2.1), i_w - Inches(0.6), i_h - Inches(0.4))
    tf_i = tb_i.text_frame
    tf_i.word_wrap = True

    p_it = tf_i.paragraphs[0]
    p_it.text = "CORE TECHNICAL NOVELTIES"
    p_it.font.name = "Segoe UI"
    p_it.font.size = Pt(11)
    p_it.font.bold = True
    p_it.font.color.rgb = ACCENT_NAVY

    p_ih = tf_i.add_paragraph()
    p_ih.text = "What Makes TerraFlow Truly 'Closed-Loop'?"
    p_ih.font.name = "Segoe UI"
    p_ih.font.size = Pt(16)
    p_ih.font.bold = True
    p_ih.font.color.rgb = TEXT_HEAD
    p_ih.space_before = Pt(2)

    innovations = [
        ("Volume-Based Delivery (No Fixed Timers):", "Target volume (L) is calculated from FAO-56 soil depletion: Volume = (Field Capacity - Current Moisture) × Area × Depth. Actuation stops based on pulse-flow meter volume integration."),
        ("Post-Irrigation Moisture Verification:", "Re-reads soil moisture 3 minutes after watering to confirm the wetting front percolation (Δθ = +18% to +24%). If no rise is observed, flags FAULT: NO_RESPONSE."),
        ("Deterministic Edge Isolation:", "The STM32 firmware guarantees fail-safe OFF behavior during Wi-Fi drops, server crashes, or sensor disconnects. Cloud advices; bare-metal controls."),
        ("Transparent Reason Codes:", "Replaces black-box switching with human-readable labels: RUN:MOISTURE_LOW, SKIP:RAIN_CONTEXT, RUN:WATER_DEFICIT backed by 80+ FAO-56/ICAR knowledge base rules.")
    ]
    for lbl, desc in innovations:
        p_pt = tf_i.add_paragraph()
        p_pt.text = f"•  {lbl} "
        p_pt.font.name = "Segoe UI"
        p_pt.font.size = Pt(12)
        p_pt.font.bold = True
        p_pt.font.color.rgb = TEXT_HEAD
        p_pt.space_before = Pt(8)

        run = p_pt.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_BODY

    # Right Column: Viva-Ready Questions & Defense
    v_left = Inches(6.81)
    create_white_card(s7, v_left, Inches(1.95), i_w, i_h, top_accent=ACCENT_BLUE)

    tb_v = s7.shapes.add_textbox(v_left + Inches(0.3), Inches(2.1), i_w - Inches(0.6), i_h - Inches(0.4))
    tf_v = tb_v.text_frame
    tf_v.word_wrap = True

    p_vt = tf_v.paragraphs[0]
    p_vt.text = "EXAMINER VIVA DEFENSE GUIDE"
    p_vt.font.name = "Segoe UI"
    p_vt.font.size = Pt(11)
    p_vt.font.bold = True
    p_vt.font.color.rgb = ACCENT_BLUE

    p_vh = tf_v.add_paragraph()
    p_vh.text = "Answers to Tough Professor Questions"
    p_vh.font.name = "Segoe UI"
    p_vh.font.size = Pt(16)
    p_vh.font.bold = True
    p_vh.font.color.rgb = TEXT_HEAD
    p_vh.space_before = Pt(2)

    viva_qa = [
        ("Q: Does your TDS sensor measure soil NPK?", "A: No, Sir. TDS measures dissolved salts in irrigation water. Claiming cheap sensors read soil NPK is chemically false; we use accredited Soil Health Card lab inputs in Supabase."),
        ("Q: Why use two microcontrollers (STM32 + ESP32)?", "A: Reliability. STM32 provides real-time deterministic safety and signal smoothing that never crash; ESP32 handles Wi-Fi, telemetry, and cloud ML connectivity."),
        ("Q: What happens if Wi-Fi disconnects?", "A: The STM32 operates autonomously under local calibrated threshold rules. Actuation never stalls or hangs open."),
        ("Q: Publication & Future Scope?", "A: Formalized as an IEEE Conference Paper. Future scope includes LoRaWAN mesh expansion for multi-zone farm coverage (TF01 → TF0N).")
    ]
    for q, a in viva_qa:
        p_q = tf_v.add_paragraph()
        p_q.text = f"{q}"
        p_q.font.name = "Segoe UI"
        p_q.font.size = Pt(11.5)
        p_q.font.bold = True
        p_q.font.color.rgb = ACCENT_NAVY
        p_q.space_before = Pt(7)

        p_a = tf_v.add_paragraph()
        p_a.text = f"{a}"
        p_a.font.name = "Segoe UI"
        p_a.font.size = Pt(11)
        p_a.font.color.rgb = TEXT_BODY
        p_a.space_before = Pt(1)

    # Save Outputs
    output_target1 = os.path.join(BASE_DIR, "TerraFlow_BioAI_SPIT_Major_Project.pptx")
    output_target2 = os.path.join(BASE_DIR, "TerraFlow_BioAI_Final_Presentation.pptx")
    output_target3 = os.path.join(BASE_DIR, "TerraFlow_BioAI_Major_Project_Presentation.pptx")

    prs.save(output_target1)
    print(f"[OK] Saved: {output_target1}")
    prs.save(output_target2)
    print(f"[OK] Saved: {output_target2}")

    try:
        prs.save(output_target3)
        print(f"[OK] Saved: {output_target3}")
    except PermissionError:
        print(f"[NOTE] {output_target3} is currently open in PowerPoint on user desktop. Saved to target1 and target2.")

    return output_target1


if __name__ == "__main__":
    build_deck()
