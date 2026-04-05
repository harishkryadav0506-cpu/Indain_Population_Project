"""
src/data/population_data.py
============================
Single source of truth for all population datasets.
Source: UN World Population Prospects (2022) + Census of India.
"""

import pandas as pd
import numpy as np

# ─────────────────────────────────────────────
# HISTORICAL DATA  (1950 – 2025)
# ─────────────────────────────────────────────
HISTORICAL_RAW = {
    "year":             [1950,1955,1960,1965,1970,1975,1980,1985,1990,1995,
                         2000,2005,2010,2015,2020,2025],
    "population_m":     [376, 409, 450, 499, 555, 623, 698, 784, 873, 964,
                         1057,1148,1234,1310,1380,1450],
    "growth_rate_pct":  [1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.3, 2.1, 2.1, 1.9,
                         1.8, 1.7, 1.5, 1.3, 1.0, 0.9],
    "urban_pct":        [17,  19,  18,  20,  20,  21,  23,  25,  26,  27,
                         28,  29,  31,  33,  35,  36],
    "life_expectancy":  [36,  40,  43,  47,  50,  54,  55,  57,  59,  61,
                         63,  64,  66,  68,  69,  70],
    "fertility_rate":   [5.9, 5.9, 5.8, 5.7, 5.4, 4.8, 4.5, 4.2, 3.7, 3.4,
                         3.2, 2.9, 2.5, 2.2, 2.1, 2.0],
}

# ─────────────────────────────────────────────
# UN MEDIUM-VARIANT PROJECTIONS  (2025 – 2100)
# ─────────────────────────────────────────────
UN_PROJECTED_RAW = {
    "year":           [2025,2030,2035,2040,2045,2050,
                       2055,2060,2065,2070,2075,2080,
                       2085,2090,2095,2100],
    "population_m":   [1450,1515,1565,1610,1645,1670,
                       1685,1695,1697,1690,1675,1655,
                       1625,1590,1560,1533],
}

# ─────────────────────────────────────────────
# STATE-WISE DATA  (2025 estimates)
# ─────────────────────────────────────────────
STATES_RAW = {
    "state":         ["Uttar Pradesh","Maharashtra","Bihar","West Bengal",
                      "Madhya Pradesh","Tamil Nadu","Rajasthan","Karnataka",
                      "Andhra Pradesh","Odisha"],
    "population_m":  [231, 126, 124, 100, 85, 78, 79, 68, 54, 46],
    "area_km2":      [240928,307713,94163,88752,308252,
                      130058,342239,191791,162975,155707],
    "literacy_pct":  [67.7, 82.9, 61.8, 76.3, 69.3,
                      80.1, 66.1, 75.6, 67.0, 72.9],
    "region":        ["North","West","East","East","Central",
                      "South","North","South","South","East"],
    "color":         ["#FF6B35","#F7C948","#1B9C85","#E94560",
                      "#7B68EE","#FF6B9D","#20C997","#4ECDC4",
                      "#FF9F43","#54A0FF"],
}

# ─────────────────────────────────────────────
# HELPER: Build DataFrames (cached-ready)
# ─────────────────────────────────────────────

def get_historical_df() -> pd.DataFrame:
    """Returns historical population DataFrame."""
    return pd.DataFrame(HISTORICAL_RAW)


def get_un_projected_df() -> pd.DataFrame:
    """Returns UN medium-variant projection DataFrame."""
    return pd.DataFrame(UN_PROJECTED_RAW)


def get_states_df() -> pd.DataFrame:
    """Returns state-wise demographic DataFrame with derived columns."""
    df = pd.DataFrame(STATES_RAW)
    df["density"]    = (df["population_m"] * 1_000_000 / df["area_km2"]).round(0)
    df["share_pct"]  = (df["population_m"] / 1450 * 100).round(2)
    return df


def get_training_arrays():
    """Returns (X, y) numpy arrays suitable for sklearn."""
    df = get_historical_df()
    X = df["year"].values.reshape(-1, 1)
    y = df["population_m"].values
    return X, y
