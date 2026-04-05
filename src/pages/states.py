"""
src/pages/states.py
====================
Page 5 — State-wise demographic analysis: bar, pie, scatter charts + table.
"""

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.data.population_data import get_states_df
from src.utils.helpers import section_title, PLOTLY_TEMPLATE


def render() -> None:
    st.markdown('<div class="big-title">🗺️ State-wise Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Population distribution, density, literacy, and regional breakdown of India\'s top states.</div>', unsafe_allow_html=True)

    df = get_states_df()

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Bar Chart", "🥧 Pie Chart", "🔵 Scatter", "📋 Data Table"])

    # ── Bar ───────────────────────────────────
    with tab1:
        section_title("Top 10 States by Population (Millions, 2025)")
        fig_bar = px.bar(
            df.sort_values("population_m", ascending=True),
            x="population_m", y="state", orientation="h",
            color="population_m", color_continuous_scale="OrRd",
            text="population_m",
            labels={"population_m": "Population (M)", "state": "State"},
            template=PLOTLY_TEMPLATE,
        )
        fig_bar.update_traces(texttemplate="%{text}M", textposition="outside")
        fig_bar.update_layout(height=440, margin=dict(l=0, r=60, t=10, b=0),
                               showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    # ── Pie ───────────────────────────────────
    with tab2:
        section_title("Share of National Population — Top 10 States")
        fig_pie = px.pie(
            df, values="population_m", names="state",
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=df["color"].tolist(),
        )
        fig_pie.update_traces(textposition="inside", textinfo="percent+label")
        fig_pie.update_layout(height=480, margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig_pie, use_container_width=True)

    # ── Scatter ───────────────────────────────
    with tab3:
        section_title("Literacy %  vs  Population — Bubble Chart")
        fig_dot = px.scatter(
            df,
            x="literacy_pct", y="population_m",
            size="population_m", color="region",
            text="state",
            labels={"literacy_pct": "Literacy %", "population_m": "Population (M)"},
            color_discrete_sequence=px.colors.qualitative.Vivid,
            template=PLOTLY_TEMPLATE,
        )
        fig_dot.update_traces(textposition="top center")
        fig_dot.update_layout(height=440, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig_dot, use_container_width=True)

        section_title("Population Density  vs  Literacy %")
        fig_den = px.scatter(
            df,
            x="literacy_pct", y="density",
            size="population_m", color="region",
            text="state",
            labels={"density": "Density (ppl / km²)", "literacy_pct": "Literacy %"},
            color_discrete_sequence=px.colors.qualitative.Vivid,
            template=PLOTLY_TEMPLATE,
        )
        fig_den.update_traces(textposition="top center")
        fig_den.update_layout(height=380, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig_den, use_container_width=True)

    # ── Table ─────────────────────────────────
    with tab4:
        section_title("Full State Data")
        show = df[["state", "population_m", "density", "literacy_pct",
                   "share_pct", "area_km2", "region"]].copy()
        show.columns = ["State", "Pop (M)", "Density (ppl/km²)",
                        "Literacy %", "National Share %", "Area km²", "Region"]
        st.dataframe(show.sort_values("Pop (M)", ascending=False),
                     use_container_width=True, hide_index=True, height=440)
