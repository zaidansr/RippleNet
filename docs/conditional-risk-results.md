# Conditional risk: little delayed forecasting headroom

This is an exploratory reconstruction of the already-disclosed v2 histories, not a fresh test or a new forecasting model. Three subagents supplied mathematical review, instrumentation/tests, and an independent statistical audit; root integrated the replay and reporting. No parameter, observation, target, seed or original result was changed.

## Main finding

Across the two balanced event worlds and delays 1–4, future innovations account for **95.763%** of exact Bayes predictive risk. Retaining the exact mixture instead of the independently evolved Gaussian projection reduces conditional expected risk by **0.03564%**. Even perfect category information adds only **0.02888%** over the retained forecast at these delayed origins.

The negligible gain is therefore not merely an inconclusive realised-loss comparison. The approximation's conditional means are already close to the exact Bayes means on these histories, while future innovation noise dominates the total risk. Conditional excess is nonnegative by the Bayes-risk identity; that positivity is mathematical, not newly discovered statistical superiority.

## Quantitative decomposition

Values below are mean squared-return units per asset, averaged within each seed over two worlds and four origins before aggregating the 128 disclosed seed blocks.

| Component | Mean risk |
| --- | ---: |
| Unpredictable future innovation | 0.010000000000 |
| Current-state uncertainty within a type | 0.000439433216 |
| Remaining uncertainty about type | 0.000003015966 |
| Total same-information Bayes risk | 0.010442449182 |
| Projection's excess above Bayes | 0.000003723471 |
| Frozen weights' excess above Bayes | 0.000023908220 |
| Total projection risk | 0.010446172653 |
| Posterior-averaged category-oracle risk | 0.010439433216 |

| Conditional risk reduction | Ratio of means | Descriptive 95% interval |
| --- | ---: | --- |
| Retained versus projection | 0.03564% | [0.02561%, 0.04756%] |
| Retained versus frozen weights | 0.22843% | [0.18574%, 0.27613%] |
| Category oracle versus retained | 0.02888% | [0.02308%, 0.03512%] |

Intervals resample entire paired seed blocks 9,999 times with fixed seed 678901. They describe these disclosed histories under the assumed model; they are not a new confirmatory family, a reopened gate, or market-generalisation evidence. The conditional reductions above use different information sets for the category oracle, which is reported explicitly.

## Why the original 5% target is infeasible here

The Gaussian projection's delayed conditional risk is 0.010446172653. Future process noise alone contributes 0.010000000000. Even a hypothetical predictor additionally told the exact current state, but not the future innovation, could improve that projection by at most **4.27116%** on this observed-history average. A 5% reduction would require risk 0.009923864020, below the future-noise floor.

This ceiling is model-conditional expected risk averaged over the reconstructed histories. It is not a bound on each realised sample loss or a statement that 5% gains are impossible in other data regimes. With the actual shared information, the exact-Bayes ceiling is much tighter: approximately 0.036% over projection.

## Timing explains the identification–forecasting gap

| Origin delay | Bayes risk | Type-information risk | Value of perfect type information | Projection excess |
| --- | ---: | ---: | ---: | ---: |
| 0 | 0.024965762 | 0.013603764 | 54.48968% | 0.000000000 |
| 1 | 0.010456764 | 0.000011944 | 0.11423% | 0.000014743 |
| 2 | 0.010437805 | 0.000000118 | 0.00113% | 0.000000149 |
| 3 | 0.010437615 | 0.000000001 | 0.00001% | 0.000000002 |
| 4 | 0.010437613 | 0.000000000 | 0.00000% | 0.000000000 |

At the event origin, knowing the category would have substantial value, but the paired observed prefixes are identical and ordinary methods cannot identify it yet. Once subsequent observations arrive, type inference improves while current-state measurements already determine nearly the same next-return forecast. Remaining category uncertainty then has little predictive value. This explains why a strong historical type score need not imply a useful next-return MSE gain.

## Verification and provenance

All five forecast-arm paths, state probabilities and normalized log-probabilities matched the actual frozen v2 implementation numerically exactly. Every saved v2 CSV metric reproduced with maximum absolute error **0**. The decomposition's maximum arithmetic residual was **6.94e-18**. The zero-persistence control retains risk .01 and has zero state/type/approximation headroom.

The replay loaded source from commit `06a4ced5bd5efda3ec2dbc4f752117b412427bf6` and verified its simulator/benchmark dependencies. Instrumented execution tree: `f31e680f359c468f99fe02a1e55efc0cbf6fac4d`. Frozen CSV canonical-text SHA256 hashes are saved in the summary; the old artifacts remain unchanged. The suite passes 53 tests.

A post-run metadata wording correction renamed equality flags from `bitwise_equal` to `exactly_equal`, matching the actual `numpy.array_equal` check. The summary records that correction and the pre-correction hash. No numeric risk, score, prediction or original artifact changed; exact numerical equality does not claim byte-level equality of NaN payloads or signed zero.

## Scope and next experiment

These are known-time, known-parameter, single-Gaussian-event results. They establish neither operational detection nor financial usefulness, novelty or robust transfer. Posterior-averaged oracle risk integrates over the current category posterior; actual true-category realised losses are not samplewise lower bounds. Simply subtracting .01 from observed MSE would not yield this decomposition, which also integrates latent-state uncertainty.

Do not enlarge the architecture to recover a missing 5% gain in this regime. The most efficient next experiment is an explicitly declared oracle-headroom map over externally justified measurement-noise regimes, with all cells reported. Keep dynamics and the noise floor controlled, then measure whether delayed same-information headroom becomes practically material before building another predictor. Synthetic favourable cells would establish possibility under their assumptions, not that markets occupy those cells. A new model chosen from that map needs fresh final data.

## Artifacts

- [Exploratory plan](conditional-risk-plan.md)
- [Derivation](conditional-risk-mathematics.md)
- [Audit plan](conditional-risk-audit-plan.md)
- [Statistical review](conditional-risk-statistical-review.md)
- [Engineering review](conditional-risk-engineering-review.md)
- [Interpretation](conditional-risk-interpretation.md)
- [Full summary](../results/conditional-risk-v2/summary.json)
- [Moderate per-origin risks](../results/conditional-risk-v2/moderate.csv)
- [Zero-control per-origin risks](../results/conditional-risk-v2/zero.csv)

Run `python -m ripplenet.risk_report` to regenerate this document. Reconstructing into another directory is possible with `python -m ripplenet.risk_reconstruction --output work/risk-reproduction`; it repeats disclosed histories, not a fresh test. Existing directories are protected from overwrite. No paid resources were started.
