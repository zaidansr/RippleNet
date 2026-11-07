# Frozen multi-session trade-versus-midpoint pilot

This new recorded-market study follows the owner's instruction to continue after the paired-source audit. It asks whether a classical full-information predictor improves trade and midpoint return forecasts beyond simple constants and a mechanical starting-gap correction. It is not a trained RippleNet, a cause-label experiment, a reconstruction of client latency or a profit claim.

## Fixed source, dates and disclosure

Use only free Tardis Kraken spot XBT/USD first-of-month trade/quote CSV pairs, exactly 12 dates from **2025-06-01 through 2026-05-01** inclusive. Train June–November 2025 (6 sessions); validate December 2025–February 2026 (3); protect March–May 2026 (3) for test. Each date is day 1 of its month. The previously inspected June 2026 session is excluded entirely. No dataset bodies for these dates have been inspected before this freeze. All selected sessions precede the documented July 2026 symbol/feed transition. A documented exchange-server relocation on November 1, 2025 at 15:00 UTC falls inside training and may affect collector-age patterns.

Recheck free no-key first-of-month access and source-specific conditions; no account, trial, paid endpoint, provider contact or cloud service. Source terms permit eligible aggregate research publication but restrict public trained models/weights and event datasets. Keep raw records, model parameters, fitted preprocessing, selections and per-origin predictions private. Publish original general code, one-way selection hashes, acquisition provenance and qualifying aggregate reports only. Do not assign a Binance CC license to Tardis findings. Any spending requires explicit owner approval.

For each day retain the preceding audit's caps: trades 32 MiB compressed/256 MiB expanded and two million rows; quotes 128 MiB compressed/1 GiB expanded and five million rows. Across 12 dates, compressed cap is 1,920 MiB and expanded cap 15 GiB. Stream expansion rather than persist uncompressed files. Pin source terms, URLs, HTTP integrity headers, gzip checks and SHA256. Missing/authentication/oversize/integrity/schema/clock failures stop this fixed design; no replacement date, silent repair or cap expansion. Do not decode protected test bodies before executable source and private-model selection hashes are public.

## Clock, reference and validity rules

Use the provider's collector `local_timestamp`, integer UTC microseconds, preserving supplied order and ties. Reject missing/invalid local clocks, out-of-day local clocks or backsteps. Never sort or deduplicate rows. Missing trade IDs are allowed and disclosed; no invented execution identities or cause labels. Accept only the documented exact headers and same `kraken`/`XBT/USD` identity. Numeric reference/amount problems make the corresponding observed state invalid until its next update, rather than bypassing it to an older valid state. Unexpected schema or malformed clocks stop acquisition/evaluation.

For each session make exactly 86,400 grid snapshots: UTC times 00:00:00 through 23:59:59 at one-second spacing. At every grid time t use the last trade and quote with collector time **strictly less than t**. Same-time records are excluded; quote-file tie order remains supplied order and proves no exchange-wide sequence. Last trade must have finite positive price/amount and age at most 5 seconds. Last quote must have finite positive bid, ask and both amounts, bid strictly below ask, and age at most 1 second. Inclusive age bounds refer to the snapshot's own clock, not last price change. Do not carry observations across days, backfill invalid states or use future quotes. Collector-clock study eligibility does not establish operational receipt, complete feed coverage or economic truth.

Set P(t) to last valid trade price and M(t)=(bid+ask)/2. A locked/crossed/otherwise invalid latest quote blocks that snapshot; an older clean-looking quote must not repair it. Record invalid/missing/age exclusions, source ties, unchanged references and coverage. Missing disconnect records prevent certification that valid-looking intervals were continuously observed.

## Shared information, labels and coverage

At origin t, the identical 12 inputs for both fitted pipelines are five adjacent one-second log returns for P, five for M (six immutable reference snapshots t-5,...,t), current relative spread (ask-bid)/M and current log gap g(t)=log P(t)-log M(t). Each history snapshot is validated at its own time. The first five clocks lack the complete history; t=00:00:00 itself has no same-day predecessor, and eligibility follows actual availability rather than a fabricated warm-up count.

Define two ten-second labels: Y_P=log P(t+10)-log P(t), Y_M=log M(t+10)-log M(t). Snapshots at t+10 use the same strict-before and age rules. Endpoints outside the 86,400-clock grid are censored; no midnight or overnight label is synthesized. Do not include delayed-start labels in this pilot.

Issue forecasts at every origin with valid current/past features, regardless of future target status. Preserve private origin statuses/counts. Score both tasks on the common subset whose two future references are valid and within the session, reporting issued-to-scorable attrition and known session-boundary censoring separately. This retrospective label availability is not an operational origin-selection rule. All reported losses are conditional on disclosed paired target coverage; do not hide outages or silently label censored outcomes zero. A day with no matched scorable origins stops the design.

## Frozen predictors and chronological selection

Use separately fitted, full-input linear ridge pipelines for P and M; no neural architecture. Equal total fitting weight per training session, population training-only feature scaling, unit scale for zero-variance features, unpenalised intercept and target mean. Minimize weighted MSE plus alpha times squared standardized coefficients, with alpha in [0,.001,.01,.1,1,10,100]. Alpha zero uses weighted least squares. Common matched X/weights imply identical feature scalers across the two targets. No refit on validation.

Include these baselines, in tie-breaking order: zero; target-specific equal-session training mean; target-specific equal-session weighted training median (first sorted target whose cumulative weight reaches .5); fixed mechanical gap correction. The last predicts Y_P=-g(t), Y_M=0, assuming no future midpoint drift or expected terminal gap. It is a diagnostic, not a fitted causal model. Every flexible fitted method receives the same admissible inputs; constant baselines may ignore them by definition.

Validation equal-session MSE selects each alpha (ties in listed order) and each baseline (ties as above). Freeze both private model-bearing selections, then publish their one-way artifact hash and executable provenance before protected test prices/metrics are opened. Do not publish learned coefficients, scalers, intercepts, medians or model-bearing JSON. Test must verify source, date and selection hashes and must not refit.

## Scores and interpretation

Primary risks are equal-session averages of within-session scorable-origin MSE. Report MAE and pooled-origin risks secondarily, all baseline losses including the fixed gap baseline, every test date separately, denominator risks and coverage. Primary descriptive comparisons are each fitted pipeline versus its validation-selected baseline and the change in absolute zero-relative improvement between P and M. Label all units. Ratios for distinct targets have different denominators; raw lower midpoint variance is not prediction skill.

Only three nonadjacent convenience-sampled monthly test sessions are available: **no bootstrap confidence intervals, p-values, significance, power or broad generalisation claims**. No practical economic margin has been established. Do not reuse the old synthetic 5% threshold or infer profitable execution from recorded returns. Preserve MSE/MAE disagreements.

The identity Y_P=Y_M+g(t+10)-g(t) explains why trade predictability can arise from the known starting gap without future midpoint prediction. Comparison with the mechanical baseline is essential. Quote reconstruction, stale/unchanged references, clock infrastructure, target variance and separately selected models are competing explanations; neither outcome identifies recording errors, efficient prices or genuine shocks.

Publish this plan before new data bodies; publish all executable fitting/evaluation code before development price inspection. Keep source/acquisition/model hashes and full private reproducibility artifacts, but publish only permissible aggregate findings. Refuse output overwrites and disclose all failures/null results. Existing studies remain unchanged.
