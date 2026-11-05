# Audit plan: exploratory reconstruction of v2 conditional risk

This analysis reuses disclosed v2 final histories. It is a post-result explanation, not a new held-out experiment or a new confirmatory gate. No filter, simulator setting, forecast origin, practical margin or sample size may be chosen using these reconstructions.

## 1. Provenance and reconstruction acceptance

Record hashes of the frozen CSVs and summary before and after analysis; preserve them unchanged. Save reconstructed quantities in a distinct directory with the frozen source tree, instrumentation revision, Python/NumPy versions, exact configuration, event time, world category and seed. Retain all 128 seeds 60000–60127 in both moderate and zero conditions, with no dropping of inconvenient paths.

Instrumentation must only copy already computed causal branch means, covariances and log weights at each origin. Avoid changing update order, matrix operations, likelihood calculations, projection timing or posterior normalisation. If reconstruction uses a separate instrumented implementation, compare its forecasts and log probabilities with the unchanged frozen implementation at every origin, not just their averages.

Before using new moments, reproduce every saved CSV field: category-specific delayed MSE, five-origin MSE, delay-zero MSE, type negative log score, Brier score and the five saved probabilities. Require absolute tolerance 1e-14 and relative tolerance 1e-12, fixed before inspection. Reproduce summary means and all original paired inference from frozen seed vectors. Report maximum discrepancies and halt substantive interpretation if reproduction fails; do not relax tolerances or overwrite v2.

Check that weights sum to one, covariance matrices are symmetric and positive semidefinite within numerical tolerance, and moments correspond to filtering at the same forecast origin rather than future-conditioned smoothing. Save maximum residuals for all identities below.

## 2. Quantities to log

For each condition, seed, world and origin, let d be asset count; A the transition; Q ordinary future process covariance; w_z the current posterior type weight; m_z,P_z the component's current state mean and covariance; m the weighted state mean; and g an alternative forecast.

Define future component means f_z=A m_z and exact forecast f=A m. Log:

- Future-noise floor q=tr(Q)/d.
- Within-component predictive uncertainty W=sum_z w_z tr(A P_z A' + Q)/d.
- Between-component forecast uncertainty B=sum_z w_z ||f_z-f||^2/d.
- Exact conditional risk V=W+B=tr(A P_mix A' + Q)/d.
- Approximation disagreement D_g=||g-f||^2/d and alternative conditional risk V+D_g.

This integrates uncertainty in both the latent state and future innovation. Subtracting q from realised MSE alone does not accomplish that integration. D_g must be nonnegative; a negative realised loss difference does not invalidate this identity.

The posterior-weighted category oracle has risk W at the same observed history. Its information headroom is B. A true-category component risk on one realized world need not be below V samplewise; do not mistake that quantity or realized oracle MSE for a per-history bound.

## 3. Aggregation and descriptive inference

Keep delay zero separate, preserve the primary tau+1,...,tau+4 window, and display all delays without selecting favorable ones. Average assets and origins within a world, then average both coupled worlds within each seed. The 128 independent seeds remain the only resampling units. Moderate and zero conditions reuse these units.

Report ratios of aggregate means, not average per-path ratios:

- Exact versus approximation gain: mean(D_g)/mean(V+D_g).
- Additional category-information gain: mean(B)/mean(V).
- Future-noise share: q/mean(V).

Any noise-subtracted denominator must be explicitly labelled and cannot be compared with the original 5% total-MSE target. Zero denominators are undefined, not repaired with epsilon. In the zero-transition control, V=q, B=0 and D_g=0; noise-subtracted effect ratios are consequently undefined.

For descriptive uncertainty, resample whole seed blocks with the fixed existing bootstrap recipe, preserving paired worlds and all within-seed quantities. Raw percentile 95% intervals may describe variability under this generator; clearly label them exploratory and avoid adding them retroactively to the original five-contrast family. Exact per-history algebraic equalities require numerical residual checks, not significance tests.

## 4. Interpretation boundary

Small D_g explains little representation headroom; small B explains little remaining value of a category label at that origin. A large noise share can dilute either gain in total-MSE units. These explanations are conditional on the known-time Gaussian generator. They supply no new transfer evidence, no independent replication and no financial claim. Any model or setting chosen from them needs fresh development and final data.
