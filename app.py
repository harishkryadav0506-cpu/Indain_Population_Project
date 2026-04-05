"""
app.py — Entry Point
=====================
India Population ML Predictor — Streamlit Application
Run with:  streamlit run app.py
"""

import streamlit as st

from src.utils.helpers import inject_css, live_population
from src.models.ml_models import train_all_models
from src.pages import dashboard, ml_explorer, forecast, compare, states

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="India Population ML Predictor",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

# ─────────────────────────────────────────────
# SIDEBAR NAVIGATION
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🇮🇳 India Population")
    st.markdown("### ML Predictor")
    st.markdown("---")

    # Live ticker
    st.success(f"🟢 Live Estimate\n\n### {live_population():,}")

    st.markdown("---")

    page = st.radio(
        "📑 Navigate to:",
        [
            "🏠 Dashboard",
            "🤖 ML Model Explorer",
            "🔮 Forecast",
            "📊 Compare Models",
            "🗺️ State Analysis",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.caption("Data: UN World Population Prospects  \n& Census of India")
    st.caption("ML Engine: Scikit-Learn + Scipy")

# ─────────────────────────────────────────────
# PAGE ROUTING
# ─────────────────────────────────────────────
# Pre-train models (cached — runs only once)
train_all_models()

if page == "🏠 Dashboard":
    dashboard.render()

elif page == "🤖 ML Model Explorer":
    ml_explorer.render()

elif page == "🔮 Forecast":
    forecast.render()

elif page == "📊 Compare Models":
    compare.render()

elif page == "🗺️ State Analysis":
    states.render()
