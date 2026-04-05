"""
src/pages/dashboard.py
=======================
Page 1 — Overview dashboard with KPIs, trend chart, and demographics.
"""

import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st

from src.data.population_data import get_historical_df, get_un_projected_df
from src.utils.helpers import kpi_card, section_title, live_population, PLOTLY_TEMPLATE


def render() -> None:
    st.markdown('<div class="big-title">🇮🇳 India Population Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Historical trends, live counter, and key demographic indicators (1950–2025).</div>', unsafe_allow_html=True)

    df     = get_historical_df()
    df_un  = get_un_projected_df()

    # ── Live Counter ──────────────────────────
    st.success(f"🟢 **Live Estimated Population:** &nbsp; **{live_population():,}**")

    st.markdown("---")

    # ── KPI Row ───────────────────────────────
    cols = st.columns(5)
    kpis = [
        ("1.45 B",   "Population (2025)",  "World's #1",       "#FF6B35"),
        ("2.0",      "Fertility Rate",      "Near replacement", "#F7C948"),
        ("28.4 yrs", "Median Age",          "Young workforce",  "#1B9C85"),
        ("36 %",     "Urban Population",    "Rising fast",      "#7B68EE"),
        ("70 yrs",   "Life Expectancy",     "+34 yrs since '50","#22c55e"),
    ]
    for col, (val, lbl, delta, clr) in zip(cols, kpis):
        col.markdown(kpi_card(val, lbl, delta, clr), unsafe_allow_html=True)

    st.markdown("---")

    # ── Main Trend Chart ──────────────────────
    c_left, c_right = st.columns([2, 1])

    with c_left:
        section_title("📈 Historical & UN Projected Population")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["year"], y=df["population_m"],
            mode="lines+markers", name="Historical (UN)",
            line=dict(color="#FF6B35", width=3),
            marker=dict(size=7, color="#FF6B35", line=dict(color="white", width=1)),
            fill="tozeroy", fillcolor="rgba(255,107,53,0.08)",
            hovertemplate="<b>%{x}</b><br>Population: %{y}M<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=df_un["year"], y=df_un["population_m"],
            mode="lines", name="UN Projection",
            line=dict(color="#1B9C85", width=2, dash="dash"),
            hovertemplate="<b>%{x}</b><br>UN Projected: %{y}M<extra></extra>",
        ))
        fig.add_vline(x=2025, line_dash="dot", line_color="#F7C948",
                      annotation_text="Now →", annotation_font_color="#F7C948")
        fig.update_layout(
            template=PLOTLY_TEMPLATE, height=340,
            margin=dict(l=0, r=0, t=10, b=0),
            yaxis_title="Population (Millions)",
            legend=dict(orientation="h", y=-0.18),
        )
        st.plotly_chart(fig, use_container_width=True)

    with c_right:
        section_title("📋 Historical Data Table")
        tbl = df[["year", "population_m", "growth_rate_pct",
                  "fertility_rate", "life_expectancy"]].copy()
        tbl.columns = ["Year", "Pop (M)", "Growth %", "TFR", "Life Exp"]
        st.dataframe(tbl, use_container_width=True, height=340, hide_index=True)

    st.markdown("---")

    # ── Sub Charts ────────────────────────────
    c1, c2 = st.columns(2)

    with c1:
        section_title("📉 Annual Growth Rate")
        fig_gr = px.bar(df, x="year", y="growth_rate_pct",
            color="growth_rate_pct", color_continuous_scale="RdYlGn",
            labels={"growth_rate_pct": "Growth % / yr", "year": "Year"},
            template=PLOTLY_TEMPLATE)
        fig_gr.update_layout(height=280, margin=dict(l=0, r=0, t=10, b=0),
                              showlegend=False)
        st.plotly_chart(fig_gr, use_container_width=True)

    with c2:
        section_title("👶 Fertility Rate  VS  Life Expectancy")
        fig_fl = make_subplots(specs=[[{"secondary_y": True}]])
        fig_fl.add_trace(go.Scatter(x=df["year"], y=df["fertility_rate"],
            name="TFR", line=dict(color="#FF6B35", width=2)), secondary_y=False)
        fig_fl.add_trace(go.Scatter(x=df["year"], y=df["life_expectancy"],
            name="Life Exp (yrs)", line=dict(color="#1B9C85", width=2, dash="dash")),
            secondary_y=True)
        fig_fl.update_layout(template=PLOTLY_TEMPLATE, height=280,
            margin=dict(l=0, r=0, t=10, b=0),
            legend=dict(orientation="h", y=-0.25))
        st.plotly_chart(fig_fl, use_container_width=True)
