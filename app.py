import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="India Population Prediction | भारत जनसंख्या अनुमान",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for UI Enhancement
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #FF6B35, #F7C948, #1B9C85);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #94a3b8;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #111827;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #f1f5f9;
    }
    .stat-label {
        color: #94a3b8;
        font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# DATA DEFINITIONS
# ==========================================
DATA = {
    "historical": {
        "years": [1950, 1955, 1960, 1965, 1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025],
        "pop": [376, 409, 450, 499, 555, 623, 698, 784, 873, 964, 1057, 1148, 1234, 1310, 1380, 1450]
    },
    "projected": {
        "years": [2025, 2030, 2035, 2040, 2045, 2050, 2055, 2060, 2065, 2070, 2075, 2080, 2085, 2090, 2095, 2100],
        "pop": [1450, 1515, 1565, 1610, 1645, 1670, 1685, 1695, 1697, 1690, 1675, 1655, 1625, 1590, 1560, 1533]
    },
    "growth_rate": {
        "years": [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020, 2025, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100],
        "rate": [1.8, 2.0, 2.2, 2.3, 2.1, 1.8, 1.5, 1.0, 0.9, 0.8, 0.5, 0.3, 0.1, -0.05, -0.15, -0.25, -0.3]
    },
    "states": [
        {"State": "Uttar Pradesh", "Population": 231, "Color": "#FF6B35"},
        {"State": "Maharashtra", "Population": 126, "Color": "#F7C948"},
        {"State": "Bihar", "Population": 124, "Color": "#1B9C85"},
        {"State": "West Bengal", "Population": 100, "Color": "#E94560"},
        {"State": "Madhya Pradesh", "Population": 85, "Color": "#7B68EE"},
        {"State": "Tamil Nadu", "Population": 78, "Color": "#FF6B9D"},
        {"State": "Rajasthan", "Population": 79, "Color": "#20C997"},
        {"State": "Karnataka", "Population": 68, "Color": "#4ECDC4"}
    ],
    "comparison": {
        "Country": ["India", "China", "USA", "Indonesia", "Pakistan", "Brazil", "Nigeria"],
        "Pop2025": [1450, 1410, 340, 280, 240, 215, 230],
        "Pop2050": [1670, 1310, 375, 315, 370, 230, 400]
    }
}

def interpolate_population(year):
    all_years = DATA["historical"]["years"] + DATA["projected"]["years"][1:]
    all_pops = DATA["historical"]["pop"] + DATA["projected"]["pop"][1:]
    
    if year <= all_years[0]: return all_pops[0]
    if year >= all_years[-1]: return all_pops[-1]
    
    for i in range(len(all_years) - 1):
        if all_years[i] <= year <= all_years[i+1]:
            t = (year - all_years[i]) / (all_years[i+1] - all_years[i])
            return all_pops[i] + t * (all_pops[i+1] - all_pops[i])
    return 0

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("## ⚙️ Settings & Predictor")
    selected_year = st.slider("Select Year to Predict:", min_value=1950, max_value=2100, value=2025, step=1)
    
    pred_pop = interpolate_population(selected_year)
    
    st.markdown("### Estimated Population:")
    st.markdown(f"<h1 style='color: #FF6B35; text-align: center;'>{int(pred_pop * 1000000):,}</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Individuals</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Navigaion")
    st.markdown("- [Live Status](#india-s-population-past-present-future)")
    st.markdown("- [Key Statistics](#key-demographics-2025)")
    st.markdown("- [Population Growth Trend](#population-growth-trend)")
    st.markdown("- [State Wise Breakdown](#top-states-by-population)")

# ==========================================
# MAIN APP
# ==========================================
st.markdown('<p class="main-header">India\'s Population: Past, Present & Future</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Explore India\'s demographic journey from 1950 to 2100 based on UN World Population Prospects.</p>', unsafe_allow_html=True)


# --- Live Counter ---
# Calculate a rough real-time current estimate
base_pop_2025 = 1450000000
growth_per_second = (0.9 / 100 / 365.25 / 24 / 3600) * base_pop_2025
start_of_year = datetime(2025, 1, 1).timestamp()
now = time.time()
current_est = int(base_pop_2025 + growth_per_second * (now - start_of_year))

st.info(f"**Live Estimated Current Population:** {current_est:,} 🟢")

st.markdown("---")
st.markdown("### 📊 Key Demographics (2025)")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Population", value="1.45 Billion", delta="0.9% / yr")
with col2:
    st.metric(label="Urban Population", value="36%", delta="Rising")
with col3:
    st.metric(label="Fertility Rate", value="2.0", delta="-0.1", delta_color="inverse")
with col4:
    st.metric(label="Median Age", value="28.4 yrs", delta="+0.3", delta_color="normal")

st.markdown("---")

# --- Tabs for Charts ---
tab1, tab2, tab3 = st.tabs(["📉 Population Growth Trend", "📊 Growth Rate %", "🌍 World Comparison"])

with tab1:
    fig_pop = go.Figure()
    # Historical
    fig_pop.add_trace(go.Scatter(
        x=DATA["historical"]["years"], y=DATA["historical"]["pop"],
        mode='lines', name='Historical', line=dict(color='#FF6B35', width=3),
        fill='tozeroy', fillcolor='rgba(255, 107, 53, 0.2)'
    ))
    # Projected
    fig_pop.add_trace(go.Scatter(
        x=DATA["projected"]["years"], y=DATA["projected"]["pop"],
        mode='lines', name='Projected', line=dict(color='#1B9C85', width=3, dash='dash'),
        fill='tozeroy', fillcolor='rgba(27, 156, 133, 0.2)'
    ))
    
    # Peak marker
    fig_pop.add_annotation(x=2065, y=1697, text="Peak: 1.697 Billion (2065)", showarrow=True, arrowhead=1)
    
    fig_pop.update_layout(
        title="Historical & Projected Population (in Millions)",
        xaxis_title="Year",
        yaxis_title="Population (Millions)",
        template="plotly_dark",
        hovermode="x unified",
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig_pop, use_container_width=True)

with tab2:
    colors = ['#22c55e' if r >= 0 else '#ef4444' for r in DATA["growth_rate"]["rate"]]
    fig_growth = go.Figure(data=[go.Bar(
        x=DATA["growth_rate"]["years"],
        y=DATA["growth_rate"]["rate"],
        marker_color=colors,
        text=[f"{r}%" for r in DATA["growth_rate"]["rate"]],
        textposition='auto'
    )])
    fig_growth.update_layout(
        title="Annual Population Growth Rate (%)",
        xaxis_title="Year",
        yaxis_title="Growth Rate (%)",
        template="plotly_dark",
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig_growth, use_container_width=True)

with tab3:
    df_comp = pd.DataFrame(DATA["comparison"])
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(
        x=df_comp['Country'], y=df_comp['Pop2025'],
        name='2025', marker_color='#FF6B35'
    ))
    fig_comp.add_trace(go.Bar(
        x=df_comp['Country'], y=df_comp['Pop2050'],
        name='2050 (Projected)', marker_color='#1B9C85'
    ))
    fig_comp.update_layout(
        title="Population Comparison (in Millions)",
        barmode='group',
        template="plotly_dark",
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig_comp, use_container_width=True)

st.markdown("---")

# --- States Section ---
st.markdown("### 🗺️ Top States by Population (2025 est.)")
df_states = pd.DataFrame(DATA["states"])

fig_states = px.bar(
    df_states.sort_values("Population", ascending=True),
    x="Population", y="State", orientation='h',
    color="State", color_discrete_sequence=df_states["Color"].tolist()[::-1],
    text="Population"
)
fig_states.update_traces(texttemplate='%{text} M', textposition='outside')
fig_states.update_layout(
    xaxis_title="Population in Millions",
    yaxis_title="",
    showlegend=False,
    template="plotly_dark",
    height=400,
    margin=dict(l=0, r=0, t=0, b=0)
)
st.plotly_chart(fig_states, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #94a3b8; font-size: 0.9rem;'>
    <p>Data sources: <a href="https://population.un.org/wpp/" target="_blank">UN World Population Prospects</a> & <a href="https://censusindia.gov.in/" target="_blank">Census of India</a></p>
    <p>Built with ❤️ using Python & Streamlit</p>
</div>
""", unsafe_allow_html=True)
