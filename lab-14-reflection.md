# Lab 14 Reflection

## Diversification

Diversification combines investments that do not move exactly together. When correlation is below +1, losses in one asset can be partly offset by different movements in another asset, reducing overall portfolio volatility.

## Why correlation below +1 lowers risk

Portfolio risk depends on individual asset volatility, portfolio weights, and correlation. If two risky assets have correlation below +1, they do not always rise and fall by the same amount at the same time. Their combined volatility can therefore be lower than either asset’s volatility.

## Inverse-volatility portfolio

Inverse-volatility weighting places the largest allocation in Treasury bills because they have the lowest volatility. Since each weight is proportional to one divided by volatility, a lower-volatility asset receives a larger weight.

## Baseline for the CIO

I would show the Benchmark first because it represents Meridian’s stated 60% global equity and 40% investment-grade bond comparison portfolio, and its expected return of 6.80% exceeds the 6.5% objective. However, it fails the reserve rule because it has 0.0% in reserve-eligible assets, while the mandate requires at least 3.0%.

## Partner Discussion and Code Explanation

### Five-Minute Diversification Discussion

I explained that two risky assets can form a less risky portfolio when their correlation is below +1. They do not move exactly together, so when one asset falls, the other may fall less or move differently. That partial offset reduces total portfolio volatility.

I explained that the `portfolio_volatility` function calculates total portfolio variance first and then takes the square root to calculate volatility. The function considers every pair of assets and multiplies the first asset’s weight, the second asset’s weight, and their covariance. It adds all of those covariance terms together to calculate total variance. Because covariance includes correlation, the calculation reflects whether assets move together or partly offset one another.

I explained that the Benchmark holds 40% investment-grade bonds and 60% global equity, but its risk is not simply a weighted average of their volatilities. Its volatility also depends on the 0.25 correlation between the two assets. Because the assets do not move perfectly together, diversification lowers the Benchmark volatility to 10.46%.

My partner asked: “Why do we multiply the weights twice?”

I answered: “Each covariance term describes the relationship between two positions, so the calculation must account for how much of both assets the portfolio holds.”

## Benchmark Volatility by Hand

The Benchmark holds 40% investment-grade bonds and 60% global equity.

Portfolio variance =
(0.40² × 0.06²)
+ (0.60² × 0.16²)
+ (2 × 0.40 × 0.60 × 0.25 × 0.06 × 0.16)

= 0.000576 + 0.009216 + 0.001152

= 0.010944

Portfolio volatility = √0.010944 = 0.1046 = 10.46%.

The correlation term is included in the third part of the formula. Because the bond/equity correlation is below +1, diversification reduces portfolio risk.
