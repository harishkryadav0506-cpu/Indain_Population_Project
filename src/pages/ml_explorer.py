"""
src/pages/ml_explorer.py
=========================
Page 2 — Inspect each ML model individually: fit curve, residuals, metrics.
"""

import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

from src.data.population_data import get_historical_df
from src.models.ml_models import train_all_models, predict, get_residuals
from src.utils.helpers import section_title, PLOTLY_TEMPLATE


def render() -> None:
    st.markdown('<div class="big-title">🤖 ML Model Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Inspect each trained model — coefficients, fit quality, and residual error analysis.</div>', unsafe_allow_html=True)

    models = train_all_models()
    df     = get_historical_df()
    X_hist = df["year"].values
    y_hist = df["population_m"].values

    # Model selector & metrics
    model_name = st.selectbox("Select model to inspect:", list(models.keys()))
    m = models[model_name]

    c1, c2, c3 = st.columns(3)
    c1.metric("R² Score",       f"{m['r2']:.4f}",  help="1.0 = perfect fit")
    c2.metric("MAE  (Millions)", f"{m['mae']:.2f}", help="Mean Absolute Error")
    c3.metric("RMSE (Millions)", f"{m['rmse']:.2f}",help="Root Mean Squared Error")

    st.info(f"**{model_name}** — {m['desc']}")

    # Fit curve vs actual
    region = np.arange(1940, 2101, 1)
    curve  = [predict(m, y) for y in region]

    section_title("📈 Model Fit over Full Range")
    fig_fit = go.Figure()
    fig_fit.add_trace(go.Scatter(x=region, y=curve,
        name=f"{model_name} curve",
        line=dict(color=m["color"], width=3),
        hovertemplate="Year: %{x}<br>Predicted: %{y:.1f}M<extra></extra>"))
    fig_fit.add_trace(go.Scatter(x=X_hist, y=y_hist,
        mode="markers", name="Actual Historical",
        marker=dict(color="white", size=8, symbol="circle-open",
                    line=dict(width=2, color="white"))))
    fig_fit.add_vline(x=2025, line_dash="dot", line_color="#F7C948",
                      annotation_text="Now")
    fig_fit.update_layout(template=PLOTLY_TEMPLATE, height=380,
        yaxis_title="Population (Millions)", xaxis_title="Year",
        margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig_fit, use_container_width=True)

    # Residuals bar chart
    section_title("📊 Residuals on Historical Data  (Actual − Predicted)")
    residuals = get_residuals(m, X_hist, y_hist)
    fig_res = px.bar(x=X_hist, y=residuals,
        color=residuals, color_continuous_scale="RdBu",
        labels={"x": "Year", "y": "Residual (M)"},
        template=PLOTLY_TEMPLATE)
    fig_res.add_hline(y=0, line_dash="dash", line_color="white", opacity=0.4)
    fig_res.update_layout(height=260, margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig_res, use_container_width=True)

    # Actual vs Predicted scatter
    section_title("🔵 Actual  vs  Predicted  (Parity Plot)")
    preds_hist = [predict(m, int(y)) for y in X_hist]
    fig_par = go.Figure()
    fig_par.add_trace(go.Scatter(x=y_hist, y=preds_hist,
        mode="markers+text",
        text=[str(yr) for yr in X_hist],
        textposition="top center",
        marker=dict(color=m["color"], size=9),
        name="Data points"))
    mn, mx = int(y_hist.min())-50, int(y_hist.max())+50
    fig_par.add_trace(go.Scatter(x=[mn, mx], y=[mn, mx],
        mode="lines", line=dict(color="white", dash="dash"),
        name="Perfect fit"))
    fig_par.update_layout(template=PLOTLY_TEMPLATE, height=320,
        xaxis_title="Actual (M)", yaxis_title="Predicted (M)",
        margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig_par, use_container_width=True)
