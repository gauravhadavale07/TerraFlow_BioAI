"""
TerraFlow BioAI - Major Project Executive Presentation Generator
Builds a world-class, professional 8-slide PowerPoint presentation
strictly adhering to the SPIT Final Major Project Report & IEEE Paper.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ── Color Palette (Dark Executive Tech Theme) ──────────────────────────────
BG_COLOR       = RGBColor(8, 14, 30)       # #080E1E Deep Dark Navy
CARD_BG        = RGBColor(17, 28, 51)      # #111C33 Dark Slate Card
CARD_BORDER    = RGBColor(30, 41, 59)      # #1E293B Slate Border
CARD_BG_LIGHT  = RGBColor(24, 38, 68)      # #182644 Slightly Lighter Slate
TEXT_WHITE     = RGBColor(255, 255, 255)  # #FFFFFF Pure White
TEXT_MUTED     = RGBColor(148, 163, 184)  # #94A3B8 Slate Gray
TEXT_BODY      = RGBColor(226, 232, 240)  # #E2E8F0 Soft White
ACCENT_GREEN   = RGBColor(16, 185, 129)   # #10B981 Emerald Green
ACCENT_CYAN    = RGBColor(56, 189, 248)   # #38BDF8 Sky Cyan
ACCENT_AMBER   = RGBColor(245, 158, 11)   # #F59E0B Warm Amber
ACCENT_PURPLE  = RGBColor(168, 85, 247)   # #A855F7 Violet
TAG_BG         = RGBColor(15, 45, 40)      # Dark emerald tint

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPIT_LOGO_PATH = os.path.join(BASE_DIR, "extracted_assets", "spit_logo_1.png")
ARCH_IMG_PATH  = os.path.join(BASE_DIR, "extracted_assets", "report_img250.jpg")


def set_slide_background(slide):
    """Fills slide background with executive dark navy."""
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_COLOR
    bg.line.fill.background()
    return bg


def add_header(slide, category_text, title_text, subtitle_text):
    """Adds a standard top header with category tracker and clean typography."""
    # Category Tracker Badge
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(9.0), Inches(0.35))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = f"TERRAFLOW BIOAI  •  SPIT MAJOR PROJECT  |  {category_text.upper()}"
    p_cat.font.name = "Segoe UI"
    p_cat.font.size = Pt(9.5)
    p_cat.font.bold = True
    p_cat.font.color.rgb = ACCENT_GREEN

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(10.5), Inches(0.55))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = "Segoe UI"
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_WHITE

    # Subtitle
    sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.0), Inches(0.35))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.font.name = "Segoe UI"
    p_sub.font.size = Pt(11.5)
    p_sub.font.color.rgb = TEXT_MUTED

    # Header Divider Line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.72), Inches(11.733), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = CARD_BORDER
    line.line.fill.background()

    # Small SPIT Logo on top right header (if exists)
    if os.path.exists(SPIT_LOGO_PATH):
        try:
            slide.shapes.add_picture(SPIT_LOGO_PATH, Inches(11.8), Inches(0.4), height=Inches(0.95))
        except Exception:
            pass


def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER, top_accent=None):
    """Creates a container card with optional top accent stripe."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()

    if top_accent:
        stripe = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(0.06))
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = top_accent
        stripe.line.fill.background()

    return card


def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Executive Academic Title)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Ambient Glow / Decorative Top Bar
    glow = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.1))
    glow.fill.solid()
    glow.fill.fore_color.rgb = ACCENT_GREEN
    glow.line.fill.background()

    # SPIT Logo on Title Slide
    if os.path.exists(SPIT_LOGO_PATH):
        try:
            s1.shapes.add_picture(SPIT_LOGO_PATH, Inches(0.8), Inches(0.6), height=Inches(1.3))
        except Exception as e:
            print(f"Could not load logo: {e}")

    # College Title Text
    inst_box = s1.shapes.add_textbox(Inches(2.3), Inches(0.6), Inches(10.0), Inches(1.2))
    tf_inst = inst_box.text_frame
    tf_inst.word_wrap = True
    p_inst1 = tf_inst.paragraphs[0]
    p_inst1.text = "BHARATIYA VIDYA BHAVAN'S SARDAR PATEL INSTITUTE OF TECHNOLOGY (SPIT)"
    p_inst1.font.name = "Segoe UI"
    p_inst1.font.size = Pt(12)
    p_inst1.font.bold = True
    p_inst1.font.color.rgb = TEXT_WHITE

    p_inst2 = tf_inst.add_paragraph()
    p_inst2.text = "DEPARTMENT OF ELECTRONICS & TELECOMMUNICATION ENGINEERING  |  MUMBAI, INDIA"
    p_inst2.font.name = "Segoe UI"
    p_inst2.font.size = Pt(10)
    p_inst2.font.color.rgb = ACCENT_CYAN

    p_inst3 = tf_inst.add_paragraph()
    p_inst3.text = "B.Tech Final Major Project  •  Academic Year 2024–2025"
    p_inst3.font.name = "Segoe UI"
    p_inst3.font.size = Pt(9.5)
    p_inst3.font.color.rgb = TEXT_MUTED

    # Project Title Card (Hero Banner)
    add_card(s1, Inches(0.8), Inches(2.1), Inches(11.733), Inches(2.6), bg_color=CARD_BG, border_color=CARD_BORDER, top_accent=ACCENT_GREEN)

    title_box = s1.shapes.add_textbox(Inches(1.1), Inches(2.3), Inches(11.1), Inches(2.2))
    tf_main = title_box.text_frame
    tf_main.word_wrap = True

    p_badge = tf_main.paragraphs[0]
    p_badge.text = "CYBER-PHYSICAL EDGE-IOT PLATFORM FOR PRECISION AGRICULTURE"
    p_badge.font.name = "Segoe UI"
    p_badge.font.size = Pt(10.5)
    p_badge.font.bold = True
    p_badge.font.color.rgb = ACCENT_GREEN

    p_t = tf_main.add_paragraph()
    p_t.text = "TerraFlow BioAI: A Zone-Aware Edge-IoT Architecture\nfor Closed-Loop Precision Irrigation & Agro-Advisory"
    p_t.font.name = "Segoe UI"
    p_t.font.size = Pt(25)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_WHITE
    p_t.space_before = Pt(8)

    p_sub = tf_main.add_paragraph()
    p_sub.text = "Deterministic Dual-Controller Safety (STM32 + ESP32), 1-D Kalman Signal Conditioning & FAO-56 Volumetric Control"
    p_sub.font.name = "Segoe UI"
    p_sub.font.size = Pt(12)
    p_sub.font.color.rgb = ACCENT_CYAN
    p_sub.space_before = Pt(8)

    # Student Authors Card (3 Columns)
    add_card(s1, Inches(0.8), Inches(5.0), Inches(7.6), Inches(1.9), bg_color=CARD_BG, border_color=CARD_BORDER, top_accent=ACCENT_CYAN)

    auth_box = s1.shapes.add_textbox(Inches(1.0), Inches(5.15), Inches(7.2), Inches(1.6))
    tf_auth = auth_box.text_frame
    tf_auth.word_wrap = True

    p_ah = tf_auth.paragraphs[0]
    p_ah.text = "PROJECT TEAM (EXTC DEPT.)"
    p_ah.font.name = "Segoe UI"
    p_ah.font.size = Pt(10)
    p_ah.font.bold = True
    p_ah.font.color.rgb = ACCENT_CYAN

    # 3 Members neatly formatted
    students = [
        ("Shreyash A Jadhav", "UID: 2023200055", "Embedded Systems & Control"),
        ("Gaurav Hadavale", "UID: 2023200054", "ML Pipeline & IoT Firmware"),
        ("Atharv Bodake", "UID: 2023200028", "Cloud Integration & Analytics")
    ]
    for name, uid, role in students:
        p_mem = tf_auth.add_paragraph()
        p_mem.text = f"•  {name}  |  {uid}  ({role})"
        p_mem.font.name = "Segoe UI"
        p_mem.font.size = Pt(10.5)
        p_mem.font.color.rgb = TEXT_BODY
        p_mem.space_before = Pt(4)

    # Faculty Mentor Card
    add_card(s1, Inches(8.65), Inches(5.0), Inches(3.88), Inches(1.9), bg_color=CARD_BG, border_color=CARD_BORDER, top_accent=ACCENT_AMBER)

    guide_box = s1.shapes.add_textbox(Inches(8.85), Inches(5.15), Inches(3.5), Inches(1.6))
    tf_guide = guide_box.text_frame
    tf_guide.word_wrap = True

    p_gh = tf_guide.paragraphs[0]
    p_gh.text = "PROJECT MENTOR"
    p_gh.font.name = "Segoe UI"
    p_gh.font.size = Pt(10)
    p_gh.font.bold = True
    p_gh.font.color.rgb = ACCENT_AMBER

    p_gn = tf_guide.add_paragraph()
    p_gn.text = "Prof. Milind Paraye"
    p_gn.font.name = "Segoe UI"
    p_gn.font.size = Pt(14)
    p_gn.font.bold = True
    p_gn.font.color.rgb = TEXT_WHITE
    p_gn.space_before = Pt(4)

    p_gd = tf_guide.add_paragraph()
    p_gd.text = "Assistant Professor\nDept. of Electronics & Telecommunication Eng.\nBharatiya Vidya Bhavan's SPIT, Mumbai"
    p_gd.font.name = "Segoe UI"
    p_gd.font.size = Pt(10)
    p_gd.font.color.rgb = TEXT_MUTED
    p_gd.space_before = Pt(4)

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT & MOTIVATION
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "01. Motivation & Technical Gap",
               "The Disconnect in Contemporary Smart Irrigation Systems",
               "Why commercial timer schedules and uncalibrated cloud-only IoT switches fail in real fields")

    # 3 Flaw Cards
    flaws = [
        ("01", "Galvanic Drift & Raw ADC Noise",
         "Resistive soil probes suffer rapid galvanic corrosion in wet soil, causing threshold calibration to drift in weeks. Raw ADC spikes and localized air pockets trigger erratic switching without signal smoothing.",
         ACCENT_AMBER,
         ["• Probe corrosion alters voltage divider ratio",
          "• High-frequency spikes trigger false pump runs",
          "• Uncalibrated % ignores soil water potential"]),
        ("02", "Cloud-Only Actuation Latency & Risk",
         "Dominant architectures stream raw telemetry to remote cloud VMs for neural inference, creating dangerous safety windows during network outages. Loss of Wi-Fi leaves actuators unmonitored.",
         RGBColor(239, 68, 68),  # Red
         ["• Cloud VM round-trip adds 200–800ms latency",
          "• Network drop leaves pump in undefined state",
          "• Single point of failure for safety shutdown"]),
        ("03", "Agronomic Disconnect & Fixed Timers",
         "Most IoT switches hard-code arbitrary rules ('pump ON if < 30%') ignoring soil hydraulics (Field Capacity, Wilting Point) and crop phenological stages (Kc). Timers run blindly regardless of actual delivered water.",
         ACCENT_CYAN,
         ["• 30% moisture is wet for Sand, but dry for Clay",
          "• Fixed 5-minute timer ignores true water depth",
          "• Zero closed-loop root-zone response feedback"])
    ]

    card_w = Inches(3.75)
    card_h = Inches(4.3)
    card_top = Inches(2.0)

    for i, (num, title, desc, accent, bullets) in enumerate(flaws):
        left = Inches(0.8 + i * 3.99)
        add_card(s2, left, card_top, card_w, card_h, bg_color=CARD_BG, border_color=CARD_BORDER, top_accent=accent)

        tb = s2.shapes.add_textbox(left + Inches(0.2), card_top + Inches(0.2), card_w - Inches(0.4), card_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p_num = tf.paragraphs[0]
        p_num.text = f"GAP {num}"
        p_num.font.name = "Segoe UI"
        p_num.font.size = Pt(11)
        p_num.font.bold = True
        p_num.font.color.rgb = accent

        p_t = tf.add_paragraph()
        p_t.text = title
        p_t.font.name = "Segoe UI"
        p_t.font.size = Pt(15)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_WHITE
        p_t.space_before = Pt(4)

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = "Segoe UI"
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = TEXT_MUTED
        p_d.space_before = Pt(8)

        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = b
            p_b.font.name = "Segoe UI"
            p_b.font.size = Pt(10.5)
            p_b.font.color.rgb = TEXT_BODY
            p_b.space_before = Pt(6)

    # Bottom Synthesis Banner
    add_card(s2, Inches(0.8), Inches(6.45), Inches(11.733), Inches(0.75), bg_color=TAG_BG, border_color=ACCENT_GREEN)
    syn_box = s2.shapes.add_textbox(Inches(1.0), Inches(6.5), Inches(11.3), Inches(0.65))
    tf_syn = syn_box.text_frame
    tf_syn.word_wrap = True
    p_syn = tf_syn.paragraphs[0]
    p_syn.text = "CORE RESEARCH OBJECTIVE: Formulate a dual-controller edge architecture where an STM32 executes real-time 1-D Kalman filtering and deterministic local safety, while an ESP32 bridges to an agronomic cloud layer governed by FAO-56 volumetric principles."
    p_syn.font.name = "Segoe UI"
    p_syn.font.size = Pt(11)
    p_syn.font.bold = True
    p_syn.font.color.rgb = ACCENT_GREEN

    # =========================================================================
    # SLIDE 3: HARDWARE DESIGN & DUAL-CONTROLLER TOPOLOGY
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "02. Embedded Hardware Architecture",
               "Deterministic Dual-Controller Topology (STM32 + ESP32)",
               "Decoupling bare-metal safety actuation from cloud telemetry and machine learning interfaces")

    # Column 1: STM32 Authority (Left)
    col_w = Inches(5.72)
    col_h = Inches(5.15)
    left1 = Inches(0.8)
    add_card(s3, left1, Inches(2.0), col_w, col_h, bg_color=CARD_BG, border_color=CARD_BORDER, top_accent=ACCENT_CYAN)

    tb1 = s3.shapes.add_textbox(left1 + Inches(0.25), Inches(2.15), col_w - Inches(0.5), col_h - Inches(0.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p1 = tf1.paragraphs[0]
    p1.text = "LOCAL SAFETY & ACTUATION AUTHORITY"
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(10)
    p1.font.bold = True
    p1.font.color.rgb = ACCENT_CYAN

    p2 = tf1.add_paragraph()
    p2.text = "STM32F103C8T6 (ARM Cortex-M3 @ 72 MHz)"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(16)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_WHITE
    p2.space_before = Pt(2)

    points_stm = [
        ("Deterministic Actuation Authority", "Retains exclusive hardware control over the pump MOSFET driver. Cloud/ML advice is gated through local checks; the cloud never triggers the pin directly."),
        ("On-Chip 1-D Kalman Filter", "Processes raw soil moisture ADC readings directly in C/C++ firmware at 10 Hz, attenuating electrical noise and capillary diffusion artifacts."),
        ("Multi-Sensor Data Acquisition", "Acquires BME280 (I2C: 0x76), Soil Probe (ADC1), Water TDS Meter (ADC2), and Pulse Flow Sensor (Hardware Interrupt EXTI)."),
        ("Hardware Safety Interlocks", "Enforces a strict 180s maximum runtime guard, plausibility bounds, and an Independent Watchdog Timer (IWDG) resetting to PUMP_OFF on faults."),
        ("Actuator Stage Protection", "IRLZ44N logic-level N-channel MOSFET with 220-ohm gate resistor, 10k pull-down to GND, and 1N4007 flyback diode across the DC pump.")
    ]
    for h, d in points_stm:
        p_h = tf1.add_paragraph()
        p_h.text = f"•  {h}: {d}"
        p_h.font.name = "Segoe UI"
        p_h.font.size = Pt(10.5)
        p_h.font.color.rgb = TEXT_BODY
        p_h.space_before = Pt(8)

    # Column 2: ESP32 Gateway (Right)
    left2 = Inches(6.81)
    add_card(s3, left2, Inches(2.0), col_w, col_h, bg_color=CARD_BG, border_color=CARD_BORDER, top_accent=ACCENT_GREEN)

    tb2 = s3.shapes.add_textbox(left2 + Inches(0.25), Inches(2.15), col_w - Inches(0.5), col_h - Inches(0.4))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p3 = tf2.paragraphs[0]
    p3.text = "IOT TELEMETRY & CLOUD GATEWAY"
    p3.font.name = "Segoe UI"
    p3.font.size = Pt(10)
    p3.font.bold = True
    p3.font.color.rgb = ACCENT_GREEN

    p4 = tf2.add_paragraph()
    p4.text = "ESP32 DevKit (Dual-Core Tensilica LX6)"
    p4.font.name = "Segoe UI"
    p4.font.size = Pt(16)
    p4.font.bold = True
    p4.font.color.rgb = TEXT_WHITE
    p4.space_before = Pt(2)

    points_esp = [
        ("UART2 Inter-MCU Bridge", "Communicates with STM32 over hardware UART2 (GPIO16/17) at 115200 baud using structured JSON packet framing with verification."),
        ("Wi-Fi Ingestion & Reconnection", "Connects to 802.11 b/g/n networks with automatic exponential backoff retry. Maintains local ring buffer during network outages."),
        ("Upstream Telemetry Dispatch", "Serializes calibrated sensor payloads and dispatches via HTTPS POST to Node.js/Supabase and the Python ML decision service."),
        ("Agronomic Advice Receiver", "Receives ML recommendations (decision, confidence, reason codes) and relays them to STM32 as decision support packets."),
        ("Fail-Safe Offline Isolation", "If network or server fails, ESP32 safely flags OFFLINE; the STM32 seamlessly maintains local threshold irrigation with zero interruption.")
    ]
    for h, d in points_esp:
        p_h = tf2.add_paragraph()
        p_h.text = f"•  {h}: {d}"
        p_h.font.name = "Segoe UI"
        p_h.font.size = Pt(10.5)
        p_h.font.color.rgb = TEXT_BODY
        p_h.space_before = Pt(8)

    # =========================================================================
    # SLIDE 4: SYSTEM ARCHITECTURE & MASTER FLOW
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "03. End-to-End System Flow",
               "Layer-by-Layer Architectural Integration",
               "Closed-loop feedback trajectory from field sensing to edge filtering, cloud advisory, and volumetric actuation")

    # Center Architecture Image Card
    img_left = Inches(0.8)
    img_top = Inches(2.0)
    img_w = Inches(7.4)
    img_h = Inches(5.15)
    add_card(s4, img_left, img_top, img_w, img_h, bg_color=CARD_BG, border_color=CARD_BORDER, top_accent=ACCENT_CYAN)

    if os.path.exists(ARCH_IMG_PATH):
        try:
            s4.shapes.add_picture(ARCH_IMG_PATH, img_left + Inches(0.15), img_top + Inches(0.2), width=img_w - Inches(0.3))
        except Exception:
            pass

    # Right Callout Cards (The 5 Cooperating Layers)
    layers = [
        ("LAYER 1: SENSING (Z01)", "Capacitive moisture, BME280 (ambient), TDS (water salinity), pulse flow meter, and DC pump MOSFET.", ACCENT_CYAN),
        ("LAYER 2: STM32 SAFETY", "Runs 1-D Kalman filter, enforces 5-state safety FSM, and executes pulse-flow volume cutoffs.", ACCENT_GREEN),
        ("LAYER 3: ESP32 BRIDGE", "Non-blocking UART-to-Wi-Fi serialization, HTTPS REST telemetry, and offline buffering.", ACCENT_AMBER),
        ("LAYER 4: CLOUD & ML", "Supabase knowledge base (FAO-56 rules), OpenWeatherMap API, and Random Forest / XGBoost models.", ACCENT_PURPLE),
        ("LAYER 5: USER ADVISORY", "React dashboard displaying live telemetry, WSI/VPD drying stress, reason codes, and closed-loop trends.", TEXT_WHITE)
    ]

    r_left = Inches(8.45)
    r_w = Inches(4.08)
    card_spacing = Inches(0.98)

    for i, (ltitle, ldesc, laccent) in enumerate(layers):
        c_top = Inches(2.0 + i * 1.05)
        add_card(s4, r_left, c_top, r_w, Inches(0.95), bg_color=CARD_BG, border_color=CARD_BORDER, top_accent=laccent)

        tb_l = s4.shapes.add_textbox(r_left + Inches(0.15), c_top + Inches(0.08), r_w - Inches(0.3), Inches(0.8))
        tf_l = tb_l.text_frame
        tf_l.word_wrap = True

        p_lt = tf_l.paragraphs[0]
        p_lt.text = ltitle
        p_lt.font.name = "Segoe UI"
        p_lt.font.size = Pt(9.5)
        p_lt.font.bold = True
        p_lt.font.color.rgb = laccent

        p_ld = tf_l.add_paragraph()
        p_ld.text = ldesc
        p_ld.font.name = "Segoe UI"
        p_ld.font.size = Pt(9.5)
        p_ld.font.color.rgb = TEXT_BODY
        p_ld.space_before = Pt(2)

    # =========================================================================
    # SLIDE 5: 1-D KALMAN FILTER & FAO-56 CONTROL
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "04. Mathematical Modeling & Control",
               "1-D Kalman Signal Conditioning & FAO-56 Volumetric Actuation",
               "Physics-based signal filtering and volumetric depth calculation eliminating uncalibrated fixed timers")

    # Left Card: Kalman Filter Math
    k_left = Inches(0.8)
    k_w = Inches(5.72)
    k_h = Inches(5.15)
    add_card(s5, k_left, Inches(2.0), k_w, k_h, bg_color=CARD_BG, border_color=CARD_BORDER, top_accent=ACCENT_CYAN)

    tb_k = s5.shapes.add_textbox(k_left + Inches(0.25), Inches(2.15), k_w - Inches(0.5), k_h - Inches(0.4))
    tf_k = tb_k.text_frame
    tf_k.word_wrap = True

    p_kt = tf_k.paragraphs[0]
    p_kt.text = "1-D KALMAN FILTER ON STM32 FIRMWARE"
    p_kt.font.name = "Segoe UI"
    p_kt.font.size = Pt(10)
    p_kt.font.bold = True
    p_kt.font.color.rgb = ACCENT_CYAN

    p_kh = tf_k.add_paragraph()
    p_kh.text = "Optimal Recursive Estimation for Soil Moisture"
    p_kh.font.name = "Segoe UI"
    p_kh.font.size = Pt(15)
    p_kh.font.bold = True
    p_kh.font.color.rgb = TEXT_WHITE
    p_kh.space_before = Pt(2)

    k_points = [
        ("The Challenge", "Capacitive and resistive probes exhibit high-frequency electrical jitter and sudden ADC dips due to localized soil air gaps."),
        ("Time Update (Prediction)", "x̂_k⁻ = x̂_(k-1)  |  P_k⁻ = P_(k-1) + Q\nModels the slow physical diffusion of moisture through soil capillaries."),
        ("Measurement Update (Correction)", "K_k = P_k⁻ / (P_k⁻ + R)  |  x̂_k = x̂_k⁻ + K_k · (z_k - x̂_k⁻)\nDynamically weights incoming ADC readings against estimated state variance."),
        ("Variance Update", "P_k = (1 - K_k) · P_k⁻\nStabilizes recursive error bounds across continuous 24/7 logging."),
        ("Tuning & Performance", "Tuned with Q = 0.01 (process noise) and R = 0.25 (sensor variance).\nAchieves 91.5% jitter reduction (σ² drops from 4.82 to 0.41) with zero lag.")
    ]
    for h, d in k_points:
        p_p = tf_k.add_paragraph()
        p_p.text = f"•  {h}: {d}"
        p_p.font.name = "Segoe UI"
        p_p.font.size = Pt(10)
        p_p.font.color.rgb = TEXT_BODY
        p_p.space_before = Pt(6)

    # Right Card: FAO-56 Volumetric Equations
    f_left = Inches(6.81)
    add_card(s5, f_left, Inches(2.0), k_w, k_h, bg_color=CARD_BG, border_color=CARD_BORDER, top_accent=ACCENT_GREEN)

    tb_f = s5.shapes.add_textbox(f_left + Inches(0.25), Inches(2.15), k_w - Inches(0.5), k_h - Inches(0.4))
    tf_f = tb_f.text_frame
    tf_f.word_wrap = True

    p_ft = tf_f.paragraphs[0]
    p_ft.text = "AGRONOMIC VOLUMETRIC CONTROL"
    p_ft.font.name = "Segoe UI"
    p_ft.font.size = Pt(10)
    p_ft.font.bold = True
    p_ft.font.color.rgb = ACCENT_GREEN

    p_fh = tf_f.add_paragraph()
    p_fh.text = "FAO-56 Water Budgeting (No Fixed Timers)"
    p_fh.font.name = "Segoe UI"
    p_fh.font.size = Pt(15)
    p_fh.font.bold = True
    p_fh.font.color.rgb = TEXT_WHITE
    p_fh.space_before = Pt(2)

    fao_points = [
        ("Crop Evapotranspiration", "ET_c = ET_0 × K_c\nCombines Penman-Monteith reference ET_0 with crop phenological stage coefficient K_c stored in Supabase."),
        ("Net Irrigation Depth (mm)", "d_target = (θ_FC - θ_Kalman) × Z_root × (1 - f_rain)\nReplenishes root-zone soil from current filtered moisture up to Field Capacity (θ_FC), discounted by forecast rainfall."),
        ("Target Water Volume (Liters)", "V_target (L) = d_target (mm) × Area_zone (m²)\nDirectly converts agronomic depth to exact volumetric requirement in Liters."),
        ("Pulse-Flow Integration", "V_delivered = ∫ Q_flow(t) dt = Σ (Pulses × K_cal)\nMeasures physical water delivery through in-line pulse sensor, not time duration."),
        ("Closed-Loop Feedback Rule", "Pump stops when V_delivered ≥ V_target. Re-reads moisture 3 minutes post-watering to verify capillary wetting front response.")
    ]
    for h, d in fao_points:
        p_p = tf_f.add_paragraph()
        p_p.text = f"•  {h}: {d}"
        p_p.font.name = "Segoe UI"
        p_p.font.size = Pt(10)
        p_p.font.color.rgb = TEXT_BODY
        p_p.space_before = Pt(6)

    # =========================================================================
    # SLIDE 6: MACHINE LEARNING MODELS & SENSOR ALIGNMENT
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "05. Machine Learning Decision Support",
               "Sensor-Aligned Machine Learning Intelligence",
               "4 models strictly aligned with real hardware sensors, evaluated with 5-fold cross-validation")

    # 4 Model Grid Cards
    models = [
        ("MODEL 1 (PRIMARY)", "Irrigation Prediction", "XGBoost Classifier",
         "90.80%", "5-Fold CV: 92.00% ± 0.91%",
         "Features: Kalman moisture (23.7%), Rainfall (33.3%), Soil drainage (16.2%), Crop Kc (9.9%), Temp & RH (6.4%). Predicts IRRIGATE / NO_IRRIGATION with explainable reason codes.",
         ACCENT_GREEN),
        ("MODEL 2", "Crop Recommendation", "Random Forest (200 trees)",
         "99.32%", "5-Fold CV: 99.45% ± 0.23%",
         "Features: BME280 temperature, humidity, soil test NPK, pH, and rainfall. Ranks 22 candidate crops to return the Top 5 suitability matches with confidence scores.",
         ACCENT_CYAN),
        ("MODEL 3", "Fertilizer Advisory", "XGBoost Classifier",
         "100.0%", "5-Fold CV: 99.90% ± 0.12%",
         "Features: Soil-test N, P, K deficit, crop type, growth stage, soil moisture. Prescribes exact commercial fertilizer grade (Urea, DAP, 10-26-26, 14-35-14, 28-28).",
         ACCENT_AMBER),
        ("MODEL 4", "Soil Classification", "Random Forest Classifier",
         "84.50%", "5-Fold CV: 84.80% ± 0.78%",
         "Features: Moisture retention dynamics, ambient climate, baseline chemistry. Classifies soil class into Black, Red, Alluvial, Sandy, Clayey, Loamy.",
         ACCENT_PURPLE)
    ]

    m_w = Inches(5.72)
    m_h = Inches(2.05)

    positions = [
        (Inches(0.8), Inches(2.0)),
        (Inches(6.81), Inches(2.0)),
        (Inches(0.8), Inches(4.25)),
        (Inches(6.81), Inches(4.25))
    ]

    for (pos, (tag, name, algo, acc, cv, desc, col)) in zip(positions, models):
        x, y = pos
        add_card(s6, x, y, m_w, m_h, bg_color=CARD_BG, border_color=CARD_BORDER, top_accent=col)

        tb_m = s6.shapes.add_textbox(x + Inches(0.2), y + Inches(0.12), m_w - Inches(0.4), m_h - Inches(0.25))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True

        p_t = tf_m.paragraphs[0]
        p_t.text = f"{tag}  •  {algo}"
        p_t.font.name = "Segoe UI"
        p_t.font.size = Pt(9.5)
        p_t.font.bold = True
        p_t.font.color.rgb = col

        p_n = tf_m.add_paragraph()
        p_n.text = f"{name}  —  Accuracy: {acc}"
        p_n.font.name = "Segoe UI"
        p_n.font.size = Pt(13.5)
        p_n.font.bold = True
        p_n.font.color.rgb = TEXT_WHITE
        p_n.space_before = Pt(2)

        p_cv = tf_m.add_paragraph()
        p_cv.text = cv
        p_cv.font.name = "Segoe UI"
        p_cv.font.size = Pt(9.5)
        p_cv.font.color.rgb = col
        p_cv.space_before = Pt(1)

        p_d = tf_m.add_paragraph()
        p_d.text = desc
        p_d.font.name = "Segoe UI"
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = TEXT_BODY
        p_d.space_before = Pt(4)

    # Bottom Honesty Callout
    add_card(s6, Inches(0.8), Inches(6.5), Inches(11.733), Inches(0.7), bg_color=TAG_BG, border_color=ACCENT_GREEN)
    tb_hon = s6.shapes.add_textbox(Inches(1.0), Inches(6.55), Inches(11.3), Inches(0.6))
    tf_hon = tb_hon.text_frame
    tf_hon.word_wrap = True
    p_hon = tf_hon.paragraphs[0]
    p_hon.text = "AGRONOMIC HONESTY LOCK: TDS Meter V1.0 measures dissolved solids in irrigation water (salinity/EC), NOT soil NPK. Nitrogen, Phosphorus, Potassium, and pH are derived from accredited Soil Health Card laboratory inputs stored in Supabase."
    p_hon.font.name = "Segoe UI"
    p_hon.font.size = Pt(10.5)
    p_hon.font.bold = True
    p_hon.font.color.rgb = ACCENT_GREEN

    # =========================================================================
    # SLIDE 7: SUPABASE KNOWLEDGE BASE & CLOSED-LOOP VERIFICATION
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "06. Knowledge Base & Benchtop Proof",
               "Agronomic Knowledge Base & Benchtop Physical Proof",
               "80+ structured FAO-56 knowledge rows in Supabase and verified closed-loop hardware response")

    # Left: Supabase Knowledge Base (Structured Tables)
    b_left = Inches(0.8)
    b_w = Inches(5.72)
    b_h = Inches(5.15)
    add_card(s7, b_left, Inches(2.0), b_w, b_h, bg_color=CARD_BG, border_color=CARD_BORDER, top_accent=ACCENT_CYAN)

    tb_sb = s7.shapes.add_textbox(b_left + Inches(0.25), Inches(2.15), b_w - Inches(0.5), b_h - Inches(0.4))
    tf_sb = tb_sb.text_frame
    tf_sb.word_wrap = True

    p_sbt = tf_sb.paragraphs[0]
    p_sbt.text = "SUPABASE AGRONOMIC KNOWLEDGE BASE"
    p_sbt.font.name = "Segoe UI"
    p_sbt.font.size = Pt(10)
    p_sbt.font.bold = True
    p_sbt.font.color.rgb = ACCENT_CYAN

    p_sbh = tf_sb.add_paragraph()
    p_sbh.text = "10 Relational Tables & 80+ Pre-Seeded Rows"
    p_sbh.font.name = "Segoe UI"
    p_sbh.font.size = Pt(15)
    p_sbh.font.bold = True
    p_sbh.font.color.rgb = TEXT_WHITE
    p_sbh.space_before = Pt(2)

    sb_points = [
        ("Operational Telemetry Tables", "zones (zone metadata), sensor_data (10-param time series), soil_tests (lab NPK entries), irrigation_events (actuation history), advisories (ML logs)."),
        ("FAO-56 Phenological Stages (crop_stages)", "16 detailed stage records across 4 core crops (Rice, Wheat, Maize, Tomato) storing duration, water demand, and official Kc crop coefficients (e.g., Rice Mid-season Kc = 1.20)."),
        ("Hydrological Soil Baselines (soil_profiles)", "Field Capacity, Wilting Point, and drainage velocity for Black (Vertisol: 38% FC), Red (Alfisol: 22% FC), Alluvial (28% FC), and Sandy (12% FC) soils."),
        ("ICAR STCR Rules (fertilizer_rules)", "Crop/stage specific nutrient response logic mapping NPK deficits to commercial fertilizer dosing with full academic citation provenance."),
        ("Explainable Reason Codes", "Every recommendation logged with audited codes: RUN:MOISTURE_LOW, RUN:WATER_DEFICIT, SKIP:RAIN_CONTEXT, FAULT:RUNTIME_EXCEEDED.")
    ]
    for h, d in sb_points:
        p_p = tf_sb.add_paragraph()
        p_p.text = f"•  {h}: {d}"
        p_p.font.name = "Segoe UI"
        p_p.font.size = Pt(10)
        p_p.font.color.rgb = TEXT_BODY
        p_p.space_before = Pt(6)

    # Right: Benchtop Verification & Metrics
    v_left = Inches(6.81)
    add_card(s7, v_left, Inches(2.0), b_w, b_h, bg_color=CARD_BG, border_color=CARD_BORDER, top_accent=ACCENT_GREEN)

    tb_v = s7.shapes.add_textbox(v_left + Inches(0.25), Inches(2.15), b_w - Inches(0.5), b_h - Inches(0.4))
    tf_v = tb_v.text_frame
    tf_v.word_wrap = True

    p_vt = tf_v.paragraphs[0]
    p_vt.text = "BENCHTOP EXPERIMENTAL VALIDATION"
    p_vt.font.name = "Segoe UI"
    p_vt.font.size = Pt(10)
    p_vt.font.bold = True
    p_vt.font.color.rgb = ACCENT_GREEN

    p_vh = tf_v.add_paragraph()
    p_vh.text = "Prototype Verification & Hardware Safety Gates"
    p_vh.font.name = "Segoe UI"
    p_vh.font.size = Pt(15)
    p_vh.font.bold = True
    p_vh.font.color.rgb = TEXT_WHITE
    p_vh.space_before = Pt(2)

    v_points = [
        ("UART Latency & Packet Reliability", "Dual-MCU UART2 (115200 baud) packet transfer latency measured at < 12 ms with 0% CRC frame loss across 10,000 continuous transmissions."),
        ("Pulse-Flow Volumetric Accuracy", "Benchtop calibrated delivery verified within ± 3.5% of target volume, eliminating the chronic over-irrigation typical of fixed timers."),
        ("Deterministic Safety Cutoff", "Hard-coded 180s maximum runtime guard independently aborts pump actuation if flow target is not reached (e.g. pipe block or dry supply)."),
        ("Sensor Plausibility Gate", "ADC open-circuit or unplugged sensor immediately blocks pump actuation, throwing safe fallback alert rather than erroneous watering."),
        ("Physical Closed-Loop Response", "Post-irrigation sensor feedback verifies capillary wetting front percolation (Δθ = +18% to +24%) within 3 minutes of pump termination.")
    ]
    for h, d in v_points:
        p_p = tf_v.add_paragraph()
        p_p.text = f"•  {h}: {d}"
        p_p.font.name = "Segoe UI"
        p_p.font.size = Pt(10)
        p_p.font.color.rgb = TEXT_BODY
        p_p.space_before = Pt(6)

    # =========================================================================
    # SLIDE 8: CONCLUSION & RESEARCH ROADMAP
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "07. Conclusion & Viva Defense",
               "Summary of Contributions & Academic Defense",
               "Core technical novelties, IEEE research paper positioning, and future deployment roadmap")

    # 3 Conclusion Cards
    cards_c = [
        ("INNOVATION 01", "Deterministic Edge Safety Authority",
         "Completely decouples physical high-voltage pump actuation from cloud latency, Wi-Fi dropouts, and API downtime. The bare-metal STM32 firmware guarantees fail-safe OFF behavior under all fault conditions.",
         ACCENT_CYAN,
         ["• Cloud advises, edge controls",
          "• Independent watchdog recovery",
          "• Offline autonomous fallback"]),
        ("INNOVATION 02", "Calibrated Closed-Loop Hydrology",
         "Replaces uncalibrated timers with pulse-flow integration and post-irrigation capillary feedback. Integrates 1-D Kalman signal filtering with FAO-56 Penman-Monteith crop evapotranspiration coefficients (Kc).",
         ACCENT_GREEN,
         ["• Measured Liter delivery vs fixed time",
          "• 91.5% moisture ADC jitter reduction",
          "• Verified wetting front feedback"]),
        ("INNOVATION 03", "Transparent Explainable AI (XAI)",
         "Eliminates black-box agricultural decisions. All 4 ML models (Irrigation, Crop, Fertilizer, Soil) provide human-readable reason codes (RUN:MOISTURE_LOW) backed by 80+ FAO-56/ICAR knowledge base rules in Supabase.",
         ACCENT_AMBER,
         ["• Provenance tracking for every rule",
          "• Verified Soil Health Card integration",
          "• 99.3% crop & 90.8% irrigation accuracy"])
    ]

    c_w = Inches(3.75)
    c_h = Inches(4.3)
    c_top = Inches(2.0)

    for i, (tag, title, desc, col, bullets) in enumerate(cards_c):
        left = Inches(0.8 + i * 3.99)
        add_card(s8, left, c_top, c_w, c_h, bg_color=CARD_BG, border_color=CARD_BORDER, top_accent=col)

        tb_c = s8.shapes.add_textbox(left + Inches(0.2), c_top + Inches(0.2), c_w - Inches(0.4), c_h - Inches(0.4))
        tf_c = tb_c.text_frame
        tf_c.word_wrap = True

        p_t = tf_c.paragraphs[0]
        p_t.text = tag
        p_t.font.name = "Segoe UI"
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = col

        p_tit = tf_c.add_paragraph()
        p_tit.text = title
        p_tit.font.name = "Segoe UI"
        p_tit.font.size = Pt(15)
        p_tit.font.bold = True
        p_tit.font.color.rgb = TEXT_WHITE
        p_tit.space_before = Pt(4)

        p_d = tf_c.add_paragraph()
        p_d.text = desc
        p_d.font.name = "Segoe UI"
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = TEXT_MUTED
        p_d.space_before = Pt(8)

        for b in bullets:
            p_b = tf_c.add_paragraph()
            p_b.text = b
            p_b.font.name = "Segoe UI"
            p_b.font.size = Pt(10.5)
            p_b.font.color.rgb = TEXT_BODY
            p_b.space_before = Pt(6)

    # Bottom Future Scope & Publication Bar
    add_card(s8, Inches(0.8), Inches(6.45), Inches(11.733), Inches(0.75), bg_color=CARD_BG_LIGHT, border_color=ACCENT_CYAN)
    f_box = s8.shapes.add_textbox(Inches(1.0), Inches(6.5), Inches(11.3), Inches(0.65))
    tf_f = f_box.text_frame
    tf_f.word_wrap = True
    p_f = tf_f.paragraphs[0]
    p_f.text = "RESEARCH STATUS: Prepared and submitted as an IEEE Conference Paper ('TerraFlow BioAI: A Zone-Aware Edge-IoT Architecture for Closed-Loop Precision Irrigation'). Future Roadmap: LoRaWAN multi-zone scaling (TF01 → TF0N) and multi-week Kharif/Rabi field validation."
    p_f.font.name = "Segoe UI"
    p_f.font.size = Pt(10.5)
    p_f.font.bold = True
    p_f.font.color.rgb = ACCENT_CYAN

    # Save Presentation
    output_pptx = os.path.join(BASE_DIR, "TerraFlow_BioAI_Major_Project_Presentation.pptx")
    prs.save(output_pptx)
    print(f"[OK] Presentation saved successfully: {output_pptx}")
    return output_pptx


if __name__ == "__main__":
    build_presentation()
