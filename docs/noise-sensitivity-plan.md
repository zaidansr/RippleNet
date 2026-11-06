# Fixed observation-noise sensitivity: five reported cells

This is a complete synthetic sensitivity study informed by the previous negative experiments. Its grid is declared before the new seeds are examined. It is not market calibration, model optimisation, or confirmation of a selected favourable regime.

## Fixed design

- Measurement/process variance ratios R/Q: **[0, .25, 1, 4, 16]**, meaning R is the ratio times .01 I. The reference cell .25 reproduces the previous data-generating settings with new seeds.
- Keep Q=.01 I, the original moderate three-asset transition A, 180 retained observations, 128 burn-in steps, one Gaussian impulse with covariance .25 I, balanced event-category prior, and event-time law unchanged.
- All methods know the true intervention time and parameters. Use the existing exact retained mixture and independently evolved once-projected Gaussian; change no architecture or fitted parameter.
- Use **128 new seed blocks, 70000–70127**, shared across all five cells and both event worlds. There is no training, tuning, additional sampling after viewing results, or winner selection.
- Couple the latent process, event time/amplitude and underlying measurement-normal draws across cells. Rescale measurement noise only. Check and record this coupling.
- Retain origins tau,...,tau+4; the primary window remains delays 1–4 with equal asset/world weights inside each seed.

## Quantities and intervals

For every cell report mean conditional Bayes and projection risk, absolute projection excess, mean realised next-return MSE, and the following ratios of aggregate means:

1. Same-information exact retention gain: mean(projection excess)/mean(projection total).
2. Privileged category-information headroom: mean(type-information risk)/mean(Bayes risk).
3. Future innovation fraction: mean(future risk)/mean(Bayes risk).
4. Perfect-current-state information ceiling: 1-mean(future risk)/mean(projection total).

These distinguish information sets and cannot be substituted for one another. Conditional Bayes superiority is a mathematical identity under the generator; effect size is the empirical question. A high percentage gain at a noisy cell need not mean lower absolute risk.

Use 9,999 bootstrap resamples, fixed seed **789012**, resampling the same 128 whole seed blocks with identical indices across all cells. Report descriptive pointwise 95% intervals for the ratios. For the primary retention-gain curve, also show five-cell Bonferroni intervals using per-cell alpha=.05/5, i.e. 99% individual percentile intervals. Coverage is approximate. Report whether any complete adjusted interval exceeds the 5% practical reference, without claiming an optimal or market-relevant setting.

## Controls and provenance

R=0 is valid because Q keeps the innovation covariance positive definite. At delays 1–4, exact observations reveal the current state, so all point forecasts coincide and conditional risk is .01 with no remaining state/type/approximation contribution (within numerical tolerance). Type probabilities may still identify the historical cause; they need not remain .5. Realised MSE remains random.

Verify identical ordinary-process and intervention paths across R; matched observed prefixes across event worlds; no future-observation access; risk decomposition and nonnegativity; the perfect-state ceiling dominates same-information retention gain. Save full matrices, versions, source tree and actual source-file hashes. Protect previous outputs and refuse to overwrite the new directory.

Save one per-origin CSV for every cell (1,280 rows per cell), plus the complete summary, per-seed paired aggregates implicit in those records, all results and independent audits. Freeze code before running the specified seed set. If a later correction affects numerical results, disclose it rather than silently replacing provenance.

## Figure and decision

Publish a standalone scientific figure made with Matplotlib: a categorical x-axis showing all five R/Q cells, a retention-gain panel with descriptive/five-cell intervals and a horizontal 5% reference, and an absolute-risk panel showing Bayes, projected and innovation-floor risks. Show known-time/synthetic scope and 128 paired blocks in the caption. No favourable-cell zoom or omitted cell.

The plotting runtime is isolated from the experiment runtime. Record plotting versions separately; it must not regenerate model results. No external dataset, cloud compute or paid resource is required.

Even if a cell shows useful conditional headroom, this establishes only possibility under its assumed observation quality. Any operational model, parameter estimation, unknown timing, real-data calibration or selected setting requires new justification and separate evaluation. No architecture expansion is authorised merely by selecting the largest synthetic gain.
