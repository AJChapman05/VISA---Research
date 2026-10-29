# Project 2 Point-in-Time Data Card — BAA

## Series record

| Field | Evidence / value | Limitation and decision consequence |
|---|---|---|
| Series ID and name | `BAA` — Moody's Seasoned Baa Corporate Bond Yield | A yield measure, not a total return or a tradable security price. |
| Source | [FRED series page](https://fred.stlouisfed.org/series/BAA); source shown there is Moody's, in the *Moody's Daily Corporate Bond Yield Averages* release. | FRED redistributes the series; Moody's licensing notes apply. |
| Point-in-time source | [ALFRED BAA vintages](https://alfred.stlouisfed.org/series?seid=BAA) and the [ALFRED release record](https://alfred.stlouisfed.org/release?rid=427). | Use ALFRED, not the current FRED page, for a historical decision. |
| What it measures | The yield on Moody's seasoned Baa corporate bonds. FRED's notes describe the underlying instruments as bonds with maturities of 20 years and above. | The methodology is Moody's-defined; it is not a broad corporate-bond total-return index. |
| Units and seasonal adjustment | Percent; not seasonally adjusted. | Keep values in percentage points; do not divide by 100 unless a downstream calculation explicitly requires decimal form. |
| Frequency | Monthly. | The observation is a monthly measure, so it is inappropriate for daily trading-timing claims. |
| Geography / coverage | Corporate bonds in Moody's seasoned Baa yield series. | The supplied FRED metadata does not make this a complete universe of all U.S. corporate bonds. |
| Download date | 2026-10-29, America/Indiana/Indianapolis. | A current download can change; preserve the as-of vintage query used in analysis. |

## Publication-lag evidence

The ALFRED release record shows the monthly BAA observation period through **September 2026**
and a release date of **2026-10-01**. Thus, the September observation was publicly available by
October 1, not during September. The documentation shown here is date-level, not intraday; a
same-day decision must either use a documented release timestamp or treat the observation as
available on the next decision day.

## Revision evidence

ALFRED preserves vintage versions of BAA, and the ALFRED release page labels the Moody's Daily
Corporate Bond Yield Averages release as having **six series revisions**. This is evidence that
current FRED history may differ from what was available earlier; it does not itself establish the
number of changed BAA observations for every cutoff. For a chosen cutoff, download
`alfredgraph.csv?id=BAA&vintage_date=YYYY-MM-DD` and compare it with current FRED only on
matching observation dates. The app's same-date revision count performs that cutoff-specific
comparison.

## Three manually verified FRED values

These values were checked against the public [FRED BAA CSV](https://fred.stlouisfed.org/graph/fredgraph.csv?id=BAA)
on 2026-10-29.

| Observation date | FRED value (percent) | App value | Match? |
|---|---:|---:|---|
| 2026-07-01 | 6.19 | 6.19 | Yes |
| 2026-08-01 | 6.32 | 6.32 | Yes |
| 2026-09-01 | 6.47 | 6.47 | Yes |

## Point-in-time rule

**Decision/as-of cutoff:** record the intended decision date and time zone before downloading.
Use the ALFRED BAA vintage whose `vintage_date` is that cutoff date. The latest usable BAA value
is the final nonmissing observation in that vintage; do not use a current FRED value merely
because its observation month precedes the cutoff. Count later-dated current observations as late,
and identify revisions only by comparing nonmissing values on the same observation date between
the ALFRED vintage and current FRED download. If the decision occurs on a release date and no
release time is documented, defer availability to the next decision day.

## Partner attack and evidence-based response

**Partner attack:** “BAA is monthly, but its observation date is the first day of the month. How
can we know that a strategy did not use the September value of 6.47 before that value was actually
released?”

**Evidence-based response:** The observation date identifies the month the value measures; it
does not prove the value was available on that date. The ALFRED release record shows the September
2026 BAA value was released on October 1, so a historical test must use the ALFRED vintage
available on its actual decision date rather than today's FRED history. If a decision occurs on
October 1 and the release time is unknown, the conservative rule is to wait until the next decision
day.

## Project 2 admission decision

**Decision: Admit, subject to the point-in-time rule.** BAA has a named primary source, stated
units and monthly frequency, documented release timing for the checked September observation,
and ALFRED vintages that allow a defensible historical information set. It may support a
monthly-rate or credit-condition input, not a daily tradable-return claim.

**Condition that would change the decision:** Quarantine BAA for any decision date for which an
ALFRED vintage cannot be retrieved or release-time ambiguity is material to a same-day trade. A
documented series-definition or unit change not reconciled to the analysis would also require a
new review before use.
