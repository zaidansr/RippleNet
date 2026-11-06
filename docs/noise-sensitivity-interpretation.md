# Interpretation of the completed observation-noise grid

Architecture work should stop for this forecasting branch as currently formulated. The fixed five-cell experiment finds no practically material same-information retention gain, even after making measurements substantially noisier. It does not justify searching additional synthetic settings until one produces a positive result.

The next scientific step is to establish a defensible data-generating mechanism, available information and observable target. That step may motivate a different, explicitly declared problem. These results do not establish that every disturbance-aware forecasting model is ineffective.

## What the complete grid shows

The [saved summary](../results/noise-sensitivity-v1/summary.json) reports all five prespecified cells on 128 new seed blocks, coupled across noise settings and event worlds. Only measurement covariance changed, through \(R=rQ\). The transition matrix, process innovation covariance, event amplitude law, balanced prior and shared known event time remained fixed.

Risks below are conditional expected squared-return errors per asset, averaged equally over the two worlds and delayed origins one through four, then across seeds. They integrate latent-state and future-innovation uncertainty under the declared model. They are not the realised test errors.

| \(R/Q\) | Retained risk | Projected risk | Projection excess | Retention gain | Five-cell-adjusted interval |
| --- | ---: | ---: | ---: | ---: | --- |
| 0 | .0100000000 | .0100000000 | approximately 0 | approximately 0% | Numerical zero |
| .25 | .0104421102 | .0104443765 | .0000022663 | .021699% | [.016045%, .028345%] |
| 1 | .0111986293 | .0112111406 | .0000125113 | .111597% | [.075588%, .152828%] |
| 4 | .0123745345 | .0123911679 | .0000166334 | .134236% | [.072975%, .227360%] |
| 16 | .0136048774 | .0136155460 | .0000106687 | .078356% | [.040775%, .134794%] |

The intervals are the reported 99% per-cell percentile-bootstrap intervals from the prespecified five-cell Bonferroni family. They are approximate simultaneous protection, not exact finite-sample guarantees. Entire seeds are the replication units; the five noise cells are not five independent sets of 128 observations.

All reported primary upper bounds are below 5%. The largest observed point gain is about .134%, at \(r=4\); it is not an estimate of a continuous-noise optimum. The data support a small conditional approximation effect at positive noise, but no practically useful gain under the declared target. At \(r=0\), tiny positive stored excesses are floating-point differences, not evidence against the exact zero-headroom control.

## Why the result is not just a future-noise problem

Three percentages describe different constraints:

| \(R/Q\) | Future innovation / retained risk | Category-oracle gain / retained risk | Perfect-current-state ceiling / projected risk |
| --- | ---: | ---: | ---: |
| 0 | 100.000% | approximately 0% | 0.000% |
| .25 | 95.766% | .025430% | 4.255% |
| 1 | 89.297% | .283065% | 10.803% |
| 4 | 80.811% | 1.610428% | 19.297% |
| 16 | 73.503% | 2.792931% | 26.555% |

The future process-noise contribution stays exactly .01 in every cell. Its share falls as noisier measurements increase state-estimation uncertainty. At \(r\ge1\), the perfect-current-state ceiling permits more than 5% improvement against projection, yet retaining the exact mixture still improves it by less than .14% at the reported point estimates.

Thus, the future-innovation floor alone does not explain the whole grid. More conditional state uncertainty is available to remove, but explicit mixture retention removes almost none beyond the once-projected Gaussian. In these settings, the Gaussian projection already preserves almost the same useful conditional future mean.

Greater measurement noise also does not monotonically increase retention value. The gain rises through the sampled \(r=4\) cell and falls at 16, while category-oracle headroom continues to rise. This is consistent with two competing effects: noisier observations leave more state uncertainty, but also change the evidence available to resolve category. The grid varies their joint consequence through one observation-noise parameter; it does not independently manipulate each inference channel.

## A mechanism-specific ceiling

The reported category-information fraction uses retained risk as its denominator. To compare the best category-informed forecast directly with projection, use

\[
G_{\mathrm{oracle\ versus\ projection}}
=1-\frac{\overline{R_{\mathrm{category\ oracle}}}}{\overline{R_{\mathrm{projected}}}}
=\frac{\overline B+\overline{E_P}}{\overline{R_{\mathrm{projected}}}},
\]

where \(B\) is posterior category-information risk and \(E_P\) is projection excess. Equivalently,

\[
G_{\mathrm{oracle\ versus\ projection}}
=G_{\mathrm{ret}}+(1-G_{\mathrm{ret}})G_{\mathrm{type}}.
\]

This derived point estimate remains below 5% in every reported cell; its largest is approximately **2.87% at \(r=16\)**. Even additionally revealing category does not rescue the 5% delayed-origin target on these averaged conditional histories. Revealing the entire current state could offer more, but that is a different information advantage and does not support an event-type mechanism claim.

This is a **post-hoc algebraic interpretation of the complete grid**, not an additional prespecified adjusted hypothesis test. The oracle integrates over the current posterior category probabilities; it is not a realised-loss lower bound within an actual-category row. Neither this derived ceiling nor the exact-Bayes same-information ceiling applies to all possible histories, unsampled settings or real markets.

## What can and cannot be concluded

Under the correctly specified generator, the retained mixture is already the exact conditional mean for the shared information. A larger causal model receiving the same information cannot improve population MSE beyond that Bayes mean. Architecture capacity therefore cannot explain away the missing 5% gain in these cells.

There are also restrictions on that conclusion. The experiment assumes known event time, known parameters, one isolated Gaussian impulse and fixed dynamics. It does not test unknown timing, persistent observation problems, heavy-tailed or dependent errors, overlapping events, parameter estimation or arbitrary histories. Those omissions do not justify adding them merely because the present mechanism failed its useful-effect target. Each would require an independently motivated new scientific question.

The experiment provides a narrow robustness check across this declared observation-noise grid, not generalisation to financial forecasting. Its small positive gains are expected consequences of approximating a specified posterior. They supply no novelty claim and no evidence of trading value.

## Most efficient next step: test whether a real information problem exists

Do not implement another network or extend the noise grid. First write a bounded, falsifiable problem specification anchored to an identifiable observation process:

1. Select an asset universe, sampling interval and **observable forecast target**, such as a declared reference-source next-period return. Explain how that reference is constructed; do not treat an inaccessible latent return as measured ground truth.
2. Identify recording errors with independently corroborated records or correction/audit information, where available. Separately specify what evidence supports a genuine move. The mere size of an observed residual is not a category label.
3. State what evidence is available at each forecast time. The current experiments show substantial event-origin oracle value that ordinary matched prefixes cannot access. An independently available contemporaneous recording-integrity signal could change that information problem; a later correction cannot be used retrospectively as a predictor.
4. Check whether observed error duration, propagation and measurement redundancy support a plausible mechanism with useful **same-information** forecasting headroom. Freeze that mechanism and target before selecting another model.

If such evidence exists, the smallest subsequent experiment is an **information-ablation study**: compare forecasting with and without that genuinely contemporaneous auxiliary evidence, using ordinary robust/state-space methods before a custom architecture. Give all competing full-information methods the same raw evidence; otherwise any gain confounds extra inputs with architecture. Keep reference labels separate from prediction inputs and use chronological evaluation. This would investigate the value of available observation-quality information, not retroactively validate the old RippleNet representation claim.

No external calibration or suitable auxiliary data has been established by this synthetic grid. A dataset and evidence audit should therefore precede that experiment. Changing the horizon, error law or information set is a new task that must be named and justified, rather than an unreported attempt to make the original result positive.

## Stop or pivot criterion

Abandon the present claim that retaining disturbance explanations yields a practically material next-return advantage in the frozen known-time Gaussian setting. Preserve its negative practical results as a reproducible benchmark.

Resume a forecasting-method branch only if an independently justified target and observation mechanism provide timely distinguishing evidence and sufficient useful headroom against credible same-information baselines. An oracle exceeding 5% is merely a necessary headroom check, not proof that an ordinary method can attain it. Use new frozen evaluation for any model selected after that justification.

If no defensible reference target, usable recording-error evidence or timely information advantage can be established, stop pursuing the forecasting-improvement claim. A clearly relabelled disturbance-identification or data-quality study may remain scientifically testable, but classification success alone must not be reported as forecasting success.

No new data or model runs, edits to other files, or spending were performed in writing this interpretation.
