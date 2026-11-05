# Experiment v1: held-out synthetic findings

This is a newly run synthetic feasibility experiment, not an analysis of pre-existing user results. The candidate is a small moment-matched Gaussian mixture filter, not a neural network or a validated financial model.

## Design and provenance

The public experiment specification and method code were committed before the final evaluation. Twenty clean training seeds fit OLS; twelve separate development seeds selected one ordinary baseline per persistence setting. The oracle gate passed on development data. Thirty new test seeds then evaluated the frozen methods with no post-test tuning. Each seed couples clean and two event worlds and is the unit of bootstrap resampling. Shift conditions share seeds and are not independent extra replications.

Frozen source tree: `1f28e2ee49c17cb041dc45ac90c975a02206ccd5`. Runtime: Python 3.13.3, NumPy 2.3.2. [Specification](experiment-v1.md), [development losses](../results/development-v1.json), [full summary](../results/experiment-v1/summary.json).

## Primary comparison: nominal, moderate persistence

Comparator selected on development data: **adaptive**. Positive relative improvement means lower MSE. Category scores average five post-event one-step forecasts and three assets within each seed. Clean scores use an event-free control after warm-up; they are not all clean intervals surrounding events.

| Category | Baseline MSE | Dual MSE | Improvement | Paired 95% interval | Adjusted interval |
| --- | ---: | ---: | ---: | --- | --- |
| observation | 0.015028 | 0.015237 | -1.4% | [-2.5%, -0.4%] | [-3.0%, +0.0%] |
| state | 0.011956 | 0.011808 | +1.2% | [-0.3%, +2.7%] | [-0.9%, +3.3%] |
| clean | 0.010579 | 0.010543 | +0.3% | [+0.2%, +0.5%] | [+0.1%, +0.6%] |

Adjusted intervals use per-contrast alpha=.05/9 for the prespecified nine nominal/moderate contrasts (three references, three categories). They are percentile bootstrap approximations using 9,999 paired resamples, not exact finite-sample guarantees.

Original exploratory point-estimate/95%-interval rule passes: **False**. At least one event improvement confidently exceeds the 5% practical margin under adjusted intervals: **False**. All three baseline contrasts meet the uncertainty-aware no-more-than-5%-harm margin: **True**.

A positive point estimate is not sufficient evidence that the gain exceeds 5%. An interval crossing -5% cannot rule out practically important harm. MSE changes establish no trading profit or market transfer.

## Scientific assessment

- **Meaningful improvement:** the candidate fails the agreed continuation rule. Its baseline-relative event gains do not reach the 5% practical target.
- **Statistical reliability:** the nominal state-shock gain is not established; its interval crosses zero. Recording-error deterioration is visible in the raw interval, but its adjusted interval reaches zero. The small clean-control gain is statistically stable under these assumptions but practically below the project's threshold.
- **Generalisation:** no transferable advantage is demonstrated. The recording-error comparison deteriorates under the price-derived corruption shift, and larger anomaly magnitudes do not produce the required gain.
- **Ablation:** the dual method beats observation-only handling on state shocks while losing on recording errors. It does not show a reliable advantage over pooled noise. This supports a robustness tradeoff, not successful event-type identification.
- **Conclusion:** stop advancement of this collapsed candidate under the current gate. This does not establish that all disturbance-aware models are ineffective; it rejects the promised benefit for this frozen candidate and tested settings.

## Mechanism ablations

| Reference ablation | Category | Dual improvement | Adjusted interval |
| --- | --- | ---: | --- |
| observation_only | observation | -33.2% | [-52.3%, -17.2%] |
| observation_only | state | +37.3% | [+21.8%, +54.6%] |
| observation_only | clean | +0.1% | [-0.0%, +0.2%] |
| pooled | observation | -0.0% | [-0.6%, +0.4%] |
| pooled | state | +0.3% | [-0.3%, +1.0%] |
| pooled | clean | -0.0% | [-0.0%, +0.0%] |

All variants use three branches, the same nominal dynamics, priors and scale, and no tuning on test data. The observation-only ablation duplicates the measurement-error branch. The pooled ablation duplicates a generic branch splitting anomaly variance between process and measurement noise.

There is an analytical confound: with identical prior state moments, the dual and pooled variants have the same current posterior mean. The dual variant retains extra between-branch covariance; this can alter subsequent forecasts. Because the filter collapses event explanations after every update, an ablation difference supports a role for uncertainty propagation, not demonstrated recovery of true event identities. No event-classification score is asserted.

## Declared shift tests

These are secondary exploratory comparisons with raw paired 95% intervals. Magnitude-shift event standard deviation is .75 rather than .5; causal methods keep their original .5 scale. Price-error shift replaces one return spike with adjacent +d,-d recording errors. The oracle is omitted there because its covariance schedule would no longer be exact.

| Condition | Persistence | Frozen baseline | Observation gain [95% interval] | State gain [95% interval] | Clean gain [95% interval] |
| --- | --- | --- | --- | --- | --- |
| nominal | moderate | adaptive | -1.4% [-2.5%, -0.4%] | +1.2% [-0.3%, +2.7%] | +0.3% [+0.2%, +0.5%] |
| nominal | weak | clipped_3 | -1.9% [-2.9%, -1.1%] | -0.1% [-0.8%, +0.7%] | +0.0% [-0.0%, +0.0%] |
| nominal | zero | zero | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] |
| magnitude_shift | moderate | adaptive | -2.1% [-3.0%, -1.2%] | +1.3% [-0.0%, +2.5%] | +0.3% [+0.2%, +0.5%] |
| magnitude_shift | weak | clipped_3 | -4.5% [-6.5%, -2.6%] | +1.1% [-0.5%, +3.0%] | +0.0% [-0.0%, +0.0%] |
| magnitude_shift | zero | zero | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] |
| price_error_shift | moderate | adaptive | -13.6% [-28.1%, -5.0%] | +1.2% [-0.3%, +2.7%] | +0.3% [+0.2%, +0.5%] |
| price_error_shift | weak | clipped_3 | -3.4% [-5.8%, -1.4%] | -0.1% [-0.8%, +0.7%] | +0.0% [-0.0%, +0.0%] |
| price_error_shift | zero | zero | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] |

Fresh seeds test repeatability under the generator. These two shifts test limited synthetic transfer, not robustness to arbitrary dynamics, estimated parameters, heavy tails, overlapping events or real markets. The zero-persistence control should erase the forecasting value of state propagation. Ratios at tiny absolute effect sizes should not be overinterpreted.

## Causal checks and statistical limits

Maximum ordinary-method forecast difference across matched observed prefixes: 1.11e-16. Per-origin MSE is saved in the summary. Matching predictions at delay zero is required; a privileged oracle may differ because it receives event metadata.

All confidence intervals condition on the fixed generator and settings. Thirty seeds can leave substantial uncertainty; no seeds were added after inspecting intervals. The primary multiplicity family excludes secondary shifts and oracle comparisons, which remain exploratory. The three event worlds and all shift conditions share randomness by design.

The oracle knows event time, category and true Gaussian impulse variance, but not realised amplitude or latent state. Baselines are simple, known-parameter methods. An established dual-disturbance approach such as CE-BASS remains necessary before any methodological-superiority or novelty claim. The simulated state itself is a prescribed latent return, not observed financial truth.

## Most discriminating next experiment

Separate event-history information from generic uncertainty adaptation. Compare (1) the collapsed dual model, (2) a filter retaining the previous event's competing explanations until new observations arrive, and (3) a Gaussian adaptive-covariance control matched for posterior mean/covariance propagation. Freeze their settings on new development seeds and use a new held-out seed set, since the v1 final seeds are now spent. Score by elapsed event time and include the price-derived corruption shift.

If retaining event history adds no benefit over the covariance-matched control, explicit disturbance identification is unnecessary for the observed gains. If benefit appears only after divergent observations and transfers across the corruption shift, that is stronger evidence for the proposed mechanism. A larger neural network would not isolate these explanations.

## Files and reproduction

Per-seed category losses are saved as one CSV per condition/persistence in results/experiment-v1. Whole-path means and per-origin means are in summary.json. Run `python -m ripplenet.report` to regenerate this document from saved results. `python -m ripplenet.evaluate` refuses to overwrite an existing final evaluation directory. Reproducing frozen evaluation in a separate checkout is permissible; reusing its results for further tuning is not an independent new test.
