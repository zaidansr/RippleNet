# Independent review: trade-versus-midpoint pilot

**Source and publication scope:** These non-reconstructive aggregate findings use [Tardis Kraken spot data](https://docs.tardis.dev/historical-data-details/kraken), under [Tardis terms](https://docs.tardis.dev/legal/terms-of-service). Raw observations, fitted parameters, preprocessing and model-bearing selections remain private. This report grants no open-data or Creative Commons license. No additional dates, models, targets or settings were selected during review.

## Reproduction and leakage audit

Reviewed the implementation before development-price parsing, identified missing expanded-byte enforcement, and verified its correction. Independently ran all ten synthetic fixtures successfully. The [frozen plan](quote-study-plan.md), [source provenance](quote-study-provenance.md) and [published selection commitment](quote-study-selection-commitment.md) document the chronological separation. Verified local executable/plan hashes against private selection and test artifacts, the committed selection-artifact hash, acquisition-manifest hash and final test-artifact hash. The remote source commits were not independently refetched in this review.

After authorized test execution, independently reread all 24 files. Compressed SHA256/MD5, expanded hashes/sizes, gzip integrity, headers, identities, collector ordering and recorded diagnostics match. A separate sliding-window construction reproduces all twelve sessions' strict-before snapshots, six-snapshot histories, shared twelve inputs, future labels, issued-origin masks and paired scoring coverage.

Independently reconstructed equal-session training weights, training-only scaling, target means and weighted medians; reproduced all fourteen frozen validation fits, their scores and selections without proposing replacements. All five predictors' MSE/MAE on every test session, equal-session and pooled summaries, gains and the absolute contrast reproduce. Maximum absolute numerical discrepancy across checked quantities was 8.88e-16. No material functional discrepancy was found.

## What the results support

The flexible model's trade MSE improves **10.11% against zero**, but is **0.0606% worse than the frozen mechanical gap baseline**. Their equal-session MSEs are 1.32494e-7 and 1.32414e-7 squared log-return units, respectively. Consequently, the aggregate trade result does not demonstrate improvement beyond a known starting-price correction. Trade MAE is also **3.23% worse** than that reference.

Midpoint MSE improves **0.7606%** against its validation-selected constant reference, while midpoint MAE worsens **1.08%**. This small MSE difference has no established practical economic meaning. Relative MSE gains vary by session: trade **−1.98%, +2.39%, +5.26%** and midpoint **−0.53%, +2.24%, +4.31%** for March, April and May. The primary ratio uses equal-session mean risks; it is not an average of these daily percentages.

The absolute difference between targets' zero-relative improvements is 1.38162e-8 squared log-return units. Different targets and separately selected models prevent interpreting this as a causal mechanism estimate.

## Limits that constrain the conclusion

Only **64,409 of 259,200** test clocks issue forecasts; **45,958** have both observed future targets. Thus losses cover **17.73% of all grid clocks**, or **71.35% of issued origins**. Explicit censoring avoids future-dependent issuance, but reported performance remains conditional on substantial retrospective target availability. It does not estimate full-day operational performance.

Three convenience-sampled monthly test sessions do not establish statistical reliability or broad generalization. No confidence interval, significance or profit claim is warranted. Overlapping horizons, unchanged references, freshness selection, collector-clock assumptions and the training-period infrastructure change remain competing explanations. The mechanical baseline is an informative control, not an error/shock ablation; midpoint prices are not efficient-price truth. These results justify neither a RippleNet architecture claim nor observation-error versus genuine-shock identification.
