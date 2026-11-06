# Independent skeptical and numerical review

Reviewed the frozen plan, implementation, numerical runner, all 20 saved condition/order records and the [results report](information-diagnostic-results.md). Independently ran the ten targeted unit tests; all passed. No code or prior experimental artifact was edited for this review.

## Formula and information audit

Let `c=P+T/2` and `v=P+T+R`. Independent conditioning gives the primary Bayes forecast `a*c*y/v` and risk `Q+a²*(c-c²/v)`. The observation-category likelihoods are identical for the primary reading, so its mean is exactly linear despite the non-Gaussian joint state model.

For a clean auxiliary, the unconditional observation covariance is `[[v,c],[c,c+U]]` and its cross-covariance with X is `(c,c)`. These produce the independently checked full-information linear risk. The source uses the appropriate distinct component covariances for exact mixture conditioning. It integrates under each generating component but does not supply that realized category to either predictor. Q is added once; forecast-distance gaps contain the required a² scaling.

The shared-artifact joint observation law is identical across categories, fixing posterior type probabilities at one half. Exact conditional means equal the full-input linear predictor. Independent ordinary-noise averaging may nevertheless improve forecasting. The duplicate is handled on its one-dimensional support without jitter. A perfect clean auxiliary reveals X, whereas a perfect shared-artifact reading would not generally do so. The zero-a control holds P fixed and correctly erases forecasting information value without erasing observation information.

The LMMSE forecast is not generally a conditional mean. The approximation-gap identity remains valid because the full Bayes forecast is the conditional mean; the relevant quantity is its squared distance from the linear forecast. The report's clarification does not change the estimand.

## Independent numerical checks

Verified every saved source hash against the current files and compared their contents with the named frozen source tree. Verified the five fixed configurations, all four declared orders, the analytic primary/linear risks, reported percentage denominators and every saved convergence decision.

Separately reimplemented the nontrivial clean-case integration at all four frozen orders using explicit two-dimensional inverse covariances and log-add-exp normalization, rather than calling the project's posterior or integrator. Its direct risks and squared-forecast gaps reproduce the saved values within 2e-15. The remaining cases agree with independently derived analytic controls. This is deterministic reproduction, not a fresh experiment.

For the clean condition, order 192 gives:

- Primary Bayes risk: **0.0340734266**.
- Full-input linear risk: **0.0108675655**.
- Full Bayes risk: **0.0106709772**.
- Information gain: **0.0234024494**, or **68.6824067% of primary risk**.
- Nonlinear approximation gap: **0.0001965884**, or **1.8089457% of full-input linear risk**.

The percentages have different denominators and cannot be added. The full-input linear forecast captures approximately 99.16% of the absolute primary-to-full improvement.

Clean-case order-96/192 differences are 1.20e-10 in full risk, 2.99e-10 in information gain and 3.83e-10 in approximation gain. Relative reductions differ by 8.78e-7 and 3.52e-6 percentage points. Final risk-identity residuals are 4.57e-12 and 1.31e-12. These pass the declared, unchanged 1e-6 risk/gap, .01-percentage-point and 1e-6 identity gates. The order-24 primary identity residual is approximately -1.002e-6; it remains disclosed rather than being described as exact at every order.

Shared-artifact information gain is **0.3649863%**, with zero nonlinear gap analytically. Duplicate information gain is zero. Perfect clean measurement gives the Q floor and **70.6516162%** primary-relative reduction. Zero a gives the Q floor and zero gains. Tiny positive control approximation gaps are floating-point roundoff, not effects. Component conditional variances receive only the implementation's documented tiny-subtraction-roundoff handling; no general covariance jitter is introduced.

## Scientific conclusion and remaining objection

No material formula, information-leakage or saved-result reporting defect was found for this stipulated diagnostic. Agreement across orders is a numerical check, not a rigorous error bound, confidence interval, significance result or replication across unknown processes.

The strongest limitation is structural: the clean auxiliary assumes a trusted simultaneous observation of the state, exactly the real-world evidence not established by the data audit. State disturbances affect both readings while observation artifacts affect only the primary by construction. Disturbance variance is 16 times ordinary base-state variance; this and sensor reliability are uncalibrated assumptions. The large information benefit therefore cannot validate a financial mechanism.

The same-input nonlinear gap is a separate, conditional approximation result, not a trained-model gain or novelty claim. Most benefit is already captured by a classical full-input linear predictor. The earlier delayed-origin null results remain unchanged because this is a different scalar origin, information set and target setting. Further architecture growth or favorable synthetic parameter search is not justified by these calculations. The empirical frontier remains independently auditable outcomes and genuinely timely additional information.
