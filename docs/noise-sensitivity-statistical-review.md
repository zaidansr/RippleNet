# Independent statistical audit: fixed R-only sensitivity

This audit independently recomputes saved-data statistics. No simulations, model runs, tuning or cell selection were performed.

## Data and aggregation checks

The five cells have precisely the declared ratios `[0, .25, 1, 4, 16]`, measurement covariances `.01 * ratio * I`, and seeds 70000–70127. Each CSV has 1,280 unique `(seed, category, delay)` triples covering both worlds and delays 0–4. All 6,400 rows are present, but there are only 128 independent paired seed blocks; neither worlds, origins nor cells increase that sample size.

Independently reproduced all eleven saved mean scores at each origin, all eleven delayed-window means and descriptive intervals, the three principal ratio-of-means quantities, the current-state information ceiling, and all their intervals. Delayed aggregation averages origins 1–4 within each world and both worlds within each seed. It does not average individual seed ratios.

One index matrix generated with seed 789012 resamples complete seed blocks 9,999 times and is reused across all cells. Recomputed raw 95% percentile intervals and five-cell Bonferroni 99% individual intervals exactly reproduce the summary within floating-point tolerance. The primary intervals use quantiles .005 and .995. These are approximate exploratory intervals; the family adjustment does not establish an optimal cell or validate unlisted comparisons.

Verified finite scores, all risk decomposition identities, constant per-asset future floor .01, normalized log probabilities, event-time probabilities .5, and coincidence of retained/projected event-time losses. Current source-file hashes match the executed manifest. Source inspection confirms explicit checks for common latent paths, intervention time/amplitude and standardized measurement streams across cells. The saved risk rows alone do not contain the latent paths needed to independently reconstruct those coupling checks; the manifest reports them and their residuals.

## Complete sensitivity table

Conditional risks and gains average the declared delayed origins. Gain intervals are the five-cell-adjusted 99% individual intervals, expressed as percentages.

| R/Q | Bayes risk | Projected risk | Retention gain | Adjusted interval | Future-noise share of Bayes risk |
| ---: | ---: | ---: | ---: | --- | ---: |
| 0 | 0.01000000 | 0.01000000 | numerical zero | numerical zero | 100.000% |
| .25 | 0.01044211 | 0.01044438 | 0.02170% | [0.01605%, 0.02834%] | 95.766% |
| 1 | 0.01119863 | 0.01121114 | 0.11160% | [0.07559%, 0.15283%] | 89.297% |
| 4 | 0.01237453 | 0.01239117 | 0.13424% | [0.07297%, 0.22736%] | 80.811% |
| 16 | 0.01360488 | 0.01361555 | 0.07836% | [0.04077%, 0.13479%] | 73.503% |

The largest observed point estimate occurs at R/Q=4; that observation is not an inference that it is optimal or that it outperforms adjacent cells. The entire grid must remain visible. Every reported upper band is below 0.23%, far below the 5% practical target.

## Zero-R control and numerical precision

With R=0, Q keeps innovation covariance positive definite. After the first post-event observation reveals the current state exactly, all forecasting representations agree to numerical precision and conditional Bayes risk is .01. Saved delayed state-risk terms are below 5.4e-33; the largest point-forecast discrepancy reported by the runner is 1.25e-16.

The raw retention fraction is approximately 1.22e-32, with a formally positive bootstrap interval. This is squared floating-point disagreement, not evidence of a positive scientific effect. It must be described as numerical zero. Realized MSE remains random and need not equal .01; its retained/projected difference is likewise numerical noise.

## Scientific interpretation

At positive R, the exact conditional mean is population-MSE optimal by construction. Positive squared disagreement with projection and intervals excluding zero are therefore not discoveries of theoretical superiority. Their sizes quantify the approximation cost under the stipulated generator, which remains practically small throughout this grid.

Larger relative gains at some higher-noise cells do not mean forecasting improved: both Bayes and projected absolute risks increase with R in these results. At R/Q=16, future noise contributes a smaller fraction of risk, yet retention remains below 0.08%. Thus future-noise dilution alone does not explain the lack of substantial representation benefit in the tested cells. The Gaussian projection's point means remain close to exact inference.

Actual-MSE relative improvements, computed from paired seed means, are secondary: approximately 0.0604%, 0.2350%, 0.3553% and 0.2228% at positive ratios. They are different, noisier estimates than conditional-risk gains; they should not replace the primary estimand or be selected to strengthen a conclusion.

The fixed-grid result supports a limited negative conclusion: this representation change does not approach the declared 5% next-return target across the five tested measurement-noise regimes. It neither rules out benefits under other dynamics, horizons or mechanisms nor establishes operational detection, market generalisation, economic value or novelty. Selecting a new model or regime from this sensitivity requires fresh development and final evaluation.
