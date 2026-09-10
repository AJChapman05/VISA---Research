# Visa Inc. (NYSE: V) — DCF Valuation, Sensitivity Grid & Reverse DCF

**Course:** FIN 43900 — Advanced Applied Valuation  
**Session:** Session 6 · Lab 06: Sensitivity, Reverse DCF, and Conditional Recommendation  
**Company:** Visa Inc. (NYSE: V)  
**Primary Filing:** Form 10-K for Fiscal Year Ended September 30, 2025 (SEC Accession No. 0001403161-25-000089)  
**Valuation Date & Time:** September 10, 2026, 13:50 EDT  
**Today's Market Price:** **$368.65** (NYSE: V intraday quote) — *Reverse DCF Target*  

---

## R — Five Rows, Each Sourced

| Input | Training Value | Visa Value | Unit | As-of Date | Where Yours Comes From (10-K Heading & Locator) |
|---|:---:|:---:|:---:|:---:|---|
| **Starting FCFF** | 100 | **$21,750.00** *(reported FCF: $21,577.00)* | USD millions | Sept 30, 2025 | **Item 8, Consolidated Statements of Cash Flows (p. 64):** Operating cash flows ($23,059M) + after-tax net interest (~$173M) − capex / purchases of property, equipment & tech ($1,482M) = $21,750M. Also normalizes the non-recurring $2,562M litigation provision in **Item 7 MD&A (pp. 45–46)** & **Note 20 (Legal Matters, p. 100)**. |
| **Growth, Years 1–5** | 8%, 6%, 5%, 4%, 3% | **10.0%, 10.0%, 10.0%, 10.0%, 10.0%** | Annual rate | Sept 30, 2025 | **Item 7, MD&A — Net Revenue & Volume Highlights (pp. 40, 45):** 3-year historical net revenue CAGR of ~10.5% ($32,653M in FY23 → $35,926M in FY24 → $40,000M in FY25), driven by processed transactions (+10%), payments volume (+8%), and cross-border volume (+12%). |
| **WACC** | 10% — never copy it | **8.0%** | Annual rate | Sept 10, 2026 | **Brief CAPM Estimate below:** Low-beta asset-light payment network; cost of equity ~8.45%, after-tax debt ~4.05%, 90/10 capital structure. |
| **Terminal Growth** | 3% | **3.0%** | Annual rate | Long-run | **The Long-Run Economy, Not the Company:** U.S. long-run nominal GDP growth benchmark (FRED series A191RL1Q225SBEA: ~2.0% real GDP + 2.0–2.5% inflation target; economy ceiling for a mature firm). |
| **Cash · Debt · Shares** | 50 · 300 · 50 | **Cash: $20,000.00**<br>**Debt: $25,180.00**<br>**Shares: 1,815.00** | Cash: $M<br>Debt: $M<br>Shares: M | Sept 30, 2025<br>Sept 30, 2025<br>Dec 31, 2025 | • **Cash:** **Item 8, Consolidated Balance Sheets (p. 59)** — $17,164M cash & cash equivalents + liquid investment securities; excludes restricted settlement & litigation funds.<br>• **Debt:** **Item 8, Note 10 — Debt (pp. 83–84)** — Senior notes carrying value ($25,171M); net debt used is **$5,180M**.<br>• **Shares:** **Form 10-Q (Q1 FY2026)** / **Note 16 (p. 92)** — As-converted fully diluted weighted-average share count across all common classes. |

### WACC Once (Brief Estimate)

$$\text{WACC once: } 4.2\% + 0.85 \times 5.0\% = 8.45\%\text{ equity; } 5.0\% \times (1 - 0.19) = 4.05\%\text{ debt; } 90/10 \rightarrow \mathbf{\approx 8.0\%}.$$

- **Cost of Equity:** 4.20% (10-Yr Treasury) + 0.85 ($\beta$) × 5.0% (ERP) = 8.45%
- **After-Tax Cost of Debt:** 5.0% (effective senior note coupon, Note 10) × (1 − 0.19 effective tax rate, Note 17) = 4.05%
- **Capital Structure Weights:** 90% equity / 10% debt → **8.0% WACC**

---

## I — Your Company Through the Model

The twelve base-case valuation lines produced by running the model for Visa Inc.:

| # | Line Item / Metric | Model Value | Units / Notes |
|---|---|---:|---|
| 1 | FCFF Year 1 | $23,925.0000 | USD millions ($21,750.00 × 1.10) |
| 2 | FCFF Year 2 | $26,317.5000 | USD millions ($23,925.00 × 1.10) |
| 3 | FCFF Year 3 | $28,949.2500 | USD millions ($26,317.50 × 1.10) |
| 4 | FCFF Year 4 | $31,844.1750 | USD millions ($28,949.25 × 1.10) |
| 5 | FCFF Year 5 | $35,028.5925 | USD millions ($31,844.18 × 1.10) |
| 6 | Present value of the five explicit FCFF | $114,942.9309 | USD millions (discounted at 8.0% WACC) |
| 7 | Terminal value at Year 5 | $721,589.0055 | USD millions ($35,028.59 × 1.03 ÷ [0.08 − 0.03]) |
| 8 | Present value of the terminal value | $491,101.3523 | USD millions (discounted 5 years at 8.0%) |
| 9 | Enterprise value | $606,044.2832 | USD millions (PV explicit + PV terminal value) |
| 10 | Equity value | $600,864.2832 | USD millions (EV + $20,000M cash − $25,180M debt) |
| 11 | Value per diluted share | $331.0547 | USD per share ($600,864.28M ÷ 1,815M shares) |
| 12 | PV of terminal value as share of EV | 0.8103 | Decimal (81.03% of Enterprise Value) |

---

## V — Reasonableness Check

| Metric | Value | Comparison / Status |
|---|---:|---|
| **DCF Model Value Per Share** | **$331.05** | Base-case intrinsic value |
| **Today's Market Price** | **$368.65** | Intraday market quote (Sept 10, 2026) |
| **Ratio (Model Value ÷ Today's Price)** | **0.898×** (~**0.90×**) | Sits inside 0.5×–2× band |

### 1. Inside 0.5×–2×: Say So
**Yes, Visa's DCF value per share ($331.05) sits squarely inside the 0.5×–2× reasonableness band beside today's price ($368.65).**  
At 0.90× of market price (an ~10.2% discount), the base-case valuation is economically grounded and mechanically sound, indicating the market is pricing in modest growth acceleration rather than an ungrounded valuation disconnect.

### 2. Input Under Most Scrutiny (Distrusted Most)
- **The Input:** **Terminal Value Parameters (WACC of 8.0% and Terminal Growth of 3.0%)**.
- **Why:** The present value of the terminal value accounts for **81.03% of total enterprise value** ($491.1B of $606.0B). A 1-percentage-point increase in WACC (8% to 9%) compresses intrinsic value by 17.2% to $274.06, dominating explicit cash flow changes.
- **Secondary Sensitivity:** The **10.0% explicit growth rate**, which depends on whether Visa can maintain 50%+ FCF margins while absorbing rising client incentives ($15.8B in FY25) and regulatory headwinds.

---

## E — Sensitivity Grid & Reverse DCF

### 1. Visa Inc. Sensitivity Grid ($ per diluted share)

| WACC \ Terminal Growth | 2.0% | 3.0% *(Base)* | 4.0% |
|---|:---:|:---:|:---:|
| **7.0%** | $343.01 | $416.62 | **$539.32** *(Furthest Bull Corner)* |
| **8.0%** *(Base)* | $283.77 | **$331.05** *(Base Case)* | $401.98 |
| **9.0%** | **$241.51** *(Furthest Bear Corner)* | $274.06 | $319.63 |

- **Base Case Center (WACC 8.0%, g 3.0%):** **$331.05**
- **Monotonicity Check:**
  - **Falls Down:** As WACC increases from 7% → 8% → 9% at constant 3% growth, value drops from **$416.62 → $331.05 → $274.06**.
  - **Rises Right:** As terminal growth increases from 2% → 3% → 4% at constant 8% WACC, value increases from **$283.77 → $331.05 → $401.98**.

### 2. Reading the Corners & Furthest Corner Predictions

- **Furthest Bull Corner (Top-Right: WACC 7.0%, g 4.0%):** **$539.32** (+62.9% above base case).  
  *Economic Driver:* Applies the lowest discount rate and the maximum perpetual GDP growth rate, expanding the capitalization multiple ($0.07 − 0.04 = 0.03 denominator).
- **Furthest Bear Corner (Bottom-Left: WACC 9.0%, g 2.0%):** **$241.51** (-27.0% below base case).  
  *Economic Driver:* Applies higher cost of capital alongside macroeconomic secular stagnation ($0.09 − 0.02 = 0.07 denominator).

---

### 3. Reverse DCF: What Today's Price Already Assumes

- **Target Market Price:** **$368.65**
- **Search Bounds:** [−5.00%, +10.00%] (converged via bisection; no growth pushed below −100%)
- **Solved Uniform Growth Shift:** **+2.56 percentage points (+0.0256)** added across all five explicit years.
- **Implied Annual FCFF Growth Rates (Years 1 to 5):** **12.56% annually** (vs. 10.00% base case).
- **Growth Hurdle Above Base Case:** **+2.56% (+256 bps)**.

**Inputs Held Fixed:**
1. Starting Normalized FCFF: **$21,750.00M**
2. WACC: **8.00%**
3. Terminal Growth Rate: **3.00%**
4. Non-Operating Cash & Securities: **$20,000.00M**
5. Total Debt: **$25,180.00M**
6. Diluted Shares: **1,815.00M**

*Note on Interpretation:* The solved shift reflects the performance expectation priced in by the market under fixed discount and balance-sheet assumptions — it is an analytical benchmark of market sentiment, not proof of mispricing.

---

## Committee Decision & Checkout Recommendation

> **"My supported valuation range is $274.06 to $416.62 per diluted share (base-case intrinsic value of $331.05) versus an observed market price of $368.65 as of September 10, 2026.**  
> 
> The conclusion is most sensitive to the **terminal value parameters (WACC and terminal growth)**, which account for **81.0%** of total enterprise value.  
> 
> For a committee with no current position, I recommend **Watch-Defer**. Today's market price of $368.65 already assumes sustained low-teens FCFF growth (**12.56% annually**), demanding a +256 bps acceleration over base case without providing any margin of safety. Revisit if market volatility or legal settlements pull the price below **$330.00**."

---

## Conditional Call — and the Floor

### 1. Conditional Call
> **"Watch-defer. Initiate if the growth the price demands drops below my 10% forecast path — a market price below about $331.00 (or below $300.00 for a 10% margin of safety), or a sourced reason to raise my five-year growth path above 12.6% (such as sustained value-added services acceleration or higher cross-border margin realization); otherwise, watch-defer.**  
> 
> **Monitor: Client incentives as a percentage of gross revenue in next quarter's Form 10-Q** *(if client incentives continue to grow faster than gross revenue, as they did in FY2025 at $15.8B, net revenue conversion and operating margins will deteriorate below the base-case forecast)*."

### 2. The Floor (Submission Summary)
- **Inputs, Sourced:**
  - Starting FCFF: **$21,750M** *(FY25 10-K Cash Flow Statement p. 64 normalized for Note 20 litigation)*
  - Growth (Years 1–5): **10.0%** *(Item 7 MD&A 3-year CAGR ~10.5%)*
  - WACC: **8.0%** *(Brief CAPM estimate: 4.2% Rf + 0.85 beta × 5.0% ERP = 8.45% Re; 4.05% Rd; 90/10)*
  - Terminal Growth: **3.0%** *(FRED long-run nominal GDP ceiling)*
  - Cash · Debt · Shares: Cash **$20,000M** (p. 59), Debt **$25,180M** (pp. 83–84; Net debt $5,180M), Shares **1,815M** (Note 16 / Q1 10-Q).
- **Company's Value:**
  - Base-Case DCF Fair Value: **$331.05 per share** (EV: **$606.04B**, Common Equity: **$600.86B**, Terminal Share: **81.03%**).
- **The Grid and the Growth the Price Assumes:**
  - Sensitivity Grid: **$241.51** (Bear Corner: 9% WACC / 2% g) to **$539.32** (Bull Corner: 7% WACC / 4% g), centered at **$331.05**.
  - Implied Growth: At today's price of **$368.65**, the Reverse DCF solves to **12.56% annual FCFF growth** for five straight years (**+256 bps** above the 10.0% base case).
- **Conditional Call:**
  - **Watch-defer.** Initiate only below **$331.00** or upon verified evidence justifying >12.6% growth; monitor quarterly **client incentives vs. gross revenue** in the 10-Q.
This is not investment advice
