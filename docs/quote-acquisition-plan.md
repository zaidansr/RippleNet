# Frozen paired quote/trade access and schema audit

This stage follows the owner's instruction to continue the trade-versus-quote roadmap. It audits whether a concrete free pair can support the next experiment. It fits no model, evaluates no forecast target and does not silently convert data acquisition into a market-performance result.

## Source choice and rights

The two bounded source reviews are [Binance engineering](quote-data-engineering-audit.md) and [independent alternatives](quote-data-source-review.md). Binance offers a same-product USD-M trade/bookTicker pair on 2024-03-30, but not a paired spot reference for our 2017 spot records, and its quote history is older than preferred. A repository collaborator states the USD-M bookTicker history ends on that day. Same-symbol spot and futures must not be mixed.

Choose the Tardis **Kraken spot XBT/USD sample for 2026-06-01**, before the documented Kraken symbol/feed transition. Its documented collector timestamps and later date motivate an access audit. File existence, size, contents and adequate coverage have not been verified. This is a new venue/product/period and cannot retrospectively validate the earlier Binance findings.

The current Tardis terms were directly retrieved and privately pinned with SHA256 `ea5901192dce12c72f2303702b7f2bf87826b4b1a44806f8659d0fd91b030b11`. Their research-publication and AI/model clauses support internal processing and qualifying aggregate reports but restrict public trained models/weights. This is not an open-data grant. Publish general original code and eligible non-reconstructive findings only; keep all raw/event-level data, fitted parameters, model-bearing artifacts and vendor snapshots private. Do not apply the Binance CC license to Tardis-derived findings. Recheck that the documented first-of-month access remains free, with no key/account/subscription; stop on an authentication or payment requirement. [Current terms](https://docs.tardis.dev/legal/terms-of-service), [sample access](https://docs.tardis.dev/downloadable-csv-files/api).

## Fixed acquisition

Only these two URLs may be requested as data bodies:

- `https://datasets.tardis.dev/v1/kraken/trades/2026/06/01/XBT-USD.csv.gz`
- `https://datasets.tardis.dev/v1/kraken/quotes/2026/06/01/XBT-USD.csv.gz`

Use an unauthenticated GET; documented HEAD behavior is not an availability test. No API keys, new accounts, trials, provider messages, paid access or cloud services. Redirect transfer accounting is not byte availability evidence; keep requests limited to this free sample. Ordinary public documentation/metadata requests may verify conditions.

Hard limits: trades at most 32 MiB compressed and 256 MiB expanded, quotes at most 128 MiB compressed and 1 GiB expanded; total at most 160 MiB compressed and 1.25 GiB expanded. At most two million trade records and five million quote records. Reject advertised oversize responses before reading their bodies; enforce streamed limits when length is unknown. No cap expansion, replacement dates, alternative instrument or automatic provider fallback after inspection. A failure remains a bounded access/schema finding. Spending still requires explicit owner approval.

Save initial URL, HTTP status, nonsensitive headers, sizes, source terms hash, retrieval time, SHA256/MD5 and any advertised content-integrity check. Do not publish signed redirect query strings. Keep compressed files and all detailed records outside the public repository. Gzip expansion must be streamed with hard limits and integrity checked if complete.

## Audit before forecasting design

Verify actual CSV headers against the documented trades/quotes schemas, and same exchange/instrument identity across files. Do not assume a live WebSocket schema is the export schema or change the intended dataset to fit an unexpected header. Count rows, missing fields, invalid numbers, trade-ID behavior, receipt/exchange-time monotonicity and ties. Use integer microsecond timestamps and exact Decimal value parsing. Do not sort or deduplicate the retrieved files or invent missing records.

Count finite positive quote prices/amounts and locked/crossed books separately. These are eligibility diagnostics, not verified bad-record causes. Record whether trades and quotes cover the requested day and any boundaries/gaps; an omitted disconnect marker cannot be treated as proof of continuous recording.

For a descriptive alignment check only, choose the last quote with a **strictly earlier collector timestamp** than each trade; preserve the supplied quote-file order within quote ties and disclose cross-file tie ambiguity. Do not use nearest-time or a later quote. If the most recent preceding quote is invalid, count it as invalid rather than backfilling an older clean-looking quote. Report missing/invalid predecessors and quote ages in fixed bands at most 100 ms, at most 1 s, at most 5 s and greater than 5 s; no threshold is selected as a winning predictor rule. These ages measure last observed quote/reconfirmation, not certainty that an unchanged book is stale.

The audit must distinguish provider collector-clock alignment from actual client receipt latency or a guaranteed exchange-wide order. Record revision, deduplication and reconstruction limitations from the provider. No source checksum proves original availability or economic truth. Any publication must satisfy the permitted aggregate-report scope; do not publish an aligned per-event dataset.

## Decision and next gate

Report access failure, schema failure, incomplete acquisition or a complete bounded inspection honestly. A pass means only that this sample is structurally inspectable under a specified clock convention. It establishes neither enough independent sessions for forecasting inference nor an error/shock ground truth.

If usable, freeze a separate multi-session forecast design using matched clock-time origins, trade/midpoint endpoints, identical inputs for compared methods, conservative quote timing, freshness and gap rules, strong baselines, purpose-specific metrics and protected data. Those numeric choices remain unresolved here; see the [comparison contract](quote-comparison-contract.md). A midpoint is an observable reference, not a latent efficient price. If this sample fails, do not train or substitute data invisibly.
