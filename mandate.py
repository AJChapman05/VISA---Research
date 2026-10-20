# Lab 13 - Portfolio Mandate Checker
# Standard library only.

# -------------------------
# Editable inputs
# -------------------------

HOLDINGS = {
    "Cash": {
        "issuer": "none",
        "business_days_to_redeem": 0,
        "reserve_eligible": True,
        "issuer_exempt": True,
    },
    "Treasury bills": {
        "issuer": "U.S. Treasury",
        "business_days_to_redeem": 1,
        "reserve_eligible": True,
        "issuer_exempt": True,
    },
    "Treasury 10-year note": {
        "issuer": "U.S. Treasury",
        "business_days_to_redeem": 1,
        "reserve_eligible": True,
        "issuer_exempt": True,
    },
    "Global equity index fund": {
        "issuer": "diversified fund",
        "business_days_to_redeem": 2,
        "reserve_eligible": False,
        "issuer_exempt": True,
    },
    "Investment-grade bond fund": {
        "issuer": "diversified fund",
        "business_days_to_redeem": 3,
        "reserve_eligible": False,
        "issuer_exempt": True,
    },
    "Private real estate fund": {
        "issuer": "diversified fund",
        "business_days_to_redeem": 90,
        "reserve_eligible": False,
        "issuer_exempt": True,
    },
    "Acme Corp bonds": {
        "issuer": "Acme Corp",
        "business_days_to_redeem": 4,
        "reserve_eligible": False,
        "issuer_exempt": False,
    },
    "Acme Corp stock": {
        "issuer": "Acme Corp",
        "business_days_to_redeem": 1,
        "reserve_eligible": False,
        "issuer_exempt": False,
    },
}

CANDIDATES = {
    "A": {
        "Cash": 2,
        "Treasury bills": 2,
        "Treasury 10-year note": 10,
        "Global equity index fund": 60,
        "Investment-grade bond fund": 26,
        "Private real estate fund": 0,
        "Acme Corp bonds": 0,
        "Acme Corp stock": 0,
    },
    "B": {
        "Cash": 1,
        "Treasury bills": 0,
        "Treasury 10-year note": 0,
        "Global equity index fund": 55,
        "Investment-grade bond fund": 20,
        "Private real estate fund": 15,
        "Acme Corp bonds": 5,
        "Acme Corp stock": 4,
    },
    "C": {
        "Cash": 1,
        "Treasury bills": 1,
        "Treasury 10-year note": 0,
        "Global equity index fund": 70,
        "Investment-grade bond fund": 20,
        "Private real estate fund": 0,
        "Acme Corp bonds": 0,
        "Acme Corp stock": 8,
    },
    "D": {
        "Cash": 3,
        "Treasury bills": 0,
        "Treasury 10-year note": 0,
        "Global equity index fund": 0,
        "Investment-grade bond fund": 97,
        "Private real estate fund": 0,
        "Acme Corp bonds": 0,
        "Acme Corp stock": 0,
    },
    "E": {
        "Cash": 0,
        "Treasury bills": 0,
        "Treasury 10-year note": 0,
        "Global equity index fund": 60,
        "Investment-grade bond fund": 40,
        "Private real estate fund": 0,
        "Acme Corp bonds": 0,
        "Acme Corp stock": 0,
    },
}

RESERVE_SIZE = 100.0            # USD millions
QUARTERLY_DISTRIBUTION = 0.75   # USD millions
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW = 5            # business days
MINIMUM_LIQUID_SHARE = 90.0     # percent
ISSUER_LIMIT = 8.0              # percent


# -------------------------
# Calculations
# -------------------------

def label(passes):
    return "pass" if passes else "FAIL"


def reserve_minimum_percent():
    return (
        QUARTERS_TO_COVER
        * QUARTERLY_DISTRIBUTION
        / RESERVE_SIZE
        * 100
    )


def reserve_eligible_weight(candidate):
    return sum(
        weight
        for holding, weight in candidate.items()
        if HOLDINGS[holding]["reserve_eligible"]
    )


def liquid_weight(candidate):
    return sum(
        weight
        for holding, weight in candidate.items()
        if HOLDINGS[holding]["business_days_to_redeem"] <= LIQUIDITY_WINDOW
    )


def largest_single_company_weight(candidate):
    issuer_weights = {}

    for holding, weight in candidate.items():
        details = HOLDINGS[holding]

        if not details["issuer_exempt"]:
            issuer = details["issuer"]
            issuer_weights[issuer] = issuer_weights.get(issuer, 0) + weight

    return max(issuer_weights.values(), default=0.0)


def check_candidate(name, candidate, reserve_minimum):
    total_weight = sum(candidate.values())
    lowest_weight = min(candidate.values())
    reserve_weight = reserve_eligible_weight(candidate)
    liquid_share = liquid_weight(candidate)
    largest_issuer = largest_single_company_weight(candidate)

    checks = [
        abs(total_weight - 100.0) < 0.0001,
        lowest_weight >= 0,
        reserve_weight >= reserve_minimum,
        liquid_share >= MINIMUM_LIQUID_SHARE,
        largest_issuer <= ISSUER_LIMIT,
    ]

    print(f"\nCandidate {name}")
    print(f"Weights sum to 100: {total_weight:.1f} {label(checks[0])}")
    print(f"Long-only (lowest weight): {lowest_weight:.1f} {label(checks[1])}")
    print(
        f"Reserve >= {reserve_minimum:.1f}%: "
        f"{reserve_weight:.1f} {label(checks[2])}"
    )
    print(
        f"Redeemable within {LIQUIDITY_WINDOW} business days "
        f">= {MINIMUM_LIQUID_SHARE:.1f}%: "
        f"{liquid_share:.1f} {label(checks[3])}"
    )
    print(
        f"Largest single company <= {ISSUER_LIMIT:.1f}%: "
        f"{largest_issuer:.1f} {label(checks[4])}"
    )
    print("Calendar-year loss: requires CIO clarification")

    failed_rules = checks.count(False)

    if failed_rules == 0:
        print("Verdict: passes every checkable rule")
    else:
        print(f"Verdict: fails {failed_rules} rule(s)")


def main():
    reserve_minimum = reserve_minimum_percent()

    print(f"Reserve minimum: {reserve_minimum:.1f}%")

    for name, candidate in CANDIDATES.items():
        check_candidate(name, candidate, reserve_minimum)


if __name__ == "__main__":
    main()
