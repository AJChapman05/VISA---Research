# Lab 14 - Portfolio Baselines
# Standard library only. Edit the inputs below to test other capital-market views.

from math import sqrt


# -------------------------
# Editable inputs
# -------------------------

SLEEVES = {
    "Treasury bills": {"expected_return": 0.035, "volatility": 0.005},
    "Treasury 10-year note": {"expected_return": 0.043, "volatility": 0.070},
    "Investment-grade bond fund": {"expected_return": 0.050, "volatility": 0.060},
    "Global equity index fund": {"expected_return": 0.080, "volatility": 0.160},
}

CORRELATIONS = {
    "Treasury bills": {
        "Treasury bills": 1.00,
        "Treasury 10-year note": 0.10,
        "Investment-grade bond fund": 0.05,
        "Global equity index fund": 0.00,
    },
    "Treasury 10-year note": {
        "Treasury bills": 0.10,
        "Treasury 10-year note": 1.00,
        "Investment-grade bond fund": 0.80,
        "Global equity index fund": -0.10,
    },
    "Investment-grade bond fund": {
        "Treasury bills": 0.05,
        "Treasury 10-year note": 0.80,
        "Investment-grade bond fund": 1.00,
        "Global equity index fund": 0.25,
    },
    "Global equity index fund": {
        "Treasury bills": 0.00,
        "Treasury 10-year note": -0.10,
        "Investment-grade bond fund": 0.25,
        "Global equity index fund": 1.00,
    },
}

OBJECTIVE_RETURN = 0.065


# -------------------------
# Reusable calculations
# -------------------------

def validate_correlations(correlations, sleeves):
    """Confirm each correlation is valid and the table is symmetric."""
    names = tuple(sleeves)
    for left in names:
        if left not in correlations:
            raise ValueError(f"Missing correlation row for {left}.")
        for right in names:
            if right not in correlations[left]:
                raise ValueError(f"Missing correlation for {left} and {right}.")
            value = correlations[left][right]
            if not -1.0 <= value <= 1.0:
                raise ValueError(
                    f"Correlation for {left} and {right} must be between -1 and 1."
                )
            if right not in correlations or left not in correlations[right]:
                raise ValueError(f"Missing matching correlation for {right} and {left}.")
            if abs(value - correlations[right][left]) > 1e-12:
                raise ValueError(f"Correlation table is not symmetric: {left}, {right}.")


def build_covariance(sleeves, correlations):
    """Return covariance = correlation x volatility x volatility."""
    return {
        left: {
            right: correlations[left][right]
            * sleeves[left]["volatility"]
            * sleeves[right]["volatility"]
            for right in sleeves
        }
        for left in sleeves
    }


def portfolio_return(weights, sleeves):
    """Calculate the weighted expected return."""
    return sum(weights[name] * sleeves[name]["expected_return"] for name in sleeves)


def portfolio_volatility(weights, covariance):
    """Calculate sqrt(w' Sigma w), the portfolio standard deviation."""
    variance = sum(
        weights[left] * weights[right] * covariance[left][right]
        for left in weights
        for right in weights
    )
    return sqrt(variance)


def reserve_eligible_weight(weights):
    """Reserve-eligible assets in this lab are bills plus the 10-year Treasury note."""
    return weights["Treasury bills"] + weights["Treasury 10-year note"]


def format_percent(value, decimals=2):
    """Format a decimal value as a percent for the lab output."""
    return f"{value:.{decimals}%}"


def print_portfolio(name, weights, sleeves, covariance, objective_return):
    """Print a portfolio's weights, risk/return measures, and objective test."""
    expected_return = portfolio_return(weights, sleeves)
    volatility = portfolio_volatility(weights, covariance)
    reserve_weight = reserve_eligible_weight(weights)
    meets_objective = expected_return >= objective_return

    print(f"\n{name}")
    for sleeve in sleeves:
        print(f"  {sleeve}: {format_percent(weights[sleeve], 1)}")
    print(f"  Expected return: {format_percent(expected_return)}")
    print(f"  Volatility: {format_percent(volatility)}")
    print(f"  Reserve-eligible weight: {format_percent(reserve_weight, 1)}")
    print(f"  Meets {format_percent(objective_return)} objective: {'yes' if meets_objective else 'no'}")


def inverse_volatility_weights(sleeves):
    """Allocate in proportion to 1/volatility, then scale weights to 100%."""
    inverse_vols = {name: 1 / details["volatility"] for name, details in sleeves.items()}
    total = sum(inverse_vols.values())
    return {name: inverse_vols[name] / total for name in sleeves}


def main():
    validate_correlations(CORRELATIONS, SLEEVES)
    covariance = build_covariance(SLEEVES, CORRELATIONS)

    portfolios = {
        "Benchmark": {
            "Treasury bills": 0.00,
            "Treasury 10-year note": 0.00,
            "Investment-grade bond fund": 0.40,
            "Global equity index fund": 0.60,
        },
        "Equal weight": {name: 1 / len(SLEEVES) for name in SLEEVES},
        "Inverse volatility": inverse_volatility_weights(SLEEVES),
    }

    print(f"Objective return: {format_percent(OBJECTIVE_RETURN)}")
    for name, weights in portfolios.items():
        print_portfolio(name, weights, SLEEVES, covariance, OBJECTIVE_RETURN)


if __name__ == "__main__":
    main()
