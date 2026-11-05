# Independent statistical audit of experiment v2

Audited the saved final CSVs and summary against `experiment-v2.md`. This audit recomputed statistics from saved losses only; it did not generate new paths, tune methods, or perform model selection using final seeds.

## Reproduction checks

- Both condition CSVs contain exactly 256 rows: the 128 unique seeds 60000–60127, each with one observation-error and one state-shock row. These two worlds form one paired seed block. The zero condition shares those blocks and adds no independent replications.
- Recomputed all five moderate-condition contrasts directly from the CSVs. Balanced losses first average the two event categories within each seed. Relative improvements are ratios of loss means, not means of individual ratios. Type-log-score improvement is an absolute paired loss reduction.
- Recreated 9,999 whole-seed bootstrap samples independently using seed 567890. Raw percentile bounds and adjusted bounds at quantiles .005 and .995 reproduce the summary to numerical tolerance. The latter use the declared five-contrast Bonferroni family.
- Per-row delayed-window losses satisfy the identity `(5 * five_origin_loss - delay0_loss) / 4`. Saved posterior probabilities reproduce Brier scores and, where representable without saturation, negative log scores.
- In the zero-persistence control, all saved type probabilities equal .5 and all forecasting arms have identical losses. All five contrasts and their intervals are exactly zero.

## Moderate-persistence conclusions

Intervals below are the declared adjusted intervals. Relative figures are percentages, whereas log-score reduction is in nats.

| Contrast | Improvement | Adjusted interval | Interpretation |
| --- | ---: | --- | --- |
| Retained versus projected forecast | -0.00125% | [-0.14487%, +0.16419%] | No positive advantage established; the 5% practical target is excluded under this approximate conditional inference. |
| Retained versus frozen forecast | +0.33755% | [+0.18393%, +0.50789%] | Positive effect supported, substantially below the 5% practical target. |
| Retained versus frozen type log score | +0.47489 nats | [+0.39257, +0.54427] | Evidence-responsive weights improve type probabilities relative to fixed prior weights. |
| Observation-category forecast versus projection | +0.00630% | [-0.15846%, +0.19249%] | Lower bound exceeds -5%; harm guard passes. |
| State-category forecast versus projection | -0.00881% | [-0.22854%, +0.21469%] | Lower bound exceeds -5%; harm guard passes. |

The practical representation gate fails. Both secondary mechanism contrasts are positive, but this does not supply the missing benefit over Gaussian projection. The supported interpretation is that updating competing explanations is useful compared with deliberately frozen weights in this specified model; retaining their full representation supplies no established practically important forecasting benefit over the projected approximation.

## Limits

These are approximate bootstrap intervals conditional on a correctly specified Gaussian generator and shared privileged intervention timing. They do not establish robustness to unknown timing, false alarms, price-derived corruption, estimated dynamics, other noise laws, or markets. Fresh seeds establish repeatability within the generator, not distributional transfer. The clean false-alarm regime is outside this conditional two-type experiment.

This audit verifies saved aggregation and inference, not every detail of the simulator or the historical timing of protocol publication. An oracle's slightly worse delayed-window sample MSE is compatible with finite-sample fluctuation; population optimality does not require winning every finite realization. Do not select a favorable delay or new scenario from these final results and call it another prespecified test.
