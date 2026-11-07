# Bounded Kraken trade/quote sample audit

This audit follows [public acquisition plan 6fed87f6b17d930d721b1c7387a0f56cf81638e2](https://github.com/zaidansr/RippleNet/commit/6fed87f6b17d930d721b1c7387a0f56cf81638e2). It inspects the fixed Tardis.dev Kraken spot XBT/USD sample for 1 June 2026. It fits no model, computes no forecast target, selects no profitable rule and substitutes no other date, instrument or provider.

**Source and publication scope:** Tardis.dev supplied the normalized Kraken records. This document publishes only non-reconstructive aggregate research-audit findings. It does not distribute or grant a license to vendor raw/event-level data, trained models, parameters or weights. The Binance CC license does not apply. Raw files, detailed inspection records and vendor snapshots remain private, outside the repository. [Current provider terms](https://docs.tardis.dev/legal/terms-of-service)

## Result

**Access, integrity, declared schema and bounded collector-clock alignment passed.** Both exact frozen URLs returned unauthenticated HTTP 200 with no redirect, account, API key or payment. Both complete gzip streams passed integrity checks and all acquisition/row limits.

This establishes that one recent same-venue, same-spot-instrument trade/BBO pair is structurally inspectable. It does not establish enough independent sessions, a protected forecasting result, original exchange-wide order, client latency, complete recording, or error-versus-shock ground truth.

## Access, rights and integrity

Only these two market-data URLs were requested:

- [Kraken trades, 2026-06-01, XBT-USD](https://datasets.tardis.dev/v1/kraken/trades/2026/06/01/XBT-USD.csv.gz)
- [Kraken quotes, 2026-06-01, XBT-USD](https://datasets.tardis.dev/v1/kraken/quotes/2026/06/01/XBT-USD.csv.gz)

The provider documents first-of-month samples without a Data API key and GET-based access; HEAD is not the appropriate availability test. [Datasets API](https://docs.tardis.dev/downloadable-csv-files/api)

The pinned current terms snapshot has SHA256 `ea5901192dce12c72f2303702b7f2bf87826b4b1a44806f8659d0fd91b030b11`, dated 28 October 2026. Their permitted research-report/derived-data clauses support qualifying aggregate publication, while raw redistribution and external publication of trained model-bearing artifacts remain restricted. This is not an open-data grant. No trained artifact was created in this stage. [Terms, especially clauses 9.3 and 9.5](https://docs.tardis.dev/legal/terms-of-service)

| File | Actual HTTP status | Compressed bytes | Expanded bytes | Data rows |
| --- | ---: | ---: | ---: | ---: |
| Trades | 200 | 811,026 | 5,316,631 | 73,704 |
| Quotes | 200 | 11,649,384 | 73,197,054 | 862,680 |
| Total | — | 12,460,410 | 78,513,685 | — |

All advertised compressed sizes matched downloaded sizes. Both advertised whole-file MD5 values matched, and full gzip EOF/CRC checks succeeded. Computed compressed-file SHA256 values are:

- Trades: `f34424bf85c03b796db5f83d5cd3801d9d9837d5d72d075742c4f7e31f417d74`
- Quotes: `cc5fbee1ae52d3eb38381990048bbfbd51a2f7f5aade612df7fc58e6a41968f6`

Expanded CSV SHA256 values are:

- Trades: `2379fdfccfc6318186ef1cec311917e86937014577e2b5e00a21d39a9b26a4cc`
- Quotes: `a9bc97bd3e2046d12f502f22c13291acc4c9dce49ce6b001c040447e9abc7f56`

The limits were unchanged: 32/128 MiB compressed, 256 MiB/1 GiB expanded, and two/five million trade/quote rows respectively, with their declared total-byte caps. No source failed and no cap expansion, fallback download, new account, provider contact or paid resource occurred. Local integrity metadata pins these retrieved versions; it does not independently certify economic correctness or original availability.

Private compressed files, acquisition manifest, bounded inspection script and aggregate inspection JSON are under workspace `work/quote-audit/tardis-sample/`. No signed redirect query strings, vendor prices, trade IDs or aligned event-level dataset are published.

## Actual schema and source identity

Both headers matched the documented eight-column schemas, and every record identified `kraken` and `XBT/USD`:

- Trades: `exchange,symbol,timestamp,local_timestamp,id,side,price,amount`
- Quotes: `exchange,symbol,timestamp,local_timestamp,ask_amount,ask_price,bid_price,bid_amount`

Timestamp values were parsed as integer UTC microseconds and prices/amounts using exact Decimal conversion. The provider defines the local field as collector message-arrival time and the other timestamp as exchange-supplied time, with a fallback when absent at source. Its `quotes` dataset reconstructs top-of-book values from L2 updates; it is distinct from a native BBO-feed export. [CSV definitions](https://docs.tardis.dev/downloadable-csv-files/data-types)

The selected date precedes the documented 10 July 2026 Kraken v1/v2 and symbol transition, so the XBT naming is appropriate. A current BTC-symbol example must not replace this fixed sample silently. [Kraken collection details](https://docs.tardis.dev/historical-data-details/kraken)

## Coverage and data-quality findings

- Both files have records from the 00:00 UTC minute through the 23:59 UTC minute. No local or exchange timestamp fell outside the requested day. This is observed boundary coverage, not a proof of continuous recording.
- No missing/invalid timestamp, nonfinite numeric field, nonpositive price/amount or invalid eligible quote state was observed. No locked or crossed quote rows were observed. These findings concern the provider's normalized/reconstructed outputs, not proof that original exchange messages contained no anomalies.
- Collector-time backsteps and exchange-time backsteps were zero in both files. Adjacent collector-time ties occurred 37,564 times in trades and 8,798 times in quotes; file order was preserved within ties. Exchange-time ties occurred 37,041 times in trades and zero times in quotes.
- **Every trade ID cell was empty.** The schema permits this, but it prevents unique execution-ID validation or later correction linkage from these files alone. There were 381 consecutive identical trade CSV rows; they were retained. Their status as repeated economic executions versus duplicate feed records was not determined, and no deduplication rule was inferred.
- The maximum observed inter-record collector gaps were about 53.6 seconds for trades and 23.0 seconds for quote updates. An unchanged book or inactive market can produce long gaps; these numbers do not diagnose an outage or justify automatic filling.

These are day-level research statistics, not raw records or a replacement high-frequency feed.

## Frozen descriptive alignment check

For each trade, select the last supplied-file quote whose **collector timestamp is strictly earlier**. All quotes at the same collector time as a trade are excluded from being that trade's predecessor. Among earlier quote ties, preserve the quote-file order. No nearest-time/future quote, sorting, deduplication or backward fill past an invalid latest quote was used.

Compact signed-64-bit timestamp arrays and quote-validity byte masks bounded memory; market prices were parsed transiently, not retained as a public dataset. The complete pair had valid ordered collector timestamps, so the predefined join could be evaluated.

| Mutually exclusive outcome | Trade rows | Share of all 73,704 trade rows |
| --- | ---: | ---: |
| No earlier quote in the fixed daily file | 1 | 0.0014% |
| Earlier valid quote, age at most 100 ms | 39,911 | 54.1504% |
| Earlier valid quote, age over 100 ms through 1 s | 27,080 | 36.7416% |
| Earlier valid quote, age over 1 s through 5 s | 6,423 | 8.7146% |
| Earlier valid quote, age greater than 5 s | 289 | 0.3921% |
| Invalid latest preceding quote | 0 | 0% |

The outcomes sum to all trade rows. Separately, 2,688 trades had at least one quote with an equal collector timestamp; those equal-time quotes were excluded under the frozen strict rule. None of the age bands was chosen after observing forecasting performance. Age measures time since the last observed quote update/reconfirmation; it is not proof that an unchanged quote is stale.

## Interpretation and next evidence gate

Collector ordering is materially more explicit than the previously inspected trade-only archive. It still represents this provider's observation point and normalization, not every client's receipt clock or a guaranteed total order across exchange channels. Equal-clock ambiguity, missing trade IDs and possible duplicate records remain relevant to a later origin contract.

The provider says CSVs omit disconnect markers and are exported from captured WebSocket data; normalization and book reconstruction introduce their own conventions. Thus zero backsteps, matching checksums and full-day boundary coverage cannot prove uninterrupted collection or reproduce every original exchange message. [Export limitations](https://docs.tardis.dev/downloadable-csv-files/api), [collection/data FAQ](https://docs.tardis.dev/faq/data), [book-reconstruction FAQ](https://docs.tardis.dev/faq/order-books)

No revision lineage, error/shock adjudication or independent latent efficient price was established. Best quotes are observable reference states, not ground truth for the original RippleNet mechanism.

The bounded acquisition/schema gate passed for this sample. The next step, if pursued, is a separately frozen multi-session design with matched origins, recorded-trade and quote-reference endpoints, identical admissible inputs, conservative clock/tie/gap rules, strong baselines, and protected evaluation. This single first-of-month day cannot supply session-level generalization or justify a forecast result, larger architecture, paid source, or public release of restricted trained artifacts.
