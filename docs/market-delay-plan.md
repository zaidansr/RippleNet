# Frozen fresh-period delayed-start market control

The owner instructed continuation after the first real recorded-market study. This next study tests whether its recorded-return predictability persists when the target excludes the origin trade price. It is a new period, not a rescore of the disclosed test set, and does not establish original as-of history or economic profitability.

## Data and protected split

Fix all 30 consecutive BTCUSDT UTC dates from 2017-09-16 through 2017-10-15 before inspecting their trade bodies. Train September 16–25; validate September 26–30; protect October 1–15 for final evaluation. None overlaps the preceding 30-day study. Acquire official daily individual-trade archives and matching publisher SHA256 sidecars under the previously audited noncommercial data terms. Recheck current terms, retain attribution and CC BY-NC-SA 4.0 notices for derived findings. Raw data stays outside GitHub.

Keep fixed caps of 2 MiB compressed and 20 MiB expanded per day and 60 MiB compressed overall. Missing/integrity/schema failures or a bound violation stop this design; do not replace dates, widen bounds or choose another asset after outcomes. No account, provider contact or paid service is needed; any spending requires explicit owner approval.

## Paired targets, features and coverage

At retrieved trade row k, features are the same five latest adjacent log returns ending at k as before. Define origin-start A=log(P[k+10])-log(P[k]) and delayed-start B=log(P[k+11])-log(P[k+1]). The price at k+1 is future label information only and never a predictor input or forecast anchor.

Evaluate both targets on exactly the same origins: k=5,...,N-12 inclusive, giving max(N-16,0) per valid day. No cross-day features or outcomes. Count five feature-unavailable origins, ten A-target-censored origins, eleven B-target-censored origins, and A's one additional complete origin excluded solely for alignment. A day with no eligible origins stops the fixed design. Preserve counts rather than fabricating outcomes; raw rows remain private.

Both targets span ten retrieved trade intervals and share nine increments, but B removes the first and adds a new last increment. Therefore different target distributions, noise, conditional dependence and model suitability can change their scores. This is not a pure removal of measurement noise or proof of bid/ask bounce.

## Frozen fitting and selection

For each target separately, use the original AR(5) ridge grid [0,.001,.01,.1,1,10,100], unpenalised intercept and train-only population feature scaling/target mean. Each of the ten training days has equal total weight. Alpha zero uses weighted least squares. Use fixed zero, target-specific training-mean constant, and ten times the mean of the five input returns as baselines. Validation equal-day MSE independently chooses each target's alpha and strongest baseline. Exact ties follow listed order. Do not refit after validation or alter features, settings or targets after results.

Publish executable source before opening development prices, then publish both selected pipelines before protected October prices are parsed. This target-specific fitting avoids interpreting a model trained on the wrong label as an information test. It also means a gain difference compares separately selected pipelines rather than an isolated coefficient ablation.

## Primary estimands and fixed inference

Use equal-day averages of within-day eligible-origin MSE as primary risks; report daily losses, pooled-origin MSE and MAE secondarily. Let G_A=1-MSE(candidate A)/MSE(validation-selected baseline A), and similarly G_B. The first two primary contrasts are G_A and G_B. For each target define D=MSE(zero)-MSE(candidate); the third primary contrast is D_A-D_B, a paired change in absolute zero-relative forecasting improvement, in squared-log-return units. The common zero reference avoids switching baseline identities and ratio denominators in this contrast. It still compares different labels and separately selected pipelines, not a causal origin-price effect. Save every denominator and risk. Report G_A-G_B descriptively as a normalized task contrast with different reference risks; do not use it as the primary attenuation test.

Use 9,999 paired noncircular three-consecutive-day moving-block bootstrap draws on the same 15 test-day vectors. Starts are 0,...,12; draw five blocks per replicate; seed 190012. The same day indices must determine every arm and contrast. Report ordinary 95% intervals and Bonferroni-adjusted 98.333333% percentile intervals (tails .05/(2*3) and 1-.05/(2*3)), for family size three. No post-hoc block tuning, extra periods, extra primary contrasts or interval recentering.

These intervals are exploratory dependence-assumption diagnostics. Fifteen adjacent days yield few blocks; noncircular blocks underweight endpoints and can shift the bootstrap center. Report that shift. They do not guarantee familywise coverage or generalisation to other markets/regimes. No purpose-specific economic improvement margin is established, and the former synthetic 5% target is not reused.

## Interpretation, artifacts and constraints

An A gain with little B gain would be consistent with predictability concentrated near the first future trade, including origin-price reversal, but not uniquely identify its cause. Persisting B skill would weaken an explanation based only on shared origin-price noise, without proving efficient-price drift or trading profit. Failure of both pipelines to improve would limit fresh-period transfer of the original result. Wide or crossing intervals remain inconclusive; do not turn nonsignificance into evidence of no effect.

Save all acquisition hashes, split dates, coverage, target-specific training-only coefficients/scales, validation choices, daily losses, paired contrasts, runtime and executable provenance. Refuse to overwrite existing outputs. Mark all data-derived findings with source attribution, changes and the applicable license. Existing results/code remain unchanged; this pilot adds a new module and output directory. Use existing local NumPy/standard-library tooling only and publish all findings, including negative results or bounded acquisition failures.
