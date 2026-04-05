# 🇮🇳 India Population ML Predictor

> An AI-powered web application to explore, analyze, and forecast India's population from 1950 to 2100 — built with Python, Streamlit, and Scikit-Learn.

<br>

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://indainpopulationproject-dykvkdfumgoe9wjkkztvgz.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.20-3F4F75?style=flat-square&logo=plotly&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)

---

🌐 **Live App URL:**

> **[https://indainpopulationproject-dykvkdfumgoe9wjkkztvgz.streamlit.app](https://indainpopulationproject-dykvkdfumgoe9wjkkztvgz.streamlit.app)**


## 📸 Screenshots

| Dashboard | Model Comparison |
|-----------|-----------------|
| Live population counter, KPIs, trend chart | All 4 ML models compared side-by-side |

| Forecast | State Analysis |
|----------|----------------|
| Year slider with AI prediction | Bar, Pie, Scatter charts for top 10 states |

---

## ✨ Features

- 🟢 **Live Population Counter** — Real-time estimation using growth-rate math, updates every second
- 🤖 **4 ML Models** — Linear, Polynomial (Degree 2 & 3), and Logistic Growth (Scipy)
- 🔮 **Interactive Forecaster** — Slide to any year (1950–2100) and get an instant ML prediction
- 📊 **Model Comparison** — Overlay all curves, compare R², MAE, and RMSE side-by-side
- 🤖 **ML Explorer** — Inspect any model's fit curve, residuals, and parity plot
- 🗺️ **State Analysis** — Bar, pie, and scatter charts for India's top 10 states
- 📋 **Historical Data Table** — UN World Population Prospects data from 1950–2025

---

## 🧠 Machine Learning Models

| Model | Algorithm | R² Score | Best For |
|-------|-----------|----------|----------|
| Linear Regression | `LinearRegression` | ~0.989 | Baseline, simple trend |
| Polynomial (Degree 2) | `PolynomialFeatures(2)` | ~0.996 | Curved demographic growth |
| Polynomial (Degree 3) | `PolynomialFeatures(3)` | ~0.999 | Peak + decline behaviour |
| Logistic Growth | `scipy.curve_fit` | ~0.998 | S-curve carrying capacity model |

> ✅ **Best Model**: Polynomial Degree 3 — R² ≈ **0.9999** on historical data

All models are trained using **Scikit-Learn** on UN historical data (1950–2025) and cached in the Streamlit session for performance.

---

## 📁 Project Structure

```
india-population-ml/
│
├── app.py                        # 🚀 Entry point — navigation & routing (50 lines)
├── requirements.txt              # Python dependencies
├── README.md
├── .gitignore
│
└── src/                          # Source package
    │
    ├── data/
    │   └── population_data.py    # 📦 All raw datasets & DataFrame builders
    │
    ├── models/
    │   └── ml_models.py          # 🧠 Model training, prediction & evaluation
    │
    ├── pages/
    │   ├── dashboard.py          # 🏠 Overview: KPIs, live counter, trend chart
    │   ├── ml_explorer.py        # 🤖 Inspect any model: fit curve, residuals
    │   ├── forecast.py           # 🔮 Year slider + prediction + reference table
    │   ├── compare.py            # 📊 All models overlaid + metrics table
    │   └── states.py             # 🗺️ State-wise bar, pie, scatter, table
    │
    └── utils/
        └── helpers.py            # 🛠️ CSS injection, live counter, KPI card HTML
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/harishkryadav0506-cpu/Indain_Population_Project.git
cd Indain_Population_Project

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

Open your browser at **http://localhost:8501** 🎉

---



---

## 📊 Data Sources

| Dataset | Source |
|---------|--------|
| Historical Population (1950–2025) | [UN World Population Prospects 2022](https://population.un.org/wpp/) |
| Future Projections (2025–2100) | UN Medium Variant Scenario |
| State-wise Data | [Census of India 2011](https://censusindia.gov.in/) + 2025 estimates |
| Growth Rate, Fertility, Life Expectancy | World Bank / UN |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend / UI | [Streamlit](https://streamlit.io) |
| Charts | [Plotly Express & Graph Objects](https://plotly.com/python/) |
| ML Models | [Scikit-Learn](https://scikit-learn.org/) |
| Logistic Growth | [Scipy `curve_fit`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html) |
| Data Wrangling | [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/) |
| Language | Python 3.9+ |

---

## 📦 Dependencies

```
streamlit>=1.33.0
pandas>=2.0.0
plotly>=5.15.0
scikit-learn>=1.3.0
numpy>=1.24.0
scipy>=1.10.0
```

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute.

---

## 🙌 Acknowledgements

- [United Nations — World Population Prospects](https://population.un.org/wpp/)
- [Census of India](https://censusindia.gov.in/)
- [Streamlit Community](https://discuss.streamlit.io/)
- [Scikit-Learn Documentation](https://scikit-learn.org/stable/)

---

<div align="center">
  Made with ❤️ for India 🇮🇳 &nbsp;|&nbsp; Data Science & ML Project
</div>
