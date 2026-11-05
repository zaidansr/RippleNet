# Independent v2 integration review

This is a post-results, read-only audit of the saved final artifacts and their integration code. No method, scoring setting, simulator, or final data was changed. No reserved simulation seeds were rerun.

## Finding

No scientifically material indexing, label-scoring, paired-aggregation, oracle-privilege, or implementation-provenance defect was found in the reviewed code and saved artifacts. This conclusion concerns the declared known-time synthetic diagnostic; it does not validate operational detection or real-market forecasting.

## Checks

- **Forecast alignment:** `known_time_forecasts` row t predicts latent x[t+1]. `history_experiment.py` compares against `truth.latent[1:]`. The five-origin slice starts at tau; its `[1:]` primary slice is exactly origins tau+1 through tau+4, targeting states tau+2 through tau+5. The secondary score includes tau. Scheduled event boundaries leave all five targets available.
- **Type labels and proper score:** category index zero is observation, one is state, matching the filter's log-probability columns. Negative log scores use normalized log weights directly, without clipping probabilities or taking `log(1-p)`. Binary Brier scores use the state probability and the corresponding zero/one truth. Frozen scores are correctly log(2) and 0.25.
- **Pairing:** losses first average the assets and selected forecast origins within a world. The two counterfactual category worlds are then averaged within each seed. Bootstrap inputs therefore contain 128 independent seed blocks, not 256 worlds or thousands of asset/origin replicates. Relative effects use a ratio of means. The zero condition reuses seed blocks and is not counted as extra replication.
- **Oracle privilege:** ordinary retained, projected, and frozen filters receive observations, known parameters, known timing, and the shared known amplitude scale. The true category only selects which already-computed conditional branch forecast is scored as oracle. Realized amplitude and latent states do not enter filter updates. Latent states and categories enter the scorer as intended.
- **Controls:** final saved checks show zero event-origin differences between ordinary arms; the maximum matched-prefix difference is 8.33e-17. Event-origin category probability is exactly one half. The zero-persistence condition has exactly zero forecasts and exactly one-half category probabilities. Future-invariance is covered by the separate pre-existing unit test; the final-run check itself is a matched-prefix check, not a new exhaustive proof of causality.
- **Source provenance:** the summary records source tree `f4e6acebd081130661b593daa6c11d9da0fab499`. The inspected method, runner, statistics, simulator, benchmark, and specification files have no diff from that declared tree. The recorded Python and NumPy versions are available. A tree hash and current-file agreement cannot independently reconstruct all historical execution actions, but no source mismatch was found.

## Saved-data reconciliation

Both final CSVs contain 256 rows: one observation-category and one state-category record for each of the 128 declared seeds 60000 through 60127. There are no missing or duplicate category/seed rows under these checks.

Recomputed CSV means match the summary for category MSE, five-origin MSE, event-origin MSE, retained/frozen type NLL and Brier scores, and balanced MSE. The largest absolute discrepancy was 6.94e-18, consistent with floating-point accumulation order. These checks used saved data only; they did not regenerate final simulations or refit anything.

## Limits on interpretation

The retained-versus-projection primary point effect is approximately -0.00125%, with an adjusted interval of approximately [-0.14487%, +0.16419%]. This does not establish any practical forecasting advantage, including the prespecified 5% target. The retained-versus-frozen gain is approximately 0.33755%, and improved type log scoring shows that later observations update mechanism probabilities usefully under the assumed model. A measurable weighting effect does not establish a useful representation advantage over the independently evolved projected Gaussian.

The oracle's slightly higher realized delayed-origin MSE than the retained arm is not an implementation defect: its expected squared-error optimality does not impose the same ordering on every finite sample. It must not be interpreted as evidence that withholding true categories is inherently better.

The experiment guarantees one event, supplies its exact time and the correct amplitude distribution, and uses known linear-Gaussian dynamics. It provides no independent evidence of transfer to unknown timing, false alarms, estimated dynamics, other contamination laws, or financial markets. The result should not reverse the negative v1 operational-feasibility conclusion or support a novelty claim.
