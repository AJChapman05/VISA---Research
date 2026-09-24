"""Five-year three-statement pro-forma for Asbury Automotive Group (USD millions)."""

from dataclasses import dataclass


@dataclass
class BalanceSheet:
    revenue: float = 17_999.0
    inventory: float = 2_135.8
    ppe: float = 3_070.4
    other_assets: float = 6_371.6
    cash: float = 40.4
    floor_plan: float = 2_027.0
    debt: float = 3_572.0
    other_liabilities: float = 2_127.5
    equity: float = 3_891.7
    revolver: float = 0.0


YEARS = range(2026, 2031)
SGA_RATIOS = dict(zip(YEARS, (0.665, 0.655, 0.645, 0.645, 0.645)))

GROWTH = 0.018
GROSS_MARGIN = 0.1705
DEPRECIATION_RATE = 82.4 / 3_070.4
IMPAIRMENT = 120.0
CAPEX = 250.0
TAX_RATE = 0.255
INVENTORY_DAYS = 2_135.8 / (17_999.0 - 3_071.7) * 365
FLOOR_PLAN_RATIO = 2_027.0 / 2_135.8
OTHER_WORKING_CAPITAL_RATE = 0.008
MINIMUM_CASH = 25.0
REVOLVER_LIMIT = 850.0
REVOLVER_RATE = 0.06
DEBT_REPAYMENT = 150.0
BUYBACK = 150.0
FLOOR_PLAN_RATE = 0.0467
TERM_DEBT_RATE = 0.0544
COST_OF_EQUITY = 0.10
TERMINAL_GROWTH = 0.025
SHARES_OUTSTANDING = 17.951349


def assert_balanced(year, balance_sheet):
    """Raise a useful error if a projected year is not a balanced, liquid balance sheet."""
    assets = balance_sheet.inventory + balance_sheet.ppe + balance_sheet.other_assets + balance_sheet.cash
    liabilities = balance_sheet.floor_plan + balance_sheet.debt + balance_sheet.other_liabilities + balance_sheet.revolver
    gap = assets - liabilities - balance_sheet.equity
    if abs(gap) > 0.05:
        raise AssertionError(f"FY{year}E is not balanced: gap {gap:.1f}")
    if balance_sheet.cash < MINIMUM_CASH - 0.05:
        raise AssertionError(f"FY{year}E cash is below the minimum: {balance_sheet.cash:.1f}")


def print_table(title, rows):
    print(f"\n{title}")
    print(f"{'':28}" + "".join(f"{year:>11}E" for year in YEARS))
    for label, values in rows.items():
        print(f"{label:28}" + "".join(f"{value:>11.1f}" for value in values))


def build_proforma():
    opening = BalanceSheet()
    income = {line: [] for line in ("Revenue", "Gross profit", "SG&A", "Depreciation", "Impairment", "Operating income", "Interest", "Pretax income", "Tax", "Net income")}
    balance = {line: [] for line in ("Inventory", "PP&E", "Other assets", "Cash", "Floor plan", "Term debt", "Revolver", "Other liabilities", "Equity")}
    cash_flow = {line: [] for line in ("Net income", "Depreciation", "Impairment", "Capital spending", "Change in inventory", "Change in other working capital", "Change in floor plan", "Debt repayment", "Share buyback", "FCFE")}
    checks = {line: [] for line in ("Assets − liabilities − equity", "Cash at/above minimum")}

    for year in YEARS:
        prior = opening
        revenue = prior.revenue * (1 + GROWTH)
        gross_profit = revenue * GROSS_MARGIN
        sga = gross_profit * SGA_RATIOS[year]
        depreciation = prior.ppe * DEPRECIATION_RATE
        operating_income = gross_profit - sga - depreciation - IMPAIRMENT
        interest = prior.floor_plan * FLOOR_PLAN_RATE + prior.debt * TERM_DEBT_RATE + prior.revolver * REVOLVER_RATE
        pretax_income = operating_income - interest
        tax = max(0.0, pretax_income) * TAX_RATE
        net_income = pretax_income - tax

        inventory = (revenue - gross_profit) * INVENTORY_DAYS / 365
        floor_plan = inventory * FLOOR_PLAN_RATIO
        ppe = prior.ppe + CAPEX - depreciation
        change_other_working_capital = OTHER_WORKING_CAPITAL_RATE * (revenue - prior.revenue)
        other_assets = prior.other_assets + change_other_working_capital - IMPAIRMENT
        debt = prior.debt - DEBT_REPAYMENT
        equity = prior.equity + net_income - BUYBACK
        fcfe = (net_income + depreciation + IMPAIRMENT - CAPEX - (inventory - prior.inventory)
                - change_other_working_capital + (floor_plan - prior.floor_plan) - DEBT_REPAYMENT)
        cash_before_revolver = prior.cash + fcfe - BUYBACK
        revolver = prior.revolver
        if cash_before_revolver < MINIMUM_CASH:
            draw = MINIMUM_CASH - cash_before_revolver
            revolver += draw
            if revolver > REVOLVER_LIMIT:
                raise AssertionError(f"FY{year}E revolver exceeds its {REVOLVER_LIMIT:.0f} limit")
            cash = MINIMUM_CASH
        else:
            repayment = min(revolver, cash_before_revolver - MINIMUM_CASH)
            revolver -= repayment
            cash = cash_before_revolver - repayment

        opening = BalanceSheet(revenue, inventory, ppe, other_assets, cash, floor_plan, debt,
                              prior.other_liabilities, equity, revolver)
        assert_balanced(year, opening)

        for label, value in (("Revenue", revenue), ("Gross profit", gross_profit), ("SG&A", sga), ("Depreciation", depreciation), ("Impairment", IMPAIRMENT), ("Operating income", operating_income), ("Interest", interest), ("Pretax income", pretax_income), ("Tax", tax), ("Net income", net_income)):
            income[label].append(value)
        for label, value in (("Inventory", inventory), ("PP&E", ppe), ("Other assets", other_assets), ("Cash", cash), ("Floor plan", floor_plan), ("Term debt", debt), ("Revolver", revolver), ("Other liabilities", prior.other_liabilities), ("Equity", equity)):
            balance[label].append(value)
        for label, value in (("Net income", net_income), ("Depreciation", depreciation), ("Impairment", IMPAIRMENT), ("Capital spending", -CAPEX), ("Change in inventory", -(inventory - prior.inventory)), ("Change in other working capital", -change_other_working_capital), ("Change in floor plan", floor_plan - prior.floor_plan), ("Debt repayment", -DEBT_REPAYMENT), ("Share buyback", -BUYBACK), ("FCFE", fcfe)):
            cash_flow[label].append(value)
        assets = inventory + ppe + other_assets + cash
        liabilities = floor_plan + debt + prior.other_liabilities + revolver
        checks["Assets − liabilities − equity"].append(assets - liabilities - equity)
        checks["Cash at/above minimum"].append(cash - MINIMUM_CASH)

    return income, balance, cash_flow, checks


def value_equity(fcfe):
    if TERMINAL_GROWTH >= COST_OF_EQUITY:
        raise ValueError("Terminal growth must be below the cost of equity.")
    present_value_fcfe = sum(cash_flow / (1 + COST_OF_EQUITY) ** period for period, cash_flow in enumerate(fcfe, 1))
    terminal_value = (fcfe[-1] + DEBT_REPAYMENT) * (1 + TERMINAL_GROWTH) / (COST_OF_EQUITY - TERMINAL_GROWTH)
    present_value_terminal = terminal_value / (1 + COST_OF_EQUITY) ** 5
    equity_value = present_value_fcfe + present_value_terminal
    return equity_value, present_value_terminal / equity_value, equity_value / SHARES_OUTSTANDING


if __name__ == "__main__":
    income_statement, balance_sheet, cash_flow_statement, check_block = build_proforma()
    print_table("INCOME STATEMENT (USD millions)", income_statement)
    print_table("BALANCE SHEET (USD millions)", balance_sheet)
    print_table("CASH FLOW / FCFE (USD millions)", cash_flow_statement)
    print_table("CHECKS", check_block)
    equity_value, terminal_share, value_per_share = value_equity(cash_flow_statement["FCFE"])
    print(f"\nEquity value: ${equity_value:,.1f} million")
    print(f"Share of value after 2030: {terminal_share:.1%}")
    print(f"Value per share: ${value_per_share:.2f}")
