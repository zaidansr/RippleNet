# Observation-noise sensitivity: post-run engineering audit

## Finding and scope

No scientifically material implementation, indexing, provenance, or reporting defect was found in the reviewed artifacts. The audit inspected frozen source, saved CSVs, metadata and report/plot code. It independently recomputed summary quantities and bootstrap intervals from saved rows. It did not regenerate any reserved seed, alter a model, or change recorded experimental results.

The scope remains a correctly specified, known-intervention-time synthetic sensitivity study. The assessment does not establish unknown-time event detection, market calibration, transfer to financial data, or methodological novelty.

## Published source and runtime

The GitHub Git-commit API was independently read for public commit [01c1a0f3d2612b502de071eef6baaa48dd39dd2a](https://github.com/zaidansr/RippleNet/commit/01c1a0f3d2612b502de071eef6baaa48dd39dd2a). Its tree is `ea5b46d35b004153384ef6044878528d8c6a6bb0`, exactly the tree recorded by the experiment. The local commit identity is correctly labeled separately; a different commit hash with an identical tree does not indicate different source content.

All five recorded actual-file SHA256 hashes match the inspected runner, filter, risk helper, benchmark and simulator files. The relevant runner/model/report source files have no diff from the declared execution tree. The manifest records an empty working-tree status before output creation. Generated result/report files appearing afterward are expected and do not invalidate that clean pre-run status.

The experiment records Python 3.13.3 and NumPy 2.3.2. The figure provenance separately records Matplotlib 3.11.2 and plotting NumPy 2.5.4. The report/plot module imports no simulator or model module, and its plot provenance states no simulator rerun. The figure's canonical input-summary SHA256 matches the saved summary. Source inspection and these records support the intended separation of model execution and plotting environments; they are not a reconstruction of every historical process action.

## Grid, counts and paired structure

The five declared variance ratios are exactly `[0, .25, 1, 4, 16]`. Each cell contains 1,280 unique seed/category/delay rows: 128 seeds, two coupled event worlds and five origins. All expected combinations from seeds 70000 through 70127 are present once, for 6,400 rows in total. This remains 128 independent seed blocks, not 6,400 independent replications or 640 independent cell/seed experiments.

Only ordinary measurement covariance changes. The transition matrix, Q=.01 I, intervention variance, timing rule, lengths, burn-in and inference privileges are fixed. Code inspection verifies that coupling checks compare latent paths and event metadata across R before scoring, and compare standardized measurement-noise paths across positive-R cells. The saved run reports exact latent/event coupling; the largest standardized-noise discrepancy is 1.33e-15, consistent with subtraction/division roundoff. Full latent paths and standardized streams are not stored in the result CSVs, so this audit validates those checks through source inspection and their saved residuals rather than another simulation replay.

## Causal, covariance and control checks

- Forecast row t targets latent x[t+1]. The main summary uses forecast origins tau+1 through tau+4; event-origin tau is saved separately. The corresponding latent targets are tau+2 through tau+5.
- The largest matched-observation-prefix ordinary-forecast difference is 1.11e-16. Ordinary arms agree exactly at the event origin, and initial type probability is exactly one half. Later probabilities use only then-arrived observations.
- Raw normalized log probabilities exponentiate to weights summing to one within tolerance; the stored state probability agrees with the exponentiated state log weight.
- Bayes risk equals future innovation plus within-type plus type-information risk. Projected/frozen total risk equals Bayes plus the corresponding excess. Posterior-averaged category-oracle risk equals future plus within-type risk; it never selects the realized category for this conditional expectation.
- Every saved risk/score is finite and nonnegative within tolerance. The largest independently recomputed decomposition residual is 1.39e-17.
- At R=0, every delayed Bayes risk is exactly .01. The largest projected excess is 5.31e-33 and largest realized retained/projected per-origin MSE difference is 1.73e-17. Those differences are floating-point effects, not evidence against the perfect-observation control. Historical event-type probabilities are allowed to change. Realized MSE is not asserted equal to .01.

The tiny positive R=0 retention interval is numerical roundoff and must not be interpreted as statistical or practical benefit. The report rounds this cell to zero and correctly explains its control meaning.

## Independent numerical reconciliation

All saved per-origin means, delayed within-seed balanced means, ratios of means, descriptive 95% intervals and primary five-cell-adjusted 99% intervals were recomputed from the raw CSVs using the declared paired seed resampling. Maximum disagreement with the saved summary was zero for these checks in the recorded NumPy environment.

The bootstrap uses the same seed-index draws across cells. Worlds and origins are aggregated within a seed before resampling. The primary adjustment uses five contrasts; the other intervals are labeled descriptive. Percentile-bootstrap coverage remains approximate. Nonnegative conditional excess follows from squared-distance algebra under the stipulated model; its interval is not a new empirical test of Bayes optimality or novelty.

## Report and plot semantics

The saved Markdown report exactly matches the renderer applied to the saved summary. It reports every declared cell, absolute Bayes/projection risks, primary headroom and intervals, category-oracle headroom, the future-noise fraction, the perfect-current-state ceiling, and realized losses. No favorable cell is presented as a tuned or market-calibrated optimum.

The figure generator uses all five categorical positions. Percentage conversion is consistent with the summary's fractional units. It draws both pointwise and five-cell intervals with the declared 5% reference, alongside absolute risk on a separate panel. It reads saved summary values and does not execute filtering. The table is needed to inspect the small nonzero effects compressed below the 5% reference line.

The distinct headroom denominators should be retained when communicating results: retention gain divides projected excess by projected total risk; category-oracle headroom divides type-information risk by retained Bayes risk; perfect-current-state ceiling is one minus the future-noise floor divided by projected total risk. These are different information comparisons.

Across the declared grid the retained-versus-projection effect remains far below the practical 5% reference; no adjusted interval establishes that target. Raising R also raises absolute conditional prediction risk. The result therefore does not justify inflating assumed measurement noise to manufacture a useful financial forecasting contribution. A changed model, detector, or externally motivated observation setting requires a separate declared evaluation after these seeds have been disclosed.
