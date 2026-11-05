"""Run the SEC facts pipeline and save its Buffett-style memo."""

from pathlib import Path
import sys
from analysis import burry_checks, build_yearly_rows, cathie_wood_checks, check_status, company_facts_for_ticker, render_console_report, write_investor_memos


def main() -> None:
    ticker = sys.argv[1] if len(sys.argv) > 1 else "COST"
    facts = company_facts_for_ticker(ticker)
    rows = build_yearly_rows(facts)
    buffett = check_status(rows)
    cathie = cathie_wood_checks(rows)
    burry = burry_checks(rows)
    print(render_console_report(ticker, rows, buffett, cathie, burry))
    memo_paths = write_investor_memos(ticker, rows, buffett, cathie, burry, Path("output"))
    print("\nSaved memos:")
    for investor, memo_path in memo_paths.items():
        print(f"  {investor}: {memo_path}")


if __name__ == "__main__":
    main()


