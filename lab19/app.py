from pathlib import Path
import pandas as pd
import streamlit as st
from analysis import (
    METRIC_LABELS,
    burry_checks,
    build_yearly_rows,
    cathie_revenue_growth,
    cathie_wood_checks,
    check_status,
    company_facts_for_ticker,
    display_number,
    display_precise_percent,
    latest_liabilities_to_equity,
    latest_r_and_d_ratio,
    recommendation_for,
    unprinted_number_warning,
    write_investor_memos,
)

st.set_page_config(page_title="Buffett 10-K Screen", layout="wide")
st.title("Buffett-Style 10-K Screen")
st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")
ticker = st.text_input("Ticker", value="COST").strip().upper()
if st.button("Analyze SEC 10-K facts", type="primary"):
    try:
        with st.spinner("Downloading SEC company facts..."):
            rows = build_yearly_rows(company_facts_for_ticker(ticker))
            buffett = check_status(rows)
            cathie = cathie_wood_checks(rows)
            burry = burry_checks(rows)
            memo_paths = write_investor_memos(ticker, rows, buffett, cathie, burry, Path("output"))
            memos = {investor: path.read_text(encoding="utf-8") for investor, path in memo_paths.items()}
        if len(rows) != 5:
            st.warning("SEC did not provide five annual revenue periods that meet this screen's rules.")
        chart_rows = pd.DataFrame({"Fiscal year end": [r["fiscal_year_end"] for r in rows], "Owner earnings": [None if r["owner_earnings"] is None else r["owner_earnings"] / 1_000_000 for r in rows], "Net income": [None if r["net_income"] is None else r["net_income"] / 1_000_000 for r in rows]}).set_index("Fiscal year end")
        st.subheader("Owner earnings and net income (USD millions)")
        st.line_chart(chart_rows)
        table_rows = []
        for row in rows:
            table = {"Fiscal year end": row["fiscal_year_end"]}
            for metric in ("revenue", "net_income", "operating_cash_flow", "capital_spending", "research_and_development", "equity", "liabilities"):
                table[f"{METRIC_LABELS[metric]} (USD millions)"] = display_number(row[metric])
                table[f"{METRIC_LABELS[metric]} XBRL tag"] = row[f"{metric}_tag"]
            table["ROE"] = display_number(row["roe"], percent=True)
            table["Owner earnings (USD millions)"] = display_number(row["owner_earnings"])
            table_rows.append(table)
        st.subheader("Financial table")
        st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)
        panel_rows = []
        evidence = {
            "Buffett": "Calculated from the printed annual facts.",
            "Cathie Wood": f"Revenue growth: {display_precise_percent(cathie_revenue_growth(rows))}; R&D/revenue: {display_precise_percent(latest_r_and_d_ratio(rows))}.",
            "Michael Burry": f"Latest liabilities/equity: {'not known' if latest_liabilities_to_equity(rows) is None else f'{latest_liabilities_to_equity(rows):.2f}' }.",
        }
        for investor, checks in (("Buffett", buffett), ("Cathie Wood", cathie), ("Michael Burry", burry)):
            panel_rows.extend({"Investor": investor, "Check": check, "Status": status, "Evidence": evidence[investor]} for check, status in checks.items())
        st.subheader("Investor check panel")
        st.dataframe(pd.DataFrame(panel_rows), use_container_width=True, hide_index=True)
        st.subheader("Investor verdicts")
        verdict_columns = st.columns(3)
        for column, (investor, checks) in zip(verdict_columns, (("Buffett", buffett), ("Cathie Wood", cathie), ("Michael Burry", burry))):
            column.metric(investor, recommendation_for(checks))
        st.subheader("Saved memos")
        memo_columns = st.columns(3)
        for column, investor in zip(memo_columns, ("Buffett", "Cathie Wood", "Michael Burry")):
            with column:
                st.caption(str(memo_paths[investor]))
                st.markdown(memos[investor])
                if investor == "Cathie Wood":
                    st.caption("Growth threshold kept: 15%, because this is the stated Lab 19 screen threshold.")
        warnings = unprinted_number_warning("\n".join(memos.values()), rows)
        if warnings:
            st.error("Unprinted-number warning: memo contains financial number(s) absent from the printed analysis: " + ", ".join(warnings))
        else:
            st.success("Unprinted-number warning: none.")
    except Exception as exc:
        st.error(f"Could not complete the SEC analysis: {exc}")


