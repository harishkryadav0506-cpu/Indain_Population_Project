# India Population Prediction 🇮🇳

A stunning, interactive web application for visualizing India's population trends and predictions from 1950 to 2100.

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.x-green?style=flat-square&logo=flask)
![Chart.js](https://img.shields.io/badge/Chart.js-4.x-orange?style=flat-square)

## 🌟 Features

- **Live Population Counter** — Real-time estimation updating every second
- **Interactive Charts** — Population trends, growth rates & world comparison
- **Population Predictor** — Slider to predict population for any year (1950-2100)
- **State-wise Data** — Top 8 most populous Indian states
- **Timeline** — Key population milestones
- **REST API** — JSON endpoints for population data
- **Responsive Design** — Works on desktop, tablet & mobile

## 📁 Project Structure

```
india-population-prediction/
├── app.py                     # Entry point (run this)
├── requirements.txt           # Python dependencies
├── Procfile                   # Deployment config (Gunicorn)
├── render.yaml                # Render.com auto-deploy config
├── .gitignore
├── README.md
│
└── src/                       # Source code package
    ├── __init__.py            # Flask app factory
    ├── config.py              # App configuration
    ├── data.py                # Population data & interpolation
    ├── routes.py              # Page & API route blueprints
    ├── templates/
    │   └── index.html         # Jinja2 HTML template
    └── static/
        ├── css/
        │   └── style.css      # Styles & animations
        └── js/
            └── app.js         # Charts, counter, interactivity
```

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Open http://localhost:5000
```

### API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Main web page |
| `GET /api/population` | All population data (historical + projected) |
| `GET /api/predict/<year>` | Predict population for a specific year (1950-2100) |
| `GET /api/states` | State-wise population data |

### Example API Response

```bash
GET /api/predict/2050
```
```json
{
  "year": 2050,
  "population_millions": 1670.0,
  "population": 1670000000,
  "formatted": "1,670,000,000"
}
```

## 📦 Deployment

### Deploy to Render (Recommended - Free)

1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. Click **New > Web Service**
4. Connect your GitHub repo
5. Settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Click **Deploy** ✅

### Deploy to Railway

1. Push code to GitHub
2. Go to [railway.app](https://railway.app)
3. Click **New Project > Deploy from GitHub**
4. Select your repo — it auto-detects Flask
5. Done! 🚀

## 📊 Data Sources

- [UN World Population Prospects](https://population.un.org/wpp/)
- [Census of India](https://censusindia.gov.in/)
- [World Bank](https://data.worldbank.org/)

## 🛠️ Tech Stack

- **Backend**: Python 3.9+, Flask, Blueprints
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js 4.x
- **Fonts**: Google Fonts (Inter, Outfit)
- **Server**: Gunicorn (production)

---

Made with ❤️ for India
