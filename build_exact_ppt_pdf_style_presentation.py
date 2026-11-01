"""
TerraFlow BioAI - Major Project Official Presentation Generator
Exact Re-creation matching the visual texture, dark-forest aesthetic, typography,
and native architecture diagram of PPT.pdf.

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

# ── Exact Color Palette from PPT.pdf ──────────────────────────────────────────
BG_CANVAS      = RGBColor(10, 26, 19)     # #0A1A13 Dark Forest Canvas
CARD_BG        = RGBColor(26, 47, 40)     # #1A2F28 Dark Pine Slate Card
CARD_BORDER    = RGBColor(38, 68, 58)     # #26443A Subtle Pine Border
ACCENT_GREEN   = RGBColor(0, 200, 121)    # #00C879 Primary Emerald Ribbon
ACCENT_CYAN    = RGBColor(0, 176, 255)    # #00B0FF Water Drop Cyan
ACCENT_AMBER   = RGBColor(255, 145, 0)    # #FF9100 Thermometer Amber
ACCENT_RED     = RGBColor(255, 23, 68)    # #FF1744 Disease/Warning Red
ACCENT_LIME    = RGBColor(0, 230, 118)    # #00E676 Bright Green Badge
ACCENT_PURPLE  = RGBColor(168, 85, 247)   # #A855F7 Intelligence Purple

TEXT_WHITE     = RGBColor(255, 255, 255)  # #FFFFFF Pure White
TEXT_MINT      = RGBColor(110, 231, 183)  # #6EE7B7 Soft Mint Subtitle
TEXT_SLATE     = RGBColor(203, 213, 225)  # #CBD5E1 Light Slate Body
TEXT_MUTED     = RGBColor(148, 163, 184)  # #94A3B8 Muted Gray

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICONS_DIR = os.path.join(BASE_DIR, "ppt_pdf_extracted_icons")
SPIT_LOGO_PATH = os.path.join(BASE_DIR, "extracted_assets", "spit_logo_0.png")
LEAF_LOGO_PATH = os.path.join(ICONS_DIR, "page_1_img_1.jpeg")


def set_canvas_bg(slide):
    """Sets the signature dark forest-green canvas background."""
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_CANVAS
    bg.line.fill.background()

    # Top vibrant emerald ribbon
    ribbon = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.08))
    ribbon.fill.solid()
    ribbon.fill.fore_color.rgb = ACCENT_GREEN
    ribbon.line.fill.background()

    # Bottom subtle footer
    ft = slide.shapes.add_textbox(Inches(10.5), Inches(7.1), Inches(2.3), Inches(0.3))
    tf_f = ft.text_frame
    tf_f.word_wrap = True
    p_f = tf_f.paragraphs[0]
    p_f.text = "TerraFlow BioAI"
    p_f.font.name = "Segoe UI"
    p_f.font.size = Pt(11)
    p_f.font.color.rgb = RGBColor(74, 120, 102)
    p_f.alignment = PP_ALIGN.RIGHT
    return bg


def add_slide_header(slide, title, subtitle):
    """Adds the clean signature header matching PPT.pdf."""
    # Title
    t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.42), Inches(11.5), Inches(0.65))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title
    p_t.font.name = "Segoe UI"
    p_t.font.size = Pt(28)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_WHITE

    # Subtitle
    s_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.1), Inches(11.5), Inches(0.4))
    tf_s = s_box.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = 0
    p_s = tf_s.paragraphs[0]
    p_s.text = subtitle
    p_s.font.name = "Segoe UI"
    p_s.font.size = Pt(13)
    p_s.font.italic = True
    p_s.font.color.rgb = TEXT_MINT


def create_dark_card(slide, left, top, width, height, border_color=CARD_BORDER, left_accent=None):
    """Creates a dark forest pine card matching PPT.pdf."""
    card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = border_color
    card.line.width = Pt(1.2)

    if left_accent:
        stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(0.08), height)
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = left_accent
        stripe.line.fill.background()

    return card


def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Matches page_1.png of PPT.pdf)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s1)

    # SPIT Official Maroon Logo (Top Left)
    if os.path.exists(SPIT_LOGO_PATH):
        try:
            s1.shapes.add_picture(SPIT_LOGO_PATH, Inches(0.8), Inches(0.5), height=Inches(1.2))
        except Exception as e:
            print(f"Error loading SPIT logo: {e}")

    # College Title (Next to Logo)
    col_box = s1.shapes.add_textbox(Inches(2.2), Inches(0.55), Inches(10.0), Inches(1.1))
    tf_col = col_box.text_frame
    tf_col.word_wrap = True

    p_c1 = tf_col.paragraphs[0]
    p_c1.text = "Sardar Patel Institute of Technology (SPIT)"
    p_c1.font.name = "Segoe UI"
    p_c1.font.size = Pt(14)
    p_c1.font.bold = True
    p_c1.font.color.rgb = TEXT_WHITE

    p_c2 = tf_col.add_paragraph()
    p_c2.text = "Dept. of Electronics & Telecommunication Eng.  |  B.Tech Major Project Presentation  •  Academic Year 2026–2027"
    p_c2.font.name = "Segoe UI"
    p_c2.font.size = Pt(11)
    p_c2.font.color.rgb = ACCENT_GREEN
    p_c2.space_before = Pt(3)

    # Big Green Leaf Logo in Center (from PPT.pdf)
    if os.path.exists(LEAF_LOGO_PATH):
        try:
            s1.shapes.add_picture(LEAF_LOGO_PATH, Inches(6.05), Inches(1.9), height=Inches(1.4))
        except Exception as e:
            print(f"Error loading leaf logo: {e}")

    # Project Title
    main_box = s1.shapes.add_textbox(Inches(0.8), Inches(3.4), Inches(11.733), Inches(1.3))
    tf_m = main_box.text_frame
    tf_m.word_wrap = True

    p_m1 = tf_m.paragraphs[0]
    p_m1.text = "TerraFlow BioAI"
    p_m1.font.name = "Segoe UI"
    p_m1.font.size = Pt(44)
    p_m1.font.bold = True
    p_m1.font.color.rgb = TEXT_WHITE
    p_m1.alignment = PP_ALIGN.CENTER

    p_m2 = tf_m.add_paragraph()
    p_m2.text = "Closed-Loop Embedded Precision Irrigation & Environmental Intelligence"
    p_m2.font.name = "Segoe UI"
    p_m2.font.size = Pt(14)
    p_m2.font.italic = True
    p_m2.font.color.rgb = ACCENT_GREEN
    p_m2.alignment = PP_ALIGN.CENTER
    p_m2.space_before = Pt(6)

    # Bottom Two Cards (Group Members & Mentor)
    # Left Card: Group Members
    create_dark_card(s1, Inches(1.2), Inches(4.9), Inches(5.2), Inches(1.9), left_accent=ACCENT_GREEN)
    gm_box = s1.shapes.add_textbox(Inches(1.5), Inches(5.05), Inches(4.7), Inches(1.6))
    tf_gm = gm_box.text_frame
    tf_gm.word_wrap = True

    p_gh = tf_gm.paragraphs[0]
    p_gh.text = "Group Members (EXTC Dept.)"
    p_gh.font.name = "Segoe UI"
    p_gh.font.size = Pt(12)
    p_gh.font.bold = True
    p_gh.font.color.rgb = ACCENT_GREEN

    members = [
        ("Shreyash A Jadhav", "2023200055"),
        ("Gaurav Hadavale", "2023200054"),
        ("Atharv Bodake", "2023200028")
    ]
    for name, uid in members:
        p_mem = tf_gm.add_paragraph()
        p_mem.text = f"{name}   (UID: {uid})"
        p_mem.font.name = "Segoe UI"
        p_mem.font.size = Pt(12)
        p_mem.font.color.rgb = TEXT_WHITE
        p_mem.space_before = Pt(4)

    # Right Card: Project Mentor
    create_dark_card(s1, Inches(6.933), Inches(4.9), Inches(5.2), Inches(1.9), left_accent=ACCENT_AMBER)
    pm_box = s1.shapes.add_textbox(Inches(7.233), Inches(5.05), Inches(4.7), Inches(1.6))
    tf_pm = pm_box.text_frame
    tf_pm.word_wrap = True

    p_mh = tf_pm.paragraphs[0]
    p_mh.text = "Project Mentor"
    p_mh.font.name = "Segoe UI"
    p_mh.font.size = Pt(12)
    p_mh.font.bold = True
    p_mh.font.color.rgb = ACCENT_AMBER

    p_mn = tf_pm.add_paragraph()
    p_mn.text = "Prof. Milind Paraye"
    p_mn.font.name = "Segoe UI"
    p_mn.font.size = Pt(16)
    p_mn.font.bold = True
    p_mn.font.color.rgb = TEXT_WHITE
    p_mn.space_before = Pt(6)

    p_md = tf_pm.add_paragraph()
    p_md.text = "Assistant Professor\nDept. of Electronics & Telecommunication Eng.\nSardar Patel Institute of Technology (SPIT)"
    p_md.font.name = "Segoe UI"
    p_md.font.size = Pt(11)
    p_md.font.color.rgb = TEXT_SLATE
    p_md.space_before = Pt(4)

    # =========================================================================
    # SLIDE 2: THE PROBLEM (Matches page_2.png of PPT.pdf + User's additions)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s2)
    add_slide_header(s2, "The Problem", "What smallholder and real-world farmers face every day in the field")

    # 4 Problem Cards (2x2 Grid) matching exact layout of PPT.pdf page 2
    c_w = Inches(5.65)
    c_h = Inches(2.4)
    x1 = Inches(0.8)
    x2 = Inches(6.88)
    y1 = Inches(1.8)
    y2 = Inches(4.55)

    problems = [
        # (x, y, icon_filename, title, title_color, desc)
        (x1, y1, "page_2_img_1.jpeg", "Schedule-Based Irrigation", ACCENT_CYAN,
         "Farmers water crops on fixed schedules, not on actual soil demand — leading to overwatering or drought stress, root hypoxia, and immense water waste."),

        (x2, y1, "page_2_img_2.jpeg", "No Real-Time Soil Data", ACCENT_AMBER,
         "Zero visibility into soil moisture, temperature, or water salinity. Farming decisions rely purely on guesswork, surface feel, and manual trial-and-error."),

        (x1, y2, "page_2_img_3.jpeg", "Rigid Hardcoded Calibration Flaws", ACCENT_RED,
         "Existing IoT setups rely on fragile, hardcoded sensor thresholds that drift and fail across different soil textures. Farmers need an adaptive ML model that learns soil dynamics, not manual recalibration values."),

        (x2, y2, "page_2_img_4.jpeg", "Targeting Hardcore Farmers", ACCENT_LIME,
         "Smallholder farmers in the field need a set-and-forget, autonomous closed-loop system. It must run deterministically on the edge without complex manual setup, app bloat, or cloud dependency.")
    ]

    for px, py, icon_name, ptitle, pcol, pdesc in problems:
        create_dark_card(s2, px, py, c_w, c_h)

        # Icon
        icon_path = os.path.join(ICONS_DIR, icon_name)
        if os.path.exists(icon_path):
            try:
                s2.shapes.add_picture(icon_path, px + Inches(0.35), py + Inches(0.28), height=Inches(0.65))
            except Exception:
                pass

        # Text Box
        tb_p = s2.shapes.add_textbox(px + Inches(1.2), py + Inches(0.25), c_w - Inches(1.4), c_h - Inches(0.4))
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
        p_pd.font.size = Pt(12)
        p_pd.font.color.rgb = TEXT_SLATE
        p_pd.space_before = Pt(8)

    # =========================================================================
    # SLIDE 3: SYSTEM ARCHITECTURE (Matches page_3.png of PPT.pdf EXACTLY)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s3)
    add_slide_header(s3, "System Architecture", "End-to-end data flow from sensors to dashboard")

    # 5 Horizontal Process Boxes with arrows (Exact match to PPT.pdf page 3)
    box_w = Inches(2.05)
    box_h = Inches(1.2)
    box_y = Inches(1.8)
    arrow_w = Inches(0.35)

    stages = [
        ("HARDWARE", "5 Sensors + STM32", ACCENT_LIME),
        ("ACTUATION", "MOSFET + Pump", ACCENT_AMBER),
        ("TELEMETRY", "ESP32 Wi-Fi", ACCENT_CYAN),
        ("BACKEND", "Node.js + Supabase", ACCENT_LIME),
        ("INTELLIGENCE", "ML + Dashboard", ACCENT_AMBER)
    ]

    for idx, (stitle, ssub, scol) in enumerate(stages):
        bx = Inches(0.8 + idx * 2.42)
        # Stage Box
        sbox = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, bx, box_y, box_w, box_h)
        sbox.fill.solid()
        sbox.fill.fore_color.rgb = CARD_BG
        sbox.line.color.rgb = scol
        sbox.line.width = Pt(2.0)

        tf_sb = sbox.text_frame
        tf_sb.word_wrap = True
        p_s1 = tf_sb.paragraphs[0]
        p_s1.text = stitle
        p_s1.font.name = "Segoe UI"
        p_s1.font.size = Pt(12)
        p_s1.font.bold = True
        p_s1.font.color.rgb = scol
        p_s1.alignment = PP_ALIGN.CENTER

        p_s2 = tf_sb.add_paragraph()
        p_s2.text = ssub
        p_s2.font.name = "Segoe UI"
        p_s2.font.size = Pt(10.5)
        p_s2.font.color.rgb = TEXT_SLATE
        p_s2.alignment = PP_ALIGN.CENTER
        p_s2.space_before = Pt(6)

        # Connecting Arrow (for first 4 boxes)
        if idx < 4:
            arr_x = bx + box_w + Inches(0.02)
            arr_y = box_y + Inches(0.45)
            arr = s3.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, arr_x, arr_y, Inches(0.33), Inches(0.28))
            arr.fill.solid()
            arr.fill.fore_color.rgb = RGBColor(74, 120, 102)
            arr.line.fill.background()

    # 5 Numbered Rows Below (Exact match to PPT.pdf page 3)
    rows = [
        ("1", "Sensors → STM32",
         "5 sensors continuously acquired via ADC, I2C, OneWire. STM32 filters data and runs local decision logic."),
        ("2", "Local Control Loop",
         "STM32 evaluates moisture + humidity + temperature thresholds. Activates MOSFET → pump if stress detected. Validates result."),
        ("3", "Wireless Telemetry",
         "STM32 serializes JSON over UART to ESP32. ESP sends HTTP POST to Node.js backend over Wi-Fi."),
        ("4", "Backend Processing",
         "Node.js computes WSI, DRI indices. Calls Python ML microservice. Stores everything in Supabase PostgreSQL."),
        ("5", "Dashboard + AI",
         "React dashboard polls /latest. Displays live sensor cards, charts, agro-indices, pump state, and ML irrigation prediction.")
    ]

    row_start_y = Inches(3.35)
    row_h = Inches(0.68)

    for i, (num, label, desc) in enumerate(rows):
        ry = row_start_y + Inches(i * 0.72)

        # Green Number Square
        sq = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), ry, Inches(0.48), Inches(0.48))
        sq.fill.solid()
        sq.fill.fore_color.rgb = ACCENT_LIME
        sq.line.fill.background()
        tf_sq = sq.text_frame
        p_sq = tf_sq.paragraphs[0]
        p_sq.text = num
        p_sq.font.name = "Segoe UI"
        p_sq.font.size = Pt(14)
        p_sq.font.bold = True
        p_sq.font.color.rgb = RGBColor(10, 26, 19)
        p_sq.alignment = PP_ALIGN.CENTER

        # Label (Green bold)
        lbl_box = s3.shapes.add_textbox(Inches(1.45), ry - Inches(0.04), Inches(2.5), Inches(0.55))
        tf_lbl = lbl_box.text_frame
        tf_lbl.word_wrap = True
        p_lbl = tf_lbl.paragraphs[0]
        p_lbl.text = label
        p_lbl.font.name = "Segoe UI"
        p_lbl.font.size = Pt(12)
        p_lbl.font.bold = True
        p_lbl.font.color.rgb = ACCENT_LIME

        # Description (White/Slate)
        desc_box = s3.shapes.add_textbox(Inches(4.1), ry - Inches(0.04), Inches(8.4), Inches(0.55))
        tf_desc = desc_box.text_frame
        tf_desc.word_wrap = True
        p_desc = tf_desc.paragraphs[0]
        p_desc.text = desc
        p_desc.font.name = "Segoe UI"
        p_desc.font.size = Pt(11.5)
        p_desc.font.color.rgb = TEXT_SLATE

    # =========================================================================
    # SLIDE 4: HARDWARE CORE (Matches page_5.png of PPT.pdf)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s4)
    add_slide_header(s4, "Hardware Core",
                     "STM32F103C8T6 & ESP32 — Bare-metal safety, power architecture, and actuation circuit")

    # Top Left Card: STM32F103C8T6 Blue Pill
    create_dark_card(s4, Inches(0.8), Inches(1.8), Inches(5.65), Inches(3.45), left_accent=ACCENT_CYAN)

    stm_icon_path = os.path.join(ICONS_DIR, "page_5_img_1.jpeg")
    if os.path.exists(stm_icon_path):
        try:
            s4.shapes.add_picture(stm_icon_path, Inches(1.05), Inches(2.0), height=Inches(0.65))
        except Exception:
            pass

    tb_s = s4.shapes.add_textbox(Inches(1.8), Inches(2.0), Inches(4.5), Inches(3.1))
    tf_s = tb_s.text_frame
    tf_s.word_wrap = True

    p_sh = tf_s.paragraphs[0]
    p_sh.text = "STM32F103C8T6 Blue Pill"
    p_sh.font.name = "Segoe UI"
    p_sh.font.size = Pt(15)
    p_sh.font.bold = True
    p_sh.font.color.rgb = ACCENT_CYAN

    stm_pts = [
        "▸ ARM Cortex-M3 @ 72 MHz — Deterministic bare-metal safety",
        "▸ 12-bit ADC — 0 to 4095 range (PA0 Moisture, PA1 TDS)",
        "▸ Hardware USART1 + USART2 (115200 baud link to ESP32)",
        "▸ I2C on PB6/PB7 — BME280 multi-variable climate sensor",
        "▸ Pulse-Flow Hardware Interrupt: terminates on volume target",
        "▸ Local decision engine — 100% fail-safe; zero cloud dependency"
    ]
    for pt in stm_pts:
        p_p = tf_s.add_paragraph()
        p_p.text = pt
        p_p.font.name = "Segoe UI"
        p_p.font.size = Pt(11)
        p_p.font.color.rgb = TEXT_SLATE
        p_p.space_before = Pt(4)

    # Top Right Card: MOSFET Actuation Circuit
    create_dark_card(s4, Inches(6.88), Inches(1.8), Inches(5.65), Inches(3.45), left_accent=ACCENT_AMBER)

    mos_icon_path = os.path.join(ICONS_DIR, "page_5_img_2.jpeg")
    if os.path.exists(mos_icon_path):
        try:
            s4.shapes.add_picture(mos_icon_path, Inches(7.13), Inches(2.0), height=Inches(0.65))
        except Exception:
            pass

    tb_m = s4.shapes.add_textbox(Inches(7.88), Inches(2.0), Inches(4.5), Inches(3.1))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True

    p_mh = tf_m.paragraphs[0]
    p_mh.text = "MOSFET Actuation Circuit"
    p_mh.font.name = "Segoe UI"
    p_mh.font.size = Pt(15)
    p_mh.font.bold = True
    p_mh.font.color.rgb = ACCENT_AMBER

    mos_pts = [
        "▸ IRLZ44N — Logic-level N-channel MOSFET gate drive",
        "▸ 220Ω gate resistor from PB0 + 10kΩ pull-down (safe default OFF)",
        "▸ 1N4007 flyback diode across 12V DC pump inductive load",
        "▸ Silent, fast solid-state switching — zero mechanical contact wear",
        "▸ 180s Independent Watchdog (IWDG) hard runaway prevention",
        "▸ Closed-loop delivery: Water source → Pump → Flow Meter → Soil"
    ]
    for pt in mos_pts:
        p_p = tf_m.add_paragraph()
        p_p.text = pt
        p_p.font.name = "Segoe UI"
        p_p.font.size = Pt(11)
        p_p.font.color.rgb = TEXT_SLATE
        p_p.space_before = Pt(4)

    # Bottom Full-Width Card: Power Architecture (Exact match to PPT.pdf page 5)
    create_dark_card(s4, Inches(0.8), Inches(5.45), Inches(11.733), Inches(1.4))

    tb_pa = s4.shapes.add_textbox(Inches(1.05), Inches(5.55), Inches(11.2), Inches(0.3))
    tf_pa = tb_pa.text_frame
    p_pah = tf_pa.paragraphs[0]
    p_pah.text = "Power Architecture"
    p_pah.font.name = "Segoe UI"
    p_pah.font.size = Pt(12)
    p_pah.font.bold = True
    p_pah.font.color.rgb = ACCENT_GREEN

    # 4 Power Stage Blocks
    pw_stages = [
        ("5V 2A Adapter", Inches(1.05)),
        ("LM2596 Buck", Inches(3.8)),
        ("3.3V Rail", Inches(6.55)),
        ("STM32 + ESP32 + BME280\n+ TDS + Moisture Sensors", Inches(9.1))
    ]
    for i, (ptext, px) in enumerate(pw_stages):
        p_blk = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, px, Inches(5.95), Inches(2.2), Inches(0.72))
        p_blk.fill.solid()
        p_blk.fill.fore_color.rgb = RGBColor(18, 38, 30)
        p_blk.line.color.rgb = CARD_BORDER

        tf_pb = p_blk.text_frame
        tf_pb.word_wrap = True
        p_ptx = tf_pb.paragraphs[0]
        p_ptx.text = ptext
        p_ptx.font.name = "Segoe UI"
        p_ptx.font.size = Pt(10)
        p_ptx.font.bold = True
        p_ptx.font.color.rgb = TEXT_WHITE
        p_ptx.alignment = PP_ALIGN.CENTER

        if i < 3:
            arr_px = px + Inches(2.25)
            arr_p = s4.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, arr_px, Inches(6.15), Inches(0.25), Inches(0.22))
            arr_p.fill.solid()
            arr_p.fill.fore_color.rgb = ACCENT_GREEN
            arr_p.line.fill.background()

    # =========================================================================
    # SLIDE 5: MACHINE LEARNING INTELLIGENCE (Matches page_7.png of PPT.pdf)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s5)
    add_slide_header(s5, "ML-Assisted Agricultural Intelligence",
                     "4 specialized models trained on sensor-aligned feature vectors with 5-fold cross-validation")

    # Left Column: 4 Validated Models Cards
    create_dark_card(s5, Inches(0.8), Inches(1.8), Inches(7.2), Inches(5.0))
    tb_ml = s5.shapes.add_textbox(Inches(1.05), Inches(1.95), Inches(6.7), Inches(4.7))
    tf_ml = tb_ml.text_frame
    tf_ml.word_wrap = True

    p_mlh = tf_ml.paragraphs[0]
    p_mlh.text = "4 VALIDATED MACHINE LEARNING MODELS"
    p_mlh.font.name = "Segoe UI"
    p_mlh.font.size = Pt(12)
    p_mlh.font.bold = True
    p_mlh.font.color.rgb = ACCENT_GREEN

    models_info = [
        ("Model 1: Irrigation Prediction", "XGBoost Classifier", "90.80% Test Acc | 92.00% 5-Fold CV",
         "Features: Filtered moisture (23.7%), Rainfall (33.3%), Soil type (16.2%), Crop Kc (9.9%), Temp & RH (6.4%). Outputs IRRIGATE / NO_IRRIGATION with explainable reason codes (RUN:MOISTURE_LOW).", ACCENT_CYAN),

        ("Model 2: Crop Suitability Recommendation", "Random Forest (200 Trees)", "99.32% Test Acc | 99.45% 5-Fold CV",
         "Features: Soil profile, BME280 temperature, humidity, rainfall, and Soil Health Card NPK. Ranks Top 5 recommended crops with percentage suitability confidence bars.", ACCENT_AMBER),

        ("Model 3: Fertilizer Prescription", "XGBoost Classifier", "100.0% Test Acc | 99.90% 5-Fold CV",
         "Features: Soil N-P-K status, crop type, growth stage, soil moisture. Prescribes exact commercial fertilizer grades (Urea for low N, DAP for low P, 10-26-26) to correct deficits.", ACCENT_LIME),

        ("Model 4: Soil Characterization", "Random Forest Classifier", "84.50% Test Acc | 84.80% 5-Fold CV",
         "Features: Moisture retention dynamics, ambient climate, baseline chemistry. Classifies soil into Black (Vertisol), Red (Alfisol), Alluvial, Sandy, Clayey, or Loamy.", ACCENT_PURPLE)
    ]

    for mtitle, malgo, mperf, mdesc, mcol in models_info:
        p_mt = tf_ml.add_paragraph()
        p_mt.text = f"•  {mtitle}  —  {malgo}"
        p_mt.font.name = "Segoe UI"
        p_mt.font.size = Pt(11.5)
        p_mt.font.bold = True
        p_mt.font.color.rgb = mcol
        p_mt.space_before = Pt(6)

        p_mp = tf_ml.add_paragraph()
        p_mp.text = f"   Performance: {mperf}"
        p_mp.font.name = "Segoe UI"
        p_mp.font.size = Pt(10.5)
        p_mp.font.bold = True
        p_mp.font.color.rgb = TEXT_WHITE
        p_mp.space_before = Pt(1)

        p_md = tf_ml.add_paragraph()
        p_md.text = f"   {mdesc}"
        p_md.font.name = "Segoe UI"
        p_md.font.size = Pt(9.5)
        p_md.font.color.rgb = TEXT_SLATE
        p_md.space_before = Pt(1)

    # Right Column: Positioning & Chemical Honesty (Matches PPT.pdf page 7 style)
    create_dark_card(s5, Inches(8.2), Inches(1.8), Inches(4.333), Inches(5.0))
    tb_pos = s5.shapes.add_textbox(Inches(8.45), Inches(1.95), Inches(3.833), Inches(4.7))
    tf_pos = tb_pos.text_frame
    tf_pos.word_wrap = True

    p_ph = tf_pos.paragraphs[0]
    p_ph.text = "Architectural Positioning"
    p_ph.font.name = "Segoe UI"
    p_ph.font.size = Pt(12)
    p_ph.font.bold = True
    p_ph.font.color.rgb = ACCENT_CYAN

    pos_bullets = [
        ("✓ STM32 = Primary Safety Authority", "Runs local 5-state safety FSM and hardware watchdog. Never waits for cloud or ML to prevent flooding."),
        ("✓ ML = Advisory & Optimization", "Acts as an intelligent agro-advisory layer: computes crop suitability, water budgeting, and fertilizer needs."),
        ("✓ AI Assists — Doesn't Blindly Command", "Ensures zero runaway actuation even if network drops or the ML server is unreachable."),
        ("✓ Chemical Honesty (TDS vs NPK)", "Our hardware TDS sensor measures dissolved solids in irrigation water (salinity hazard). Soil NPK and pH are derived from accredited Soil Health Card lab tests stored in Supabase with ICAR baseline autofill.")
    ]
    for btitle, bdesc in pos_bullets:
        p_bt = tf_pos.add_paragraph()
        p_bt.text = btitle
        p_bt.font.name = "Segoe UI"
        p_bt.font.size = Pt(11)
        p_bt.font.bold = True
        p_bt.font.color.rgb = TEXT_WHITE
        p_bt.space_before = Pt(8)

        p_bd = tf_pos.add_paragraph()
        p_bd.text = bdesc
        p_bd.font.name = "Segoe UI"
        p_bd.font.size = Pt(10)
        p_bd.font.color.rgb = TEXT_SLATE
        p_bd.space_before = Pt(2)

    # =========================================================================
    # SLIDE 6: BACKEND & CLOUD STORAGE (Matches page_9.png of PPT.pdf)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s6)
    add_slide_header(s6, "Backend & Cloud Storage",
                     "Node.js Express  •  Supabase PostgreSQL  •  React Operator Console")

    # Left Card: Node.js API Routes (Matches PPT.pdf page 9)
    create_dark_card(s6, Inches(0.8), Inches(1.8), Inches(5.65), Inches(3.55))
    tb_api = s6.shapes.add_textbox(Inches(1.05), Inches(1.95), Inches(5.15), Inches(3.2))
    tf_api = tb_api.text_frame
    tf_api.word_wrap = True

    p_apih = tf_api.paragraphs[0]
    p_apih.text = "Node.js API Routes"
    p_apih.font.name = "Segoe UI"
    p_apih.font.size = Pt(13)
    p_apih.font.bold = True
    p_apih.font.color.rgb = ACCENT_GREEN

    routes = [
        ("POST", "/sensor-data", "Receive JSON from ESP32. Compute WSI, DRI. Store.", ACCENT_AMBER),
        ("GET", "/latest", "Return most recent readings for dashboard polling.", ACCENT_CYAN),
        ("GET", "/history", "Return time-series telemetry for trend charts.", ACCENT_CYAN),
        ("POST", "/pump", "Dashboard manual pump override command.", ACCENT_AMBER),
        ("GET", "/predict", "Proxy call to Python ML model microservice.", ACCENT_CYAN)
    ]
    for method, endpoint, rdesc, mcol in routes:
        p_r = tf_api.add_paragraph()
        p_r.text = f"[{method}]  {endpoint}  —  "
        p_r.font.name = "Segoe UI"
        p_r.font.size = Pt(10.5)
        p_r.font.bold = True
        p_r.font.color.rgb = mcol
        p_r.space_before = Pt(7)

        run = p_r.add_run()
        run.text = rdesc
        run.font.bold = False
        run.font.color.rgb = TEXT_SLATE

    # Right Card: Supabase Schema (Matches PPT.pdf page 9)
    create_dark_card(s6, Inches(6.88), Inches(1.8), Inches(5.65), Inches(3.55))
    tb_db = s6.shapes.add_textbox(Inches(7.13), Inches(1.95), Inches(5.15), Inches(3.2))
    tf_db = tb_db.text_frame
    tf_db.word_wrap = True

    p_dbh = tf_db.paragraphs[0]
    p_dbh.text = "Supabase — PostgreSQL Schema"
    p_dbh.font.name = "Segoe UI"
    p_dbh.font.size = Pt(13)
    p_dbh.font.bold = True
    p_dbh.font.color.rgb = ACCENT_CYAN

    db_items = [
        ("moisture, soil_temp, tds", "Core physical sensor readings"),
        ("amb_temp, humidity, pressure", "BME280 environmental telemetry"),
        ("vpd, wsi, dri", "Computed agro-stress & drying indices"),
        ("prediction, confidence", "ML model classification output"),
        ("crops (JSONB)", "Ranked top-5 crop recommendations"),
        ("80+ Reference Rules", "FAO-56 Kc crop stages & ICAR baseline tables")
    ]
    for col_name, col_desc in db_items:
        p_d = tf_db.add_paragraph()
        p_d.text = f"▸ {col_name}"
        p_d.font.name = "Segoe UI"
        p_d.font.size = Pt(10.5)
        p_d.font.bold = True
        p_d.font.color.rgb = ACCENT_GREEN
        p_d.space_before = Pt(5)

        run = p_d.add_run()
        run.text = f"  :  {col_desc}"
        run.font.bold = False
        run.font.color.rgb = TEXT_SLATE

    # Bottom Full-Width Card: React Dashboard Components (Matches PPT.pdf page 9)
    create_dark_card(s6, Inches(0.8), Inches(5.55), Inches(11.733), Inches(1.3))
    tb_rc = s6.shapes.add_textbox(Inches(1.05), Inches(5.65), Inches(11.2), Inches(0.3))
    tf_rc = tb_rc.text_frame
    p_rch = tf_rc.paragraphs[0]
    p_rch.text = "React Dashboard Components"
    p_rch.font.name = "Segoe UI"
    p_rch.font.size = Pt(12)
    p_rch.font.bold = True
    p_rch.font.color.rgb = ACCENT_AMBER

    # 6 Component Pills
    comps = [
        ("Moisture Trend Chart", Inches(1.05)),
        ("WSI Stress Gauge", Inches(3.0)),
        ("Climate Telemetry", Inches(4.95)),
        ("ML Prediction Card", Inches(6.9)),
        ("Volumetric Meter", Inches(8.85)),
        ("Simulation Mode", Inches(10.8))
    ]
    for cname, cx in comps:
        c_box = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx, Inches(6.05), Inches(1.75), Inches(0.6))
        c_box.fill.solid()
        c_box.fill.fore_color.rgb = RGBColor(18, 38, 30)
        c_box.line.color.rgb = CARD_BORDER

        tf_cb = c_box.text_frame
        tf_cb.word_wrap = True
        p_ctx = tf_cb.paragraphs[0]
        p_ctx.text = cname
        p_ctx.font.name = "Segoe UI"
        p_ctx.font.size = Pt(9.5)
        p_ctx.font.bold = True
        p_ctx.font.color.rgb = TEXT_WHITE
        p_ctx.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 7: CLOSED-LOOP DEMO SEQUENCE (Matches page_10.png of PPT.pdf)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_canvas_bg(s7)
    add_slide_header(s7, "Closed-Loop Demo Sequence & Validation",
                     "Live physical demonstration of the complete autonomous irrigation loop")

    # 6 Step Cards (2 columns x 3 rows) matching exact layout of PPT.pdf page 10
    steps = [
        ("1", "Pull Moisture Probe from Soil",
         "Moisture ADC value drops below calibrated threshold. Dashboard moisture gauge enters dry warning band in real time.",
         ACCENT_RED),

        ("2", "WSI & Moisture Deficit Climbs",
         "Water Stress Index (WSI) climbs in real time on the React console. VPD and climate context indicate high transpiration demand.",
         ACCENT_AMBER),

        ("3", "STM32 Local Safety Logic Fires",
         "STM32 detects moisture below 35% threshold. Local decision engine triggers independently without requiring cloud connection.",
         ACCENT_CYAN),

        ("4", "ML Prediction Flips to IRRIGATE",
         "Python ML model evaluates sensor vector, confirms decision with 90.8% confidence, and generates explainable reason code RUN:MOISTURE_LOW.",
         ACCENT_LIME),

        ("5", "MOSFET Activates — Pump Runs",
         "STM32 PB0 goes HIGH. IRLZ44N MOSFET turns on 12V DC pump. Pulse-flow meter integrates delivered liters in real time.",
         ACCENT_AMBER),

        ("6", "Wetting Front Verified — Pump Stops",
         "Delivered volume reaches target liters. Pump shuts off. Moisture probe verifies percolation (Δθ ≥ +18%) confirming true closed-loop success.",
         ACCENT_LIME)
    ]

    card_sw = Inches(5.65)
    card_sh = Inches(1.55)
    left_x1 = Inches(0.8)
    left_x2 = Inches(6.88)
    tops_y = [Inches(1.8), Inches(3.52), Inches(5.24)]

    for idx, (snum, stitle, sdesc, scol) in enumerate(steps):
        col_x = left_x1 if idx % 2 == 0 else left_x2
        row_y = tops_y[idx // 2]

        create_dark_card(s7, col_x, row_y, card_sw, card_sh, left_accent=scol)

        # Number Badge (Square)
        nb = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, col_x + Inches(0.2), row_y + Inches(0.2), Inches(0.48), Inches(0.48))
        nb.fill.solid()
        nb.fill.fore_color.rgb = scol
        nb.line.fill.background()
        tf_nb = nb.text_frame
        p_nb = tf_nb.paragraphs[0]
        p_nb.text = snum
        p_nb.font.name = "Segoe UI"
        p_nb.font.size = Pt(14)
        p_nb.font.bold = True
        p_nb.font.color.rgb = RGBColor(10, 26, 19)
        p_nb.alignment = PP_ALIGN.CENTER

        # Title & Description
        tb_st = s7.shapes.add_textbox(col_x + Inches(0.82), row_y + Inches(0.15), card_sw - Inches(1.0), card_sh - Inches(0.3))
        tf_st = tb_st.text_frame
        tf_st.word_wrap = True

        p_sth = tf_st.paragraphs[0]
        p_sth.text = stitle
        p_sth.font.name = "Segoe UI"
        p_sth.font.size = Pt(13)
        p_sth.font.bold = True
        p_sth.font.color.rgb = scol

        p_std = tf_st.add_paragraph()
        p_std.text = sdesc
        p_std.font.name = "Segoe UI"
        p_std.font.size = Pt(10.5)
        p_std.font.color.rgb = TEXT_SLATE
        p_std.space_before = Pt(4)

    # Save Outputs
    output_target1 = os.path.join(BASE_DIR, "TerraFlow_BioAI_SPIT_Major_Project.pptx")
    output_target2 = os.path.join(BASE_DIR, "TerraFlow_BioAI_Final_Presentation.pptx")
    output_target3 = os.path.join(BASE_DIR, "TerraFlow_BioAI_Major_Project_Presentation.pptx")

    for tgt in [output_target1, output_target2, output_target3]:
        try:
            prs.save(tgt)
            print(f"[OK] Saved: {tgt}")
        except PermissionError:
            print(f"[NOTE] {tgt} is currently locked by PowerPoint. Skipped.")

    return output_target1


if __name__ == "__main__":
    build_deck()
