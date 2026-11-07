# Real recorded BTCUSDT forecasting results

**Attribution and findings license:** Binance Vision daily individual-trade archives, [source](https://data.binance.vision/), [dataset terms](https://github.com/binance/binance-public-data/blob/master/TERMS_AND_CONDITIONS.md). This document's data-derived findings are distributed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Changes: computed features, forecasts, coverage, losses and uncertainty; no raw trades reproduced. No endorsement or change to independent code licensing is implied.

## Finding

The first real-data benchmark improves held-out recorded-return **MSE by 7.98%** against the validation-selected constant baseline. Its **MAE is 0.95% worse**. This is an AR(5) linear benchmark on a retrieved early-period trade archive, not a test of a trained neural RippleNet or the observation-error versus genuine-shock mechanism.

## Data and protected chronology

All 30 consecutive BTCUSDT dates, August 17–September 15, 2017, were acquired from the official daily spot individual-trades archives within frozen size limits. Every publisher checksum and ZIP integrity check passed. Raw data remain outside GitHub; [public provenance](market-data-provenance.md) records sources, terms, dates, hashes and bounds. The previously inspected August 17 sample was assigned training only. Additional dates were fixed before their prices/outcomes were inspected.

| Partition | Dates, inclusive | Days | Recorded trades | Common eligible origins |
| --- | --- | ---: | ---: | ---: |
| Training | August 17–26 | 10 | 47,290 | 47,140 |
| Validation | August 27–31 | 5 | 21,890 | 21,815 |
| Protected test | September 1–15 | 15 | 95,128 | 94,903 |

Each day resets features and targets. The first five origins lack the complete lag history; the last ten have incomplete future targets. These exclusions are counted and disclosed per day, not silently converted to zero outcomes. The study stores common eligible arrays and coverage counts, not a public forecast record for every excluded origin. No additional filtering or date substitution occurred.

The [plan](market-study-plan.md) was published as `ad52381d89716c20076d07333f8656c97fa415cd`. Executable source was published as `329a7d86fdf10f6afec216ae981a4c5ca46d06c0`, tree `36274c3d9197502dd71e50a6d724f114d6c5edfc`, before development execution. That source publication also corrected protocol text encoding, without changing dates, parameters or split. The development [selection](../results/market-v1/selection.json) was published as `ce52f2cb3312509778828dcff04ca7dbf3ffd203` before protected test prices were parsed or losses evaluated. The test output pins that exact selection's SHA256 and matching source hashes.

## Models and estimand

Target: log price change over the next ten retrieved trade rows. Inputs: the five most recent adjacent trade log returns, all ending at or before the origin. No future price, event label, correction notice or whole-file statistic enters these features. Training-only weighted means/scales and an unpenalised intercept are used. Each training day has equal total fit weight.

Validation selected **alpha=0**, unregularised weighted least squares, from the seven frozen ridge settings. It separately selected the **training-mean constant** from zero, constant and ten-times-recent-five-return-mean baselines. No validation refit or test selection occurred. Primary evaluation averages within-day MSE equally across the 15 test days. Trade-volume-weighted losses are secondary; both appear in the [complete test output](../results/market-v1/test.json). See [mathematics](market-study-mathematics.md).

## Held-out results

| Predictor | Equal-day MSE | Equal-day MAE |
| --- | ---: | ---: |
| Selected AR(5) | 0.00001849151 | 0.002628852 |
| Zero return | 0.00002009389 | 0.002602048 |
| Training-mean constant | 0.00002009438 | 0.002604194 |
| Scaled recent-return mean | 0.00009198004 | 0.005588681 |

| Frozen comparison | MSE reduction | Adjusted exploratory interval |
| --- | ---: | ---: |
| AR(5) versus zero | 7.974% | [4.120%, 12.199%] |
| AR(5) versus selected constant | 7.977% | [4.124%, 12.200%] |

Intervals are the prespecified Bonferroni-adjusted 97.5% percentile intervals for two contrasts, using 9,999 paired noncircular three-day moving-block resamples, seed 190011. These are approximate dependence-assumption diagnostics, not guaranteed familywise coverage. The references have nearly identical risk, so these are closely related comparisons rather than two independent confirmations.

The AR predictor has lower daily MSE than the constant on 14 of 15 days. Its relative daily result ranges from about 16.60% improvement to 1.33% deterioration. Do not treat these days or overlapping row targets as independent trials in a binomial significance test.

MSE and MAE disagree: MAE deteriorates by 0.947% versus the constant and approximately 1.03% versus zero. The result is loss-specific, not uniform forecast superiority. No economic utility, cost-adjusted profit or minimum practical market margin has been established. The old synthetic 5% threshold is not reused.

## Statistical reliability and competing explanations

The exploratory intervals exclude zero under the frozen procedure. Nevertheless, 15 adjacent test days provide only about five three-day blocks. The noncircular resampler underweights endpoints: expected day weights are proportional to (1,2,3,...,3,2,1), rather than equal. Against the constant, its mean gain is 8.183%, approximately 0.206 percentage point above the empirical 7.977% gain. This centering difference and possible longer dependence weaken coverage claims. Broader statistical reliability requires a separately frozen evaluation across more periods/regimes; 94,903 overlapping origins are not 94,903 independent replications.

The standardized fitted lag coefficients are all negative. This is compatible with recorded trade-price reversal, including bid/ask bounce; it does not identify its cause. The latest feature return and target share the observed origin price. That is legitimate for this declared target because the origin price is available, but predictability of its reversal need not represent efficient-price drift or an executable trading opportunity. No quotes, spreads, fees, order fills or counterfactual clean prices were measured.

The archive may have been revised after 2017 and has no original receipt/revision ledger. Chronological fitting prevents use of later rows under retrieved-file order; it cannot certify original historical availability. Neither the source nor this model supplies independently adjudicated error/shock outcomes. Results therefore support a narrow recorded-price comparison only.

## Review, validation and conclusion

The complete suite passes **101 tests**, including nine new market-study tests for feature/target indexing, day weighting, training-only scaling, protected-date separation, no refit, source guards and paired bootstrap calculations. Three subagents checked data acquisition/provenance, mathematical design and the [independent quantitative review](market-study-review.md). All 30 archive/CSV hashes match the acquisition manifest, and every eligible count is N-15. Frozen prior experiments and data are unchanged.

This real-market archive pilot finds a held-out MSE benefit for a simple linear predictor, with a small MAE deterioration and limited uncertainty/generalisation evidence. It establishes no RippleNet-specific gain, mechanism, novelty, market-wide transfer or profitability.

The most efficient next experiment is a **fresh-period delayed-start target control**: keep origin information fixed at row k, but compare prediction of log(P[k+11])-log(P[k+1]) with the original origin-start return, on matched eligible origins with strong same-information baselines. Freeze dates, fitting, targets and multiplicity before opening the new period. This can distinguish predictability concentrated in reversal of the origin trade price from more persistent recorded-return predictability. It would still not create clean efficient-price or error/shock labels, and should not be presented as retrospective confirmation on this test set.

## Reproduce

Obtain the same permitted local ZIPs and publisher sidecars, retain the documented hashes and applicable source conditions, then run:

```sh
python -m unittest discover -s tests -q
python -m ripplenet.market_study development --data-dir PRIVATE_DATA_DIRECTORY --output work/market-reproduction
python -m ripplenet.market_study test --data-dir PRIVATE_DATA_DIRECTORY --output work/market-reproduction
```

The output directory must not already exist for development; test refuses to overwrite its result and checks source consistency with selection. Reproduction repeats disclosed data and settings; it is not a fresh evaluation. Output files carry data attribution/license metadata. No paid service, cloud compute, provider contact or spending was used.
