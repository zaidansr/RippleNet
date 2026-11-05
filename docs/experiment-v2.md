# Experiment v2: exact known-time representation diagnostic

## Why this experiment

V1 did not establish a useful advantage for its collapsed mixture. This v2 design is explicitly informed by those disclosed results. It asks whether preserving competing Gaussian explanations and updating their probabilities has a practically useful effect under a correctly specified intervention model. It is not a new operational detector or evidence of financial usefulness or methodological novelty.

Engineering, mathematical, and statistical subagents independently reviewed the controls before implementation. The intervention time is shared privileged information supplied to every arm. Removing event-detection and arrival-model uncertainties makes this a simpler, easier problem than v1; gains cannot be compared directly with v1 as evidence of operational progress.

## Data and information

Reuse the stable three-asset simulator's moderate A, Q=.01 I, R=.0025 I, 180 retained observations and 128 burn-in steps. Each independent seed draws one intervention time uniformly from indices 40–149 and amplitude d~N(0,.5^2 I). Generate a recording-error world and a state-shock world using identical amplitude and ordinary noise. Their observed histories match through the intervention time tau. Exactly one intervention is guaranteed; there are no later events.

All arms know tau, A,Q,R, the Gaussian amplitude distribution and a balanced observation/state prior. None receives the realised amplitude, category or latent states, except the explicitly reported category oracle. Ordinary noise and intervention randomness remain independent. All numerical settings are inherited or fixed before examining v2 development data.

There is no fitted model and no training stage. Reserve seeds 40000–40019 unused. Development seeds are 50000–50031; final seeds are 60000–60127, fixed at 128 before opening data. V1 seeds are spent and may only inform development. Do not extend final sample size after viewing intervals.

## Arms

1. **Retained exact mixture:** ordinary KF before tau; two conditional Gaussian updates at tau (extra measurement covariance versus extra process covariance). Retain both conditional KFs thereafter and update their probabilities by newly arrived observation likelihoods.
2. **Projected Gaussian:** match the exact mixture's mean and total covariance once at tau, then evolve independently using ordinary KF updates. Never resynchronise its moments with the retained mixture.
3. **Frozen weights:** use the identical conditional KF trajectories as the retained mixture, but keep the two weights at .5. The only difference from retained inference is evidence-responsive weighting.
4. **Category oracle:** select the conditional KF corresponding to the actual category; it knows category but not realised amplitude. Report separately.

Copying the retained mean/covariance at every origin would make linear point forecasts identical by construction and is not a valid empirical control. A Gaussian pooled-noise arm alone would conflate representation and weighting effects.

## Causal and negative controls

At tau, both event likelihoods and retained type weights must be equal. Retained, projected and frozen forecasts must coincide then, including across matched worlds. Differences can first appear after observing y[tau+1]. Altering future observations must not change earlier forecasts. Simultaneously renaming the hypotheses and their component definitions must preserve predictions.

Repeat final evaluation with A=0 as a negative control: category probabilities must remain .5 and next-state forecasts must be zero. This control shares seed blocks with the moderate condition and supplies no additional independent sample size.

The conditional two-event-type experiment contains no clean-event case. No-event paths without an intervention flag are an ordinary-KF sanity check, not evidence of noninferiority on false alarms. False timing flags, unknown timing, price-derived contamination and parameter misspecification require separate experiments; v1 already shows that such shifts can matter.

## Estimands

For each seed average squared next-return error equally across two coupled worlds, three assets and forecast origins tau+1,...,tau+4. This balanced delayed-origin MSE is the v2 primary endpoint. The change from v1's five-origin endpoint is prespecified and motivated by the identical-information constraint at tau. Save tau separately and the original tau,...,tau+4 window as secondary measures.

Save category-specific delayed-origin MSE and per-origin MSE. Score posterior type probabilities using binary Brier score and negative log probability of the true category. For the mechanistic log-score contrast, average origins tau+1,...,tau+4 and both worlds within each seed. Frozen probabilities are .5. Use normalized log weights directly; do not obtain log scores by clipping or subtracting rounded probabilities. The projected forecaster has no type posterior and receives no fabricated classification score.

## Inference and gates

Prespecify five primary contrasts, all within the moderate condition:

- Retained versus projected balanced forecast MSE (relative improvement).
- Retained versus frozen balanced forecast MSE (relative improvement).
- Retained versus frozen type negative log score (absolute reduction, nats).
- Retained versus projected observation-category forecast MSE (relative improvement).
- Retained versus projected state-category forecast MSE (relative improvement).

Use 9,999 paired bootstrap resamples of entire seeds, fixed bootstrap seed 567890. Report raw 95% and Bonferroni-adjusted intervals with per-contrast alpha=.05/5. These percentile intervals are approximate, not exact finite-sample guarantees. Coupled worlds, assets, times and conditions are not independent replications.

Practical representation benefit requires the primary relative-improvement lower adjusted bound to exceed 5%. Mechanism support additionally requires positive lower adjusted bounds for both retained-versus-frozen forecast improvement and type log-score reduction. The observation and state category harm guards require lower adjusted relative-improvement bounds above -5% versus projection. An interval crossing zero is inconclusive; an interval not crossing zero but below the practical margin does not establish the practical target.

Development data are used only for implementation checks and descriptive precision estimates. No model or margin tuning is planned. The exact posterior conditional mean is already population-MSE optimal under the specified generator, so v2 quantifies practical effect size and approximations; it does not discover theoretical optimality or uniquely identify real causes.

## Artifacts and execution

Freeze method code before final seeds are opened. Save complete seed-level losses, parameters, version/source provenance, per-origin results, type scores and confidence intervals. Keep v1 results unchanged. Publish the result even if every gate fails. Use local NumPy computation; no GPU, cloud capacity or spending is authorised or needed.
