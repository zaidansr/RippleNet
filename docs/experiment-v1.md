# Frozen experiment v1: oracle headroom, then causal ablations

This specification is written before development results are examined. It extends the implementation diagnostic to comparative forecasting. All results remain synthetic and exploratory; no claim of financial utility or novelty is made.

## Data and information

Three assets; 180 retained observations; 128 burn-in steps; ordinary Q=0.01 I and R=0.0025 I. Moderate A=[[.55,.10,0],[0,.45,.10],[.05,0,.35]], weak A=0.2 times moderate A, and zero A. Each independent seed generates shared ordinary noises across clean, observation-error and state-shock worlds. These coupled worlds are one inferential block, not independent samples.

Each event vector is sampled N(0,tau^2 I), with all assets eligible, and the same realised vector is used in the two event worlds. Its time is randomly selected between retained indices 40 and 149 inclusive. There is one isolated event per path. Training seeds 10000–10019 fit observed-return OLS separately for each A on clean paths. Development seeds 20000–20011 select baselines; held-out seeds 30000–30029 are opened only after methods are fixed. Event randomness uses a separate seeded stream.

Development tau=.5. Final evaluation includes tau=.5 replication and tau=.75 magnitude shift, with paired seeds. A second shift creates an observation error in log price, hence adjacent return errors +d,-d; this is explicitly outside the ordinary return-error generator.

Ordinary methods know A,Q,R and initialisation, not event time, label, amplitude or latent state. Their initial covariance is propagated through exactly the simulator's burn-in from zero. The oracle alone knows event time and category and the true tau. With Gaussian impulse vectors, adding tau^2 I to process or measurement covariance is the exact conditional Gaussian filtering update under the event schedule, with no realised amplitude disclosed. Its future-event conditional mean is zero. It is not run on price-derived contamination, whose cross-time error law requires a different oracle.

## Development stage and gate

Compare zero, fitted OLS, ordinary KF, innovation-clipped KF (thresholds 2,3,5), generic residual-adaptive noise KF, and the oracle. Select one strongest ordinary method per persistence setting by mean development MSE averaged equally across the two event categories. No final-test data participates. Oracle headroom of at least 10% in either event category under moderate persistence permits implementation of the causal mixture stage. Otherwise stop that branch and report the development result.

## Contingent causal stage

If the gate passes, implement a three-hypothesis Gaussian-sum update (normal, observation anomaly, process anomaly) with a moment-matched Gaussian state after every update. Fix event prior probability .01 and tau=.5 before testing. This is an approximation, not CE-BASS or a novel architecture: a one-event path does not have a memoryless arrival process, and moment matching discards multimodality.

Use three branches for each matched-computation ablation: (a) replace the process hypothesis with a duplicate observation hypothesis; (b) replace both anomaly hypotheses with duplicate generic hypotheses inflating process and observation covariances by half the anomaly variance each. Use the same priors, scale, A,Q,R and tuning budget. No test-set tuning and no retraining on shifts.

## Scores and inference

For each seed and event category, average squared errors over all three assets and the five one-step forecasts with origins t_event,...,t_event+4. Clean control loss averages origins 40,...,178 on an independent-event-free coupled world; this does not claim to measure all clean periods surrounding events. Also save whole-path MSE after origin 40 and error by forecast-origin delay. Delay-zero inputs in the two event worlds must match, and ordinary forecasts must match to numerical precision.

Persist per-seed losses. Report absolute MSE and improvement 1-mean(method loss)/mean(reference loss), using paired bootstrap resampling of whole seeds (9999 replicates; fixed bootstrap seed 456789). Raw 95% intervals describe all secondary comparisons. The primary family is moderate-persistence nominal-test comparisons of the dual mixture with selected baseline and each of two ablations, across observation, state and clean categories: nine contrasts. Also report Bonferroni-adjusted percentile intervals (per-contrast alpha=.05/9); these are approximate bootstrap intervals, not exact finite-sample guarantees.

The original 5% continuation and no-more-than-5% harm margins remain exploratory. A point estimate over 5% with an interval above zero does not establish a gain over 5%. Stronger practical-effect claims require the lower interval bound above 5%; a harm claim requires the lower improvement bound above -5%. Report both point-estimate and uncertainty-aware decisions. Generalisation evidence is limited to the two declared shifts and does not establish market transfer.

No test seeds may be reused for tuning after this run. Any code defect affecting evaluation must be disclosed, corrected, and evaluated with a new final-test seed set.
