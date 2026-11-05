"""SEC 10-K fact selection and Buffett-style business checks."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
import json
import re
from typing import Any, Iterable

import requests

SEC_USER_AGENT = "AJ Chapman <chapm119@purdue.edu>"
TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
CATHIE_GROWTH_THRESHOLD = 0.15
CATHIE_R_AND_D_THRESHOLD = 0.05

FLOW_TAGS = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"],
    "net_income": ["NetIncomeLoss"],
    "operating_cash_flow": ["NetCashProvidedByUsedInOperatingActivities"],
    "capital_spending": ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"],
    "research_and_development": ["ResearchAndDevelopmentExpense"],
}
INSTANT_TAGS = {"equity": ["StockholdersEquity"], "liabilities": ["Liabilities"]}
METRIC_LABELS = {
    "revenue": "Revenue",
    "net_income": "Net income",
    "operating_cash_flow": "Operating cash flow",
    "capital_spending": "Capital spending",
    "research_and_development": "Research and development",
    "equity": "Equity",
    "liabilities": "Liabilities",
}


@dataclass(frozen=True)
class Fact:
    value: float
    tag: str
    end: str
    filed: str
    accession: str


def sec_get_json(url: str) -> dict[str, Any]:
    """Fetch one SEC JSON resource with the assignment's required User-Agent."""
    response = requests.get(url, headers={"User-Agent": SEC_USER_AGENT}, timeout=30)
    response.raise_for_status()
    return response.json()


def cik_for_ticker(ticker: str) -> int:
    ticker_upper = ticker.upper().strip()
    ticker_data = sec_get_json(TICKERS_URL)
    for company in ticker_data.values():
        if company["ticker"].upper() == ticker_upper:
            return int(company["cik_str"])
    raise ValueError(f"Ticker not found in SEC ticker data: {ticker_upper}")


def company_facts_for_ticker(ticker: str) -> dict[str, Any]:
    cik = cik_for_ticker(ticker)
    return sec_get_json(FACTS_URL.format(cik=cik))


def _is_one_year_duration(unit: dict[str, Any]) -> bool:
    if not unit.get("start") or not unit.get("end"):
        return False
    return 350 <= (date.fromisoformat(unit["end"]) - date.fromisoformat(unit["start"])).days <= 380


def _latest_by_end(units: Iterable[dict[str, Any]], *, flow: bool) -> dict[str, Fact]:
    """Keep the newest-filed annual 10-K fact for each fiscal-period end date."""
    chosen: dict[str, Fact] = {}
    for unit in units:
        if unit.get("form") != "10-K" or not unit.get("fy") or unit.get("fp") != "FY":
            continue
        if flow and not _is_one_year_duration(unit):
            continue
        if not flow and unit.get("start"):
            continue
        if not unit.get("end") or unit.get("val") is None:
            continue
        fact = Fact(float(unit["val"]), "", unit["end"], unit.get("filed", ""), unit.get("accn", ""))
        current = chosen.get(fact.end)
        if current is None or (fact.filed, fact.accession) > (current.filed, current.accession):
            chosen[fact.end] = fact
    return chosen


def select_metric_facts(company_facts: dict[str, Any], tags: list[str], *, flow: bool) -> dict[str, Fact]:
    """Select a metric, trying its permitted XBRL tags in priority order."""
    us_gaap = company_facts.get("facts", {}).get("us-gaap", {})
    for tag in tags:
        units = us_gaap.get(tag, {}).get("units", {}).get("USD", [])
        facts = _latest_by_end(units, flow=flow)
        if facts:
            return {end: Fact(f.value, tag, f.end, f.filed, f.accession) for end, f in facts.items()}
    return {}


def build_yearly_rows(company_facts: dict[str, Any]) -> list[dict[str, Any]]:
    """Turn SEC company facts into five annual rows, one row per fiscal-year-end date.

    Revenue establishes the available annual fiscal years. Each metric is selected
    independently by allowed tag, then matched to the same end date. Missing values
    stay None and are rendered as `not found`; no values are inferred.
    """
    selected = {metric: select_metric_facts(company_facts, tags, flow=True) for metric, tags in FLOW_TAGS.items()}
    selected.update({metric: select_metric_facts(company_facts, tags, flow=False) for metric, tags in INSTANT_TAGS.items()})
    fiscal_ends = sorted(selected["revenue"])[-5:]
    rows: list[dict[str, Any]] = []
    for fiscal_end in fiscal_ends:
        row: dict[str, Any] = {"fiscal_year_end": fiscal_end}
        for metric in (*FLOW_TAGS, *INSTANT_TAGS):
            fact = selected[metric].get(fiscal_end)
            row[metric] = fact.value if fact else None
            row[f"{metric}_tag"] = fact.tag if fact else "not found"
        equity, net_income = row["equity"], row["net_income"]
        capex, ocf = row["capital_spending"], row["operating_cash_flow"]
        row["roe"] = net_income / equity if equity is not None and equity > 0 and net_income is not None else None
        row["owner_earnings"] = ocf - capex if ocf is not None and capex is not None else None
        rows.append(row)
    return rows


def check_status(rows: list[dict[str, Any]]) -> dict[str, str]:
    """Return pass/fail/not known statuses for the three assignment checks."""
    roes = [row["roe"] for row in rows]
    owner_earnings = [row["owner_earnings"] for row in rows]
    roe_status = "not known" if len(rows) != 5 or any(value is None for value in roes) else ("pass" if all(value >= 0.15 for value in roes) else "fail")
    oe_status = "not known" if len(rows) != 5 or any(value is None for value in owner_earnings) else ("pass" if all(value > 0 for value in owner_earnings) else "fail")
    growth_status = "not known" if len(rows) != 5 or any(value is None for value in owner_earnings) else ("pass" if owner_earnings[-1] > owner_earnings[0] else "fail")
    return {"ROE is 15% or more every year": roe_status, "Owner earnings are positive every year": oe_status, "Owner earnings grew from the first year to the last year": growth_status}


def cathie_revenue_growth(rows: list[dict[str, Any]]) -> float | None:
    """Calculate Cathie's four-interval annualized revenue growth from five rows."""
    revenues = [row.get("revenue") for row in rows]
    if len(rows) != 5 or any(value is None for value in revenues) or revenues[0] <= 0:
        return None
    return (revenues[-1] / revenues[0]) ** (1 / 4) - 1


def latest_r_and_d_ratio(rows: list[dict[str, Any]]) -> float | None:
    latest = rows[-1] if rows else {}
    r_and_d, revenue = latest.get("research_and_development"), latest.get("revenue")
    return r_and_d / revenue if r_and_d is not None and revenue is not None and revenue > 0 else None


def latest_liabilities_to_equity(rows: list[dict[str, Any]]) -> float | None:
    latest = rows[-1] if rows else {}
    liabilities, equity = latest.get("liabilities"), latest.get("equity")
    return liabilities / equity if liabilities is not None and equity is not None and equity > 0 else None


def cathie_wood_checks(rows: list[dict[str, Any]]) -> dict[str, str]:
    """Return Cathie Wood's growth and R&D checks without filling absent facts."""
    growth, r_and_d_ratio = cathie_revenue_growth(rows), latest_r_and_d_ratio(rows)
    return {
        "Revenue annual growth from first to last year is at least 15%": "not known" if growth is None else ("pass" if growth >= CATHIE_GROWTH_THRESHOLD else "fail"),
        "Latest R&D divided by latest revenue is at least 5%": "not known" if r_and_d_ratio is None else ("pass" if r_and_d_ratio >= CATHIE_R_AND_D_THRESHOLD else "fail"),
    }


def burry_operating_cash_flow_check(rows: list[dict[str, Any]]) -> str:
    """Check that annual operating cash flow meets or exceeds annual net income."""
    cash_flows = [row.get("operating_cash_flow") for row in rows]
    net_incomes = [row.get("net_income") for row in rows]
    if len(rows) != 5 or any(value is None for value in cash_flows + net_incomes):
        return "not known"
    return "pass" if all(ocf >= income for ocf, income in zip(cash_flows, net_incomes)) else "fail"


def burry_liabilities_to_equity_check(rows: list[dict[str, Any]]) -> str:
    """Check latest liabilities against twice latest positive equity."""
    leverage = latest_liabilities_to_equity(rows)
    return "not known" if leverage is None else ("pass" if leverage <= 2 else "fail")


def burry_checks(rows: list[dict[str, Any]]) -> dict[str, str]:
    """Return Burry's cash-flow and balance-sheet checks from printed SEC facts."""
    return {
        "Operating cash flow is at least net income every year": burry_operating_cash_flow_check(rows),
        "Latest liabilities are no more than twice latest equity": burry_liabilities_to_equity_check(rows),
    }


def recommendation_for(checks: dict[str, str]) -> str:
    statuses = list(checks.values())
    if all(status == "pass" for status in statuses):
        return "own the business"
    if any(status == "not known" for status in statuses):
        return "watch it"
    return "pass"


def display_number(value: float | None, *, percent: bool = False) -> str:
    if value is None:
        return "not found" if not percent else "not known"
    if percent:
        return f"{value * 100:.1f}%"
    return f"{value / 1_000_000:,.0f}"


def display_precise_percent(value: float | None) -> str:
    """Render a calculated screen ratio to two decimals, or preserve not-known status."""
    return "not known" if value is None else f"{value * 100:.2f}%"


def printed_financial_numbers(rows: list[dict[str, Any]]) -> set[str]:
    """Financial-number strings that the console/table renderer prints."""
    allowed: set[str] = set()
    for row in rows:
        for metric in (*FLOW_TAGS, *INSTANT_TAGS, "owner_earnings"):
            value = row.get(metric)
            if value is not None:
                allowed.add(display_number(value))
        if row.get("roe") is not None:
            allowed.add(display_number(row["roe"], percent=True).rstrip("%"))
    for derived in (cathie_revenue_growth(rows), latest_r_and_d_ratio(rows)):
        if derived is not None:
            allowed.add(display_number(derived, percent=True).rstrip("%"))
            allowed.add(display_precise_percent(derived).rstrip("%"))
    leverage = latest_liabilities_to_equity(rows)
    if leverage is not None:
        allowed.add(f"{leverage:.2f}")
    allowed.update({"5", "15"})  # The printed Cathie screen thresholds are 5% and 15%.
    return allowed


def unprinted_number_warning(memo: str, rows: list[dict[str, Any]]) -> list[str]:
    """Find financial-looking numbers in a memo that were not printed by the analysis."""
    allowed = printed_financial_numbers(rows)
    found: list[str] = []
    for match in re.finditer(r"(?<![\w-])\d{1,3}(?:,\d{3})*(?:\.\d+)?%?", memo):
        token = match.group()
        bare = token.rstrip("%")
        surrounding = memo[max(0, match.start() - 4):match.end() + 4]
        if re.fullmatch(r"20\d{2}", bare) or re.search(r"\b10-K\b|\bLab 19\b", surrounding):
            continue
        if bare not in allowed:
            found.append(token)
    return found


def render_console_report(ticker: str, rows: list[dict[str, Any]], checks: dict[str, str], cathie_checks: dict[str, str] | None = None, burry_check_results: dict[str, str] | None = None) -> str:
    lines = [f"{ticker.upper()} SEC 10-K facts (USD millions)"]
    for row in rows:
        lines.append(f"\nFY end {row['fiscal_year_end']}")
        for metric in (*FLOW_TAGS, *INSTANT_TAGS):
            lines.append(f"  {METRIC_LABELS[metric]} [{row[f'{metric}_tag']}]: {display_number(row[metric])}")
        lines.append(f"  ROE: {display_number(row['roe'], percent=True)}")
        lines.append(f"  Owner earnings: {display_number(row['owner_earnings'])}")
    lines.append("\nBuffett-style checks")
    lines.extend(f"  {name}: {status}" for name, status in checks.items())
    if cathie_checks is not None:
        lines.extend(["\nCathie Wood checks", f"  Revenue annual growth: {display_precise_percent(cathie_revenue_growth(rows))}", f"  Latest R&D / latest revenue: {display_precise_percent(latest_r_and_d_ratio(rows))}", "  Growth threshold: 15%", "  R&D threshold: 5%"])
        lines.extend(f"  {name}: {status}" for name, status in cathie_checks.items())
    if burry_check_results is not None:
        leverage = latest_liabilities_to_equity(rows)
        lines.extend(["\nMichael Burry checks", f"  Latest liabilities / latest equity: {'not known' if leverage is None else f'{leverage:.2f}'}"])
        lines.extend(f"  {name}: {status}" for name, status in burry_check_results.items())
    return "\n".join(lines)


def write_memo(ticker: str, rows: list[dict[str, Any]], checks: dict[str, str], output_dir: Path) -> Path:
    recommendation = recommendation_for(checks)
    lines = [f"# Buffett-Style Memo: {ticker.upper()}", "", f"Recommendation: {recommendation}", "", "This is a business-quality screen using SEC 10-K facts; it does not assess stock price.", "", "## Checks", ""]
    lines.extend(f"- {name}: {status}" for name, status in checks.items())
    lines.extend(["", "The recommendation follows the printed check results and uses no estimates."])
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"buffett_memo_{ticker.upper()}.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_investor_memos(ticker: str, rows: list[dict[str, Any]], buffett: dict[str, str], cathie: dict[str, str], burry: dict[str, str], output_dir: Path) -> dict[str, Path]:
    """Save price-free investor memos using only statuses and printed screen numbers."""
    output_dir.mkdir(parents=True, exist_ok=True)
    latest = rows[-1] if rows else {}
    growth = cathie_revenue_growth(rows)
    memo_specs = {
        "Buffett": (buffett, [f"Latest owner earnings: {display_number(latest.get('owner_earnings'))} million.", f"Latest ROE: {display_number(latest.get('roe'), percent=True)}."]),
        "Cathie Wood": (cathie, [f"Revenue annual growth: {display_precise_percent(growth)}.", "Growth threshold kept: 15%, because this is the stated Lab 19 screen threshold."]),
        "Michael Burry": (burry, [f"Latest operating cash flow: {display_number(latest.get('operating_cash_flow'))} million.", f"Latest net income: {display_number(latest.get('net_income'))} million."]),
    }
    paths: dict[str, Path] = {}
    for investor, (checks, notes) in memo_specs.items():
        lines = [f"# {investor} Memo: {ticker.upper()}", "", f"Verdict: {recommendation_for(checks)}", "", "This is a business-quality screen using SEC 10-K facts; it does not assess stock price.", *notes, "", "## Checks", ""]
        lines.extend(f"- {name}: {status}" for name, status in checks.items())
        path = output_dir / f"{investor.lower().replace(' ', '_')}_memo_{ticker.upper()}.md"
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        paths[investor] = path
    return paths


def rows_as_json(rows: list[dict[str, Any]]) -> str:
    return json.dumps(rows, indent=2)


