# Lab 11 - Visa Sensitivity

## Locked Changed-Input Record

**Timestamp:** September 29, 2026, 2:00 pm

### Driver 1 - Net-revenue growth

| Item | Value |
|---|---:|
| Base case | 10.0% |
| Lower case | 8.0% |
| Higher case | 12.0% |
| Forecast years affected | FY2026E-FY2030E |

**Prediction before running:**
If net-revenue growth decreases from 10.0% to 8.0%, I expect FY2030 operating income, FCFE, and value per share to decrease because lower revenue reduces the revenue base used to generate operating profit and cash flow. If growth increases to 12.0%, I expect all three outputs to increase. I expect value per share to be especially sensitive because final-year FCFE affects terminal value.

**Range reason:**
Visa's recent reported revenue growth was near 10%-11%, so 8%, 10%, and 12% test a slower, base, and stronger growth path without assuming an extreme change.

### Driver 2 - Operating-cost ratio excluding D&A

| Item | Value |
|---|---:|
| Base case | 31.0% of net revenue |
| Lower case | 29.0% of net revenue |
| Higher case | 33.0% of net revenue |
| Forecast years affected | FY2026E-FY2030E |

**Prediction before running:**
If the operating-cost ratio rises from 31.0% to 33.0%, I expect operating income, FCFE, and value per share to decrease because Visa retains less operating profit from each dollar of net revenue. If the ratio falls to 29.0%, I expect those outputs to increase. I expect the effect to compound as revenue grows over the forecast period.

**Range reason:**
The 31.0% base reflects normalized Visa operating costs excluding D&A and the unusual FY2025 litigation charge. A 2-percentage-point range tests modest margin pressure or improvement.

## Partner Exchanges

### Exchange 1 - Before runs

**Partner question:** Why is your revenue-growth range 8% to 12% instead of using Visa's most recent 14% quarterly growth rate?

**My answer:** I used a 10% base because Visa's FY2023-FY2025 reported revenue growth was roughly 10%-11%. The 14% Q3 FY2026 result supports continued strength, but I did not assume one quarter persists for five years. The 8%-12% range tests a modest slowdown and modest outperformance around the historical trend.

**Partner check of units:** The 8%, 10%, and 12% growth inputs are percentage rates applied to prior-year net revenue, rather than percent changes to a reported statement total.

**My response:** The inputs are independent growth-rate assumptions. The model recalculates linked revenue, operating income, FCFE, and value per share in every scenario.

**My check of my partner's model:** I checked that my partner changed only one independent input at a time, confirmed the units were percentage points rather than percent changes, and recomputed one change-from-base result as scenario output minus base output. I asked whether their larger sensitivity span reflected the economics of the driver or simply a wider chosen range.

### Exchange 2 - After runs

**Partner question:** Why does a lower operating-cost ratio improve your value per share?

**My answer:** The ratio measures operating costs as a percentage of net revenue. At 29% instead of 31%, Visa keeps two additional cents of operating profit per revenue dollar before D&A, which increases net income and FCFE. Higher final-year FCFE also increases terminal value, so the per-share effect can be larger than the initial operating-profit change.

**Scenario my partner recomputed:** My partner recomputed the difference between the high-growth FY2030 FCFE result and the base-case FY2030 FCFE result. High-growth FY2030 FCFE was $37,369.5 million; base-case FY2030 FCFE was $34,122.0 million; the change was +$3,247.5 million.

**Partner check after the runs:** We confirmed that only revenue growth changed and that the operating-cost ratio remained at the 31.0% base assumption.

### Exchange 3 - Driver ranking

**Partner question:** Could revenue growth appear to be the biggest driver only because you tested a wider range for it?

**My answer:** Yes. Sensitivity rankings apply only over the ranges tested. A larger output span can mean the driver is economically important, but it can also reflect a wider or less realistic range. I interpret the result as "most important over these stated ranges," not as a probability forecast.

**Partner's summary and my response:** My partner summarized that revenue growth was the larger driver over the stated ranges, while I confirmed that the ranking can reflect both the economics of growth and the width of the ranges tested.

## Saved Visible Output

- [Base-case model output](lab-11-base-output.txt)
- [Full sensitivity-analysis output](lab-11-sensitivity-output.txt)

## Results and Interpretation

Run completed with `python3 visa_proforma_sensitivity.py`. All six scenarios were valid. In every scenario, the annual balance-sheet check displayed $0.0 (within displayed rounding) and cash remained above the $5,000 minimum.

### Net-Revenue Growth Results

Changed input: FY2026E-FY2030E net-revenue growth, expressed as a percentage of prior-year net revenue. All other assumptions reset to base for each independent run.

| Scenario | Actual changed input | FY2030E operating income ($mm) | Change vs. base ($mm) | FY2030E FCFE before distributions ($mm) | Change vs. base ($mm) | Value per share | Change vs. base |
|---|---:|---:|---:|---:|---:|---:|---:|
| Lower | 8.0% | 38,680.3 | -3,805.4 | 31,101.8 | -3,020.2 | $270.77 | -$24.02 |
| Base | 10.0% | 42,485.7 | +0.0 | 34,122.0 | +0.0 | $294.79 | +$0.00 |
| Higher | 12.0% | 46,581.0 | +4,095.3 | 37,369.5 | +3,247.5 | $320.53 | +$25.74 |
| Valid-run span (maximum − minimum) | — | 7,900.7 | — | 6,267.7 | — | $49.76 | — |

### Operating-Cost Ratio Excluding D&A Results

Changed input: FY2026E-FY2030E operating-cost ratio excluding D&A, expressed as a percentage of net revenue. All other assumptions reset to base for each independent run.

| Scenario | Actual changed input | FY2030E operating income ($mm) | Change vs. base ($mm) | FY2030E FCFE before distributions ($mm) | Change vs. base ($mm) | Value per share | Change vs. base |
|---|---:|---:|---:|---:|---:|---:|---:|
| Lower | 33.0% | 41,197.3 | -1,288.4 | 33,053.8 | -1,068.2 | $285.55 | -$9.23 |
| Base | 31.0% | 42,485.7 | +0.0 | 34,122.0 | +0.0 | $294.79 | +$0.00 |
| Higher | 29.0% | 43,774.1 | +1,288.4 | 35,190.1 | +1,068.2 | $304.02 | +$9.23 |
| Valid-run span (maximum − minimum) | — | 2,576.8 | — | 2,136.3 | — | $18.47 | — |

### Restored Base Check

| FY2030E output | Original base | Restored base | Match within displayed rounding |
|---|---:|---:|---|
| Operating income ($mm) | 42,485.7 | 42,485.7 | PASS |
| FCFE before distributions ($mm) | 34,122.0 | 34,122.0 | PASS |
| Value per share | $294.79 | $294.79 | PASS |

Restored-base inputs matched the base assumption set: **PASS**.

### Main Driver Over These Ranges

Over these ranges, net-revenue growth had the larger FY2030 operating-income span: $7,900.7 million, compared with $2,576.8 million for the operating-cost ratio excluding D&A.

Over these ranges, net-revenue growth had the larger FY2030 FCFE-before-distributions span: $6,267.7 million, compared with $2,136.3 million for the operating-cost ratio excluding D&A.

Over these ranges, net-revenue growth had the larger value-per-share span: $49.76, compared with $18.47 for the operating-cost ratio excluding D&A.

This result reflects both the economics of revenue growth and the width of the tested ranges. Revenue growth compounds through all five forecast years, affecting operating income, FCFE, and terminal value. The 8.0%-12.0% growth range also contributes to the larger span, so this is a conclusion only over these ranges and not a probability forecast.

The result does not change my valuation question: the model value remains below Visa's market price across the base case, so the key research question remains whether Visa can sustain revenue growth and margins strong enough to justify the market's higher implied value.

### Reflection

**What result surprised me:** I was surprised that revenue growth created a much larger value-per-share span than the operating-cost ratio. Both inputs affect profitability, but growth compounds for five years and also changes terminal value.

**Whether the results changed my valuation question or research priority:** The results did not change my research priority. They reinforced that Visa's long-term net-revenue growth is the key assumption to investigate, especially the durability of payments-volume, cross-border, value-added-services, and client-incentive trends.

**Whether my prediction was correct; if not, why it differed from the actual output:** My prediction was correct: lower revenue growth and a higher operating-cost ratio reduced operating income, FCFE, and value per share. Revenue growth had the larger effect because it compounds through every forecast year and influences terminal value.

This is not investment advice
