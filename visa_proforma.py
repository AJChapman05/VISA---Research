"""Five-year Visa Inc. three-statement pro-forma (USD millions).

Run: python3 visa_proforma.py
Test the balance-sheet safeguard: python3 visa_proforma.py --break-fy2026
"""

from dataclasses import dataclass
import sys


YEARS = range(2026, 2031)

# FY2025 opening-balance-sheet values are from Visa's FY2025 Form 10-K,
# Consolidated Balance Sheets: cash and cash equivalents $17,164 million;
# PP&E and technology, net $4,236 million; total assets $99,627 million;
# total liabilities $61,718 million; debt $25,171 million; and total equity
# $37,909 million. Other assets = $99,627 - $17,164 - $4,236 = $78,227 million.
# Other liabilities = $61,718 - $25,171 = $36,547 million.
# Source: https://www.sec.gov/Archives/edgar/data/1403161/000140316125000089/v-20250930.htm
OPENING = {
    "revenue": 40_000.0,
    "cash": 17_164.0,
    "ppe": 4_236.0,
    "other_assets": 78_227.0,
    "debt": 25_171.0,
    "other_liabilities": 36_547.0,
    "equity": 37_909.0,
}

# Assumptions, all expressed as decimals unless otherwise noted.
REVENUE_GROWTH = 0.10
OPERATING_COST_RATIO = 0.31       # excluding D&A and the FY25 litigation charge
DEPRECIATION_RATE = 1_220.0 / 3_824.0
CAPEX_RATIO = 0.04
TAX_RATE = 4_136.0 / 24_194.0
INTEREST_RATE = 589.0 / 25_171.0
OTHER_NWC_RATE = 0.02
DIVIDENDS = 4_800.0
BUYBACKS = 10_000.0
MINIMUM_CASH = 5_000.0
REVOLVER_LIMIT = 10_000.0
REVOLVER_RATE = 0.06
COST_OF_EQUITY = 0.085
TERMINAL_GROWTH = 0.03
SHARES_OUTSTANDING = 1_815.0


@dataclass
class BalanceSheet:
    revenue: float
    cash: float
    ppe: float
    other_assets: float
    debt: float
    other_liabilities: float
    revolver: float
    equity: float


def assert_balanced(year, balance_sheet):
    """Refuse a pro-forma year that does not balance or lacks liquidity."""
    assets = balance_sheet.cash + balance_sheet.ppe + balance_sheet.other_assets
    liabilities = balance_sheet.debt + balance_sheet.other_liabilities + balance_sheet.revolver
    gap = assets - liabilities - balance_sheet.equity
    if abs(gap) > 0.05:
        raise AssertionError(f"FY{year}E is not balanced: gap {gap:.1f}")
    if balance_sheet.cash < MINIMUM_CASH - 0.05:
        raise AssertionError(f"FY{year}E cash is below the ${MINIMUM_CASH:,.0f} minimum: {balance_sheet.cash:.1f}")


def print_table(title, rows):
    print(f"\n{title}")
    print(f"{'':31}" + "".join(f"{year:>12}E" for year in YEARS))
    for label, values in rows.items():
        print(f"{label:31}" + "".join(f"{value:>12,.1f}" for value in values))


def build_proforma(break_fy2026=False):
    opening = BalanceSheet(revolver=0.0, **OPENING)
    income = {line: [] for line in (
        "Net revenue", "Operating costs excl. D&A", "Depreciation & amortization",
        "Operating income", "Interest expense", "Pretax income", "Tax", "Net income")}
    balance = {line: [] for line in (
        "Cash & equivalents", "PP&E and technology", "Other assets", "Debt",
        "Other liabilities", "Revolver", "Equity")}
    cash_flow = {line: [] for line in (
        "Net income", "Depreciation & amortization", "Capital spending",
        "Change in other operating assets", "Change in other liabilities",
        "FCFE before distributions", "Dividends", "Share repurchases", "Change in cash")}
    checks = {line: [] for line in ("Assets - liabilities - equity", "Cash above minimum")}

    for year in YEARS:
        prior = opening
        revenue = prior.revenue * (1 + REVENUE_GROWTH)
        operating_costs = revenue * OPERATING_COST_RATIO
        depreciation = prior.ppe * DEPRECIATION_RATE
        operating_income = revenue - operating_costs - depreciation
        interest = (prior.debt * INTEREST_RATE) + (prior.revolver * REVOLVER_RATE)
        pretax_income = operating_income - interest
        tax = max(0.0, pretax_income) * TAX_RATE
        net_income = pretax_income - tax

        capex = revenue * CAPEX_RATIO
        ppe = prior.ppe + capex - depreciation
        change_other_assets = OTHER_NWC_RATE * (revenue - prior.revenue)
        other_assets = prior.other_assets + change_other_assets
        # Settlement, client-incentive and accrued-liability balances are grouped
        # here; holding net working capital flat is a transparent conservative
        # simplification for this asset-light network business.
        change_other_liabilities = change_other_assets
        other_liabilities = prior.other_liabilities + change_other_liabilities
        debt = prior.debt
        equity = prior.equity + net_income - DIVIDENDS - BUYBACKS

        fcfe = (net_income + depreciation - capex - change_other_assets
                + change_other_liabilities)
        cash_before_revolver = prior.cash + fcfe - DIVIDENDS - BUYBACKS
        revolver = prior.revolver
        if cash_before_revolver < MINIMUM_CASH:
            draw = MINIMUM_CASH - cash_before_revolver
            revolver += draw
            if revolver > REVOLVER_LIMIT:
                raise AssertionError(f"FY{year}E revolver exceeds its ${REVOLVER_LIMIT:,.0f} limit")
            cash = MINIMUM_CASH
        else:
            repayment = min(revolver, cash_before_revolver - MINIMUM_CASH)
            revolver -= repayment
            cash = cash_before_revolver - repayment

        if break_fy2026 and year == 2026:
            cash = prior.cash  # Deliberate test: the check must refuse this plug.

        opening = BalanceSheet(revenue, cash, ppe, other_assets, debt,
                               other_liabilities, revolver, equity)
        assert_balanced(year, opening)

        for label, value in (("Net revenue", revenue), ("Operating costs excl. D&A", -operating_costs),
                             ("Depreciation & amortization", -depreciation), ("Operating income", operating_income),
                             ("Interest expense", -interest), ("Pretax income", pretax_income),
                             ("Tax", -tax), ("Net income", net_income)):
            income[label].append(value)
        for label, value in (("Cash & equivalents", cash), ("PP&E and technology", ppe),
                             ("Other assets", other_assets), ("Debt", debt),
                             ("Other liabilities", other_liabilities), ("Revolver", revolver), ("Equity", equity)):
            balance[label].append(value)
        for label, value in (("Net income", net_income), ("Depreciation & amortization", depreciation),
                             ("Capital spending", -capex), ("Change in other operating assets", -change_other_assets),
                             ("Change in other liabilities", change_other_liabilities), ("FCFE before distributions", fcfe),
                             ("Dividends", -DIVIDENDS), ("Share repurchases", -BUYBACKS),
                             ("Change in cash", cash - prior.cash)):
            cash_flow[label].append(value)
        assets = cash + ppe + other_assets
        liabilities = debt + other_liabilities + revolver
        checks["Assets - liabilities - equity"].append(assets - liabilities - equity)
        checks["Cash above minimum"].append(cash - MINIMUM_CASH)

    return income, balance, cash_flow, checks


def value_equity(fcfe):
    if TERMINAL_GROWTH >= COST_OF_EQUITY:
        raise ValueError("Terminal growth must be below the cost of equity.")
    pv_explicit = sum(flow / (1 + COST_OF_EQUITY) ** period for period, flow in enumerate(fcfe, 1))
    terminal_value = fcfe[-1] * (1 + TERMINAL_GROWTH) / (COST_OF_EQUITY - TERMINAL_GROWTH)
    pv_terminal = terminal_value / (1 + COST_OF_EQUITY) ** 5
    equity_value = pv_explicit + pv_terminal
    return equity_value, pv_terminal / equity_value, equity_value / SHARES_OUTSTANDING


if __name__ == "__main__":
    break_test = "--break-fy2026" in sys.argv
    income_statement, balance_sheet, cash_flow_statement, check_block = build_proforma(break_test)
    print_table("INCOME STATEMENT (USD millions)", income_statement)
    print_table("BALANCE SHEET (USD millions)", balance_sheet)
    print_table("CASH FLOW / FCFE (USD millions)", cash_flow_statement)
    print_table("CHECKS", check_block)
    equity_value, terminal_share, value_per_share = value_equity(cash_flow_statement["FCFE before distributions"])
    print(f"\nEquity value: ${equity_value:,.1f} million")
    print(f"Share of value after 2030: {terminal_share:.1%}")
    print(f"Value per share: ${value_per_share:.2f}")
