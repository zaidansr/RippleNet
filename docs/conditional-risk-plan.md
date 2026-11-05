# Exploratory conditional risk reconstruction

This analysis is chosen after v2 results are known. It is not a new independent test, a replacement confidence claim, or permission to tune on the disclosed histories. No model, observation distribution, target, seed set, or v2 decision changes.

## Question

Does the absence of a useful retained-mixture forecast gain reflect nearly identical conditional forecast means, or differences obscured by realised future innovations? Decompose exact conditional MSE into future innovation variance, remaining within-type state uncertainty, uncertainty about type, and approximation excess risk.

For observed history H, n assets, exact current-state mixture mean m and covariance C, the predictive Bayes mean is mu=A m and covariance V=A C A'+Q. For any H-measurable forecast g, conditional mean squared error per asset is trace(V)/n+||g-mu||^2/n. The type-uncertainty contribution is pi_O*pi_S*||A(m_S-m_O)||^2/n. Posterior-averaged category-oracle risk equals the future innovation plus within-type state terms; no realised-category loss is used as a samplewise lower bound.

## Reconstruction and safeguards

- Reconstruct only v2 final seeds 60000–60127, with exactly the frozen moderate and zero-persistence generators and Gaussian event law.
- Retrieve the original uninstrumented history filter from public pre-evaluation commit 06a4ced5bd5efda3ec2dbc4f752117b412427bf6. Compare every forecast arm and normalized type log-probability path with the instrumented filter, including pre-event NaNs. Require exact numerical equality.
- Verify the original benchmark/simulator dependency files have not changed, and compare reconstructed MSE, five-origin MSE, event-origin MSE, type NLL, Brier and saved probabilities against the frozen CSVs. Record canonical-text SHA256 hashes of those CSVs.
- Added instrumentation exposes posterior covariance components only. It must not change any existing prediction, weight update or data path. No latent states or true category enters ordinary risk calculation.
- Verify pointwise decomposition identities, nonnegativity within floating tolerance, zero-persistence risk=.01 with zero headroom, and unchanged causal behaviour in fixture tests.
- Refuse to overwrite any original or new result directory. Preserve all v1/v2 result files.

## Outputs and interpretation

Save per-seed/category/delay risk terms for origins tau,...,tau+4 and means by delay. Also aggregate delays1–4 within each category and then equally across paired worlds to obtain one block per seed. Report future-innovation fraction, projection excess relative to projection risk, frozen-weight excess relative to frozen risk, and type-information value relative to Bayes risk. Ratios use pooled means, not averages of per-case ratios.

If bootstrap intervals are included, resample the same 128 paired seed blocks using fixed seed 678901 and 9,999 replicates. They describe variation across these disclosed histories under the assumed model; they are not a new confirmatory family or a reopened 5% gate.

The mathematics is a known-model identity. Small conditional excess directly demonstrates close forecast means for these histories, while a large future-innovation term explains why realised differences are noisy. Neither result establishes an unknown-time detector, a real-market mechanism, economic value, or novelty. Publish even if the decomposition offers no new practical opportunity. All computation remains local and requires no spending.
