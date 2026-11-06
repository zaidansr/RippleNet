# Binance recorded-trade readiness audit

**Attribution and document license:** Dataset-derived inspection findings in this document use Binance Vision's BTCUSDT daily raw-trades archive for 17 August 2017. Source: [selected archive](https://data.binance.vision/data/spot/daily/trades/BTCUSDT/BTCUSDT-trades-2017-08-17.zip), [dataset documentation](https://github.com/binance/binance-public-data), [dataset terms](https://github.com/binance/binance-public-data/blob/master/TERMS_AND_CONDITIONS.md). This document is distributed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Changes: schema, coverage and integrity checks were computed from the archive; no raw trades are reproduced or altered here. This document-specific notice does not relicense independently written project code or imply Binance endorsement.

## Decision

**Go for a bounded noncommercial recorded-price/schema audit. No-go for validation of the original online as-of prefix or error-versus-shock mechanism.** The selected archive is accessible, small, checksum-verifiable and parseable. It does not record original receiver availability, corrections or version-by-version availability. A current historical file with ordered trade identifiers is not proof of what an online observer knew in 2017.

No model was fitted. No account, API token, purchase, provider contact, or paid resource was used. Raw data and source snapshots remain in scratch storage outside the public repository.

## Current terms checked before download

The official dataset-specific terms were retrieved on 6 November 2026. They identify version 1.0, updated 26 August 2026. Sections 2.3, 3.1, 4.1 and 4.5 respectively provide free access, specify CC BY-NC-SA 4.0, include noncommercial research/evaluation among permitted uses, and require attribution and the same license for redistributed derivative works. Commercial uses have separate restrictions. The README's final code-license heading is not a substitute for these dataset-specific conditions. [Official terms](https://raw.githubusercontent.com/binance/binance-public-data/master/TERMS_AND_CONDITIONS.md)

On that stated basis, the narrow noncommercial inspection and publication of attributed, share-alike schema/coverage findings are supported. The Creative Commons terms also require indicating changes and linking the license; those notices appear above. This is a source-specific readiness assessment, not an unrestricted-use or legal-compliance certification. [CC license summary](https://creativecommons.org/licenses/by-nc-sa/4.0/)

## Selection, bounds and integrity

The choice was fixed before accessing market data: **BTCUSDT, 2017-08-17, spot daily individual trades**, not aggregate trades. Limits were 2 MiB compressed and 20 MiB total uncompressed. They were not expanded.

Requests succeeded without authentication at:

- [Selected ZIP](https://data.binance.vision/data/spot/daily/trades/BTCUSDT/BTCUSDT-trades-2017-08-17.zip)
- [Its publisher checksum sidecar](https://data.binance.vision/data/spot/daily/trades/BTCUSDT/BTCUSDT-trades-2017-08-17.zip.CHECKSUM)

Inspection time was 2026-11-06 09:17 UTC. The ZIP was **63,039 bytes**, containing one **231,002-byte** CSV. Its SHA256 matched the publisher sidecar:

`a23fe0dae54b7143d5cffb42184e1a05afe7124aaca641cd438297ce83c9f9ec`

The uncompressed CSV SHA256 was:

`f1ca7241eba6cf27aac03ac32bea5c4e8a7c88b725b8f2f6276e6b178230d557`

The private manifest retains exact URLs, retrieval time, response headers, checksums, bounds, and read-only inspection findings. The access-time terms snapshot SHA256 is `99c4921dbe023cd68c1a447775707d621453cc78aec6ac0bfe2e6c06a5114ee0`; the README snapshot SHA256 is `2e133d9945a9263a02781369078e72805eff074680f305cd5460016471c6caad`.

## Verified recorded-file properties

The archive contained 3,427 headerless rows, each with the seven fields documented for individual spot trades: trade ID, price, base quantity, quote quantity, time, buyer-maker flag, and best-match flag. This agrees with the [public-data schema](https://raw.githubusercontent.com/binance/binance-public-data/master/README.md) and the [official historical-trade response schema](https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market#old-trade-lookup).

| Check | Observed finding | What it does not prove |
| --- | --- | --- |
| Trade identifiers | Unique, strictly increasing IDs 0 through 3426; no internal gaps | Completeness of every original trade, original dissemination order, or completeness of other feed messages |
| Time representation | Thirteen-digit integer timestamps; milliseconds produce the selected UTC date | Original client receive time or absence of delayed/revised records |
| Observed time range | 04:00:28.322 through 23:58:40.719 UTC on 17 August 2017 | Complete coverage before the first or after the last recorded trade |
| Ordering | No timestamp backsteps; 404 adjacent equal-time pairs | That tied events were received in this file's order by every client |
| Numeric fields | Finite decimals; positive prices/base quantities; nonnegative quote quantities; price times quantity exactly matched quote quantity in this file | Independent validation of economic truth, error-free prices, or a latent efficient price |
| Boolean fields | Valid maker booleans; best-match field was true throughout this sample | An independently verified recording-error label |

The file's order was preserved during inspection. Decimal arithmetic was used for price/quantity consistency. No deduplication, price cleaning, interpolation, or sorting changed the data. For future imports, the documented spot timestamp regime changes to microseconds from 1 January 2025; a single global timestamp-unit assumption would therefore be invalid. [Official archive documentation](https://raw.githubusercontent.com/binance/binance-public-data/master/README.md)

## Revision and information-availability limits

The publisher explicitly warns that archived files may later change and documents replacement-file checksums for listed updates. Its documentation does not make the selected archive an immutable contemporaneous capture. The HTTP Last-Modified header observed for this ZIP was **25 May 2023**, years after the trades; that header is object metadata, not proof of either the original 2017 observations or a particular correction history. [Archive update policy](https://raw.githubusercontent.com/binance/binance-public-data/master/README.md)

A matching sidecar authenticates integrity relative to the currently retrieved published file. It does not establish that the file is the earliest version, that the selected day was never revised, or that a correction was available by a particular forecast origin. No original-version comparison or trade-level revision ledger was provided or inferred.

None of the seven fields supplies client receive time, dissemination-message sequence, cancellation/correction announcement, replacement linkage or label maturity. Trade IDs are trade identifiers, not evidence of an exchange-wide lossless message stream. A maker-side flag describes trade participation; a best-match flag is not an error-versus-shock adjudication. [Trade schema](https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market#old-trade-lookup)

## Narrow next-step contract

An importer could honestly evaluate a frozen **recorded-file** next-trade target if it preserves file ordinal, IDs, decimal values, hashes and explicit millisecond units. Equal timestamps must retain file order. Any target horizon, split, incomplete-window censoring and fitted preprocessing must be fixed before analysis. The reported object would be a price recorded in this downloaded archive, not an independently observed latent price or a demonstrated original online information set.

An original as-of forecasting claim remains blocked until there is evidence for contemporaneous availability and revision handling. It cannot be repaired merely by sorting this file by event time, freezing its current hash, using contiguous IDs, or applying a chronological split. A recording-error classification claim additionally requires independently defensible error labels and their announcement times; genuine-shock labels and counterfactual clean prices are also absent.

The single preselected early trading day is a plumbing sample, not a justified training corpus or generalization test. No model, predictive result, operational latency claim, or financial usefulness conclusion is warranted by this inspection. No larger sample, alternative date or provider was automatically substituted.
