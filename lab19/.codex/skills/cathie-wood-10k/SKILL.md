---
name: cathie-wood-10k
description: Screen a company with Cathie Wood-style growth checks using shared printed SEC EDGAR 10-K facts.
---

Use only the shared printed SEC EDGAR 10-K facts; never estimate or introduce a new number. Calculate revenue annual growth across the five fiscal years as `(last / first) ** (1/4) - 1` and mark it pass at 15% or more. Calculate latest R&D divided by latest revenue and mark it pass at 5% or more. Missing required data is `not known`. Write a memo using only values printed by the program.
