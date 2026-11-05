# Interpreting the exploratory v2 conditional-risk diagnostic

The reconstructed conditional risks show very little delayed forecasting headroom for the retained exact mixture over the once-projected Gaussian. The near-zero realised v2 difference is therefore not adequately explained as a useful improvement hidden by random future returns. Under the declared model, the conditional means themselves are already close once distinguishing evidence arrives.

This conclusion is restricted to the average over the disclosed v2 histories, their known parameters and shared intervention-time information. It does not reject all history-retaining models, all disturbance-identification problems or other observation regimes.

## What was analysed

The [saved diagnostic summary](../results/conditional-risk-v2/summary.json) reconstructs missing posterior moments on the existing 128 seed blocks. It records bitwise agreement with frozen forecast and type-probability paths and zero discrepancy in the recovered original metrics. No independent observations were acquired. These are post-hoc, model-conditional calculations; their descriptive intervals do not provide a new confirmatory test or replace v2's original decisions.

For origins one through four after the event, averaged across the two paired worlds and assets, the decomposition is:

| Quantity | Conditional risk per asset |
| --- | ---: |
| Independent future innovation | 0.0100000000 |
| Within-category state uncertainty | 0.0004394332 |
| Remaining category-information headroom | 0.0000030160 |
| Retained exact Bayes risk | 0.0104424492 |
| Projection excess over retained | 0.0000037235 |
| Frozen-weight excess over retained | 0.0000239082 |
| Projected total risk | 0.0104461727 |

The [mathematical derivation](conditional-risk-mathematics.md) integrates latent-state uncertainty and future process noise conditional on each recorded history. It uses posterior category probabilities. The category-oracle risk in this calculation is posterior-averaged, not the realised loss or conditional risk of a particular true-category row.

## Headroom versus realised noise

Independent future innovations account for **95.763%** of retained conditional risk. That alone would not establish that two forecasts are similar; the squared difference between their conditional means supplies the relevant additional evidence.

The conditional relative reduction from replacing projection with the retained exact mean is **0.035644%**, with a descriptive paired-bootstrap interval of approximately **[0.025615%, 0.047561%]**. This is well below the 5% practical target. It is a small positive model-conditional effect, whereas the realised v2 estimate was approximately zero and slightly favoured projection. Those findings are compatible: realised losses contain random cross terms that the conditional calculation integrates out.

Retention improves conditional risk over frozen weights by **0.228429%**, descriptively **[0.185740%, 0.276130%]**. Evidence-responsive reweighting changes the forecast, but its useful magnitude remains small here. Relative to retained risk, revealing the true category would remove only **0.028882%** at the delayed origins, descriptively **[0.023085%, 0.035118%]**. Better type scores therefore do not imply substantial remaining next-return value.

These intervals are exploratory, unadjusted descriptive intervals for reused histories. Positive squared-distance excess is also guaranteed by the assumed exact conditional mean; an interval above zero does not discover a new optimality theorem. All these percentages use ratios of averaged risks, not averages of individual history ratios.

## Timing explains the apparently conflicting evidence

| Forecast-origin delay | Retained conditional risk | Category-information headroom | Projection excess |
| --- | ---: | ---: | ---: |
| Event origin, 0 | 0.0249657619 | 0.0136037640 | 0 |
| 1 | 0.0104567636 | 0.0000119443 | 0.0000147428 |
| 2 | 0.0104378049 | 0.0000001183 | 0.0000001494 |
| 3 | 0.0104376151 | 0.0000000013 | 0.0000000016 |
| 4 | 0.0104376131 | approximately 0 | approximately 0 |

At the event instant, knowing the category could reduce retained conditional risk by approximately **54.5%** on these histories. Ordinary methods cannot obtain that benefit from the matched prefixes: the two category likelihoods are equal, and retained, projected and frozen forecasts must coincide.

Once the next observation arrives, the category can become informative, but current-state re-observation has already removed most of its forecasting relevance. At delay one, category headroom is approximately **0.114%** of retained conditional risk; at delay two it is approximately **0.00113%**. Projection excess also collapses rapidly.

The proper interpretation is a timing limitation in this model: historical-cause information becomes available after most of its next-return value has disappeared. The projected Gaussian captures nearly the same useful future mean without carrying an explicit category posterior. It does not follow that projection recovers event labels or reproduces the exact posterior distribution.

## A stronger feasibility warning for the 5% gate

For every allowed origin, future state innovation is independent of all current-state information. Even a hypothetical forecaster that additionally knows the current latent state perfectly, but cannot see future innovation, retains conditional risk

\[
\operatorname{tr}(Q)/n=0.01.
\]

Against mean projected conditional risk 0.0104461727 on the disclosed delayed histories, this privileged lower floor permits at most

\[
1-\frac{0.01}{0.0104461727}\approx4.27\%
\]

improvement. A 5% reduction would require risk below that future-innovation floor. The tighter bound for the actual shared-information task is the retained exact Bayes mean, which improves projection by only 0.035644% on this average.

This is a bound on **conditional expected risks averaged over these conditioning histories**. It is not a bound on every realised test loss, every possible history, the population average in a different regime or performance with information about future innovations. It is not a fresh confirmatory result. It does show that the frozen delayed-origin task and practical gate are badly mismatched in this reconstructed setting; more architecture cannot repair that information constraint.

The zero-transition control is consistent with the decomposition: future risk is 0.01, and within-category, type-information and forecast-excess terms are zero.

## Next decision and most efficient experiment

Stop architecture development for the frozen v2 setting. Adding more seeds could refine the small effect estimate, but would not create missing conditional forecasting headroom. Keep v1 and v2 numerical results, practical failures and reported limitations unchanged.

If continuing the research question, the next efficient experiment is a **prespecified observation-quality sensitivity diagnostic**, using the existing exact and projected methods. Change only the measurement covariance over a small, externally justified range; keep transition dynamics, process covariance, event-amplitude law and causal timing fixed. Use new seed blocks and conditional risk by delay as the primary diagnostic. This directly tests whether rapid re-observation of the current state explains the vanishing value of retained disturbance history, while avoiding a simultaneous architecture change.

Declare the settings and useful-headroom threshold before evaluation. Report every setting. A positive result only under arbitrarily severe recording noise would demonstrate a conditional simulator regime, not justify a financial model. If no defensible target observation regime offers sufficient headroom, stop this forecasting branch rather than enlarging the model.

Exploiting the large event-origin oracle headroom is a different information problem: it would require genuinely available contemporaneous evidence that distinguishes a bad recording from a state shock. Future observations cannot be moved backwards into that forecast. Any proposal using such additional evidence must identify its source and test it as a separately declared task.

No new data or model runs were performed in writing this interpretation, and no spending was incurred.
