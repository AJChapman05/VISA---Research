# Lab 13 — Portfolio Mandate Checker

`mandate.py` checks each candidate portfolio against these rules:

- weights sum to 100%;
- long-only positions (no negative weights);
- at least 3.0% in reserve-eligible assets, covering four $0.75 million quarterly distributions on a $100 million reserve;
- at least 90.0% redeemable within five business days;
- no non-exempt single-company issuer above 8.0%.

Cash, U.S. Treasury securities, and diversified funds are exempt from the issuer limit. Acme Corp bonds and stock are combined for the issuer test. Calendar-year loss is not tested; the program prints `Calendar-year loss: requires CIO clarification`.

## Final results

| Candidate | Result |
|---|---|
| A | Passes every checkable rule |
| B | Fails 3 rules: reserve, liquidity, and issuer concentration |
| C | Fails 1 rule: reserve |
| D | Passes every checkable rule |

## Run command

```bash
python3 mandate.py
```

## S1-S10 classification

| Statement | Classification | Reason |
|---|---|---|
| S1 | Hard constraint | The seven-year horizon and annual rebalancing instruction specify the portfolio’s operating time frame and rebalancing requirement. |
| S2 | Objective | CPI plus 4% net of costs over rolling five-year periods states the desired investment outcome. |
| S3 | Hard constraint | The required quarterly payout and twelve-month cash or daily-liquid government-security reserve are measurable requirements. |
| S4 | Preference | The 60% global equity and 40% U.S. investment-grade bond benchmark provides a comparison point, but it does not explicitly require the portfolio to hold those weights. |
| S5 | Hard constraint | Long-only, no borrowing, no short sales, and no derivatives are explicit prohibitions. |
| S6 | Hard constraint | No single issuer above 8% is a measurable portfolio limit. |
| S7 | Hard constraint | Turnover cannot exceed 25% annually without committee approval. |
| S8 | Hard constraint | At least 90% must be redeemable within five business days. |
| S9 | Unverifiable promise | The no-more-than-10% calendar-year-loss statement gives no risk measure, probability, testing method, or breach procedure. |
| S10 | Missing | The CIO has not specified what the portfolio should optimize or any sector, ESG, tax, or home-bias preferences. |

## Required negative-weight probe

I temporarily changed Candidate A’s Cash weight from 2% to -2% and its Global equity index fund weight from 60% to 64%. The checker correctly showed a lowest weight of -2.0 and failed only the long-only rule; the reserve rule still passed at 10.0%. I then restored the original inputs.

## Candidate D judgment

Candidate D holds 3% cash and 97% in the investment-grade bond fund, so it passes every coded rule. However, the CIO could reasonably reject it because it differs sharply from the 60% global-equity and 40% investment-grade-bond benchmark in S4, which may indicate that the benchmark is intended to represent the desired long-term strategic mix.

## Skeptical colleague check

As a skeptical colleague, I would challenge Candidate D under S4. A nearly all-bond portfolio may be too conservative to pursue the CPI plus 4% objective in S2, even though it satisfies the coded liquidity, reserve, issuer, and long-only rules.

## Question for the CIO

Before optimization, the CIO must answer: “Is the 60% global-equity and 40% U.S. investment-grade-bond benchmark only a performance comparison, or is it the intended strategic allocation?”

If it is the intended strategic allocation, the portfolio should remain reasonably close to 60/40. If it is only a performance benchmark, the portfolio can be optimized more freely around the return objective, spending need, liquidity requirement, and risk tolerance.

## Investment policy statement

An investment policy statement, or IPS, is a document that translates a client’s goals and limitations into investment objectives, constraints, benchmarks, and governance rules. It helps ensure that investment decisions are consistent with the client’s purpose rather than based on short-term reactions.

For Meridian, S2 is the return objective; S1 describes time horizon and rebalancing; S3, S5, S6, S7, and S8 are measurable constraints; S4 is the benchmark; S9 needs clarification before it can become a testable risk constraint; and S10 identifies missing preferences and an unspecified optimization target.

## Reflection

A portfolio can pass every coded rule and still be unsuitable because the checker only tests measurable restrictions. It cannot decide whether a portfolio has enough expected return to pursue the CPI plus 4% objective, whether it fits the benchmark’s intended role, or what risk measure the CIO means in S9.

The most difficult classification was S4 because a benchmark can be used only to evaluate performance, but it can also signal the CIO’s preferred long-term risk exposure. The CIO must clarify which role the benchmark plays before the portfolio is optimized.
