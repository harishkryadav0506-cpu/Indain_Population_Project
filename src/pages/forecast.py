"""
src/pages/forecast.py
======================
Page 3 — Interactive population forecast with year slider + quick-reference table.
"""

import numpy as np
import plotly.graph_objects as go
import streamlit as st
import pandas as pd

from src.data.population_data import get_historical_df, get_un_projected_df
from src.models.ml_models import train_all_models, predict, best_model_name
from src.utils.helpers import section_title, PLOTLY_TEMPLATE


def render() -> None:
    st.markdown('<div class="big-title">🔮 Population Forecast</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Select an ML model and a target year to get an AI-powered population estimate.</div>', unsafe_allow_html=True)

    models   = train_all_models()
    best     = best_model_name(models)
    df       = get_historical_df()
    df_un    = get_un_projected_df()

    # ── Controls ──────────────────────────────
    c_cfg, c_chart = st.columns([1, 2])

    with c_cfg:
        section_title("⚙️ Predictor Settings")
        sel_model = st.selectbox("ML Model:", list(models.keys()),
                                 index=list(models.keys()).index(best))
        sel_year  = st.slider("Target Year:", 1950, 2100, 2050)

        m         = models[sel_model]
        pred_pop  = predict(m, sel_year)
        delta     = pred_pop - 1450.0

        st.markdown("---")
        st.markdown(f"### 📍 {sel_year} Prediction")
        st.markdown(
            f"""
            <div class="kpi-box" style="margin-top:8px;">
                <div style="font-size:0.8rem;color:#94a3b8;">Model: {sel_model}</div>
                <div style="font-size:2.2rem;font-weight:800;color:#FF6B35;margin:8px 0;">{pred_pop:,.1f} M</div>
                <div style="font-size:1.1rem;font-weight:700;color:#f1f5f9;">{int(pred_pop * 1_000_000):,}</div>
                <div style="color:{'#22c55e' if delta >= 0 else '#ef4444'};font-size:0.88rem;margin-top:6px;">
                    {"▲" if delta >= 0 else "▼"} {abs(delta):.1f}M vs today
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(f"> R² = `{m['r2']:.4f}` | MAE = `{m['mae']:.2f}M`")

        # Quick reference
        st.markdown("---")
        section_title("📋 Quick Reference")
        key_yrs = [2025, 2030, 2040, 2050, 2060, 2075, 2100]
        tbl = pd.DataFrame({
            "Year":     key_yrs,
            "ML Pred (M)": [f"{predict(m, y):.1f}" for y in key_yrs],
            "UN Base (M)": [
                str(next((p for yr, p in zip(df_un["year"], df_un["population_m"]) if yr == y), "—"))
                for y in key_yrs
            ],
        })
        st.dataframe(tbl, use_container_width=True, hide_index=True)

    # ── Forecast Chart ────────────────────────
    with c_chart:
        section_title("📈 Forecast Chart (1950 – 2100)")
        yr_range   = np.arange(1950, 2101)
        curve      = [predict(m, y) for y in yr_range]

        fig = go.Figure()

        # Model curve
        fig.add_trace(go.Scatter(
            x=yr_range, y=curve, fill="tozeroy",
            fillcolor="rgba(255,107,53,0.07)",
            line=dict(color="#FF6B35", width=3),
            name=sel_model,
            hovertemplate="Year: %{x}<br>Predicted: %{y:.1f}M<extra></extra>"))

        # Historical dots
        fig.add_trace(go.Scatter(
            x=df["year"], y=df["population_m"],
            mode="markers", name="Historical (UN)",
            marker=dict(color="white", size=7, symbol="circle-open",
                        line=dict(width=2))))

        # UN projection line
        fig.add_trace(go.Scatter(
            x=df_un["year"], y=df_un["population_m"],
            mode="lines", name="UN Projection",
            line=dict(color="#1B9C85", width=2, dash="dot")))

        # Selected year star
        fig.add_trace(go.Scatter(
            x=[sel_year], y=[pred_pop],
            mode="markers+text",
            marker=dict(color="#F7C948", size=14, symbol="star"),
            text=[f"  {sel_year}: {pred_pop:.1f}M"],
            textfont=dict(color="#F7C948", size=13),
            textposition="middle right",
            showlegend=False))

        fig.add_vline(x=2025, line_dash="dot", line_color="#94a3b8",
                      opacity=0.6, annotation_text="Now")
        fig.update_layout(template=PLOTLY_TEMPLATE, height=520,
            yaxis_title="Population (Millions)", xaxis_title="Year",
            margin=dict(l=0, r=0, t=10, b=0),
            legend=dict(orientation="h", y=-0.12))
        st.plotly_chart(fig, use_container_width=True)
