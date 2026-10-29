"""A point-in-time interest-rates viewer using public FRED and ALFRED CSV downloads.

Run with: streamlit run lab-17-point-in-time/asof_app.py
"""

from datetime import date
from io import StringIO

import pandas as pd
import requests
import streamlit as st


FRED_GRAPH_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv"
ALFRED_GRAPH_URL = "https://alfred.stlouisfed.org/graph/alfredgraph.csv"
SERIES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year mortgage rate",
}


def clean_fred_csv(response_text: str, series_id: str) -> pd.DataFrame:
    """Return a date-indexed numeric series; FRED uses '.' for missing observations."""
    frame = pd.read_csv(StringIO(response_text))

    if frame.empty or "observation_date" not in frame.columns:
        raise ValueError("FRED did not return a usable observation table for this series ID.")

    value_columns = [column for column in frame.columns if column != "observation_date"]

    if len(value_columns) != 1:
        raise ValueError("FRED did not return exactly one value column for this series ID.")

    frame = frame.rename(columns={value_columns[0]: series_id})
    frame["observation_date"] = pd.to_datetime(frame["observation_date"], errors="coerce")
    frame[series_id] = pd.to_numeric(frame[series_id].replace(".", pd.NA), errors="coerce")
    return frame[["observation_date", series_id]].dropna(subset=["observation_date"]).sort_values("observation_date")


@st.cache_data(ttl=60 * 60, show_spinner=False)
def get_current_fred(series_id: str) -> pd.DataFrame:
    """Download the currently published FRED history. No API key is required."""
    response = requests.get(FRED_GRAPH_URL, params={"id": series_id}, timeout=20)
    response.raise_for_status()
    return clean_fred_csv(response.text, series_id)


@st.cache_data(ttl=60 * 60, show_spinner=False)
def get_alfred_vintage(series_id: str, vintage_date: str) -> pd.DataFrame:
    """Download the version of a series that ALFRED exposed on ``vintage_date``.

    ALFRED's vintage_date parameter enforces the point-in-time boundary: the
    returned CSV contains only observations available in that historical vintage.
    """
    response = requests.get(
        ALFRED_GRAPH_URL,
        params={"id": series_id, "vintage_date": vintage_date},
        timeout=20,
    )
    response.raise_for_status()
    return clean_fred_csv(response.text, series_id)


def last_known_observation(frame: pd.DataFrame, series_id: str):
    """Find the last nonmissing observation in a downloaded vintage."""
    known = frame.dropna(subset=[series_id])
    return None if known.empty else known.iloc[-1]


def display_value(row, series_id: str) -> str:
    if row is None:
        return "No nonmissing observation"
    return f"{row['observation_date'].date():%Y-%m-%d}: {row[series_id]:,.3f}"


def comparison_counts(current: pd.DataFrame, vintage: pd.DataFrame, series_id: str):
    """Calculate publication-lag and revision diagnostics without imputing values."""
    old_last = last_known_observation(vintage, series_id)
    if old_last is None:
        return pd.NA, pd.NA

    # Late count: current observations dated after the vintage's final known
    # observation were not usable at the as-of cutoff.
    late_count = int(
        current.loc[current["observation_date"] > old_last["observation_date"], series_id].notna().sum()
    )
    merged = current.merge(vintage, on="observation_date", how="inner", suffixes=("_today", "_then"))
    comparable = merged.dropna(subset=[f"{series_id}_today", f"{series_id}_then"])
    # Revision count: only same-date observations are comparable; a changed
    # value means the historical observation was revised after the cutoff.
    revised_count = int((comparable[f"{series_id}_today"] != comparable[f"{series_id}_then"]).sum())
    return late_count, revised_count


def fred_link(series_id: str) -> str:
    return f"https://fred.stlouisfed.org/series/{series_id}"


def main():
    st.set_page_config(page_title="Point-in-Time Interest Rates", layout="wide")
    st.title("Point-in-Time Interest Rates")
    st.caption(
        "Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, downloaded today; "
        "built with AI help, a learning demonstration, not investment advice."
    )

    with st.sidebar:
        st.header("Controls")
        selected = st.multiselect(
            "FRED series",
            options=list(SERIES),
            default=list(SERIES),
            format_func=lambda series_id: f"{series_id} — {SERIES[series_id]}",
        )
        extra = st.text_input("Another FRED series ID", placeholder="Example: CPIAUCSL")
        start_date = st.date_input("Start date", value=date(2020, 1, 1))
        as_known_on = st.date_input("As known on", value=date.today())

    extra_ids = [item.strip().upper() for item in extra.replace(",", " ").split() if item.strip()]
    series_ids = list(dict.fromkeys(selected + extra_ids))
    if not series_ids:
        st.info("Choose at least one series ID.")
        return

    results = []
    for series_id in series_ids:
        label = SERIES.get(series_id, "Additional FRED series")
        try:
            current = get_current_fred(series_id)
            vintage = get_alfred_vintage(series_id, as_known_on.isoformat())
            current_from_start = current.loc[current["observation_date"].dt.date >= start_date].dropna(subset=[series_id])

            st.subheader(f"{series_id} — {label}")
            if current_from_start.empty:
                st.warning(f"No nonmissing current {series_id} values exist on or after {start_date:%Y-%m-%d}.")
            else:
                st.line_chart(current_from_start.set_index("observation_date")[[series_id]], use_container_width=True)

            known_row = last_known_observation(vintage, series_id)
            today_row = last_known_observation(current, series_id)
            st.write(f"Last value known on {as_known_on:%Y-%m-%d}: **{display_value(known_row, series_id)}**")
            late_count, revised_count = comparison_counts(current, vintage, series_id)
            results.append(
                {
                    "Series ID": series_id,
                    "Latest measured/value as known then": display_value(known_row, series_id),
                    "Latest measured/value today": display_value(today_row, series_id),
                    "Today's values after latest known then": late_count,
                    "Same-date values revised since": revised_count,
                }
            )
        except (requests.RequestException, ValueError, pd.errors.ParserError) as error:
            st.error(f"{series_id}: unable to load this FRED/ALFRED series ({error}).")

    if results:
        st.header("Point-in-time comparison")
        table = pd.DataFrame(results)
        table["Series ID"] = table["Series ID"].map(lambda item: f"[{item}]({fred_link(item)})")
        st.markdown(table.to_markdown(index=False), unsafe_allow_html=False)
        st.caption("Counts exclude missing values. A revision is a changed value on the same observation date.")


if __name__ == "__main__":
    main()
