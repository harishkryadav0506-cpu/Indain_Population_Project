"""
Flask route blueprints — main pages and API endpoints.
"""

from flask import Blueprint, render_template, jsonify
from src.data import (
    HISTORICAL_DATA, PROJECTED_DATA, GROWTH_RATE_DATA,
    COMPARISON_DATA, STATE_DATA, PREDICTION_DETAILS, MILESTONES,
    interpolate_population
)

# =============================================================
# BLUEPRINTS
# =============================================================
main_bp = Blueprint("main", __name__)
api_bp = Blueprint("api", __name__)


# =============================================================
# PAGE ROUTES
# =============================================================
@main_bp.route("/")
def index():
    """Main page with all population data."""
    max_state_pop = max(s["population"] for s in STATE_DATA)
    states = []
    for s in STATE_DATA:
        state = dict(s)
        state["bar_pct"] = round(s["population"] / max_state_pop * 100)
        states.append(state)

    return render_template(
        "index.html",
        states=states,
        predictions=PREDICTION_DETAILS,
        milestones=MILESTONES,
        comparison=COMPARISON_DATA,
    )


# =============================================================
# API ROUTES
# =============================================================
@api_bp.route("/population")
def api_population():
    """API: Get all population data for charts."""
    hist_years = sorted(HISTORICAL_DATA.keys())
    proj_years = sorted(PROJECTED_DATA.keys())
    growth_years = sorted(GROWTH_RATE_DATA.keys())

    return jsonify({
        "historical": {
            "years": hist_years,
            "population": [HISTORICAL_DATA[y] for y in hist_years]
        },
        "projected": {
            "years": proj_years,
            "population": [PROJECTED_DATA[y] for y in proj_years]
        },
        "growthRate": {
            "years": growth_years,
            "rate": [GROWTH_RATE_DATA[y] for y in growth_years]
        },
        "comparison": COMPARISON_DATA
    })


@api_bp.route("/predict/<int:year>")
def api_predict(year):
    """API: Predict population for a specific year."""
    if year < 1950 or year > 2100:
        return jsonify({"error": "Year must be between 1950 and 2100"}), 400

    pop_millions = interpolate_population(year)
    pop_full = round(pop_millions * 1_000_000)

    return jsonify({
        "year": year,
        "population_millions": round(pop_millions, 2),
        "population": pop_full,
        "formatted": f"{pop_full:,}"
    })


@api_bp.route("/states")
def api_states():
    """API: Get state-wise population data."""
    return jsonify(STATE_DATA)
