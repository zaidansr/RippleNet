# Results audit

**Historical initial audit.** A subsequent benchmark now supplies new synthetic results: see [experiment v1 findings](experiment-v1-results.md). The undetermined verdicts below describe the evidence available before that run, not its current outcome.

No pre-existing RippleNet result tables, trained model, ablations, or seed-level losses were located in the searched workspace files, connected Drive search, or accessible zaidansr repository list. This is a bounded search, not proof that no results exist anywhere. The repository was newly created during this work.

## Verdict on the requested scientific conclusions

| Question | Current verdict | Evidence still required |
| --- | --- | --- |
| Is improvement meaningful? | Undetermined; no comparative forecasting losses supplied or found | Absolute and relative loss differences against a frozen credible comparator |
| Is it statistically reliable? | Undetermined | Independent paired run losses, uncertainty estimates, prespecified claims and margins |
| Does the model generalise? | Unestablished; no candidate has been evaluated | Fresh generators/dynamics and later real-data validation |
| Does an ablation support the mechanism? | Untested | Matched-capacity, equal-information mechanism ablations |
| Do results justify the conclusion? | No claim of predictive superiority is currently justified | Complete held-out experiment and appropriately limited conclusion |

## What the new diagnostic actually shows

`results/diagnostic.json` is newly generated implementation evidence, not pre-existing experimental results. Under moderate persistence, the maximum observed-prefix difference and causal forecast-prefix difference are both zero. State propagation matches the analytical identity to approximately 3.3e-17. With zero persistence, the constructed observation paths match throughout and subsequent state differences vanish. These checks support the paired-world construction and causal indexing only.

The diagnostic uses one seed, no fitted candidate, no loss comparison, no held-out model selection, and no ablation. Consequently it establishes none of the five performance claims above. Passing unit tests is also not a statistical significance test.

## Define the estimand before evaluation

Let b index independent simulation runs, e an event, c its category, j an asset, and k=0,...,4 a forecast-origin delay. Let t_e be the event index. Define an individual squared error

    error[b,e,k,j] = (prediction[b,t_e+k,j] - latent[b,t_e+k+1,j])**2.

Average over the three assets, five origins, and events within each category to obtain one loss L[b,c] per independent run. Use equal asset scaling in the initial simulator; if scales differ, prespecify weights or training-only standardisation. State whether aggregation weights runs equally or weights events equally. Exclude incomplete windows in advance, not based on the realised loss.

For method M and development-selected baseline B, calculate paired differences D[b,c]=L[B,b,c]-L[M,b,c]. Positive means improvement. Report mean absolute differences and the relative reduction 1-mean(L[M])/mean(L[B]); do not silently replace this with an average of per-run ratios. Resample entire runs as paired blocks for bootstrap intervals. Assets, timesteps, paired counterfactual worlds, and events within the same simulated path are not extra independent replications.

## Reliability and decision thresholds

Thirty seeds is an initial budget, not a precision guarantee. Estimate interval width on development runs. Freeze the final sample size and test seeds before opening final losses; do not stop collecting results when significance appears.

A confidence interval excluding zero supports a positive average difference under its assumptions; it does not show that improvement exceeds the practical 5% margin. Likewise a point-estimate loss increase below 5% does not establish no important harm. Report uncertainty relative to those margins. If either of two event categories can trigger success, control multiplicity or label the result exploratory. Document every configuration tried and select the comparator using development data only.

## Efficient discriminating experiment

Use the paired-world construction across observation/state interventions and zero/moderate persistence. Report each forecast-origin delay. Compare a future full causal model with an observation-only version and a generic adaptive-noise model matched for information, tuning and compute; include an appropriately specified privileged diagnostic separately.

- If the privileged diagnostic cannot improve losses, the tested setting has little demonstrated headroom.
- If it improves but the causal method does not, information/identification limits or an ineffective estimator remain explanations.
- If a no-separation ablation matches the full method, generic adaptation is sufficient to explain the gain.
- If the full method gains only after observations diverge and loses its gain under mechanism ablation, that supports its use of the assumed temporal signature.
- If gains vanish under price-derived corruption or changed dynamics, generalisation remains simulator-specific.

This matrix separates explanations more efficiently than increasing network size or repeating only the same generator.
