# Lab 12 - Visa Presentation Notes

## 1. Target Selection

I selected Visa Inc. (NYSE: V) because it is a large, profitable payment-network company with public filings, recurring transaction-related revenue, and strong cash generation. Visa is suitable for valuation because its growth drivers, operating risks, and cash flows are visible in annual filings.

My initial view was watch-defer. Visa's network scale and margins are attractive, but its valuation depends on whether net-revenue growth and client-incentive economics remain durable.

**Show:** `Project-1-Edition-A-Visa.md`

## 2. Company and Evidence

Visa operates VisaNet, a payments network that facilitates authorization, clearing, and settlement among consumers, issuers, acquirers, and merchants. Visa is not a lender and does not carry consumer credit risk in the same way as a bank.

Visa earns service revenue, data-processing revenue, international-transaction revenue, and other revenue, net of client incentives.

FY2025 net revenue was $40.0 billion, compared with $35.926 billion in FY2024 and $32.653 billion in FY2023. FY2025 net income was $20.058 billion.

The most important company-specific line is client incentives. Client incentives were $15.751 billion in FY2025 and can reduce the conversion of gross revenue into reported net revenue.

Important risks include regulation, alternative-payment rails, pricing pressure, client incentives, cybersecurity, and litigation.

**Sources:** Visa FY2025 Form 10-K, Item 1, Item 1A, Item 7, Item 8, and Note 3.  
**Show:** `Visa-Research-Report-Draft.md` and `sources.md`

## 3. Visa Pro-Forma

Visa is an asset-light payments network, so I did not force an inventory, floor-plan, gross-profit, or retailer-style SG&A model onto it.

My model uses net revenue and Visa's operating-cost structure. The company-specific driver is client incentives.

My key assumptions are:

| Assumption | Base Case |
|---|---:|
| Net-revenue growth | 10.0% annually |
| Operating costs excluding D&A | 31.0% of net revenue |
| Capital spending | 4.0% of net revenue |
| Tax rate | 17.1% |
| Cost of equity | 8.5% |
| Terminal growth | 3.0% |
| Shares outstanding | 1.815 billion |

The FY2030 base case produces:

| Output | FY2030E |
|---|---:|
| Operating income | $42.486 billion |
| FCFE before distributions | $34.122 billion |
| Value per share | $294.79 |

The balance-sheet check equals zero in every forecast year, and cash remains above the $5.0 billion minimum.

**Show:** `lab-10-visa-proforma.md` and `visa_proforma.py`

## 4. Valuation

My earlier Visa FCFF DCF used normalized FY2025 FCFF of $21.75 billion, 10.0% five-year FCFF growth, an 8.0% WACC, and 3.0% terminal growth.

The DCF produced:

| Item | Value |
|---|---:|
| Enterprise value | $606.04 billion |
| Equity value | $600.86 billion |
| Value per share | $331.05 |
| Terminal value share of EV | 81.03% |

The saved intraday market price was $368.65 on September 10, 2026. The September 10 closing price was $367.21.

At $368.65, the reverse DCF implied 12.56% annual FCFF growth for five years, compared with my 10.0% base-case assumption.

My Mastercard P/E reference was $349.08 per Visa share. I do not average the DCF and P/E values because they use different valuation methods and assumptions. The DCF depends heavily on long-term FCFF, WACC, and terminal growth. The P/E reference depends on Mastercard's market multiple and comparability.

**Show:** `visa-dcf-inputs.md` and `lab08_deal_triangulation.md`

## 5. Sensitivity and Drivers

I tested two independent operating drivers one at a time:

| Driver | Low | Base | High |
|---|---:|---:|---:|
| Net-revenue growth | 8.0% | 10.0% | 12.0% |
| Operating-cost ratio excluding D&A | 33.0% | 31.0% | 29.0% |

Revenue growth had the larger impact over these ranges:

| FY2030E output span | Revenue Growth | Operating-Cost Ratio |
|---|---:|---:|
| Operating income | $7.901 billion | $2.577 billion |
| FCFE before distributions | $6.268 billion | $2.136 billion |
| Value per share | $49.76 | $18.47 |

The causal link is:

Net-revenue growth → net revenue → operating income → net income and FCFE → terminal value → value per share.

Revenue growth ranks as the larger driver only over these selected ranges. The ranking can reflect the range width as well as the economics of the input. Sensitivity analysis does not provide a probability forecast.

**Show:** `lab-11-visa-sensitivity.md` and `lab-11-sensitivity-output.txt`

## 6. Interpretation

My supported conclusion is watch-defer.

Visa has strong payment-network economics, large-scale transaction processing, and strong cash generation. However, my DCF value of $331.05 and statement-based pro-forma value of $294.79 are below the saved market-price references.

The key question is whether Visa can sustain net-revenue growth and margins strong enough to justify the market's higher implied value.

I would investigate payments-volume growth, cross-border growth, value-added-services growth, and client incentives in the next filing. I would become more positive if new evidence supported durable growth above my base assumptions without worsening client-incentive economics, or if the market price created a larger margin of safety.

## Key Limitation

Terminal value represents 81.03% of the earlier DCF enterprise value. Therefore, the DCF is highly sensitive to the 8.0% WACC and 3.0% terminal-growth assumptions.

## Presenter Review Notes

- **Question received:** Why did you choose Visa, what did the analysis teach you that you did not expect, and why do you still conclude watch-defer?  
  **My Visa-model answer:** I selected Visa because it is a payments-network business with recurring transaction-related revenue and cash generation. The existing work identifies client incentives as the company-specific economic pressure and retains watch-defer because durable net-revenue growth and client-incentive economics remain the key valuation questions.  
  **Limitation or unresolved item:** The Project 1 decision-user and valuation-date fields remain incomplete, and this does not add a new conclusion beyond the saved work.

- **Question received:** What evidence supports 10% net-revenue growth for five years, and what would make you lower it to 8%?  
  **My Visa-model answer:** The base case uses 10.0% annual net-revenue growth; the existing evidence shows reported growth of 11.0% in FY2023, 10.0% in FY2024, and 11.3% in FY2025, while the saved FY2026 Q3 release reports 14% growth driven by payments volume, cross-border volume, and processed transactions. The sensitivity model tests an 8.0% case.  
  **Limitation or unresolved item:** Five years at 10.0% is a judgment, not management guidance; the model does not separately forecast payment volume, transaction counts, or cross-border activity.

- **Question received:** How could client incentives change your cash-flow forecast, including possible pressure on FCFE or the cash floor?  
  **My Visa-model answer:** The pro-forma forecasts net revenue after client incentives rather than modeling gross revenue and incentives as separate lines. It sets changes in other operating assets and other liabilities equal, so the modeled net-working-capital cash effect is zero. In the base case, cash remains above the $5 billion floor and the revolver remains at zero.  
  **Limitation or unresolved item:** The model does not separately forecast the timing of upfront client-incentive payments, so it cannot test whether a different cash-timing pattern would reduce FCFE or use the cash floor.

- **Question received:** Why do the earlier FCFF/WACC DCF and linked FCFE/cost-of-equity valuation differ, and can you reconcile them with consistent dates and shares?  
  **My Visa-model answer:** The earlier FCFF DCF produces $331.05 per share using 8.0% WACC and 3.0% terminal growth; the linked FCFE pro-forma produces $294.79 per share using an 8.5% cost of equity and 3.0% terminal growth. The FCFF model values enterprise cash flow and bridges cash and debt, whereas the pro-forma values FCFE before distributions directly.  
  **Limitation or unresolved item:** The $36.26 difference is not reconciled in a single same-date, same-share-basis schedule in the existing work. The two models have different cash-flow definitions, discount rates, balance-sheet treatment, and valuation dates.

- **Question received:** What supports the 3% terminal-growth assumption, and how does the linked terminal calculation fund that growth?  
  **My Visa-model answer:** The linked model uses 3.0% terminal growth and shows that 79.4% of linked equity value comes after FY2030. Its forecast includes capital spending at 4.0% of revenue, matched changes in other operating assets and liabilities, and debt held flat.  
  **Limitation or unresolved item:** The terminal-growth assumption is a judgment. The linked model does not provide a separate terminal-period schedule for incremental capex, working capital, or debt repayment beyond its stated ongoing assumptions.

- **Question received:** Why are the 8%/10%/12% revenue-growth and 33%/31%/29% operating-cost ranges reasonable, and could another range change the driver ordering?  
  **My Visa-model answer:** The sensitivity changes one independent input at a time. Revenue-growth cases are 8.0%, 10.0%, and 12.0%; the operating-cost ratio cases are 33.0%, 31.0%, and 29.0%, with 31.0% as base. Over these ranges, revenue growth has a $49.76 per-share span versus $18.47 for the operating-cost ratio.  
  **Limitation or unresolved item:** The ranking applies only over the selected ranges; another defensible range could change the ordering, and the sensitivity is not a probability forecast.

- **Question received:** Can you trace the 12% growth sensitivity through the statements and show its accounting checks?  
  **My Visa-model answer:** In the 12.0% growth case, FY2030 operating income rises from $42.486 billion to $46.581 billion, FCFE before distributions rises from $34.122 billion to $37.370 billion, and value per share rises from $294.79 to $320.53. Taxes and capex recalculate through the linked model; capex remains 4.0% of revenue, and changes in other operating assets and liabilities remain matched. All forecast balance-sheet checks passed, cash stayed above the $5 billion floor, and the revolver remained at zero.  
  **Limitation or unresolved item:** The high-growth case holds the other independent assumptions at base, including the capex ratio, so it does not test whether faster growth would require a different investment rate.

- **Question received:** How reliable is the Mastercard comparison, given that Mastercard is the only admitted peer?  
  **My Visa-model answer:** Lab 08 admits Mastercard because it meets the global four-party network policy; American Express is excluded because issuing, lending, deposit, and credit-risk economics are material. Mastercard’s FY2025 GAAP diluted EPS was $16.52 and was filed February 13, 2026, before the September 10, 2026 comparison date. Applying Mastercard’s P/E to Visa produces a $349.08-per-share reference.  
  **Limitation or unresolved item:** Mastercard is the only admitted peer, so removing it leaves no peer estimate. Differences in business mix and GAAP earnings items limit comparability; the result is a reference estimate, not a peer range.

- **Question received:** What does the reverse DCF’s 12.56% FCFF-growth result imply, and why is it different from the revenue-growth sensitivity?  
  **My Visa-model answer:** The earlier DCF solves for 12.56% annual FCFF growth for five years to match the saved September 10, 2026 intraday price of $368.65, while holding the stated DCF inputs fixed. The revenue-growth sensitivity instead changes net-revenue growth in the linked FCFE model from 8.0% to 12.0% with the operating-cost ratio held at its base assumption.  
  **Limitation or unresolved item:** The reverse DCF is a conditional analytical benchmark, not investors’ actual expectations, and the earlier DCF does not translate the solved FCFF growth into a separate revenue, margin, and investment schedule.

- **Question received:** What evidence about growth, incentives, or costs would change your conclusion, and which assumption would you research next?  
  **My Visa-model answer:** The existing conclusion is watch-defer. The high-growth case reaches $320.53 per share, below the saved $368.65 quote when those figures are compared as stated. The existing research priorities are payments volume, cross-border growth, value-added-services growth, and client incentives; evidence of durable growth above base assumptions without worse client-incentive economics would support a more positive assessment, while weaker growth or margin evidence would make the case more cautious.  
  **Limitation or unresolved item:** The source notes that dates and share bases must be comparable. No new evidence, model change, or updated valuation conclusion is claimed here.

## Reviewer Notes About My Partner

- **Selection and evidence question I asked:** Why did you choose META, and which evidence supports the claim that advertising is the central revenue driver?
- **Model and valuation question I asked:** How does the linked pro-forma produce negative early economic FCFF despite positive net income, and why does the linked value differ from the earlier DCF?
- **Sensitivity and interpretation question I asked:** Why does ad-price growth have a slightly larger value-per-share span than impression growth over the tested ranges, and could another defensible range change that ordering?
- **Source or calculation checked and result:** Pending: record the actual source/calculation checked during the discussion.
- **My explanation back of my partner’s conclusion, main driver, and limitation:** Pending: record my partner’s actual conclusion, main driver, and limitation.
- **Evidence-backed strength and specific improvement:** Pending: record the evidence-backed strength and specific improvement after listening.

## Reflection

- **Question that made me reconsider something:** Pending—complete after the live partner discussion.
- **What I understand better about Visa:** The linked model shows that revenue growth affects operating income, FCFE, and terminal value, while client incentives can weaken conversion from gross revenue to net revenue.
