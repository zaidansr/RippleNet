# Independent review: fresh-market delayed-start control

**Attribution and findings license:** Derived findings use Binance Vision BTCUSDT daily individual-trade archives for 16 September–15 October 2017. [Source](https://data.binance.vision/), [dataset terms](https://github.com/binance/binance-public-data/blob/master/TERMS_AND_CONDITIONS.md). This document's derived findings are distributed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Changes: independently reconstructed paired features/targets, fitted parameters, validation scores, losses and bootstrap statistics; no raw trades reproduced. No endorsement or relicensing of independent code is implied.

## Reproduction and leakage checks

Reviewed the frozen plan and source before price access and independently ran all seven synthetic fixture tests successfully. After the protected run finished, read the same 30 real archives solely for independent reproduction. No new setting, model, period or target was selected.

All ZIP/CSV hashes and publisher sidecars match stored provenance. Independently rebuilt both targets on the common N-16 origins, using a different sliding-window implementation. Verified coverage, including A's one otherwise-complete origin excluded for pairing rather than censoring. Eligible counts are 81,529 training, 51,848 validation and 130,872 test origins per target.

Independent weighted regression reproduces both training-only scalers and fitted models. Recomputed all 14 already-declared validation fits and baseline scores: both targets selected alpha zero and the training-mean constant. All 15 days × two targets × four predictors × two held-out loss metrics reproduce, with maximum absolute discrepancy 5.42e-18. Matching source hashes, the test-pinned selection SHA256, target definitions and date guards were verified. Neither predictor uses the future target-start price as an input.

## Quantitative finding

Independently reproduced all summaries and the complete joint three-day-block bootstrap, including raw and family-three-adjusted intervals and centering shifts. The same 9,999 day-index draws determine both targets and all contrasts.

| Primary contrast | Estimate | Adjusted exploratory interval |
| --- | ---: | --- |
| Origin-start MSE reduction versus its selected constant | 13.4384% | [9.1043%, 16.2156%] |
| Delayed-start MSE reduction versus its selected constant | 3.2387% | [0.9286%, 5.1771%] |
| Difference in absolute zero-relative MSE improvements | 5.43028e-7 | [3.73563e-7, 7.09654e-7] |

The third contrast has squared-log-return units. It uses a common zero reference and does not subtract percentages with different denominators. Daily candidate MSE beats the constant on 15/15 origin-start days and 14/15 delayed-start days. Nevertheless, MAE worsens by **0.6240%** and **4.1422%**, respectively. The result is loss-specific.

## Interpretation and limits

The positive absolute contrast supports attenuation of this pipeline's MSE advantage when the first future increment is removed and a later increment added. Delayed-target skill persists, so an explanation confined entirely to the shared origin price is insufficient for the observed pattern. Neither finding uniquely identifies bid/ask bounce: legitimate short-lived efficient-return predictability and other recorded-price dynamics can also produce attenuation. The models were separately fitted; this is not an isolated coefficient or causal-mechanism ablation.

Only 15 adjacent test days inform uncertainty. Noncircular three-day blocks underweight endpoints; bootstrap mean gains shift by approximately -0.310 and -0.257 percentage point, and the absolute contrast shifts by -1.24e-8. Reported intervals exclude zero under the frozen approximate procedure, not guaranteed familywise coverage or broad market reliability. Overlapping origins are not independent replications.

This independently reproduces a fresh-period result for refitted linear pipelines, not transfer of the original fixed coefficients. It supplies no correction/shock labels, verified original receipt history, executable profit, efficient-price truth or RippleNet-specific novelty. A future quote/midpoint comparison would need separately justified data availability and a new frozen evaluation. The [results report](market-delay-results.md) respects these limits; no material computational defect was found. No further analyses were added.
