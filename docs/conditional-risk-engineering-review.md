# Conditional-risk replay: independent engineering audit

## Scope and finding

No scientifically material indexing, posterior-oracle-conditioning, aggregation, or source-preservation defect was found. This audit inspected the reconstruction and filter code, the saved CSVs and summaries, the actual frozen-source copy, and Git provenance. It recomputed summaries and descriptive bootstrap intervals from saved rows only. It did not rerun simulation seeds or modify any model, scoring implementation, or original result.

The reconstruction is explicitly post hoc on the 128 disclosed v2 seed blocks. Its intervals describe variation of model-conditional risk functions across those replayed histories. They are not new confirmatory forecast-performance intervals.

## Implementation and provenance

- The original function loaded by the runner comes from published code commit `06a4ced5bd5efda3ec2dbc4f752117b412427bf6`. The saved `work/frozen-history-v2.py` text exactly matches that commit's `ripplenet/history.py`; its canonical-text SHA256 is `0eacca7e969dad6e9cc67e98f761d8be2c999e8778d6de8a4051cb8e79cd2a85`.
- The runner checks that its simulator and benchmark dependencies agree with the frozen code. Inspection found no such dependency change. The original v2-final artifacts and risk/filter code also had no diff from the recorded replay execution tree `f31e680f359c468f99fe02a1e55efc0cbf6fac4d` at audit time.
- The comparison loop checks every original forecast path, state-probability path, and normalized-log-probability path, not just the five scoring origins. The saved run reports exact numerical agreement and zero maximum error across every reproduced numeric v2 CSV field.
- This is numerical array equality, including matching NaN positions, rather than byte identity. The post-run metadata correction now uses `exactly_equal` and explicitly records this distinction. Independently reversing only that correction, its explanatory note, and four equality-key renamings reconstructs the original summary exactly. The preserved original-summary canonical hash matches the correction record. No numeric value changed. `source_tree_at_run` appropriately continues to identify the executed code before this label-only patch.
- Current hashes of the original v2 CSV canonical text match both hashes saved by the reconstruction. The runner also checks those hashes before and after its replay.

The full historical execution cannot be independently proved from aggregate outputs alone. In particular, this audit did not regenerate full forecast paths. The saved equality flags are supported by direct inspection of the runner's comparisons and by independent scalar/CSV reconciliation, rather than an additional end-to-end seed replay.

## Indexing and conditioning

The selected slice is origins tau through tau+4; the delayed summary uses origins tau+1 through tau+4. Row t remains a forecast of latent x[t+1]. Future process variance is therefore tr(Q)/n; future measurement variance is correctly excluded.

At each origin the within-type term uses current posterior weights and conditional state covariances. The type-information term uses the posterior-weighted separation of conditional next-state means. The category-oracle conditional risk is future plus within-type risk. It does not select the actual category, although the replay's row label records which counterfactual observation history generated the posterior.

Projected and frozen excesses are squared distances from the retained conditional mean, normalized by asset count. They are model-conditional expectations, not realized squared-error differences. Their nonnegativity is an identity under the stipulated model; a positive descriptive interval is not a new confirmatory superiority test.

## Independent saved-data checks

Each persistence setting contains 1,280 unique rows: 128 declared seeds times two coupled category worlds times five origins. Every expected seed/category/delay combination is present exactly once. All terms are finite and nonnegative within the stated numerical tolerance.

Independently recomputed checks include:

- Bayes = future + within-type + type-information.
- Comparator total = Bayes + comparator excess.
- Posterior-averaged category oracle = future + within-type.
- All per-origin means, delayed whole-seed means, four ratios of means, and their saved descriptive percentile-bootstrap intervals.

The maximum risk-identity residual is 6.94e-18. The maximum summary mean/ratio discrepancy is 4.24e-22; the maximum interval-endpoint discrepancy is 1.73e-18. Aggregation treats the entire seed, including its two worlds and multiple origins, as one resampling block. Neither category worlds nor delays are counted as independent samples.

At delay zero, both ordinary comparator excesses are zero. In the zero-persistence control, within-type, type-information, and comparator excess risks are zero; all total risks are 0.01.

## Scientific reading and limits

For the delayed moderate-persistence histories:

- Future innovation accounts for approximately 95.763% of retained Bayes risk.
- Projecting once adds approximately 3.72e-6 risk, corresponding to a 0.03564% model-conditional improvement from using the retained mixture instead.
- Frozen weighting adds approximately 2.39e-5 risk, corresponding to a 0.22843% model-conditional improvement from retained weighting.
- Knowing the actual category would remove approximately 3.02e-6 posterior-averaged risk, or 0.02888% of retained risk.

These conditional quantities need not numerically equal the previously published finite-sample realized MSE differences. That distinction does not imply an inconsistency or justify replacing the original held-out findings.

The future-noise floor also gives a useful post-hoc bound on these histories: even perfect knowledge of the current latent state could lower the projected arm's mean conditional risk by no more than `1 - 0.01 / 0.010446172652966022`, approximately 4.271%. Thus a 5% improvement is unavailable in this particular delayed-origin setting under its specified independent future-noise law. This is not a general bound for other generators or targets.

The large delay-zero type-information term rapidly disappears once later observations arrive. Together with the tiny retained-versus-projection excess, this supports limited forecasting headroom in the declared scenario. It supplies no evidence of real-market transfer, unknown-time detection, robustness to misspecification, or methodological novelty. Any changed generator motivated by this audit requires a separately declared experiment and must be presented as informed by these disclosed findings.
