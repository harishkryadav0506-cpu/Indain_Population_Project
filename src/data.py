"""
Population data and interpolation logic.
All data sourced from UN World Population Prospects (Medium Variant).
"""


# =============================================================
# HISTORICAL POPULATION DATA (in millions)
# =============================================================
HISTORICAL_DATA = {
    1950: 376, 1955: 409, 1960: 450, 1965: 499,
    1970: 555, 1975: 623, 1980: 698, 1985: 784,
    1990: 873, 1995: 964, 2000: 1057, 2005: 1148,
    2010: 1234, 2015: 1310, 2020: 1380, 2025: 1450
}

# =============================================================
# PROJECTED POPULATION DATA (UN medium variant, in millions)
# =============================================================
PROJECTED_DATA = {
    2025: 1450, 2030: 1515, 2035: 1565, 2040: 1610,
    2045: 1645, 2050: 1670, 2055: 1685, 2060: 1695,
    2065: 1697, 2070: 1690, 2075: 1675, 2080: 1655,
    2085: 1625, 2090: 1590, 2095: 1560, 2100: 1533
}

# =============================================================
# GROWTH RATE DATA (% per year)
# =============================================================
GROWTH_RATE_DATA = {
    1950: 1.8, 1960: 2.0, 1970: 2.2, 1980: 2.3,
    1990: 2.1, 2000: 1.8, 2010: 1.5, 2020: 1.0,
    2025: 0.9, 2030: 0.8, 2040: 0.5, 2050: 0.3,
    2060: 0.1, 2070: -0.05, 2080: -0.15, 2090: -0.25, 2100: -0.3
}

# =============================================================
# WORLD COMPARISON DATA (population in millions)
# =============================================================
COMPARISON_DATA = {
    "countries": ["India", "China", "USA", "Indonesia", "Pakistan", "Brazil", "Nigeria"],
    "pop2025": [1450, 1410, 340, 280, 240, 215, 230],
    "pop2050": [1670, 1310, 375, 315, 370, 230, 400]
}

# =============================================================
# STATE-WISE DATA
# =============================================================
STATE_DATA = [
    {"rank": 1, "name": "Uttar Pradesh",   "population": 231, "color": "#FF6B35"},
    {"rank": 2, "name": "Maharashtra",      "population": 126, "color": "#F7C948"},
    {"rank": 3, "name": "Bihar",            "population": 124, "color": "#1B9C85"},
    {"rank": 4, "name": "West Bengal",      "population": 100, "color": "#E94560"},
    {"rank": 5, "name": "Madhya Pradesh",   "population": 85,  "color": "#7B68EE"},
    {"rank": 6, "name": "Tamil Nadu",       "population": 78,  "color": "#FF6B9D"},
    {"rank": 7, "name": "Rajasthan",        "population": 79,  "color": "#20C997"},
    {"rank": 8, "name": "Karnataka",        "population": 68,  "color": "#4ECDC4"},
]

# =============================================================
# PREDICTION CARDS DATA
# =============================================================
PREDICTION_DETAILS = [
    {
        "year": 2030, "population": "1.515 Billion",
        "growth_rate": "+0.8%", "growth_class": "up",
        "median_age": "30.5 yrs", "urban_pct": "40%",
        "bar_width": 60, "featured": False
    },
    {
        "year": 2065, "population": "1.697 Billion",
        "growth_rate": "~0%", "growth_class": "neutral",
        "median_age": "40.2 yrs", "urban_pct": "55%",
        "bar_width": 100, "featured": True
    },
    {
        "year": 2050, "population": "1.670 Billion",
        "growth_rate": "+0.3%", "growth_class": "up",
        "median_age": "37.5 yrs", "urban_pct": "50%",
        "bar_width": 85, "featured": False
    },
    {
        "year": 2100, "population": "1.533 Billion",
        "growth_rate": "-0.3%", "growth_class": "down",
        "median_age": "48.1 yrs", "urban_pct": "68%",
        "bar_width": 72, "featured": False
    },
]

# =============================================================
# POPULATION MILESTONES
# =============================================================
MILESTONES = [
    {"year": 1947, "text": "Independence: Population ~340 Million", "active": False},
    {"year": 1966, "text": "Crossed 500 Million mark", "active": False},
    {"year": 1998, "text": "Reached 1 Billion — 2nd country ever", "active": False},
    {"year": 2023, "text": "Surpassed China as World's Most Populous Nation", "active": False},
    {"year": 2065, "text": "Projected Peak: ~1.7 Billion", "active": True},
]


# =============================================================
# INTERPOLATION FUNCTION
# =============================================================
def interpolate_population(year: int) -> float:
    """
    Interpolate population for any year between 1950-2100.

    Args:
        year: The year to predict population for (1950-2100).

    Returns:
        Estimated population in millions.
    """
    all_data = {**HISTORICAL_DATA, **PROJECTED_DATA}
    years = sorted(all_data.keys())
    pops = [all_data[y] for y in years]

    if year <= years[0]:
        return pops[0]
    if year >= years[-1]:
        return pops[-1]

    for i in range(len(years) - 1):
        if years[i] <= year <= years[i + 1]:
            t = (year - years[i]) / (years[i + 1] - years[i])
            return pops[i] + t * (pops[i + 1] - pops[i])

    return 0
