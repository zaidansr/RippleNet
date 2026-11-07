# Fresh-period delayed-start market control

**Attribution and findings license:** Binance Vision BTCUSDT daily individual-trade archives, [source](https://data.binance.vision/), [dataset terms](https://github.com/binance/binance-public-data/blob/master/TERMS_AND_CONDITIONS.md). Data-derived findings in this document are distributed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Changes: computed paired targets, fitted forecasts, coverage, losses and resampling diagnostics. No raw trades are reproduced, endorsement implied or independent code relicensed.

## Finding

In the fresh October test period, the origin-start target shows **13.44% lower MSE** than its validation-selected constant baseline. Starting the target one trade later reduces that gain to **3.24%**. The prespecified common-zero absolute improvement contrast is positive under the exploratory paired bootstrap. **MAE worsens for both targets:** approximately **0.62%** and **4.14%**, respectively.

The result is consistent with substantial predictability concentrated near the first future trade, while some recorded-return MSE skill remains for the delayed target. It does not prove bid/ask bounce, recording error, efficient-price predictability or an executable trading advantage.

## Fresh data and frozen execution

Use the 30 consecutive BTCUSDT dates September 16–October 15, 2017, disjoint from the earlier study. Training: September 16–25; validation: September 26–30; protected test: October 1–15. All files passed the fixed download, hash, integrity and schema checks without substitution. The [provenance record](market-delay-provenance.md) contains attribution, applicable conditions, byte bounds and hashes; raw trades remain private.

| Partition | Days | Recorded trades | Common eligible origins per target |
| --- | ---: | ---: | ---: |
| Training | 10 | 81,689 | 81,529 |
| Validation | 5 | 51,928 | 51,848 |
| Protected test | 15 | 131,112 | 130,872 |

The paired count is N-16 per day. Five origins lack full history; A has ten censored targets plus one additional complete origin excluded for alignment, while B has eleven censored targets. These are disclosed coverage counts rather than public per-origin forecasts. No outcomes were invented for excluded origins.

The [plan](market-delay-plan.md) was published as `1cdfb3d0fe3eed36e1892d10c4c7c78ec84be3c6` before trade-body inspection. Executable source was published as `e956fb0ae62f37266ddbb07239e18893142a8bf9`, tree `1c4116104ea1161c0d4b291624218a9cd3a269d3`, before development execution. Both target-specific [selections](../results/market-delay-v1/selection.json) were published as `7dd78b308a2ce059e5466ba52f18f9bd7faf0c09` before October prices were parsed. The [test artifact](../results/market-delay-v1/test.json) pins that selection and executable hashes. No refit, target change or additional period followed the test outcomes.

## Matched information and target definitions

Both predictors use the same five adjacent trade log returns ending at origin k. Target A is log(P[k+10])-log(P[k]); target B is log(P[k+11])-log(P[k+1]). The future starting price of B is label information only, never an input. Both pipelines use exactly the same origins and identical training feature scalers, with separate target means, coefficients and validation choices.

Each pipeline selected alpha zero (weighted AR(5) least squares) from the frozen ridge grid, and the target-specific training-mean constant from the frozen baseline set. Fits and population scaling use training only, with equal total weight per training day. Validation selects settings without refitting; primary test risks average daily mean losses equally. Definitions, estimands and caveats are derived in the [mathematics](market-delay-mathematics.md).

## Held-out risks

| Target | Predictor | Equal-day MSE | Equal-day MAE |
| --- | --- | ---: | ---: |
| Origin-start A | AR(5) | 0.000004608346 | 0.001394037 |
| Origin-start A | Selected constant | 0.000005323779 | 0.001385391 |
| Delayed-start B | AR(5) | 0.000005150803 | 0.001442739 |
| Delayed-start B | Selected constant | 0.000005323206 | 0.001385355 |

Zero and scaled-lag-mean baselines, pooled-origin risk, all daily MSE/MAE values and fitted coefficients are also disclosed in the artifacts. The origin-start model wins daily MSE versus its constant on 15/15 test days; delayed-start wins on 14/15. These correlated days are not independent binomial trials.

| Prespecified primary contrast | Estimate | Adjusted exploratory interval |
| --- | ---: | ---: |
| A MSE reduction versus selected baseline | 13.438% | [9.104%, 16.216%] |
| B MSE reduction versus selected baseline | 3.239% | [0.929%, 5.177%] |
| (zero-risk minus candidate-risk) A minus B | 5.4303e-7 | [3.7356e-7, 7.0965e-7] |

The third contrast is in **squared-log-return units**, not percentage points. It uses a common zero-return reference to avoid switching selected baselines or ratio denominators. The descriptive difference of the two selected-baseline percentage reductions is 10.200 percentage points; it is not the primary contrast or a causal share attributable to price noise.

Intervals are the frozen 98.333333% percentile intervals for three contrasts, using 9,999 identical paired noncircular three-day block resamples, seed 190012. Fifteen adjacent days provide few blocks. Endpoint underweighting and ratio nonlinearity shift bootstrap centers: the gain distributions' means are about 0.310 and 0.257 percentage point below the two empirical estimates. No recentering or method adjustment was made. These diagnostics do not guarantee familywise coverage, broad statistical reliability or market generalisation.

## What this distinguishes, and what it does not

The smaller delayed-start MSE gain weakens an explanation that all observed predictive value is stable across the next ten trades. However, the remaining delayed-start gain also weakens an explanation based solely on sharing the origin price. Neither statement identifies a causal mechanism. The targets share nine increments but exchange the first future increment for a later one; legitimate short-lived predictability, changing noise, price reversal and the behavior of separately trained pipelines can all affect the comparison.

The same-origin information boundary rules out supplying P[k+1] to the delayed predictor. Matched coverage avoids comparing different sets of origins. Target-specific training avoids a model-transfer failure caused by applying coefficients trained for a different label. These controls improve interpretation, but do not turn the task into an isolated manipulation of bid/ask noise.

The gains are **loss-specific**. MAE is 0.624% worse for A and 4.142% worse for B versus their selected constants. A mean-squared-error improvement is neither uniform forecast superiority nor economic value. No spread, fee, fill, midquote, independent recording-error label or efficient-price ground truth is measured. No practical market margin or synthetic 5% gate is used.

The predictor is itself a classical AR baseline. This comparison does not establish superiority over a broader collection of autoregressive, state-space or quote-aware methods. No new baseline is added after these outcomes; future comparisons require their own frozen design.

This single asset's early listing-period archives may have been revised after 2017. Source chronology-aware processing does not verify original publication or receipt availability. No neural RippleNet is fitted and no cause-specific ablation, novelty or profitability claim is supported. Earlier numerical findings remain unchanged.

## Verification and research decision

The complete suite passes **108 tests**, including seven new paired-target fixtures. They cover exact endpoints, common masks, future-label exclusion, identical feature scalers, development-only dates, no refit, protected-source guards, shared bootstrap pairing and the absolute common-reference contrast. All 30 ZIP/CSV hashes and N-16 counts match acquisition records; the test pins the unchanged selection and source files. Three subagents supplied acquisition provenance, mathematical review and the [independent results audit](market-delay-review.md).

The result warrants investigating recorded-price microstructure and a stronger observable reference before architecture growth. The most discriminating next empirical comparison would use a separately frozen period with **contemporaneous trades and bid/ask quotes**, if a rights-cleared source with auditable timing can be established: compare trade-return predictability with quote-midpoint-return predictability using matched origins and the same information. A disappearance of skill only for the midpoint would be consistent with a trade-price component, but midpoints themselves are imperfect observations and timing/availability must be audited. No suitable quote source is claimed to have been acquired here.

Do not extend the delay grid on this disclosed test set and call the strongest setting confirmation. A new period or observation source is needed for another protected evaluation.

## Reproduce

With the documented permitted private local archives and checksum sidecars:

```sh
python -m unittest discover -s tests -q
python -m ripplenet.market_delay development --data-dir PRIVATE_DATA_DIRECTORY --output work/delay-reproduction
python -m ripplenet.market_delay test --data-dir PRIVATE_DATA_DIRECTORY --output work/delay-reproduction
```

Development refuses an existing output directory; test refuses overwriting results and checks frozen source/dates. Reproduction repeats disclosed observations, not a new independent experiment. No paid resources, cloud computation, accounts, provider contact or spending were used.
