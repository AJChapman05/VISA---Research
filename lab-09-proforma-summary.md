# Lab 09 — Pro-Forma Build: key takeaways

- The playlist’s DRIVER method is a guardrail for using AI without outsourcing judgment: Define the task, Represent the plan and inputs, Implement, Validate the logic and sources, Evolve the work, and Reflect by explaining it in your own words. The stages are iterative, not a one-pass checklist.
- In finance, AI can help build and revise the engine, but the analyst remains responsible for source quality, model logic, and defensible assumptions. The relevant skill is judgment, not merely formula-writing.
- Begin with reported history and distinguish organic performance from acquired growth. For ABG, reported revenue growth included major acquisitions; the relevant base for a recurring forecast was same-store growth.
- Preserve provenance: every input should be visibly labeled as a fact, history-derived ratio, management guidance, or judgment. Data-provider values still need to be checked against the underlying filings.
- A pro-forma model is a connected three-statement engine, not independent forecasts. Every operating assumption must ultimately flow through income, the balance sheet, and cash.
- The highest-impact ABG judgments are revenue growth (1.8%), gross margin (17.05%), and the SG&A-to-gross-profit path (66.5% to 64.5%). These drive operating income and therefore valuation.
- Cash is calculated last because it is the residual consequence of operating performance, investment, working capital, financing, and capital returns. It should never be manually plugged.
- Inventory is financed substantially through floor-plan borrowing. Higher inventory raises both the inventory asset and floor-plan liability; omitting this financing would incorrectly push cash sharply negative.
- Depreciation, impairment, capex, working capital, debt paydown, and buybacks each have distinct cash and balance-sheet effects. Impairment is non-cash, so it reduces earnings but is added back in FCFE.
- Balancing checks are part of the model itself. A nonzero assets-minus-liabilities-minus-equity gap identifies an inconsistent link; forcing FY2026 cash back to $40.4 should produce the expected -$61.4 gap.
- DCF value is driven heavily by continuing value: this case has about 80% of its equity value after 2030. The terminal-value assumptions therefore deserve explicit scrutiny.

## ABG validation result

Running `python3 proforma.py` reproduces the lab’s known answer: FY2026 revenue $18,323.0m, operating income $844.2m, net income $413.6m, FCFE $211.4m, and cash $101.8m; FY2030 revenue $19,678.3m, operating income $971.4m, net income $527.5m, FCFE $342.3m, and cash $719.8m. The model balances in every year and values ABG at **$291.75 per share**, with approximately **80%** of value after 2030.
