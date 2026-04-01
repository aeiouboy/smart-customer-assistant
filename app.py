"""Smart Customer Assistant - Streamlit Application."""

from html import escape as _h

import streamlit as st  # ty: ignore[unresolved-import]

from config import (
    COLOR_SAFE,
    COLOR_WARN,
    CONFIDENCE_THRESHOLD,
    OPENROUTER_API_KEY,
)
from ai_client import analyze_product_image
from url_builder import build_tops_search_url


def _safe(value: object) -> str:
    """HTML-escape a value for safe insertion into markup."""
    return _h(str(value))


# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Smart Customer Assistant",
    page_icon="\U0001f6d2",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------
st.html("""
<style>
/* ===== Hide Streamlit defaults ===== */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
div[data-testid="stToolbar"] {visibility: hidden;}

/* ===== Typography ===== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* ===== Background ===== */
.stApp {
    background: #f7faf7;
}

/* ===== Glass card ===== */
.glass-card {
    background: #fff;
    border: 1px solid #e8efe8;
    border-radius: 16px;
    padding: 1.75rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 8px rgba(0,0,0,0.04);
}

/* ===== Upload zone ===== */
.upload-zone {
    background: #fff;
    border: 2px dashed #c8e6c9;
    border-radius: 20px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin-bottom: 1rem;
    transition: border-color 0.2s ease, background 0.2s ease;
}
.upload-zone:hover {
    border-color: #27AE60;
    background: #f0faf0;
}
.upload-zone-icon {
    font-size: 3rem;
    margin-bottom: 0.5rem;
    display: block;
}
.upload-zone-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #2c3e50;
    margin-bottom: 0.25rem;
}
.upload-zone-sub {
    font-size: 0.85rem;
    color: #999;
}

/* ===== Allergen banner ===== */
.allergen-banner {
    background: #fff5f5;
    border: 1px solid #fed7d7;
    border-left: 4px solid #E74C3C;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin: 0.75rem 0;
}
.allergen-banner-title {
    font-size: 0.9rem;
    font-weight: 700;
    color: #C0392B;
    margin-bottom: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.allergen-pill {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 20px;
    background: #E74C3C;
    color: #fff;
    margin: 3px 4px;
    font-weight: 600;
    font-size: 0.85rem;
}

/* ===== Risk pills ===== */
.risk-pill {
    padding: 4px 12px;
    border-radius: 20px;
    color: #fff;
    font-size: 0.78rem;
    font-weight: 600;
    display: inline-block;
}
.risk-high { background: #E74C3C; }
.risk-medium { background: #F39C12; }
.risk-low { background: #27AE60; }

/* ===== Confidence bar ===== */
.conf-track {
    background: #eee;
    border-radius: 10px;
    height: 6px;
    overflow: hidden;
    flex: 1;
}
.conf-fill {
    height: 100%;
    border-radius: 10px;
    transition: width 0.6s ease;
}

/* ===== CTA button ===== */
.tops-cta {
    display: block;
    width: 100%;
    padding: 1rem;
    background: linear-gradient(135deg, #E31E24 0%, #c0392b 100%);
    color: #fff !important;
    text-align: center;
    border-radius: 14px;
    font-size: 1.1rem;
    font-weight: 700;
    text-decoration: none;
    box-shadow: 0 4px 20px rgba(227,30,36,0.25);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.tops-cta:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 28px rgba(227,30,36,0.35);
    color: #fff !important;
}

/* ===== Ingredients table ===== */
.ing-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    border-radius: 12px;
    overflow: hidden;
    font-size: 0.9rem;
}
.ing-table thead th {
    background: #27AE60;
    color: #fff;
    padding: 0.7rem 1rem;
    text-align: left;
    font-weight: 600;
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}
.ing-table tbody tr { background: #fff; }
.ing-table tbody tr:nth-child(even) { background: #fafffe; }
.ing-table tbody td {
    padding: 0.6rem 1rem;
    border-bottom: 1px solid #f0f0f0;
    color: #444;
}
.ing-table tbody tr:last-child td { border-bottom: none; }

/* ===== Section label ===== */
.section-label {
    font-size: 0.78rem;
    font-weight: 700;
    color: #999;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 0.75rem;
}

/* ===== Product field ===== */
.field-label {
    font-size: 0.72rem;
    color: #aaa;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 600;
    margin-bottom: 2px;
}
.field-value {
    font-size: 1.15rem;
    color: #2c3e50;
    font-weight: 600;
    margin-bottom: 0.75rem;
}

/* ===== Health gauge ===== */
.gauge-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0.5rem 0;
}
.gauge-ring {
    position: relative;
    width: 140px;
    height: 140px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}
.gauge-inner {
    width: 110px;
    height: 110px;
    border-radius: 50%;
    background: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
}
.gauge-num {
    font-size: 2.4rem;
    font-weight: 800;
    line-height: 1;
}
.gauge-label {
    font-size: 0.75rem;
    color: #aaa;
    margin-top: 2px;
}
.gauge-verdict {
    margin-top: 0.6rem;
    font-size: 0.9rem;
    color: #555;
    font-weight: 500;
    text-align: center;
}

/* ===== Streamlit overrides ===== */
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #27AE60, #2ECC71) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.9rem 2rem !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 20px rgba(39,174,96,0.25) !important;
    transition: all 0.2s ease !important;
}
div.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 28px rgba(39,174,96,0.35) !important;
}
div.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: #aaa !important;
    border: 1px solid #ddd !important;
    border-radius: 14px !important;
    font-weight: 500 !important;
}
div.stButton > button[kind="secondary"]:hover {
    border-color: #bbb !important;
    color: #777 !important;
}

section[data-testid="stFileUploader"] {
    border: none !important;
    background: transparent;
}
section[data-testid="stFileUploader"] > div {
    padding: 0 !important;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Checkbox styling */
div[data-testid="stCheckbox"] label span {
    font-size: 0.85rem;
    color: #888;
}

/* Image preview */
div[data-testid="stImage"] {
    border-radius: 12px;
    overflow: hidden;
}
div[data-testid="stImage"] img {
    border-radius: 12px;
}

/* Tab styling */
div[data-baseweb="tab-list"] button {
    font-weight: 600;
    font-size: 0.9rem;
}
</style>
""")

# ---------------------------------------------------------------------------
# Hero header
# ---------------------------------------------------------------------------
st.html("""
<div style="text-align:center; padding: 2rem 0 1rem 0;">
    <div style="font-size: 3rem; margin-bottom: 0.3rem;">🛒</div>
    <div style="font-size: 1.8rem; font-weight: 800; color: #2c3e50; line-height: 1.2;">
        Smart Customer Assistant
    </div>
    <div style="color: #999; font-size: 0.9rem; margin-top: 0.4rem; font-weight: 400;">
        สแกนฉลากสินค้า · วิเคราะห์ส่วนประกอบ · สั่งซื้อผ่าน Tops Online
    </div>
</div>
""")

# ---------------------------------------------------------------------------
# API key check
# ---------------------------------------------------------------------------
if not OPENROUTER_API_KEY:
    st.error(
        "⚠️ ไม่พบ OPENROUTER_API_KEY — "
        "กรุณาตั้งค่า environment variable ก่อนใช้งาน"
    )

# ---------------------------------------------------------------------------
# Upload section
# ---------------------------------------------------------------------------
st.html("""
<div class="upload-zone">
    <span class="upload-zone-icon">📸</span>
    <div class="upload-zone-title">อัปโหลดรูปฉลากสินค้า</div>
    <div class="upload-zone-sub">รองรับไฟล์ JPG, JPEG, PNG, WEBP</div>
</div>
""")

uploaded_file = st.file_uploader(
    "เลือกไฟล์รูปภาพ",
    type=["jpg", "jpeg", "png", "webp"],
    label_visibility="collapsed",
)

# Camera toggle
enable_camera = st.checkbox("เปิดใช้กล้อง", value=False)
camera_image = None
if enable_camera:
    camera_image = st.camera_input("ถ่ายรูปฉลากสินค้า")

# Determine active image source
image_source = uploaded_file or camera_image

if image_source is not None:
    st.image(image_source, caption="ตัวอย่างรูปภาพ", use_container_width=True)

# ---------------------------------------------------------------------------
# Analyze button
# ---------------------------------------------------------------------------
st.html('<div style="height:0.25rem"></div>')

if st.button("🔍 วิเคราะห์สินค้า", type="primary", use_container_width=True):
    if image_source is None:
        st.warning("กรุณาอัปโหลดรูปภาพก่อน")
    else:
        with st.spinner("กำลังวิเคราะห์ด้วย AI..."):
            image_bytes = image_source.getvalue()
            result = analyze_product_image(image_bytes)
            st.session_state["analysis_result"] = result

# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------
if "analysis_result" in st.session_state:
    result = st.session_state["analysis_result"]

    if "error" in result:
        st.error(f"❌ {result.get('message', 'เกิดข้อผิดพลาด')}")
    else:
        product_info = result.get("product_info", {})
        ingredients = result.get("ingredients_analysis", {})
        health = result.get("health_dashboard", {})
        metadata = result.get("metadata", {})

        confidence = metadata.get("ai_confidence_score", 0)
        health_score = health.get("score", 0)
        allergens = health.get("allergens_detected", [])
        additives = ingredients.get("additives_found", [])

        st.html('<hr style="border:none; border-top:1px solid #e8efe8; margin:1.5rem 0 1rem 0;">')

        # --- Confidence warning ---
        if confidence < CONFIDENCE_THRESHOLD:
            st.warning(
                "⚠️ ความมั่นใจต่ำ — "
                "ลองถ่ายรูปใหม่ให้ชัดเจนขึ้น"
            )

        # --- Product Info + Health Score ---
        col_product, col_health = st.columns([3, 2], gap="medium")

        with col_product:
            brand = _safe(product_info.get("brand_name", "-"))
            name = _safe(product_info.get("product_name", "-"))
            conf_pct = f"{confidence:.0%}"
            conf_width = f"{min(confidence, 1.0) * 100:.0f}%"
            conf_color = (
                COLOR_SAFE if confidence >= 0.7
                else ("#F39C12" if confidence >= 0.5 else COLOR_WARN)
            )

            st.html(f"""
            <div class="glass-card">
                <div class="section-label">ข้อมูลสินค้า</div>
                <div class="field-label">ยี่ห้อ</div>
                <div class="field-value">{brand}</div>
                <div class="field-label">ชื่อสินค้า</div>
                <div class="field-value">{name}</div>
                <div style="margin-top:0.25rem;">
                    <div class="field-label">ความมั่นใจ AI</div>
                    <div style="display:flex; align-items:center; gap:0.75rem; margin-top:4px;">
                        <div class="conf-track">
                            <div class="conf-fill"
                                 style="width:{conf_width}; background:{conf_color};"></div>
                        </div>
                        <span style="font-weight:700; color:{conf_color}; font-size:0.9rem; min-width:40px;">
                            {conf_pct}
                        </span>
                    </div>
                </div>
            </div>
            """)

        with col_health:
            if health_score > 70:
                score_color = "#2ECC71"
            elif health_score >= 50:
                score_color = "#F39C12"
            else:
                score_color = "#E74C3C"

            verdict_th = _safe(health.get("verdict_th", ""))

            st.html(f"""
            <div class="glass-card">
                <div class="section-label" style="text-align:center;">คะแนนสุขภาพ</div>
                <div class="gauge-wrap">
                    <div class="gauge-ring"
                         style="background: conic-gradient({score_color} {health_score}%, #eee {health_score}%);">
                        <div class="gauge-inner">
                            <span class="gauge-num" style="color:{score_color};">{health_score}</span>
                            <span class="gauge-label">คะแนน</span>
                        </div>
                    </div>
                    <div class="gauge-verdict">{verdict_th}</div>
                </div>
            </div>
            """)

        # --- Allergen Alerts ---
        if allergens:
            pills = "".join(
                f'<span class="allergen-pill">⚠️ {_safe(a)}</span>' for a in allergens
            )
            st.html(f"""
            <div class="allergen-banner">
                <div class="allergen-banner-title">สารก่อภูมิแพ้ที่ตรวจพบ</div>
                <div>{pills}</div>
            </div>
            """)

        # --- Ingredients table ---
        if additives:
            risk_map = {
                "high": '<span class="risk-pill risk-high">สูง</span>',
                "medium": '<span class="risk-pill risk-medium">ปานกลาง</span>',
                "low": '<span class="risk-pill risk-low">ต่ำ</span>',
            }

            rows_html = ""
            for item in additives:
                name_th = _safe(item.get("name_th", "-"))
                purpose = _safe(item.get("purpose", "-"))
                risk_raw = str(item.get("risk_level", "low")).lower()
                risk_pill = risk_map.get(risk_raw, risk_map["low"])
                rows_html += f"<tr><td>{name_th}</td><td>{purpose}</td><td>{risk_pill}</td></tr>"

            st.html(f"""
            <div class="glass-card">
                <div class="section-label">รายการสารปรุงแต่ง</div>
                <table class="ing-table">
                    <thead>
                        <tr>
                            <th>ชื่อสาร</th>
                            <th>วัตถุประสงค์</th>
                            <th>ระดับความเสี่ยง</th>
                        </tr>
                    </thead>
                    <tbody>{rows_html}</tbody>
                </table>
            </div>
            """)

        # --- Tops Online CTA ---
        keyword = product_info.get("clean_search_keyword", "")
        tops_url = build_tops_search_url(keyword)

        st.html(f"""
        <div class="glass-card" style="text-align:center; padding:1.5rem;">
            <div class="section-label">สั่งซื้อออนไลน์</div>
            <a href="{_safe(tops_url)}" target="_blank" class="tops-cta">
                🛒 สั่งซื้อที่ Tops Online
            </a>
        </div>
        """)

    # --- Reset button ---
    st.html('<div style="height:0.5rem"></div>')
    if st.button("🔄 สแกนสินค้าใหม่", type="secondary", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
