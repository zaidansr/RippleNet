# Independent audit plan: fixed R-only headroom sensitivity

## Scope and frozen choices

Evaluate all five predeclared ratios `R/Q = [0, .25, 1, 4, 16]`, with `Q=.01 I` and therefore `R=[0, .0025, .01, .04, .16] I`. Keep moderate A, three assets, 128 burn-in steps, 180 retained observations, one Gaussian intervention with covariance `.25 I`, balanced categories and the existing event-time distribution unchanged. All arms receive the same stipulated timing and parameter knowledge.

Use exactly the 128 new seeds 70000–70127, shared across every cell and both counterfactual worlds. There is no training, fitting, tuning, sample extension or selected-cell confirmation. This is a complete exploratory sensitivity table, not an optimisation of noise or a test of market usefulness.

Before computing these seeds, commit the protocol, model, instrumentation, aggregation and plotting settings. Save the executed source-tree hash, versions and complete matrices; refuse to overwrite either original v2 or prior sensitivity artifacts. A post-run bug correction must be disclosed and cannot silently replace its provenance.

## Pairing and information checks

For a given seed, verify identical intervention time, amplitude and latent process across R cells. Reuse the same underlying ordinary process and measurement-normal streams; only measurement-noise scaling changes. At zero R, ordinary measurement error is zero, but observation-category intervention error remains present at the event.

Labels, amplitudes and latent states remain outside the forecaster; they are available only to simulation and scoring. Retain every seed and cell. Save one row for each `(R/Q, seed, category, delay)` for delays 0–4: 1,280 rows per cell and 6,400 overall. These rows contain only 128 independent seed blocks, not independent category, origin or cell replications.

At the matched event origin, ordinary forecasts must agree across paired worlds. Record maximum discrepancy and applicable causality checks. Log the future floor, within-type state uncertainty, between-type information, Bayes conditional risk, projection excess and total risk, posterior-weighted category-oracle risk, and realized forecast loss.

## Zero-R validity and negative control

R being singular does not make the innovation covariance singular: `S=A P A' + Q + R` is positive definite because Q is positive definite. Do not add undocumented jitter or substitute a positive R.

At the first subsequent observation, `y[tau+1]=x[tau+1]` exactly. Each conditional branch and the independently projected filter then has the same current state and point forecast; all posterior state uncertainty relevant to the next forecast vanishes. Consequently, at delayed origins 1–4, within-type risk, type-information risk and projection excess are zero, and conditional Bayes risk is `.01` per asset. Event-type posterior probabilities may still be informative; that does not supply additional next-return value once the current state is observed exactly. Realized MSE remains a random sample and need not equal `.01`.

## Aggregation, ratios and inference

Preserve the existing delayed endpoint: average squared error over assets and origins tau+1,...,tau+4 within a world, then weight both worlds equally within each seed. Save delay zero and the original five-origin window separately. Do not choose a favorable delay after inspection.

The primary sensitivity quantity in each cell is the ratio of aggregate means `mean(projection_excess)/mean(projected_total)`. Also report absolute risks and excess, future-noise share `mean(future)/mean(bayes)`, and category-information fraction `mean(type_information)/mean(bayes)`. Verify rowwise Bayes decomposition, projection-total identity and `category_oracle=future+within_type`. The category oracle is posterior-weighted at the same observation history, not a realized-category samplewise bound.

Report the perfect-current-state information cap `1-.01/mean(projected_total)` as a model-conditional bound for the sampled histories. It must dominate the same-information retention gain. Do not compare noise-subtracted ratios with the original 5% total-MSE target; zero denominators stay undefined.

For descriptive uncertainty, fix 9,999 bootstrap replicates and a seed such as 789012 before execution. Resample the 128 complete paired seed blocks using exactly the same indices across all five cells. Report raw 95% pointwise intervals. If reporting five-cell simultaneous retention-gain bands, use Bonferroni per-cell alpha `.05/5`, yielding 99% individual percentile intervals, and label their coverage approximate. Other risk fractions remain descriptive; adding them does not turn this into a confirmatory family.

## Invalid conclusions to prevent

A larger relative retention gain at higher R can reflect a worse projection denominator, not better absolute prediction. Show absolute Bayes and projected risk next to percentages. Do not assume monotonicity, select the largest gain as an optimal configuration, claim independent replication from correlated cells, or treat synthetic correct-model headroom as operational identification or financial value. Any model or setting selected from this table requires separate development and final evaluation.
