# Experiment v2: identification improves, practical forecast value does not

Three subagents reviewed the engineering, mathematics and statistical design. The engineer implemented the exact-history filter and nine tests; the statistical subagent implemented paired inference and twelve tests; the mathematical reviewer derived the controls and limitations. The root agent integrated the runner and reporting. The combined suite passes 45 tests.

## What was tested

This is an exact known-intervention-time diagnostic, deliberately easier than operational detection. All methods are told when the single Gaussian intervention occurred and know its distribution and dynamics. They do not know its category, realised amplitude or latent state. Compare retained two-component inference, projection to a Gaussian once at the intervention followed by independent updates, and identical component filters with weights fixed at .5. A category oracle is reported separately.

The design is informed by v1 and was published before v2 data inspection. There is no training or post-test tuning. Thirty-two development seed blocks precede 128 new final blocks, 60000–60127. Each block couples both categories; the worlds, assets and times do not inflate replication count. The zero-persistence condition shares these blocks and is a negative control.

Primary scores average origins tau+1 through tau+4, three assets and both categories within each seed. Event-origin and five-origin metrics are secondary. Python 3.13.3; NumPy 2.3.2. Frozen final-run source tree: `f4e6acebd081130661b593daa6c11d9da0fab499`.

[Prespecified design](experiment-v2.md), [mathematical derivations and v1 covariance correction](experiment-v2-mathematics.md), [full summary](../results/experiment-v2-final/summary.json), [moderate seed losses](../results/experiment-v2-final/moderate.csv), [zero-control losses](../results/experiment-v2-final/zero.csv).

## Five prespecified contrasts

Positive values favour retained inference. MSE entries are percentage reductions; type-score entries are absolute reductions in nats. Adjusted intervals use 9,999 paired seed-bootstrap resamples, Bonferroni family size five. These are approximate intervals conditional on the simulator.

| Contrast | Improvement | Raw 95% interval | Adjusted interval |
| --- | ---: | --- | --- |
| Balanced MSE versus projection | -0.0013% | [-0.1132, +0.1224]% | [-0.1449, +0.1642]% |
| Balanced MSE versus frozen weights | +0.3375% | [+0.2183, +0.4612]% | [+0.1839, +0.5079]% |
| Type negative-log-score reduction | +0.4749 nats | [+0.4130, +0.5293] nats | [+0.3926, +0.5443] nats |
| Observation-category MSE versus projection | +0.0063% | [-0.1210, +0.1485]% | [-0.1585, +0.1925]% |
| State-category MSE versus projection | -0.0088% | [-0.1769, +0.1618]% | [-0.2285, +0.2147]% |

## Decision

Practical representation gate (lower adjusted bound above 5% versus projection): **False**. Evidence-responsive weighting criterion (positive forecast and type-log-score bounds versus frozen weights): **True**. Both category harm guards versus projection (lower bound above -5%): **True**.

The retained-versus-projection interval includes zero and its upper bound is far below the project's 5% practical target. This supports a tightly limited finding of no practically important added forecasting value at that margin under this setup; it is not proof of exact equivalence. The result does not justify a larger operational model on the premise that Gaussian collapse is the missing source of substantial improvement.

An independent statistical subagent reproduced all five contrasts and bootstrap intervals from the saved CSVs without using the inference helper. The engineering subagent checked indexing, labels, timing privileges and source provenance and found no scientifically material integration defect. [Statistical audit](experiment-v2-statistical-review.md), [engineering audit](experiment-v2-engineering-review.md).

Weight updating does have a statistically detectable forecasting effect against the intentionally frozen-weight ablation, but it is small. The improved type log score supports evidence-responsive inference under the stipulated Gaussian mechanism. Beating frozen weights is not the same as beating the stronger independently updated projection control.

## Magnitude and mechanism

| Arm | Balanced delayed-origin MSE |
| --- | ---: |
| retained | 0.0109863489 |
| projected | 0.0109862110 |
| frozen | 0.0110235585 |
| oracle | 0.0109962006 |

Balanced retained type negative log score is 0.218254 nats versus 0.693147 for fixed .5 probabilities. Binary Brier score is 0.067470 versus .25. These are averages of origins tau+1 through tau+4, not instantaneous detection metrics.

The exact model can learn the event type after distinguishing observations arrive while a Gaussian state approximation already forecasts almost as well. Event identification and useful forecast improvement are separate objectives. These observations do not establish that all history-aware models are ineffective or that the v1 failure has one universal cause.

## Causal checks and scope

- **moderate:** matched-prefix forecast difference 8.33e-17; event-origin arm difference 0; initial probability deviation from .5 0.
- **zero:** matched-prefix forecast difference 0; event-origin arm difference 0; initial probability deviation from .5 0.

With zero persistence all next-return means are zero, type probabilities stay .5, and every contrast is exactly zero. With moderate persistence the ordinary methods still agree at the event origin; no method uses later observations to revise an earlier forecast. The type oracle is privileged and is not an operational competitor.

There is no clean-event case in this conditional experiment, so it supplies no false-alarm or clean-period noninferiority evidence. No unknown-time detection, alternative corruption family, parameter estimation, real-market transfer, economic value or novelty is established. V1's adverse price-error-shift finding remains relevant and is not overturned by this easier experiment.

Exact Bayes conditioning is already population-MSE optimal under this correctly specified model. V2 quantifies the size of its benefit and approximation costs; it is not a discovery of a new theoretical optimality result. The point estimate can be slightly negative against a projection through finite-sample variation. Similarly, a category oracle can rank slightly worse on realised finite-sample losses despite its information advantage in expected risk; its observed mean is not a samplewise risk bound.

## Most efficient next analysis

Before adding model complexity, decompose conditional predictive risk into irreducible uncertainty and squared disagreement with the exact Bayes mean. Under the known simulator, integrating over the future innovation can remove much of the noise in method comparisons. Treat an analysis of these already-disclosed observations as exploratory; any newly selected operational model requires new development and final data.

This would distinguish low forecast headroom from merely noisy realised losses. If the Gaussian approximation's conditional means are already close to the Bayes means, further classification machinery is unlikely to meet the present next-return improvement target in this setting.

## Reproduction

Run `python -m unittest discover -s tests -v` and `python -m ripplenet.history_report` for tests and this report. Reproducing the exact final run uses `python -m ripplenet.history_experiment --stage final --output work/v2-reproduction`; this reuses disclosed seeds and is reproduction, not a fresh test. Existing result directories are protected against overwrite. All computation was local; no paid capacity was purchased.
