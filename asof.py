import csv
from datetime import date
from io import StringIO


# =========================
# EDITABLE INPUTS
# =========================

DECISION_DATE = "2026-03-31"

TABLE = """row,ticker,month,published_on,index
1,AAA,2026-01,2026-02-10,101.0
2,AAA,2026-02,2026-03-10,104.0
3,AAA,2026-03,2026-04-10,109.0
4,AAA,2026-02,2026-03-25,103.0
5,BBB,2026-01,2026-02-10,98.0
6,BBB,2026-02,2026-03-10,97.0
7,BBB,2026-02,2026-03-10,97.0
8,BBB,2026-03,2026-04-10,92.0
9,CCC,2026-01,2026-02-10,110.0
10,CCC,2026-02,2026-04-05,112.0
11,,2026-02,2026-03-10,99.0
12,CCC,2026-02,2026-03-10,111.0
"""


def parse_rows(table_text):
    """Convert the pasted training table into usable Python rows."""
    rows = []
    for row in csv.DictReader(StringIO(table_text.strip())):
        rows.append(
            {
                "row": int(row["row"]),
                "ticker": row["ticker"],
                "month": row["month"],
                "published_on": date.fromisoformat(row["published_on"]),
                "index": float(row["index"]),
            }
        )
    return rows


def row_numbers(rows):
    """Return original row numbers for printing."""
    return [row["row"] for row in rows]


def print_funnel_step(label, removed_rows):
    """Print one line of the row funnel."""
    print(f"{label}: removed {len(removed_rows)} row(s): {row_numbers(removed_rows)}")


def remove_blank_tickers(rows):
    """Rule 1: Quarantine rows that have no ticker."""
    removed = [row for row in rows if not row["ticker"]]
    kept = [row for row in rows if row["ticker"]]
    return kept, removed


def remove_exact_duplicates(rows):
    """Rule 2: Remove a row if an identical row already appeared."""
    seen, kept, removed = set(), [], []
    for row in rows:
        signature = (row["ticker"], row["month"], row["published_on"], row["index"])
        if signature in seen:
            removed.append(row)
        else:
            seen.add(signature)
            kept.append(row)
    return kept, removed


def remove_after_decision_date(rows, decision_date):
    """Rule 3: Keep only rows published on or before the decision date."""
    removed = [row for row in rows if row["published_on"] > decision_date]
    kept = [row for row in rows if row["published_on"] <= decision_date]
    return kept, removed


def keep_latest_revision(rows):
    """Rule 4: For each ticker-month, keep the latest publication."""
    latest_by_ticker_month = {}
    for row in rows:
        key = (row["ticker"], row["month"])
        if key not in latest_by_ticker_month or row["published_on"] > latest_by_ticker_month[key]["published_on"]:
            latest_by_ticker_month[key] = row
    kept = list(latest_by_ticker_month.values())
    kept_row_ids = {row["row"] for row in kept}
    removed = [row for row in rows if row["row"] not in kept_row_ids]
    return sorted(kept, key=lambda row: row["row"]), removed


def print_panel(panel, title):
    """Print the rows that remain after the filter."""
    print(f"\n{title}")
    print("Row  Ticker  Month     Published on  Index")
    print("-" * 43)
    for row in sorted(panel, key=lambda row: row["row"]):
        print(f'{row["row"]:>3}  {row["ticker"]:<6}  {row["month"]}  {row["published_on"].isoformat()}    {row["index"]:.1f}')


def calculate_signals(panel):
    """Calculate the change from each ticker's prior month to its latest month."""
    by_ticker = {}
    for row in panel:
        by_ticker.setdefault(row["ticker"], []).append(row)
    signals = {}
    for ticker, ticker_rows in by_ticker.items():
        ticker_rows.sort(key=lambda row: row["month"])
        if len(ticker_rows) < 2:
            continue
        previous, latest = ticker_rows[-2:]
        signals[ticker] = {
            "month": latest["month"],
            "percent_change": ((latest["index"] - previous["index"]) / previous["index"]) * 100,
        }
    return signals


def month_name(month_text):
    """Change 2026-02 into February."""
    return date(2026, int(month_text.split("-")[1]), 1).strftime("%B")


def print_signals(title, signals):
    """Print the signals to two decimal places."""
    print(f"\n{title}")
    for ticker in sorted(signals):
        signal = signals[ticker]
        sign = "+" if signal["percent_change"] >= 0 else ""
        print(f"{ticker}: {sign}{signal['percent_change']:.2f}% ({month_name(signal['month'])})")


def main():
    decision_date = date.fromisoformat(DECISION_DATE)
    original_rows = parse_rows(TABLE)
    after_no_ticker, no_ticker_rows = remove_blank_tickers(original_rows)
    after_duplicates, duplicate_rows = remove_exact_duplicates(after_no_ticker)
    after_date_filter, after_decision_rows = remove_after_decision_date(after_duplicates, decision_date)
    asof_panel, replaced_revision_rows = keep_latest_revision(after_date_filter)

    print(f"DECISION DATE: {decision_date.isoformat()}")
    print("\nROW FUNNEL")
    print_funnel_step("Quarantined: no ticker", no_ticker_rows)
    print_funnel_step("Exact duplicate", duplicate_rows)
    print_funnel_step(f"Published after {decision_date.strftime('%d %B')}", after_decision_rows)
    print_funnel_step("Older vintage replaced by a revision", replaced_revision_rows)
    print(f"As-of panel rows: {row_numbers(asof_panel)}")

    print_panel(asof_panel, "AS-OF PANEL")
    print_signals("AS-OF SIGNALS", calculate_signals(asof_panel))

    # Comparison only: ignores publication date but preserves basic hygiene rules.
    naive_panel, _ = keep_latest_revision(after_duplicates)
    print_signals("NAIVE SIGNALS (ignores publication date)", calculate_signals(naive_panel))


if __name__ == "__main__":
    main()
