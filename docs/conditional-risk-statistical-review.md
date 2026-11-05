# Statistical audit: exploratory conditional-risk reconstruction

This audit reads saved reconstruction rows and independently recomputes their summaries. It does not rerun models, tune settings or generate new test data. All 128 histories were already disclosed in v2; this analysis cannot reopen its confirmatory gate.

## Audit checks

Each condition has exactly 1,280 unique `(seed, category, delay)` rows: seeds 60000–60127, both coupled categories, and delays 0–4. There are 128 independent seed blocks, not 1,280 independent observations; the zero condition shares those blocks.

Independent calculations reproduced all nine quantities at all five delays, all nine delayed-window means and descriptive intervals, and all four ratio-of-means estimates and intervals. Within each seed, the delayed window weights both worlds and origins 1–4 equally. Bootstrap resampling uses complete seed blocks, 9,999 replicates and seed 678901. These are raw descriptive 95% percentile intervals, without retroactive insertion into v2's prespecified family.

All row values are finite and nonnegative. Verified rowwise:

- `bayes = future + within_type + type_information`;
- `projected_total = bayes + projected_excess`;
- `frozen_total = bayes + frozen_excess`;
- `category_oracle = future + within_type`;
- `bayes - category_oracle = type_information`.

Maximum identity discrepancy is 6.94e-18 under moderate persistence and zero under zero persistence. Every future-noise term is exactly .01. In the zero control, Bayes risk is .01 and all within-type, category-information and approximation-excess terms are exactly zero.

Current frozen CSV canonical-text SHA256 digests match reconstruction metadata. Code inspection confirms that replay compares complete forecast and type arrays with the frozen implementation using `np.array_equal(..., equal_nan=True)` and checks every original CSV metric. The run records maximum frozen-metric discrepancy zero. This means exact numerical array equality, not bytewise identity. Independently verified the disclosed post-run equality-label correction against the preserved original summary and its canonical-text hash: only equality labels and the disclosure were changed, with all numerical values unchanged. This audit did not itself regenerate the paths.

## What the decomposition shows

For delayed origins 1–4 under moderate persistence:

| Quantity | Estimate | Descriptive 95% interval |
| --- | ---: | --- |
| Exact Bayes conditional risk | 0.01044245 | [0.01044185, 0.01044310] |
| Projection excess conditional risk | 0.0000037235 | [0.0000026754, 0.0000049688] |
| Exact-over-projection conditional improvement | 0.03564% | [0.02561%, 0.04756%] |
| Exact-over-frozen conditional improvement | 0.22843% | [0.18574%, 0.27613%] |
| Additional category-oracle improvement over exact filtering | 0.02888% | [0.02308%, 0.03512%] |
| Future-innovation share of Bayes risk | 95.7630% | [95.7570%, 95.7685%] |

Ratios use aggregate numerator and denominator means. The category oracle is posterior-weighted at the same observed history, not selected using the realized category; its headroom is therefore a nonnegative conditional-information quantity.

At delay zero, category-information risk is 0.01360376, but no permitted observation distinguishes the categories then. By delay one it is approximately 0.00001194, and it decays further. Once distinguishing observations arrive, little next-return headroom remains. A persistent improvement in category log score consequently need not yield meaningful forecasting improvement.

The reconstructed positive conditional projection gain does not contradict v2's slightly negative realized-MSE estimate: the conditional identity integrates future and latent-state uncertainty, whereas realized losses retain sampling noise. They are different estimators. Neither result provides evidence for the 5% practical target. The conditional decomposition instead indicates that projection disagreement is intrinsically small in the tested histories under the assumed model.

There is also a broader information bound. Average projected conditional risk is 0.01044617; even an oracle revealing the current latent state cannot predict the independent future innovation and therefore has risk at least .01. Its maximum possible relative improvement averaged over these disclosed histories is `1 - .01 / .01044617 = 4.27116%`, already below 5%. This is a conditional-expected-risk bound under the stipulated model, not a bound on realized sample MSE or a universal population bound across unobserved histories. The same-information exact Bayes gain of 0.03564% is much tighter.

## Limits and conclusion

The future-noise floor is per asset, `tr(Q)/3`, not `tr(Q)`; observation noise is not added again to the latent-return forecast target. Noise-subtracted ratios would answer a different question and cannot rescue the original total-MSE threshold. Their denominators vanish in the zero control and must remain undefined rather than receive an epsilon.

These descriptive intervals condition on an exactly specified Gaussian generator, known event time and parameters. They provide no independent replication, false-alarm assessment, distributional generalisation, financial utility or novelty evidence. The disclosed v2 practical-benefit failure remains unchanged. Any setting or model selected using this explanation requires new development and final data.
