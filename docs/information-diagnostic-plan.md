# Frozen single-origin information-value diagnostic

This new conditional synthetic question follows the owner's instruction to continue after the recommended research option was offered. It does not reinterpret earlier negative experiments or establish the existence of a real auxiliary signal. Plan fixed before the full numerical grid is executed.

## Question and generator

Does a contemporaneous second measurement improve optimal next-return forecasting, and how much additional benefit remains beyond a linear predictor given the same inputs?

This is one scalar forecast origin, with no past observations, detection, training or delayed-origin averaging. Let independent base state b, disturbance d and observation noises have zero-mean Gaussian laws with variances P, T, R and U. Event type is equally likely observation corruption O or state shock S. Under O, X=b; under S, X=b+d. The primary observation is Y=X+noise_y+1{O}d. The target is aX+w with independent future innovation variance Q.

Freeze a=.6, Q=.01, R=.0025, T=.25, U=.0025 and P=.01/(1-.6^2)=.015625. P is the ordinary base-state prior, not a filtered history or the variance of the intervention mixture. Known parameters, known event origin and the balanced prior are shared privileges. These numbers define a new scalar problem, not a calibrated market or a reproduction of the earlier three-asset delayed endpoint.

## Fixed conditions and arms

- Clean auxiliary: Z=X+independent noise of variance U. This favorable structural assumption installs distinguishing information by construction.
- Shared-disturbance control: Z=X+noise_z+1{O}d. Joint observation laws of the two categories coincide; ordinary noise averaging may still help forecasts.
- Duplicate control: Z=Y exactly. Handle singular support as one observation, without jitter or fabricated information.
- Perfect clean auxiliary: U=0, so Z=X. Forecast risk must equal Q and category information adds no further forecasting benefit.
- Zero forecast dependence: clean auxiliary with a=0, holding P and all observation laws fixed at their nominal values. Every next-return risk must equal Q.

Compare exact primary-only Bayes, exact full-information Bayes and full-information linear minimum-MSE predictions. Both full-information arms receive identical measurements and parameter knowledge. No new architecture is trained. A category oracle is optional diagnostic mathematics, not a primary numerical arm or permission to expand the contrast family.

## Estimands and identities

Report absolute expected squared forecast risk for every arm. Separately report information value, primary Bayes risk minus full Bayes risk, and nonlinear approximation headroom, full-information linear risk minus full Bayes risk. Also compute each gap directly as the expected squared difference between its two forecasts. Report the two relative reductions with their own denominators: primary risk and full-information linear risk respectively. Classification information is not a forecasting benefit by itself.

Wording clarification before full execution: the linear predictor is not generally a conditional mean. Replacing "conditional-mean predictions" with "forecasts" corrects that description without changing an estimand, formula, parameter or numerical gate.

Conditional forecast risk is Q+a^2 Var(X|observations). Exact posterior weights use Gaussian likelihoods, and within-category conditioning uses the correct cross-covariance with X. Never pass realised category, X or future w to ordinary predictors.

## Numerical method frozen before outputs

Integrate the two true observation laws with equal mixture weights using deterministic Gauss-Hermite quadrature at orders 24, 48, 96 and 192 per dimension. Evaluate every fixed condition and disclose every order. No random sample, fitted parameter, seed, significance test or confidence interval is involved. Analytical formulas provide primary and linear risks and all degeneracy controls.

Numerical resolution requires the order-96 versus order-192 difference to be at most 1e-6 for each reported risk and gap integral, at most .01 percentage point for each relative reduction, and absolute risk-identity residuals at most 1e-6. A failing quantity is numerically inconclusive under this design. Do not add quadrature orders, change noise levels or tune conditions after seeing results. Numerical agreement is a diagnostic, not a rigorous integration-error bound.

Freeze and publish executable source before the full grid. Save parameters, all orders, identity residuals, runtime versions and source hashes in a new directory protected against overwriting existing output. Existing source experiments and results remain unchanged. Unit tests may use small analytical fixtures before full execution.

## Interpretation and stop rule

No practical market margin is available for this hypothetical sensor. Do not reuse the earlier 5% criterion, claim statistical significance from quadrature, or interpret a positive toy result as market validation, novelty or justification for a neural architecture. A dominant information gain with small same-input approximation headroom would favor seeking a defensible real signal over model growth. Any synthetic approximation headroom remains conditional on the stipulated generator.

Use local NumPy and existing standard-library tooling only. No new market data, provider contact, cloud service or spending is required. Publish negative, positive or numerically inconclusive findings alike.
