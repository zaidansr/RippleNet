# Public-data engineering feasibility audit

Audit date: 6 November 2026. This is an access, schema and causal-validation audit following the negative same-information forecasting-headroom findings. No real-data model was trained, no dataset was purchased, and no account or API token was created.

## Finding

A small official LOBSTER sample is technically accessible and can support local parser and observable-order-book target checks. It does **not** supply independent labels distinguishing recording errors from genuine market shocks. Its processed event stream lacks the raw broken-trade messages needed even to reconstruct subsequent exchange reversals. The original RippleNet mechanism claim therefore remains unsupported by this candidate.

## Actual bounded sample inspection

The provider's [official sample page](https://php.lobsterdata.com/info/DataSamples.php) links directly to [the GOOG level-one ZIP for 21 June 2012](https://php.lobsterdata.com/info/sample/LOBSTER_SampleFile_GOOG_2012-06-21_1.zip). It identifies its samples as derived from Nasdaq's historical TotalView-ITCH sample.

An unauthenticated read succeeded on 6 November 2026 with a 1 MiB transfer limit and a 10 MiB total uncompressed-size limit. The archive contains the matching message and order-book CSVs plus a vendor readme. Actual six-column message and four-column book layouts were verified. This was an inspection of the downloaded archive, not merely a successful documentation-page request.

Integrity metadata: archive size 636,670 bytes; SHA256 `34ec126261ac19831972f47edd8ab874d52d93b54a9ab623ee4ce89d3f90f5cc`.

The ZIP, readme and detailed inspection output remain in workspace scratch storage outside the public repository. No raw rows, prices, copied readme, data-derived counts or price statistics are published here. The [public terms page](https://php.lobsterdata.com/termsAndConditions.php) says academic subscription terms accompany the contract and that there is no standalone public terms PDF. The bundled readme supplied schema information but no explicit redistribution grant. Public accessibility alone does not resolve publication rights; this audit makes no claim that the sample carries an open-data license.

## What its fields can establish

The [official output specification](https://php.lobsterdata.com/info/DataStructure.php) defines:

| File | Fields | Engineering interpretation |
| --- | --- | --- |
| Message CSV | Seconds after midnight, event type, order reference, size, integer price, direction | Event time and order lifecycle; an order reference can recur across updates and is not a unique trade identifier. |
| Level-one book CSV | Best ask price/size, best bid price/size | The book after the event on the corresponding message row. Prices use dollars multiplied by 10,000. |

Types 2 and 3 are resting-order cancellation/deletion, not cancellation of an erroneous executed trade. Types 4 and 5 indicate executions. Type 6 is a crossing/auction event; type 7 is a halt indicator. None is a general recording-error label. Dummy empty levels and halt values have defined meanings and must not be treated as ordinary executable prices. [Output specification](https://php.lobsterdata.com/info/DataStructure.php)

The CSV schema contains no exchange-wide message sequence, execution match identifier, client receive timestamp, or correction-notification timestamp. A file row index preserves supplied order; it cannot certify full-feed completeness or network delivery. LOBSTER filters output to changes relevant to the requested depth, so apparent gaps cannot be interpreted as lost exchange messages. [Reconstruction description](https://php.lobsterdata.com/info/HowDoesItWork.php)

Most importantly, the provider explicitly ignores broken-trade messages during reconstruction. Its FAQ also says subsequent trade cancellations are not retroactively incorporated into the supplied books. Consequently neither a clean latent series nor a complete later-correction ledger can be recovered from these two CSVs. [Broken-trade handling](https://php.lobsterdata.com/info/help_reconstruction.php), [data-processing FAQ](https://php.lobsterdata.com/info/help_faq_general.php)

## Minimum importer and causal checks

The following are proposed implementation requirements, not claims that a full importer has been built:

1. Save source URL, retrieval time, byte hash, schema version, file identity and immutable row index. Keep vendor data out of Git until the intended use and publication permissions are established.
2. Parse price/size/reference fields as integers and decimal event time without losing precision. Attach session date and a verified exchange timezone before any cross-asset UTC alignment; do not infer UTC from seconds-after-midnight alone.
3. Require six message fields, four level-one book fields, equal row counts and stable row alignment. Check nondecreasing event times while preserving tie order. Never deduplicate by timestamp or order reference.
4. Validate known event codes, directions and nonnegative sizes using event-specific exceptions. Identify sentinel levels, halts, locked/crossed quotes and stale states explicitly; flagging one does not establish its cause or supply a true error label.
5. Treat book row k as the post-message-k state. Use only rows at or before a forecast origin. Specify event-time versus clock-time horizon, tie handling, staleness rules, market sessions and target availability before computing features.
6. An observed target could be a future displayed midquote change. State explicitly that it is an observable proxy, not the latent efficient return used in the synthetic experiments. A single asset/day sample checks plumbing, not cross-asset transfer or out-of-sample scientific performance.
7. Preserve an append-only correction ledger if a later source provides one: original event time, announcement/availability time, original identifier and reversal/replacement relation. A later announcement may define a retrospective scoring label; it cannot enter the original online information set. Label maturation must also respect training/test boundaries.

Without a receiver clock or independently documented delivery guarantees, any benchmark from this sample is an idealized supplied-feed-order study. It cannot support an operational claim about what a particular client knew at a wall-clock instant. No error/shock classifier should be evaluated using order cancellations or large price movements as fabricated ground truth.

## Two public crypto alternatives checked at documentation level

**Binance Vision:** the [official public-data repository](https://github.com/binance/binance-public-data) documents downloadable daily/monthly archives and links to the [data index](https://data.binance.vision/). Individual trades contain trade ID, price, quantity, quote quantity, timestamp and maker/match flags. Those fields supply no correction/cancellation lineage or receiver clock. Spot archive timestamps switch to microseconds from 1 January 2025, so unit handling must follow documented date coverage. This could support an observed-trade target audit, not independently labeled recording-error research.

The repository's current [dataset terms](https://github.com/binance/binance-public-data/blob/master/TERMS_AND_CONDITIONS.md), dated 26 August 2026, explicitly state free access and CC BY-NC-SA 4.0 licensing, allow specified noncommercial research uses, and impose attribution/share-alike conditions with separate restrictions on commercial use. It must not be described as unrestricted data or assumed to inherit a code license. No Binance archive was downloaded in this bounded audit.

**Coinbase Exchange:** the [documented public trade endpoint](https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/products/get-product-trades) is `GET https://api.exchange.coinbase.com/products/BTC-USD/trades?limit=5`; its schema has time, trade ID, price, size and maker side, without correction lineage. Its suitability is nevertheless blocked by the currently published [Market Data Terms](https://www.coinbase.com/legal/market_data), updated 7 August 2026: section 3.5 restricts AI/ML development, validation and benchmarking absent prior written consent; section 3.2 restricts external dissemination including derived research. Ordinary public access is therefore insufficient for the proposed RippleNet ML use. No Coinbase market data was downloaded.

These are source-specific factual access and usage observations, not a legal opinion or a request to contact providers. No provider was contacted.

## Decision

The verified next engineering step could be a bounded schema importer and observable-target audit, with its data-use basis settled first. It would test data plumbing, not validate RippleNet's proposed mechanism. Proceeding with mechanism-identification claims requires a separate source with defensible correction labels and their availability times, plus independent evidence concerning genuine shocks. This audit found no such paired ground truth in the inspected sample or the two documented crypto trade schemas. A reversal label alone would still not identify the counterfactual true market price or prove that an observed disturbance was only a recording error.
