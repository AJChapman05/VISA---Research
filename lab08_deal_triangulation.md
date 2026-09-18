# Lab 08 — Visa Peer Comparison and Valuation Triangulation

**Target:** Visa Inc. (NYSE: V)  
**Comparison date:** September 10, 2026, using regular-session closing prices  
**Valuation object:** Common equity value per diluted share

## Define/Discover

Visa earns fees by operating a global payments network. Its revenue comes from
services, data processing, international transactions, and other payment
services, net of client incentives. Visa's FY2025 annual GAAP diluted EPS was
positive at **$10.20**, so P/E can support an equity-value reference. I need a
peer that operates a comparable four-party network, has positive annual GAAP
diluted EPS public by the comparison date, and has a closing price from the
same date.

P/E divides a peer's share price by its annual diluted EPS. Applying that
equity multiple to Visa's diluted EPS gives an implied Visa share price. Cash
and debt do not enter this calculation because P/E is already an equity
multiple.

## Peer policy and rejection criteria

I will admit listed operating companies that principally operate a global,
four-party payment network connecting issuing banks, acquiring banks, merchants,
and account holders. The company must earn primarily from network and related
transaction services rather than from lending, deposit-taking, or holding the
consumer credit exposure. It must report positive annual GAAP diluted EPS that
was public on or before September 10, 2026.

I will exclude a candidate if issuing, lending, deposit, or credit-loss
economics are a material driver of earnings; if annual GAAP diluted EPS was not
public by the date; if EPS is nonpositive; or if I cannot reconcile the price
to the comparison date.

## Candidate research and decisions

| Candidate | Decision | Business-model evidence and difference | Annual GAAP diluted EPS, period, publication date | Same-date price and source |
| --- | --- | --- | --- | --- |
| Mastercard (MA) | **Use** | [Mastercard 2025 Form 10-K, Item 1, pp. 8 and 13](https://www.sec.gov/Archives/edgar/data/1141391/000114139126000013/ma-20251231.htm) says Mastercard's network links issuers and acquirers and supports a four-party network. Mastercard also has a larger relative mix of value-added services and solutions. | **$16.52**, FY ended Dec. 31, 2025; [filed Feb. 13, 2026](https://www.sec.gov/Archives/edgar/data/1141391/000114139126000013/ma-20251231.htm), Item 8, Consolidated Statements of Operations. | **$565.37** close on Sept. 10, 2026, [Nasdaq historical data](https://www.nasdaq.com/market-activity/stocks/ma/historical). |
| American Express (AXP) | **Exclude** | [American Express 2025 Form 10-K, Business](https://www.sec.gov/Archives/edgar/data/4962/000000496226000080/axp-20251231.htm) describes card issuing, merchant acquiring, card-network, banking, and financing businesses. Its issuer and lender economics, including credit risk, conflict with the policy. | **$15.38**, FY ended Dec. 31, 2025; [reported Jan. 30, 2026](https://www.sec.gov/Archives/edgar/data/4962/000000496226000037/q425exhibit991.htm). | **$320.71** close on Sept. 10, 2026, [Nasdaq historical data](https://www.nasdaq.com/market-activity/stocks/axp/historical). Excluded from the calculation. |

Visa's own source is its [FY2025 earnings release](https://www.sec.gov/Archives/edgar/data/1403161/000140316125000077/q42025earningsrelease.htm), published Nov. 6, 2025, which reports GAAP diluted EPS of $10.20. Its Sept. 10, 2026 closing price was **$367.21**, from [Nasdaq historical data](https://www.nasdaq.com/market-activity/stocks/v/historical). The former DCF worksheet's $368.65 was an intraday quote, so I do not use it in this same-date closing-price comparison.

## Implemented P/E reference

Only Mastercard passes the policy.

| Company / role | Closing price, Sept. 10, 2026 | FY2025 GAAP diluted EPS | P/E |
| --- | ---: | ---: | ---: |
| Visa (V), target | $367.21 | $10.20 | — |
| Mastercard (MA), peer | $565.37 | $16.52 | 34.223366x |

Mastercard P/E = $565.37 ÷ $16.52 = **34.223366x**.

Applying it to Visa: 34.223366x × $10.20 = **$349.08 per Visa share**.

Because Mastercard is the only admitted peer, **$349.08 is a reference estimate, not a peer range**. It is 4.94% below Visa's $367.21 market close.

## Validation

I checked Mastercard by hand: $565.37 ÷ $16.52 = **34.223366x**, which matches the calculator.

Before removing Mastercard, I predict the reference will disappear because it is the only admitted peer. The calculator confirms that removing MA leaves no admitted peers and no P/E estimate. This avoids pretending that a rejected issuer-lender provides a second network multiple. The lost information is dispersion across a peer set.

## Compare with the DCF and judge criticism

| Method | Value per share | What it measures | Limitation |
| --- | ---: | --- | --- |
| DCF base case | $331.05 | Visa's forecast FCFF, WACC, terminal growth, and net debt assumptions | Terminal value represents 81.03% of enterprise value. |
| DCF sensitivity range | $241.51–$416.62 | Sensitivity to WACC and terminal growth | A wide range reflects assumptions, not a probability distribution. |
| Mastercard P/E reference | $349.08 | Market pricing of Mastercard's FY2025 GAAP earnings applied to Visa FY2025 GAAP EPS | One admitted peer, plus business-mix differences. |
| Visa market close | $367.21 | The price investors paid at the comparison date | Not an intrinsic-value estimate. |

The P/E reference sits $18.03 above the DCF base case and $18.13 below the
market close. Both methods fall below market, but neither supports mechanically
averaging values. The skeptical criticism I accept is that Visa's FY2025 GAAP
EPS includes substantial litigation and other special items, while Mastercard's
GAAP EPS has its own item mix. The calculation uses the same reported GAAP
definition for both firms, but comparability remains limited. I would need a
source-supported, consistently normalized earnings definition before treating
the difference as evidence of a stronger or weaker multiple.

**Question that could change my decision:** Do Visa's litigation charges and
Mastercard's special items create a material difference between their FY2025
GAAP EPS and their ongoing earnings power?

What would change my mind: a second listed pure network operator that passes
the policy, consistently normalized annual earnings for both Visa and
Mastercard, or evidence that Visa's client incentives or litigation exposure
changes its sustainable earnings and cash-flow trajectory.

## Reflection and conclusion

Mastercard belongs because both companies operate global four-party payment
networks and derive income from network activity. Mastercard differs through
its value-added-service mix. American Express does not belong under this policy
because its issuer, lender, deposit, and credit-risk economics are material.

The peer result adds a market-based reference of **$349.08**, while the DCF
provides a cash-flow-based base value of **$331.05** and a sensitivity range of
**$241.51–$416.62**. The one-peer P/E result cannot establish a market range.

**Decision: Watch-defer.** The Sept. 10 market close of $367.21 exceeds both
the DCF base case and the one-peer reference. The DCF sensitivity range contains
the market price, and the P/E evidence has only one admitted peer. I would not
initiate until the price offers a clearer margin of safety or new evidence
supports higher sustainable cash flow or a more comparable peer multiple.

## Files and command

- Calculator: `lab07_pe_comps.py`
- Write-up: `lab08_deal_triangulation.md`
- Run command: `python3 lab07_pe_comps.py`

This is not financial advice.
