"""
src/models/ml_models.py
========================
Machine-learning model training and prediction logic.

Models trained:
  1. Linear Regression
  2. Polynomial Regression (degree 2)
  3. Polynomial Regression (degree 3)
  4. Logistic Growth  (scipy curve_fit)
"""

from __future__ import annotations

import numpy as np
import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from scipy.optimize import curve_fit
from typing import Dict, Any

from src.data.population_data import get_training_arrays

# ─────────────────────────────────────────────
# TYPE ALIAS
# ─────────────────────────────────────────────
ModelDict = Dict[str, Any]   # keys: model, type, r2, mae, rmse, color, desc, …


# ─────────────────────────────────────────────
# LOGISTIC GROWTH FUNCTION
# ─────────────────────────────────────────────
def _logistic(t: np.ndarray, L: float, k: float, t0: float) -> np.ndarray:
    """Classic sigmoid / logistic growth curve."""
    return L / (1 + np.exp(-k * (t - t0)))


# ─────────────────────────────────────────────
# TRAINING
# ─────────────────────────────────────────────
@st.cache_resource
def train_all_models() -> ModelDict:
    """
    Train all ML models on historical data.
    Results are cached by Streamlit so training only runs once per session.
    """
    X, y = get_training_arrays()
    trained: ModelDict = {}

    # ── 1. Linear Regression ──────────────────
    lr = LinearRegression().fit(X, y)
    _reg_entry(trained, "Linear Regression", lr, None, 1, X, y,
               color="#7B68EE",
               desc="Straight-line model — fast but ignores demographic inflection.")

    # ── 2. Polynomial Degree 2 ────────────────
    poly2 = PolynomialFeatures(degree=2)
    X2    = poly2.fit_transform(X)
    lr2   = LinearRegression().fit(X2, y)
    _reg_entry(trained, "Polynomial (Degree 2)", lr2, poly2, 2, X2, y,
               color="#FF6B35",
               desc="Quadratic curve — captures accelerating + decelerating growth phase.")

    # ── 3. Polynomial Degree 3 ────────────────
    poly3 = PolynomialFeatures(degree=3)
    X3    = poly3.fit_transform(X)
    lr3   = LinearRegression().fit(X3, y)
    _reg_entry(trained, "Polynomial (Degree 3)", lr3, poly3, 3, X3, y,
               color="#1B9C85",
               desc="Cubic curve — adds peak + decline behaviour for demographic transition.")

    # ── 4. Logistic Growth ────────────────────
    try:
        popt, _ = curve_fit(
            _logistic, X.flatten(), y,
            p0=[1750, 0.04, 2000],
            maxfev=15_000,
            bounds=([1200, 0.001, 1960], [2500, 0.5, 2070]),
        )
        y_log = _logistic(X.flatten(), *popt)
        trained["Logistic Growth"] = {
            "type":   "logistic",
            "params": popt,
            "r2":     r2_score(y, y_log),
            "mae":    mean_absolute_error(y, y_log),
            "rmse":   np.sqrt(mean_squared_error(y, y_log)),
            "color":  "#F7C948",
            "desc":   (
                f"S-curve — predicts carrying capacity ≈ {int(popt[0])}M "
                f"with inflection ≈ {int(popt[2])}."
            ),
        }
    except RuntimeError:
        pass   # curve_fit didn't converge — skip

    return trained


def _reg_entry(
    store: ModelDict,
    name: str,
    model: LinearRegression,
    poly: PolynomialFeatures | None,
    degree: int,
    X_fit: np.ndarray,
    y: np.ndarray,
    color: str,
    desc: str,
) -> None:
    """Helper that stores a regression model entry in `store`."""
    y_pred = model.predict(X_fit)
    store[name] = {
        "type":   "linear" if degree == 1 else "poly",
        "model":  model,
        "poly":   poly,
        "degree": degree,
        "r2":     r2_score(y, y_pred),
        "mae":    mean_absolute_error(y, y_pred),
        "rmse":   np.sqrt(mean_squared_error(y, y_pred)),
        "color":  color,
        "desc":   desc,
    }


# ─────────────────────────────────────────────
# PREDICTION
# ─────────────────────────────────────────────
def predict(model_info: dict, year: int | float) -> float:
    """
    Predict population (in millions) for a given year using a model dict.

    Args:
        model_info: Entry from the dict returned by `train_all_models()`.
        year:       Target calendar year.

    Returns:
        Predicted population in millions (clamped to ≥ 0).
    """
    X_in = np.array([[year]])
    mtype = model_info["type"]

    if mtype == "linear":
        val = model_info["model"].predict(X_in)[0]

    elif mtype == "poly":
        Xp  = model_info["poly"].transform(X_in)
        val = model_info["model"].predict(Xp)[0]

    elif mtype == "logistic":
        L, k, t0 = model_info["params"]
        val = _logistic(np.array([year]), L, k, t0)[0]

    else:
        val = 0.0

    return float(max(0.0, round(val, 4)))


def best_model_name(models: ModelDict) -> str:
    """Returns the name of the model with the highest R² score."""
    return max(models, key=lambda k: models[k]["r2"])


def get_residuals(model_info: dict, years: np.ndarray, actuals: np.ndarray) -> np.ndarray:
    """Compute residuals (actual − predicted) for a model over historical years."""
    preds = np.array([predict(model_info, int(y)) for y in years])
    return actuals - preds
