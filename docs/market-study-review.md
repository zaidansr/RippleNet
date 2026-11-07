# Independent review: real recorded-market pilot

**Attribution and findings license:** Data-derived findings use Binance Vision BTCUSDT daily individual-trade archives for 17 August–15 September 2017. [Source](https://data.binance.vision/), [dataset terms](https://github.com/binance/binance-public-data/blob/master/TERMS_AND_CONDITIONS.md). This document's derived findings are distributed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Changes: independently recomputed features, fitted parameters, validation scores, held-out losses and resampling statistics; no raw trades reproduced. No endorsement or relicensing of independently written code is implied.

## Independent checks

Reviewed the frozen plan, source, selection artifact, complete test output and [results report](market-study-results.md). Independently ran the nine market-study fixture tests; all passed. Actual market archives were read for reproduction only after the frozen protected evaluation finished. No new settings, model, date selection or post-hoc target was introduced.

All 30 ZIP and uncompressed CSV hashes match the stored coverage provenance and publisher sidecars. Counts reproduce: 47,140 common training origins, 21,815 validation origins and 94,903 test origins. Each day has N-15 evaluated origins under the fixed five-return warm-up and ten-row target boundary. Excluded origins are coverage counts, not stored individual forecasts.

Reconstructed features independently using sliding return windows and rebuilt targets directly from recorded prices. An independent weighted least-squares calculation with an augmented intercept reproduces training-only centering, scales and the selected coefficients. Recomputed the seven already-frozen validation settings and all baseline scores: alpha zero and the training-mean constant are the recorded winners. This is reproduction of existing choices, not retuning. Independently recomputed all 15 days × four predictors × two loss metrics; maximum absolute discrepancy is 1.39e-17.

Verified matching development/test source hashes, current source-file hashes and the exact selection SHA256 pinned by the test output. Source inspection and mocked tests confirm that development opens only the first 15 dates, test does not refit, and a changed source is rejected before test loading. The published chronology records source freeze and selection publication before protected-price inspection; code alone cannot prove absence of every possible external inspection.

## Effect and statistical interpretation

The equal-day candidate MSE is **1.849150626e-5**, versus **2.009437811e-5** for the selected constant. The absolute reduction is **1.602871850e-6**, corresponding to **7.97672%**. The zero-return comparison gives **7.97447%**. The candidate beats the constant on daily MSE on 14 of 15 days. These are closely related baseline comparisons, not independent confirmations.

Independently reproduced all equal-day and pooled-origin summaries and the complete paired bootstrap output. The procedure uses 9,999 identical day-index draws for both contrasts, fixed seed 190011, and five noncircular three-day blocks per replicate. Adjusted 97.5% percentile intervals reproduce as **[4.12416%, 12.20026%]** versus constant and **[4.11958%, 12.19941%]** versus zero.

These intervals exclude zero under the frozen resampling procedure, but do not establish guaranteed coverage or broad statistical reliability. Only 15 adjacent days and about five three-day blocks inform inference. Noncircular resampling underweights endpoint days; together with ratio nonlinearity, this shifts the bootstrap distribution's mean. The constant-relative bootstrap mean exceeds the observed estimate by **0.20599 percentage point**. No interval recentering, block tuning or alternative inferential procedure was substituted after observing this result.

MAE is **0.94684% worse** than the constant and **1.03012% worse** than zero. Thus the supported result is an MSE-specific benefit, not uniform forecast improvement. No purpose-specific practical margin or economic-value calculation exists, so the former synthetic 5% threshold is inapplicable.

## Claims the evidence does not support

- The protected later-period comparison supplies limited temporal holdout evidence within retrieved records from one asset's early listing period. It does not establish cross-period, current-market or cross-asset generalisation.
- Current archive order and chronology-aware fitting do not prove original 2017 publication/receipt availability or absence of later revisions.
- This study contains no independently adjudicated correction/shock outcomes and no mechanism-specific ablation. Negative lag coefficients or improved MSE do not identify recording errors, genuine shocks or a RippleNet mechanism.
- Predicting a recorded trade-price return does not establish efficient-price drift, executable fills, net trading profit or novelty. The winning predictor is ordinary weighted AR(5), not a trained neural RippleNet.

## Most discriminating next experiment

Use a fresh, predeclared period to compare the original origin-start return with a delayed-start target `log(P[k+11])-log(P[k+1])`, keeping inputs fixed at origin k and using matched eligible origins. This tests whether predictability persists after excluding the origin price from the target. Shared origin-price reversal, including possible bid/ask bounce, is a competing explanation; it is legitimate predictability of the current target rather than mathematical leakage.

Specify target-specific training-only fits and strong baselines, or explicitly name a fixed-model transfer test; otherwise target mismatch could be confused with absent information. Freeze all choices before the new period. A change in result would not uniquely prove bid/ask bounce or create latent-price/error labels. The present held-out period is now disclosed and cannot provide another independent confirmation.

The results report is consistent with this bounded conclusion. No material computational defect was found, and the observed-return MSE finding is reproducible; the practical, mechanism and broad-generalisation claims remain unestablished.
