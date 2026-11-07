# Frozen real recorded-market forecasting pilot

The owner explicitly requested real market data. This study changes the target to prices recorded in a retrieved historical Binance spot individual-trades archive. It does not validate original 2017 receiver availability, efficient prices, an error/shock mechanism, trading profit or a current-market predictor. No synthetic outcome is used as market evidence.

## Fixed acquisition and split

Select BTCUSDT for every UTC date from 2017-08-17 through 2017-09-15 inclusive, before inspecting additional prices or outcomes. The previously inspected first day is training only. Use the official daily individual-trades ZIPs and SHA256 sidecars under `data.binance.vision/data/spot/daily/trades/BTCUSDT/`.

Fit: August 17–26 (10 days). Validation: August 27–31 (5 days). Protected test: September 1–15 (15 days). This early listing period was chosen as a small bounded extension of the already audited source, not as a representative sample of all markets. No date or instrument substitution, price-based exclusion or automatic bound expansion is allowed. Missing files, integrity/schema failures or size-cap failures stop this fixed design and must be reported.

Bounds: 2 MiB compressed and 20 MiB expanded per day, 60 MiB compressed total. Recheck the current dataset-specific terms before acquisition. This is noncommercial research; derived data findings retain Binance Vision attribution and the applicable CC BY-NC-SA 4.0 notice. Keep all raw archives, rows and source snapshots outside the public repository. No purchase, account, provider contact or paid computation is needed; any spending requires explicit owner approval.

## Target, information and coverage

Use the strict existing importer, explicit millisecond units and UTC date identity. Preserve file order, ties and IDs; do not sort, clean, impute or manufacture correction labels. Each day is a separate sequence.

For price P_k at retrieved row k, target Y_k=log(P_{k+10})-log(P_k). Features are the five most recent adjacent trade log returns r_k through r_{k-4}, where r_k=log(P_k)-log(P_{k-1}). All are present by the origin under retrieved-file order. No cross-day features or targets. The first five origins lack full features; the final ten lack complete future targets. Retain and disclose those statuses separately, including their overlap on a short day. Evaluate every common eligible origin, without outcome-based filtering. For N valid rows, common eligible count is max(N-15,0).

This is a ten-retrieved-trade horizon, not ten seconds, ten complete-market events or executable latency. Archive revisions and historical availability remain unverified. The source has no correction ledger or genuine-shock labels.

## Frozen predictors and selection

Baselines: zero return; a constant equal to the training target mean; ten times the mean of the five available adjacent returns. The last baseline has the target's ten-row scale. Fit an AR(5) ridge predictor using those five returns and an unpenalised intercept, with alpha in [0,.001,.01,.1,1,10,100]. Alpha zero is unregularised least squares, using a pseudoinverse if necessary. Do not add features or architectures after outcomes.

Each training day receives equal total fitting weight, distributed equally across its eligible origins. Compute feature means/scales, target mean, intercept and coefficients from training only. Use population weighted standard deviations; assign unit scale to a zero-variance feature. Ridge minimizes weighted mean squared error plus alpha times squared standardized coefficients. No normalisation, clipping or fitted preprocessing uses validation or test rows.

Select alpha by minimum equal-day validation MSE; break exact ties in the stated alpha order. Separately select the strongest baseline by validation MSE, breaking ties in listed baseline order. Freeze both choices before any test losses are evaluated. Do not refit using validation. Target labels crossing a day boundary never enter a fit.

## Estimands and uncertainty

Primary risk is the equal-day average of within-day eligible-origin MSE, giving a retrieved day rather than a trade-volume-weighted day equal importance. Report per-day losses and pooled-origin losses separately, and MAE as secondary. Compare the frozen AR candidate with zero and with the validation-selected baseline; both comparisons use identical origins. Report absolute loss differences and ratio-of-mean-risk reductions, not averages of individual percentage errors.

For exploratory uncertainty, use 9,999 paired moving-block bootstrap resamples of the 15 test-day loss vectors, with noncircular three-consecutive-day blocks, drawing five blocks per replicate. Fix seed 190011. Use the same resampled days for all predictors and contrasts. Report ordinary 95% and Bonferroni-adjusted 97.5% percentile intervals for each of the two primary contrasts (family size two, even if the selected baseline is zero). These are approximate dependence-assumption diagnostics, not exact coverage guarantees: only 15 days and roughly five blocks provide weak evidence about broader regimes. No rows, overlapping targets or correlated methods are independent replications.

No market-specific minimum useful effect or trading-cost model is established. Do not import the old synthetic 5% margin, equate statistical/nonzero improvement with economic utility, or claim cross-market generalisation. Results may support only a narrow held-out comparison in this retrieved early-period window.

## Execution and disclosure

Publish this plan before additional trade bodies are inspected. Publish executable fitting/evaluation source before opening protected test outcomes. Data may be downloaded and integrity-checked beforehand without evaluating protected prices/targets; keep protected test bodies unread by the modeller until source freeze. Save acquisition hashes, split dates, training-only fitted parameters, validation choices, all test-day losses, coverage, intervals, versions and source hashes. Refuse to overwrite prior experiment output.

Use existing local NumPy and standard-library tooling. Publish a null result or a bounded acquisition/validation failure without replacing dates, increasing sample size or altering parameters after observing results. Existing synthetic findings remain unchanged.
