# Lab 16 — Provenance Gate

## Files

- `asof.py` contains the point-in-time filter and signal calculations.
- This README records the required verification and reflection.

## Run the program

From the repository’s main folder, run:

```bash
python3 lab-16-provenance-gate/asof.py
```

## Verification

With decision date `2026-03-31`, the row funnel should show:

- no ticker: row 11;
- exact duplicate: row 7;
- published after the decision date: rows 3, 8, and 10; and
- older vintage replaced by a revision: row 2.

The valid as-of panel is rows `[1, 4, 5, 6, 9, 12]`. Its February signals are
AAA `+1.98%`, BBB `-1.02%`, and CCC `+0.91%`.

## Reflection

The naive comparison ignores publication dates and therefore uses April
observations that would not have been known on March 31. It changes AAA’s
signal from `+1.98%` in February to `+5.83%` in March and BBB’s from `-1.02%`
to `-5.15%`. That is hindsight bias, not a better historical signal.

## Learning and Reflection

### What is look-ahead bias?

Look-ahead bias occurs when an analysis or backtest uses information that was
not available at the time a real decision would have been made. It makes past
performance look better or more accurate than would have been possible in real
time.

### How do event time, publication time, and revisions work together?

Event time is when the underlying activity happened, such as February 2026
spending. Publication time is when that February number became available to
investors. A revision is a later update to a value for an earlier month. For a
point-in-time analysis, I must use only the version of each value that had been
published by the decision date.

### Why was AAA’s +5.83% unavailable on 31 March?

AAA’s naive signal uses the March index value of 109.0. Even though it measures
March, it was published on 10 April 2026. Since the decision date was 31 March,
that value was not yet knowable. The latest available AAA data was the revised
February value of 103.0, so the valid as-of signal was +1.98%.

### Which rule removed the row that mattered most?

The publication-date rule removed AAA row 3, the March value of 109.0. That
row matters most because including it changes AAA’s result from the realistic
+1.98% as-of signal to the much stronger-looking +5.83% naive signal.

### What would a naive backtest claim?

A naive backtest would incorrectly claim that the strategy could react to
information released after the decision date. It would overstate the signal
quality and could make the strategy appear more profitable than it would have
been in real trading.

This is not financial advice. This is for educational and research purposes.
