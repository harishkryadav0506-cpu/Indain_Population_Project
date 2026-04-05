"""
src/pages/compare.py
=====================
Page 4 — Side-by-side comparison of all ML models with metrics table,
         overlay chart, and year-by-year prediction grid.
"""

import numpy as np
import plotly.graph_objects as go
import streamlit as st
import pandas as pd

from src.data.population_data import get_historical_df, get_un_projected_df
from src.models.ml_models import train_all_models, predict, best_model_name
from src.utils.helpers import section_title, PLOTLY_TEMPLATE


def render() -> None:
    st.markdown('<div class="big-title">📊 Model Comparison</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">All ML models visualised together — overlay curves, accuracy metrics, and future predictions.</div>', unsafe_allow_html=True)

    models  = train_all_models()
    best    = best_model_name(models)
    df      = get_historical_df()
    df_un   = get_un_projected_df()

    # ── Metrics table ─────────────────────────
    section_title("📋 Model Performance Metrics")
    rows = []
    for name, m in models.items():
        rows.append({
            "Model":      name,
            "R² Score":   f"{m['r2']:.4f}",
            "MAE (M)":    f"{m['mae']:.2f}",
            "RMSE (M)":   f"{m['rmse']:.2f}",
            "Best model": "🏆 YES" if name == best else "",
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.success(f"🏆 **Best Model by R²:** {best}  —  R² = {models[best]['r2']:.4f}")

    # ── Overlay curves chart ──────────────────
    section_title("📈 All Models — Prediction Curves (1950 – 2100)")
    yr_range = np.arange(1950, 2101)

    fig = go.Figure()

    # Actual data
    fig.add_trace(go.Scatter(
        x=df["year"], y=df["population_m"],
        mode="markers", name="Actual Historical",
        marker=dict(color="white", size=8, symbol="circle-open",
                    line=dict(width=2, color="white")),
        hovertemplate="Year: %{x}<br>Actual: %{y}M<extra></extra>"))

    # UN baseline
    fig.add_trace(go.Scatter(
        x=df_un["year"], y=df_un["population_m"],
        mode="lines", name="UN Projection",
        line=dict(color="gray", width=2, dash="dash")))

    # Each model
    for name, m in models.items():
        preds = [predict(m, y) for y in yr_range]
        fig.add_trace(go.Scatter(
            x=yr_range, y=preds, mode="lines",
            name=name, line=dict(color=m["color"], width=2.5),
            hovertemplate=f"<b>{name}</b><br>Year: %{{x}}<br>Pred: %{{y:.1f}}M<extra></extra>"))

    fig.add_vline(x=2025, line_dash="dot", line_color="#F7C948",
                  opacity=0.6, annotation_text="Now")
    fig.update_layout(template=PLOTLY_TEMPLATE, height=500,
        yaxis_title="Population (Millions)", xaxis_title="Year",
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig, use_container_width=True)

    # ── Year-by-year grid ─────────────────────
    section_title("📅 All Models — Key Year Predictions vs UN Baseline")
    key_years = [2025, 2030, 2040, 2050, 2060, 2070, 2080, 2100]
    grid_rows = []
    for yr in key_years:
        un_val = next((p for y, p in zip(df_un["year"], df_un["population_m"]) if y == yr), "—")
        row    = {"Year": yr, "UN Baseline (M)": f"{un_val}M" if un_val != "—" else "—"}
        for nm, m in models.items():
            row[nm] = f"{predict(m, yr):.1f}M"
        grid_rows.append(row)
    st.dataframe(pd.DataFrame(grid_rows), use_container_width=True, hide_index=True)
