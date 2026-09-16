# Lab 07 — Comparable-Company Policy and Implied Range

## Define/Discover

Price-to-earnings (P/E) is a market-price multiple: share price divided by
diluted earnings per share (EPS). Price per share is the market value of one
common share, while diluted EPS is the earnings available to common
shareholders divided by diluted shares outstanding. A P/E multiple shows how
much investors are currently paying for one dollar of a company's earnings.

Comparing P/E multiples makes firms with different absolute earnings more
comparable because the measure is expressed per dollar of earnings rather than
in total dollars. It adds a market-based check to my DCF: the DCF values the
company from its own forecasted cash flows, while P/E indicates how the market
is valuing similar companies' current earnings.

P/E is most useful when the companies have comparable business models,
accounting periods, profitability, growth prospects, risk, and capital
structures. It can be misleading when EPS is negative or unusually affected by
one-time items, or when peers have materially different growth, margins,
leverage, or business mix. A lower P/E is not automatically a better investment;
it may reflect weaker growth, greater risk, lower-quality earnings, or a less
comparable business.

P/E is an equity multiple. Applying it to EPS produces an implied share price,
so cash and debt must not be added or subtracted.

## Peer policy and decisions

My policy prioritizes franchised vehicle retail and the related service and
parts businesses, because these activities drive the dealership economics more
directly than a broad industry label.

| Candidate | Decision | Rationale |
| --- | --- | --- |
| AutoNation (AN) | Use | AN is a franchised automotive retailer with dealership, service, and parts operations that are relevant to Asbury's core business model. |
| Group 1 Automotive (GPI) | Qualify | GPI is also a franchised automotive retailer with relevant dealership, service, and parts operations. It remains useful, but differences in geographic footprint, dealership mix, scale, and growth should be kept in mind when interpreting its multiple. |

## Case inputs and calculation

| Company / role | Price | FY2024 GAAP diluted EPS | P/E |
| --- | ---: | ---: | ---: |
| Asbury Automotive (ABG), target | $243.03 | $21.50 | — |
| AutoNation (AN), peer | $169.84 | $16.92 | 10.037825× |
| Group 1 Automotive (GPI), peer | $421.48 | $36.81 | 11.450149× |

The peer P/E minimum is **10.037825×**, the median is **10.743987×**, and
the maximum is **11.450149×**. Applying these unrounded multiples to ABG's
$21.50 EPS gives:

| Basis | Implied ABG price |
| --- | ---: |
| Minimum peer P/E | $215.81 |
| Median peer P/E | $231.00 |
| Maximum peer P/E | $246.18 |

The peer-implied range is **$215.81–$246.18**, with a median-based estimate of
**$231.00**.

## Validation and evolution

If the higher-multiple peer, GPI, is removed, the remaining peer is AN. The
median-implied ABG price becomes **$215.81**, a **−$15.18** change from the
two-peer median estimate. The result falls because the higher P/E is no longer
in the peer set. With only AN remaining, $215.81 is a reference estimate—not a
range—because there is no dispersion across multiple peers to measure.

For completeness, removing AN leaves GPI and produces a remaining
median-implied price of **$246.18**, a **+$15.18** change from the full-peer
median estimate.

## Reflection

This comparison does not prove that ABG is fairly valued. It is a market-based
cross-check that depends on the peer policy and on whether the peers' earnings,
business mix, growth, and risk are genuinely comparable. I should compare this
independent P/E evidence with my DCF assumptions rather than mechanically
averaging the two methods.

## Files and command

- Calculator: `lab07_pe_comps.py`
- Write-up: `lab07_comparable_policy.md`
- Run command: `python3 lab07_pe_comps.py`

This is not financial advice
