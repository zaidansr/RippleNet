# Skeptical review: threats that can invalidate conclusions

1. **Identical inputs cannot support immediate causal discrimination.** Couple ordinary randomness and add the same vector either to the current state or current observation. Observed histories match through the event. A deterministic causal predictor must return the same forecast; a stochastic predictor must have the same conditional output distribution. Any apparent instantaneous classification advantage requires investigation for leakage or unequal inputs. Later observations can legitimately change the inference.

2. **The generator assumes the signature the method is meant to discover.** Single-step observation errors versus known, persistent state propagation is an intentionally identifiable construction after sufficient observations. Success shows performance under that construction. It does not show that markets have those mechanisms. Known A,Q,R and accurately specified event priors further favour the model. Test estimated and misspecified parameters separately.

3. **A return error is not automatically a quote-error model.** If observed log price is p_t+eta_t, observed return is r_t+eta_t-eta_(t-1). One bad quote creates adjacent opposite-signed return errors. An additive one-return spike instead describes a different recording process. Include the price-derived family in an external mechanism test.

4. **The oracle can combine detection, timing and classification privileges.** Define exactly what it knows. A hand-designed covariance inflation with true labels need not compute the optimal conditional mean. Weak results from such a heuristic do not prove that event information is useless. Do not give it latent states or realised amplitudes without explicitly changing the benchmark.

5. **Omitting a dual-mechanism comparator weakens the central claim.** CE-BASS already handles additive and innovative outliers with particle-mixture Kalman filtering. Methodological novelty or superiority requires an appropriate comparison. [Primary paper](https://arxiv.org/abs/2007.03238). An established observation-robust alternative is also available. [Duran-Martin et al.](https://proceedings.mlr.press/v235/duran-martin24a.html)

6. **Either-category success permits selection.** Two outcomes and multiple simulator settings create multiple opportunities to pass. Freeze one primary contrast or use simultaneous/multiplicity-adjusted intervals. The original gates are exploratory until this is resolved. Noninferiority needs uncertainty bounds against the harm margin, not a favourable point estimate.

7. **Correlated observations do not provide independent sample size.** Use independent simulation runs as paired blocks. Common random numbers improve comparison precision but do not make the paired worlds independent replicates. Heavy-tailed errors can dominate MSE; publish run-level losses and absolute differences alongside relative percentages.

8. **MSE gains do not identify the mechanism.** Generic smoothing, shrinkage, adaptive noise, extra compute, or correct dynamics may explain gains. Ablate competing disturbance explanations while preserving other operations and tuning budgets. Cross-asset propagation claims additionally need a matched cross-asset information ablation. Removing graph edges changes the generator; removing information from the predictor answers a different question. State which intervention is being tested.

9. **Leakage can enter outside the forecast function.** Whole-series scaling, test-set tuning, shared latent trajectories across splits, event-boundary filter resets, and revised historical predictions can all invalidate evaluation. Use independent sequences, training-only transformations, fixed online state, and tests that changing future observations cannot change earlier predictions.

10. **Fresh seeds are not evidence of market transfer.** Unseen magnitudes probe one narrow shift. Change event mechanisms, noise tails, persistence, propagation and arrival patterns before claiming broader synthetic generalisation. Financial utility would require separate real-data targets and an appropriate evaluation; latent synthetic-state recovery establishes no trading return.

The highest-value next action is the paired-world timing experiment in the protocol, followed by a matched mechanism ablation. Enlarging a neural architecture is premature.
