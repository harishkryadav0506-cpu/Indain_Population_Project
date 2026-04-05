"""
src/utils/helpers.py
=====================
Shared utility functions used across all pages.
"""

import time
from datetime import datetime
import streamlit as st


# ─────────────────────────────────────────────
# LIVE POPULATION ESTIMATOR
# ─────────────────────────────────────────────
_BASE_POP      = 1_450_000_000          # population at start of 2025
_GROWTH_RATE   = 0.009                  # 0.9 % annual growth rate
_SEC_PER_YEAR  = 365.25 * 24 * 3600
_GROWTH_PER_S  = (_GROWTH_RATE / _SEC_PER_YEAR) * _BASE_POP
_EPOCH_2025    = datetime(2025, 1, 1).timestamp()


def live_population() -> int:
    """Return the real-time estimated India population."""
    elapsed = time.time() - _EPOCH_2025
    return int(_BASE_POP + _GROWTH_PER_S * elapsed)


# ─────────────────────────────────────────────
# STYLES
# ─────────────────────────────────────────────
PLOTLY_TEMPLATE = "plotly_dark"

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.big-title {
    font-size: 2.6rem; font-weight: 800;
    background: linear-gradient(90deg, #FF6B35, #F7C948, #1B9C85);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    line-height: 1.2; margin-bottom: 2px;
}
.subtitle {
    color: #94a3b8; font-size: 1rem; margin-bottom: 1.2rem;
}
.kpi-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 12px; padding: 18px 16px; text-align: center;
}
.kpi-value  { font-size: 1.8rem; font-weight: 800; color: #f1f5f9; }
.kpi-label  { font-size: 0.8rem; color: #94a3b8; margin-top: 4px; }
.kpi-delta  { font-size: 0.8rem; font-weight: 600; margin-top: 4px; }
.section-title {
    font-size: 1.25rem; font-weight: 700; color: #f1f5f9; margin: 1.4rem 0 0.6rem;
}
</style>
"""


def inject_css() -> None:
    """Inject global CSS into the Streamlit page."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# KPI CARD HTML
# ─────────────────────────────────────────────
def kpi_card(value: str, label: str, delta: str, delta_color: str = "#22c55e") -> str:
    """Return HTML for a single KPI card."""
    return f"""
    <div class="kpi-box">
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-delta" style="color:{delta_color};">{delta}</div>
    </div>
    """


def section_title(text: str) -> None:
    """Render a styled section title."""
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)
