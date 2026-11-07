# Multi-session trade-versus-midpoint findings

**Source and publication scope:** Tardis Kraken spot XBT/USD first-of-month trade/quote samples, [source documentation](https://docs.tardis.dev/historical-data-details/kraken), [applicable terms](https://docs.tardis.dev/legal/terms-of-service). This document reports non-reconstructive aggregate research statistics. Raw records, fitted parameters, preprocessing, model-bearing selections and per-origin outputs remain private. No open-data or Binance CC license is claimed for these findings; no endorsement is implied.

## Finding

The full-input linear model **does not improve aggregate trade-return MSE over the fixed mechanical gap-reversion baseline**: it is 0.061% worse. For midpoint returns, its MSE is 0.761% lower than the validation-selected constant. MAE is worse than the selected references for both targets, by 3.23% and 1.08%, respectively.

A trade-only comparison against zero would show a 10.11% MSE gain, but the simple mechanical baseline slightly exceeds it in aggregate. This is the principal lesson of the control: the apparent trade-return benefit does not establish additional model value beyond the known starting trade-to-midpoint gap in this pilot. It does not prove a causal explanation, statistical equivalence or universal dominance of the baseline.

## Frozen sessions and execution

Exactly twelve free first-of-month sessions, June 2025–May 2026, were selected before data-body inspection. Training used June–November 2025 (six sessions), validation December 2025–February 2026 (three), and protected test March–May 2026 (three). The June 2026 source-audit session was excluded entirely. This is convenience sampling, not twelve consecutive days or a representative sample of all market conditions. The documented November 2025 server relocation occurs within training and can affect collector-age patterns.

This is a retrospectively designed research holdout. The June 2026 audit, later in calendar time than the test dates, informed source/QC choices. Excluding it from fitting and testing does not turn the study into a prospectively deployed historical trading process.

The [plan](quote-study-plan.md) was published as `6993f9a12311d759b8e5d3370fcac8dc2ade6ed7`. Executable source was published as `45684955d4ab62e558c9d79992b2ff612e23ca5e`, tree `9ea90338d151a52f6242a5c3a75c427c5d8a261f`, before development records were decoded. The [private-selection commitment](quote-study-selection-commitment.md) was published as `746ccd80975642f086da5156a3b40b0015cf2547` before the protected test. Its exact SHA256, executable hashes, acquisition-manifest hash and protected dates were checked before test loading. No refit followed validation.

All 24 fixed files passed the frozen access, byte, gzip integrity and source-hash checks without replacement. [Acquisition provenance](quote-study-provenance.md) gives source dates and hashes. Private final test-artifact SHA256 is `657aa0989f98d305ec3ab6b370e29e92209d5a401373d6d1a6c439a190a7418d`; it is not a public model download. No learned coefficients, selected regularisation values, fitted constants or model-bearing JSON are published.

## What was predicted

Both tasks use the same one-second collector-clock grid and twelve inputs: five adjacent one-second trade returns, five midpoint returns, current relative spread and current log trade-to-midpoint gap. Every input uses strictly earlier observed records; six historical snapshots are required. Fixed maximum observation ages are five seconds for trades and one second for quotes, each checked at its own snapshot time. Invalid latest states block a reference rather than being bypassed.

Targets are the next ten-second recorded trade and midpoint log returns, with the same strict-before endpoint convention. The full-input ridge/OLS family is fitted separately for the two targets, using identical common training features, session weights and scalers. Training alone determines parameters; validation chooses from the frozen settings and baseline list.

The mandatory fixed baseline predicts trade return as minus the current log trade/midpoint gap, and midpoint return as zero. It assumes no expected future midpoint move or terminal gap and uses no fitted coefficient. The identity

`trade_return = midpoint_return + future_gap - current_gap`

explains why a model can predict trade returns without predicting future midpoint movement. This baseline does not independently identify bid/ask bounce or recording error. See [the mathematical contract](quote-study-mathematics.md).

## Held-out aggregate risks

Risks give each test session equal weight after averaging within-session paired scorable origins. These are point estimates only.

| Target | Predictor | MSE | MAE |
| --- | --- | ---: | ---: |
| Trade | Full-input linear | 1.324942e-7 | 0.000197816 |
| Trade | Fixed gap reversion, selected reference | 1.324140e-7 | 0.000191620 |
| Trade | Zero return | 1.474021e-7 | 0.000214939 |
| Trade | Training-mean constant | 1.473971e-7 | 0.000215315 |
| Trade | Training-median constant | 1.474021e-7 | 0.000214939 |
| Midpoint | Full-input linear | 1.417716e-7 | 0.000214562 |
| Midpoint | Training-mean constant, selected reference | 1.428581e-7 | 0.000212264 |
| Midpoint | Zero return | 1.428632e-7 | 0.000211765 |
| Midpoint | Training-median constant | 1.428632e-7 | 0.000211765 |
| Midpoint | Fixed gap baseline, zero by definition | 1.428632e-7 | 0.000211765 |

The relative MSE reductions versus the selected references are **-0.0606% for trades** and **+0.7606% for midpoints**. The descriptive change in absolute zero-relative improvement, trade minus midpoint, is **1.3816e-8 squared-log-return units**. Its different target variances and mechanical starting-gap component prevent a causal interpretation.

| Test session | Trade MSE reduction vs selected gap reference | Midpoint MSE reduction vs selected constant |
| --- | ---: | ---: |
| 2026-03-01 | -1.984% | -0.533% |
| 2026-04-01 | +2.387% | +2.244% |
| 2026-05-01 | +5.258% | +4.305% |

Two of three sessions show improvement for each target, while the larger-risk March session changes the aggregate conclusion. The primary aggregate is a ratio of equal-session mean risks, not an average of these daily percentages. MAE disagreement remains material; no uniform superiority or economic-value result follows.

## Coverage is part of the result

| Test session | Grid origins | Feature-eligible issued origins | Paired scorable origins |
| --- | ---: | ---: | ---: |
| 2026-03-01 | 86,400 | 22,485 | 16,094 |
| 2026-04-01 | 86,400 | 25,904 | 18,755 |
| 2026-05-01 | 86,400 | 16,020 | 11,109 |
| Total | 259,200 | 64,409 | 45,958 |

Only **17.73% of all grid origins** are scored, and **71.35% of issued forecasts** have both future references available under the frozen rules. Of the 18,451 unscored issued origins, two hit the session-end boundary and 18,449 lack at least one qualifying future reference. No future label mask chooses whether to issue a forecast; it only determines the reported paired-loss subset.

Training has 87,531 issued and 58,426 scorable origins; validation has 74,817 and 58,184. Reference-age limits, six valid historical snapshots and paired future coverage select an active/fresh subset. These are conditional-coverage losses, not full-day deployment performance. Observation age does not prove an unchanged quote is economically stale, and CSVs omit disconnect evidence.

On the paired test subset, 15.29% of trade targets and 30.79% of midpoint targets are unchanged. Different update/noise patterns and zero-return fractions can affect risk. Lower raw midpoint/trade variance alone is not prediction skill; the comparison uses target-specific reference risks.

## Reliability, mechanism and research decision

There are only **three nonadjacent monthly test sessions**. In accordance with the plan, no confidence intervals, p-values, power, significance or broad-generalisation claim is made. Overlapping one-second origins are not independent replications. The small midpoint MSE reduction has no established practical threshold, worsens MAE and is mixed across sessions. It is insufficient evidence of a robust market edge.

Collector clock, source reconstruction/deduplication, missing trade IDs, cross-channel ordering, timestamp ties, omitted disconnects, publication revisions and the training-period infrastructure change remain limitations. The midpoint is an observable book reference, not efficient-price truth. These observations contain no independently adjudicated error/shock labels, executable fills or trading costs.

The mechanical control exposes the weakness of claiming value from beating a zero-return trade baseline alone. It does not prove that all earlier 2017 gains had the same cause: source venue, currency pair, sampling clock, dates and trained models differ. This study establishes no RippleNet-specific novelty or architecture advantage.

**Do not grow the architecture or tune another parameter grid on these sessions.** Any next forecasting claim needs an independently motivated hypothesis, an intended use and a practical metric requirement, followed by genuinely protected observations and an explicit coverage/outage policy. If deployment or open model release is the objective, source rights, executable targets and timing evidence require separate resolution. More complexity is not justified by the present benchmark.

The full suite passes **118 tests**, including ten new fixtures for timing, future-label separation, weighted fitting/median, mechanical controls, byte caps and private-artifact guards. The [independent review](quote-study-review.md) audits numerical and methodological claims. Three subagents supplied acquisition provenance, mathematical design and skeptical review. Earlier studies and learned parameters are unchanged; all fitted artifacts from this source remain private.

After review, an integration check fetched the public executable and commitment objects and verified their exact Git tree, executable/plan blob SHA256 values and selection commitment against the private run's provenance. This supplements the review's local artifact checks; it is not a second experiment.

## Reproduce privately

Obtain the same permitted files and an acquisition manifest with the documented hashes. All output paths must be outside the public repository:

```sh
python -m unittest discover -s tests -q
python -m ripplenet.quote_study development --data-dir PRIVATE_DATA --manifest PRIVATE_MANIFEST --output PRIVATE_NEW_OUTPUT
python -m ripplenet.quote_study test --data-dir PRIVATE_DATA --manifest PRIVATE_MANIFEST --output PRIVATE_NEW_OUTPUT --expected-selection-sha256 HASH_FROM_YOUR_DEVELOPMENT_RUN
```

The second stage checks the exact private artifact hash before loading test data and refuses overwrites. Reproduction of disclosed sessions is not an independent evaluation. A different private manifest/provenance environment can change artifact hashes; input hashes, executable versions and numerical methods identify the substantive reproduction. Publish only qualifying aggregate findings under the applicable source conditions. No paid access, credits purchase, cloud compute, account or provider contact was used.
