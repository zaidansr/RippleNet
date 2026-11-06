# Single-origin auxiliary-information findings

The new diagnostic separates the value of a second measurement from nonlinear inference using the same measurements. Under its favorable clean-sensor assumption, additional information reduces optimal next-return risk by **68.6824%**. Exact nonlinear inference reduces risk by **1.80895% relative to the full-input linear predictor**. These have different denominators and must not be added. This is a conditional synthetic calculation, not market validation or a reversal of earlier null results.

## Frozen design and provenance

The [plan](information-diagnostic-plan.md) was published as `41a72bf237848e787d497f7c929e4e69674b7eb3` before the full numerical grid. Executable source was published as `f750ac9e1cd6a489dd69b8433a548f1c3dcaf77a`, tree `baad130acbee91615b54f61d97a68e1dc22dc080`, before execution. A documented wording correction clarified that the linear predictor is not generally a conditional mean; it changed no formula or gate.

This scalar one-origin task has no history, training, detection or estimated parameters. Base-state variance P=.015625, disturbance variance T=.25, primary/auxiliary ordinary noise variances R=U=.0025, forecast multiplier a=.6 and independent future innovation variance Q=.01 are fixed. Category priors are balanced. An observation error affects the primary alone in the favorable condition; a state shock affects the state read by both channels. That assumption supplies distinguishing information by construction. See the [derivation](information-diagnostic-mathematics.md).

Deterministic Gauss-Hermite integration evaluates both true observation laws at every frozen order 24, 48, 96 and 192. It integrates the exact label-free posterior, not sampled future outcomes. No seed, fitted model, statistical significance test or confidence interval applies. All 20 condition/order records, numerical diagnostics, parameters, runtime and source hashes are in the [unaltered summary](../results/information-v1/summary.json).

## Absolute risks and separate comparisons

Order-192 values are below. Risk means expected squared error predicting aX+w. Numerical zeros are shown as zero; the raw summary retains floating-point residuals.

| Condition | Primary Bayes risk | Full-input linear risk | Full Bayes risk | Information reduction vs primary | Nonlinear reduction vs full-input linear |
| --- | ---: | ---: | ---: | ---: | ---: |
| Clean independent auxiliary | .03407343 | .01086757 | .01067098 | 68.6824% | 1.80895% |
| Shared artifact | .03407343 | .03394906 | .03394906 | .364986% | 0% |
| Exact duplicate | .03407343 | .03407343 | .03407343 | 0% | 0% |
| Perfect clean auxiliary | .03407343 | .01000000 | .01000000 | 70.6516% | 0% |
| Zero forecast multiplier, same P | .01000000 | .01000000 | .01000000 | 0% | 0% |

In the clean condition, the absolute information gain is .02340245 and the remaining nonlinear gap is .0001965884. The full-input linear predictor captures approximately **99.16% of the absolute improvement** from primary Bayes to full Bayes. An apparent large gain against a primary-only baseline would therefore mainly be an information comparison, not evidence for a custom architecture.

The .364986% shared-artifact improvement is ordinary independent-noise averaging. Its categories have identical joint observation likelihoods, so event-origin category weights remain one half and exact full-input inference is linear. Forecast improvement alone cannot be attributed to cause discrimination.

The duplicate adds no information. The perfect clean sensor reveals the state and leaves only Q; knowing category cannot improve that forecast. With a=0, no current-state information predicts the independent next target, although category likelihoods could still differ. Tiny positive approximation gaps near 1e-32 in degenerate controls are roundoff, not effects.

## Numerical reliability and review

Every fixed condition passes the declared convergence gate. For the nonlinear clean case, order-96 versus order-192 changes are approximately 1.20e-10 for full risk, 2.99e-10 for information gain and 3.83e-10 for approximation gain. Relative reductions change by 8.78e-7 and 3.52e-6 percentage points respectively. Final information and approximation risk-identity residuals are about 4.57e-12 and 1.31e-12. The controls agree with their analytic identities to floating-point precision.

This agreement is a numerical diagnostic, not a rigorous quadrature-error bound or empirical uncertainty estimate. The analytic primary and linear risks provide independent anchors; squared-forecast-distance integrals avoid relying solely on cancellation of risks. All orders and residuals remain disclosed, including lower-order discrepancies.

The engineering subagent implemented the core and ten deterministic tests. The mathematical subagent independently checked the covariance, conditioning and risk identities. The [skeptical quantitative review](information-diagnostic-review.md) audits the implementation and saved outcomes. The complete repository suite passes **92 tests**. No original simulator, archive importer or frozen prior result was changed.

## What the results justify

- **Meaningfulness:** additional clean information has a large effect inside this stipulated generator. No market utility margin has been established, and the former 5% criterion is not reused. The 1.81% nonlinear gap is model-specific headroom, not an attainable trained-model result or a practical deployment recommendation.
- **Reliability:** the calculations meet their frozen numerical checks and analytic controls. They do not constitute a statistical replication across markets or an uncertainty interval for an unknown real process.
- **Generalisation:** none is demonstrated. The trusted simultaneous sensor, independent noises, known event origin, known parameters, Gaussian laws and scalar one-step target are assumptions. The disturbance is large relative to the ordinary base-state variance, and neither this ratio nor sensor quality is market-calibrated.
- **Mechanism:** the controls support the mathematical distinction between additional information, shared-error averaging and nonlinear inference under the model. The causal categories were specified rather than discovered or independently adjudicated.
- **Conclusion:** do not grow a neural architecture on this evidence. A simple full-input method already captures most benefit. Establishing a defensible real independent signal and auditable outcomes remains the useful research frontier; the current archive still cannot validate the original cause hypothesis.

The next empirical experiment, conditional on obtaining that evidence, should compare a primary-only baseline with a strong baseline using the timely signal, then compare any candidate with exactly that same full input set. Keep source availability and label maturation auditable. Another favorable synthetic sensor setting would not establish those missing facts.

## Reproduce

```sh
python -m unittest discover -s tests -q
python -m ripplenet.information_experiment --output work/information-reproduction
```

The output directory must not already exist. Reproduction repeats a deterministic known model, not an independent test. The saved source tree distinguishes executable content from later reports and remote/local commit metadata. No market data, paid resource, provider contact or cloud service was used.
