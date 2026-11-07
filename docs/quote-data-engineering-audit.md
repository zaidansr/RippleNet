# Trade and best-quote archive engineering audit

Audit date: 8 November 2026, Singapore time. Scope: Binance only, with spot and USD-M futures as the two product options. Two candidate ZIPs were checked by HEAD and checksum-sidecar requests; no ZIP body was downloaded, decompressed or parsed. No account, provider contact, paid source, model or new forecasting experiment was used.

**Attribution and document license:** Acquisition-metadata findings concern Binance Vision public files. Sources: [Binance public-data repository](https://github.com/binance/binance-public-data), [dataset terms](https://github.com/binance/binance-public-data/blob/master/TERMS_AND_CONDITIONS.md). This document and its data-derived findings are distributed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Changes: documentation and metadata were inspected and summarized; no vendor rows or prices are reproduced. This notice does not relicense independently written code or imply Binance endorsement.

## Decision

A same-product historical pair exists for **Binance USD-M BTCUSDT, 30 March 2024**: individual trades and `bookTicker`. It is older than the preferred 2025 period and is not a tiny sample. Actual archived quote schema, expanded size, row ordering and timestamp conventions remain unverified because trade/quote bodies were deliberately not accessed.

The recent-date limitation is explicit: an identified Binance repository collaborator stated on 6 October 2026 that historical `bookTicker` is no longer provided and that the last USD-M daily file is 30 March 2024. This supports rejecting an assumed 2025 USD-M `bookTicker` archive, rather than silently substituting a different product. [Official repository response, issue 380](https://github.com/binance/binance-public-data/issues/380)

**Conditional go for a separately frozen, bounded actual-schema acquisition of that documented pair; no-go for a 2025 archive claim, immediate modelling, or original receiver-time validation.** No body download is authorized by this audit itself. Existing 2 MiB-per-file acquisition limits would exclude both candidate files; bounds must be explicitly declared for any next acquisition rather than expanded automatically.

## Product options and schema evidence

| Option | Primary-source evidence | Readiness assessment |
| --- | --- | --- |
| Spot BTCUSDT | The public archive README documents trades, aggregate trades and candles. The official spot live stream does expose best bid/ask price and quantity with a book update ID. | A live stream definition is not proof of a historical spot quote archive. No historical spot trade/quote pair was established within this audit. |
| USD-M BTCUSDT | The historical trade README documents six fields: trade ID, price, quantity, quote quantity, time and maker flag. Both selected futures archive objects and sidecars respond successfully. | A potential same-instrument/product pair is established at object level. Archived quote columns, actual headers and units still require bounded body inspection. |

[Official archive format documentation](https://raw.githubusercontent.com/binance/binance-public-data/master/README.md), [official spot live book-ticker definition](https://raw.githubusercontent.com/binance/binance-spot-api-docs/master/web-socket-streams.md#individual-symbol-book-ticker-streams)

Do not pair the existing **spot** BTCUSDT trade studies with **USD-M futures** BTCUSDT quotes. Identical symbol text does not make the contracts, price process or available information identical. The existing seven-column spot importer is also not the documented six-column futures format.

`bookDepth` is not an interchangeable BBO source. A Binance collaborator describes its values as coin/notional depth at percentage distances from the midpoint. Those percentage-band summaries do not supply best bid and ask prices or an identifiable spread. Dividing notional by depth does not recover the best quote. This audit therefore does not use recent `bookDepth` as a substitute quote series. [Official repository clarification, issue 447](https://github.com/binance/binance-public-data/issues/447)

## Two candidate objects: metadata only

Metadata was checked at 2026-11-07 16:20 UTC, which is 8 November in Singapore. Both objects returned HTTP 200 to HEAD; both publisher checksum sidecars returned HTTP 200. The private record is workspace `work/quote-audit/candidate-metadata.json`, outside the repository.

| Same USD-M BTCUSDT date | Compressed bytes from HEAD | Last-Modified header | Publisher archive SHA256 |
| --- | ---: | --- | --- |
| [bookTicker, 2024-03-30](https://data.binance.vision/data/futures/um/daily/bookTicker/BTCUSDT/BTCUSDT-bookTicker-2024-03-30.zip) | 87,758,829 | 2024-03-31 07:48:28 GMT | `6c6310b48a0de980d61f7e7edab7975abd0a6fe7d6b63a1156f7ea74bb15d151` |
| [Individual trades, 2024-03-30](https://data.binance.vision/data/futures/um/daily/trades/BTCUSDT/BTCUSDT-trades-2024-03-30.zip) | 12,403,562 | 2024-03-31 06:54:26 GMT | `a385248e48e38c8ae96641cf3a34887be080ae2d1558b70a80efddceb211b9d0` |

Append `.CHECKSUM` to each URL for its sidecar. The pair totals **100,162,391 compressed bytes**, approximately 95.5 MiB. These are advertised object sizes and publisher checksum values, not verification of downloaded bodies. Uncompressed sizes, CRCs, CSV hashes, row counts and empirical data quality were not established. Multipart ETags are not treated as SHA256 checksums.

## Rights checked

Current official dataset terms were rechecked during this audit. They identify version 1.0, updated 26 August 2026. Free access and specified noncommercial research uses are stated, together with CC BY-NC-SA 4.0 and attribution/share-alike obligations for derived works. This supports an appropriately attributed noncommercial schema audit and publication of its findings; it does not establish unrestricted commercial permission. The dataset terms apply independently of a repository code-license heading. [Official dataset terms](https://raw.githubusercontent.com/binance/binance-public-data/master/TERMS_AND_CONDITIONS.md)

Any subsequent publication of data-derived summaries must preserve source attribution, the license link and indication of changes. Raw archives should remain outside Git. No monetary spending was incurred, and this finding does not authorize future spending.

## Required checks before even a recorded-file benchmark

1. Freeze exact product, symbol, date, source URLs, byte caps and failure policy before body inspection. Require the actual quote CSV to contain best bid **price and quantity** and best ask **price and quantity**. A filename or live endpoint alone does not validate archived field order or meaning.
2. Verify archive SHA256/CRC, expanded size, member layout, headers and every row's types. Confirm unit/date conventions separately for trades and quotes. The README's 2025 microsecond change is explicitly for **spot**; do not automatically apply it to USD-M futures.
3. Preserve all source timestamp fields and update identifiers that actually exist. Distinguish exchange event/transaction timestamps from receiver availability. Do not invent a client clock or assume a quote update ID and trade ID form one joint sequence.
4. Audit within-file backsteps, repeated IDs, duplicate/tied timestamps, quote validity, nonpositive prices/sizes, crossed/locked books, gaps and stale periods. Report failures and exclusions rather than sorting or cleaning them into an apparently valid online prefix.
5. Freeze a cross-stream alignment convention, tie rule and maximum quote age before scoring. Never use a nearest quote that can lie after the trade origin. Even a backward timestamp join remains a declared archival event-time convention until original availability is justified.
6. Fix the target price, origin and horizon. Last-trade returns and future midquote returns are different targets; liquidity and staleness handling can change coverage. All competing methods must receive the same admissible information and use matched origins for the declared contrast.

These are proposed checks, not completed quote-schema or causal validations. They require no new model architecture.

## What remains unknown and where to stop

The publisher permits later archive revisions. A current sidecar and Last-Modified header do not reveal complete version history or what a client could observe at an original timestamp. Neither trades nor BBO should automatically become a recording-error label, genuine-shock label, latent efficient price or executable-profit target. [Archive revision policy](https://raw.githubusercontent.com/binance/binance-public-data/master/README.md)

This bounded audit establishes a dated same-product object pair and its size/license constraints. It does not establish a tiny permitted download, actual bid/ask rows, original cross-stream sequencing, receiver latency, sampling completeness, revision linkage or usable forecasting headroom. No additional provider, date sweep, paid service or model expansion is justified by these metadata alone. A next step, if chosen, must be the explicitly bounded acquisition/schema gate; otherwise stop this source branch with the documented limitations.
