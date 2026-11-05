import pytest

from analysis import burry_checks, build_yearly_rows, cathie_revenue_growth, cathie_wood_checks, check_status, latest_liabilities_to_equity, unprinted_number_warning


def complete_row(**changes):
    row = {"fiscal_year_end": "2026-08-30", "net_income": 20.0, "equity": 100.0, "operating_cash_flow": 40.0, "capital_spending": 10.0, "roe": 0.20, "owner_earnings": 30.0}
    row.update(changes)
    return row


def five_rows(**changes):
    return [complete_row(fiscal_year_end=f"202{index}-08-30", **changes) for index in range(2, 7)]


def test_missing_capex_makes_owner_earnings_checks_not_known():
    ends = ["2022-08-28", "2023-09-03", "2024-09-01", "2025-08-31", "2026-08-30"]

    def units(values):
        return [
            {"form": "10-K", "fy": 2022 + index, "fp": "FY", "start": f"{int(end[:4]) - 1}-09-01", "end": end, "filed": f"202{index + 3}-10-01", "accn": str(index), "val": value}
            for index, (end, value) in enumerate(zip(ends, values))
        ]

    facts = {"facts": {"us-gaap": {
        "RevenueFromContractWithCustomerExcludingAssessedTax": {"units": {"USD": units([100, 110, 120, 130, 140])}},
        "NetIncomeLoss": {"units": {"USD": units([20, 20, 20, 20, 20])}},
        "NetCashProvidedByUsedInOperatingActivities": {"units": {"USD": units([40, 40, 40, 40, 40])}},
        "PaymentsToAcquirePropertyPlantAndEquipment": {"units": {"USD": units([10, 10, 10, 10])}},
        "StockholdersEquity": {"units": {"USD": [{"form": "10-K", "fy": 2022 + index, "fp": "FY", "end": end, "filed": f"202{index + 3}-10-01", "accn": str(index), "val": 100} for index, end in enumerate(ends)]}},
    }}}
    rows = build_yearly_rows(facts)
    assert rows[-1]["capital_spending"] is None
    assert rows[-1]["owner_earnings"] is None
    checks = check_status(rows)
    assert checks["Owner earnings are positive every year"] == "not known"
    assert checks["Owner earnings grew from the first year to the last year"] == "not known"


def test_zero_or_negative_equity_makes_roe_not_known():
    for equity in (0.0, -1.0):
        rows = five_rows()
        rows[1]["equity"] = equity
        rows[1]["roe"] = None
        assert check_status(rows)["ROE is 15% or more every year"] == "not known"


def test_unprinted_number_warning_detects_manual_financial_number():
    rows = five_rows()
    assert "99,999" in unprinted_number_warning("Recommendation: watch it. Financial detail: 99,999.", rows)


def test_missing_research_and_development_is_not_known_for_cathie():
    rows = five_rows()
    for row in rows:
        row["revenue"] = 100.0
        row["research_and_development"] = None
    assert cathie_wood_checks(rows)["Latest R&D divided by latest revenue is at least 5%"] == "not known"


def test_missing_liabilities_or_nonpositive_equity_is_not_known_for_burry():
    rows = five_rows()
    for row in rows:
        row["liabilities"] = 100.0
    rows[-1]["liabilities"] = None
    assert burry_checks(rows)["Latest liabilities are no more than twice latest equity"] == "not known"
    rows[-1]["liabilities"] = 100.0
    rows[-1]["equity"] = 0.0
    assert burry_checks(rows)["Latest liabilities are no more than twice latest equity"] == "not known"
    rows[-1]["equity"] = -1.0
    assert burry_checks(rows)["Latest liabilities are no more than twice latest equity"] == "not known"


def test_missing_cathie_growth_input_is_not_known():
    rows = five_rows()
    for row in rows:
        row["revenue"] = 100.0
    rows[0]["revenue"] = None
    assert cathie_wood_checks(rows)["Revenue annual growth from first to last year is at least 15%"] == "not known"


def cost_lab_19_fixture():
    """Offline COST facts in USD for the known Lab 19 screen result."""
    values = [
        ("2022-08-28", 226_954, 5_844, 7_392, 3_891, 20_642, 43_519),
        ("2023-09-03", 242_290, 6_292, 11_068, 4_323, 25_058, 43_936),
        ("2024-09-01", 254_453, 7_367, 11_339, 4_710, 23_622, 46_209),
        ("2025-08-31", 275_235, 8_099, 13_335, 5_498, 29_164, 47_935),
        ("2026-08-30", 303_154, 9_226, 15_817, 6_435, 35_803, 53_242),
    ]
    rows = []
    for fiscal_year_end, revenue, net_income, cash_flow, capex, equity, liabilities in values:
        row = {
            "fiscal_year_end": fiscal_year_end,
            "revenue": revenue * 1_000_000,
            "net_income": net_income * 1_000_000,
            "operating_cash_flow": cash_flow * 1_000_000,
            "capital_spending": capex * 1_000_000,
            "research_and_development": None,
            "equity": equity * 1_000_000,
            "liabilities": liabilities * 1_000_000,
        }
        row["roe"] = row["net_income"] / row["equity"]
        row["owner_earnings"] = row["operating_cash_flow"] - row["capital_spending"]
        rows.append(row)
    return rows


def test_cost_lab_19_fixture_has_required_investor_results():
    rows = cost_lab_19_fixture()
    assert list(check_status(rows).values()) == ["pass", "pass", "pass"]
    assert cathie_revenue_growth(rows) == pytest.approx(0.0751, abs=0.0001)
    cathie = cathie_wood_checks(rows)
    assert cathie["Revenue annual growth from first to last year is at least 15%"] == "fail"
    assert cathie["Latest R&D divided by latest revenue is at least 5%"] == "not known"
    assert list(burry_checks(rows).values()) == ["pass", "pass"]
    assert latest_liabilities_to_equity(rows) == pytest.approx(1.49, abs=0.01)


@pytest.mark.parametrize("investor", ["Buffett", "Cathie Wood", "Michael Burry"])
def test_unprinted_number_in_any_investor_memo_triggers_warning(investor):
    rows = five_rows()
    memo = f"# {investor} Memo\n\nUnsupported financial number: 99,999."
    assert "99,999" in unprinted_number_warning(memo, rows)


