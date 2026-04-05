import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import root_mean_squared_error, r2_score

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="India Population Predictor | ML Version",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
</style>
""", unsafe_allow_html=True)

# ==========================================
# DATA DEFINITIONS
# ==========================================
# Ground truth historical data
HISTORICAL_YEARS = np.array([
    1950, 1955, 1960, 1965, 1970, 1975, 1980, 1985, 1990, 
    1995, 2000, 2005, 2010, 2015, 2020, 2025
]).reshape(-1, 1)

HISTORICAL_POP = np.array([
    376, 409, 450, 499, 555, 623, 698, 784, 873, 
    964, 1057, 1148, 1234, 1310, 1380, 1450
])

# UN Projected data for benchmarking
UN_PROJECTED_YEARS = [2025, 2030, 2035, 2040, 2045, 2050, 2060, 2070, 2080, 2090, 2100]
UN_PROJECTED_POP = [1450, 1515, 1565, 1610, 1645, 1670, 1695, 1690, 1655, 1590, 1533]

STATES_DATA = [
    {"State": "Uttar Pradesh", "Population": 231, "Color": "#FF6B35"},
    {"State": "Maharashtra", "Population": 126, "Color": "#F7C948"},
    {"State": "Bihar", "Population": 124, "Color": "#1B9C85"},
    {"State": "West Bengal", "Population": 100, "Color": "#E94560"},
    {"State": "Madhya Pradesh", "Population": 85, "Color": "#7B68EE"}
]

# ==========================================
# MACHINE LEARNING ENGINE
# ==========================================
@st.cache_resource
def train_models():
    """Trains regression models to forecast population."""
    models = {}
    
    # 1. Linear Regression
    lr = LinearRegression()
    lr.fit(HISTORICAL_YEARS, HISTORICAL_POP)
    models['Linear Regression'] = {'model': lr, 'degree': 1}
    
    # 2. Polynomial Regression (Degree 2)
    poly2 = PolynomialFeatures(degree=2)
    X_poly2 = poly2.fit_transform(HISTORICAL_YEARS)
    lr2 = LinearRegression()
    lr2.fit(X_poly2, HISTORICAL_POP)
    models['Polynomial Regression (2nd Degree)'] = {'model': lr2, 'poly': poly2, 'degree': 2}
    
    # 3. Polynomial Regression (Degree 3)
    poly3 = PolynomialFeatures(degree=3)
    X_poly3 = poly3.fit_transform(HISTORICAL_YEARS)
    lr3 = LinearRegression()
    lr3.fit(X_poly3, HISTORICAL_POP)
    models['Polynomial Regression (3rd Degree)'] = {'model': lr3, 'poly': poly3, 'degree': 3}
    
    return models

def predict_population(models_dict, model_name, year):
    X_pred = np.array([[year]])
    model_obj = models_dict[model_name]
    
    if model_obj['degree'] == 1:
        pred = model_obj['model'].predict(X_pred)
    else:
        poly = model_obj['poly']
        X_poly_pred = poly.transform(X_pred)
        pred = model_obj['model'].predict(X_poly_pred)
        
    return max(0, pred[0]) # Population can't be negative

models = train_models()

# ==========================================
# SIDEBAR CONTROLS
# ==========================================
with st.sidebar:
    st.markdown("## ⚙️ AI Predictor Configuration")
    
    selected_model = st.selectbox(
        "🧠 Select Machine Learning Model:",
        options=list(models.keys()),
        index=1  # Default to Degree 2
    )
    
    st.markdown("---")
    st.markdown("### 🎯 Single Year Predictor")
    selected_year = st.slider("Select Year:", min_value=1950, max_value=2100, value=2050, step=1)
    
    # ML Prediction
    pred_val = predict_population(models, selected_model, selected_year)
    
    st.markdown("#### Model Estimation:")
    st.markdown(f"<h1 style='color: #1B9C85; text-align: center; margin: 0;'>{int(pred_val * 1000000):,}</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Individuals</p>", unsafe_allow_html=True)
    
    # Calculate R2 Score for selected model
    hist_preds = []
    for y in HISTORICAL_YEARS.flatten():
        hist_preds.append(predict_population(models, selected_model, y))
    r2 = r2_score(HISTORICAL_POP, hist_preds)
    
    st.info(f"📈 Model R² Score: {r2:.4f}\n\n(Score near 1.0 indicates perfect fit to historical data)")

# ==========================================
# MAIN APP UI
# ==========================================
st.markdown('<p class="main-header">India Population: ML Predictions</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-driven analysis leveraging historical regression to forecast India\'s demographic future.</p>', unsafe_allow_html=True)

# Generate predictions curve
future_years = np.arange(1950, 2101, 1).reshape(-1, 1)
future_preds = [predict_population(models, selected_model, y) for y in future_years.flatten()]

tab1, tab2, tab3 = st.tabs(["🤖 ML Forecasting Curve", "📊 Model Evaluation vs UN", "🗺️ State Distribution"])

with tab1:
    st.markdown(f"#### Analyzing population growth using: **{selected_model}**")
    
    fig = go.Figure()

    # Model Prediction Line
    fig.add_trace(go.Scatter(
        x=future_years.flatten(), y=future_preds,
        mode='lines', name=f'{selected_model} Prediction',
        line=dict(color='#1B9C85', width=3),
        hovertemplate='Year: %{x}<br>Predicted Pop: %{y:.0f}M<extra></extra>'
    ))
    
    # Historical Data Points
    fig.add_trace(go.Scatter(
        x=HISTORICAL_YEARS.flatten(), y=HISTORICAL_POP,
        mode='markers', name='Actual Historical Data',
        marker=dict(color='#FF6B35', size=8, line=dict(color='white', width=1)),
        hovertemplate='Year: %{x}<br>Actual Pop: %{y}M<extra></extra>'
    ))
    
    # UN Projections Data Points
    fig.add_trace(go.Scatter(
        x=UN_PROJECTED_YEARS, y=UN_PROJECTED_POP,
        mode='lines+markers', name='UN Medium Variant (Baseline)',
        line=dict(color='#F7C948', width=2, dash='dot'),
        marker=dict(size=6),
        hovertemplate='Year: %{x}<br>UN Projected: %{y}M<extra></extra>'
    ))
    
    # Point showing User's Selected Year
    fig.add_trace(go.Scatter(
        x=[selected_year], y=[pred_val],
        mode='markers+text', name='Your Selection',
        marker=dict(color='red', size=12, symbol='star'),
        text=[f"{selected_year}: {int(pred_val)}M"],
        textposition="top center",
        showlegend=False
    ))

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Population (Millions)",
        template="plotly_dark",
        hovermode="x unified",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        height=550
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("#### Error Analysis: How does the ML Model compare?")
    
    # Calculate RMSE against historical
    rmse_hist = root_mean_squared_error(HISTORICAL_POP, hist_preds)
    
    # Calculate RMSE of Model vs UN Projections (for future years)
    un_model_preds = [predict_population(models, selected_model, y) for y in UN_PROJECTED_YEARS]
    rmse_un = root_mean_squared_error(UN_PROJECTED_POP, un_model_preds)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Historical Model RMSE", f"{rmse_hist:.1f} Million", help="Lower is better. Error against known data.")
    with col2:
        st.metric("Deviation from UN Baseline (RMSE)", f"{rmse_un:.1f} Million", help="Difference between AI and UN estimates.")
    
    # Bar chart for residuals
    residuals = HISTORICAL_POP - np.array(hist_preds)
    fig_resid = px.bar(
        x=HISTORICAL_YEARS.flatten(), y=residuals,
        title="Model Residuals (Actual - Predicted) on Historical Data",
        labels={'x': 'Year', 'y': "Residual Error (Millions)"},
        color=residuals, color_continuous_scale="RdBu"
    )
    fig_resid.update_layout(template="plotly_dark")
    st.plotly_chart(fig_resid, use_container_width=True)

with tab3:
    st.markdown("#### Top 5 Most Populous States (2025 Current)")
    df_states = pd.DataFrame(STATES_DATA)
    fig_states = px.pie(
        df_states, values='Population', names='State',
        title="Population Distribution among Top 5 States",
        color='State', color_discrete_map={row['State']: row['Color'] for idx, row in df_states.iterrows()}
    )
    fig_states.update_layout(template="plotly_dark")
    st.plotly_chart(fig_states, use_container_width=True)

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #94a3b8; font-size: 0.9rem;'>
    <p>Machine Learning Engine powered by Scikit-Learn. Datasets: <a href="https://population.un.org/wpp/" target="_blank">UN World Population Prospects</a>.</p>
</div>
""", unsafe_allow_html=True)
