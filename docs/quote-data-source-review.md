# Independent quote-source review

Reviewed 8 November 2026. Scope: two alternatives to Binance Vision, using providers' own documentation and terms. No compressed dataset bodies, live market messages, accounts or paid services were used. This is a source/access review, not a data-quality result or forecast experiment.

## Decision

**Tardis.dev's Kraken spot archive is the strongest documented candidate for a bounded paired trade/quote audit.** Its free monthly samples and research-publication terms establish a plausible route, subject to actual file-size, coverage and schema checks. It is not yet an acquired, validated dataset. Direct Kraken access does not establish an equivalent historical paired dataset in the sources reviewed.

## Candidate 1: Tardis.dev, Kraken spot

Tardis documents Kraken coverage from 4 June 2019, free first-of-month CSV downloads without an API key, and explicitly links both trades and quotes for XBT-USD on 1 July 2019. The provider changed from Kraken WebSocket v1 to v2 on 10 July 2026; exchange-native XBT/USD became BTC/USD. Collection uses multiple connections in London. [Kraken coverage and sample links](https://docs.tardis.dev/historical-data-details/kraken).

The concrete proposed access check is **1 June 2026, Kraken XBT/USD spot**, before that format transition:

- [Trades endpoint](https://datasets.tardis.dev/v1/kraken/trades/2026/06/01/XBT-USD.csv.gz).
- [Quotes endpoint](https://datasets.tardis.dev/v1/kraken/quotes/2026/06/01/XBT-USD.csv.gz).

These paths follow the documented API and coverage rules; this review did not establish their current HTTP success, nonempty contents or sizes. The metadata summary endpoint was inaccessible through browsing, and a bounded local metadata request failed DNS resolution. No alternate date was selected by inspecting prices.

Files are daily gzip CSV, partitioned and sorted by collector receipt time. They can be empty. Exports normally follow the next day; disconnect markers are omitted. MD5 response metadata can verify retrieved bytes. Importantly, the documented API returns 404 for HEAD requests; that response cannot establish absence. A storage redirect counts the entire file toward transfer limits. Exact compressed/expanded sizes and row counts remain unknown. [Datasets API](https://docs.tardis.dev/downloadable-csv-files/api).

Quotes are reconstructed from actual exchange WebSocket L2 updates, rather than an independently sampled price or synthetic corruption. BBO changes produce rows containing bid/ask prices and amounts, exchange timestamp and collector `local_timestamp`, with microsecond UTC encoding. A missing exchange timestamp can fall back to receipt time. These quotes are distinct from the provider's native-feed `book_ticker` dataset. [CSV schemas and construction](https://docs.tardis.dev/downloadable-csv-files/data-types).

### Rights that constrain the public repository

Retrieval provenance: search-service `find` on the primary terms URL returned the current clauses, whereas opening the Markdown variant failed through that service and older search snippets differed. The coordinating agent then obtained a successful direct HTTP GET, returning Markdown, and saved a private snapshot on 8 November 2026. I independently read its modification date and §§9.3–9.5 and verified SHA256 `ea5901192dce12c72f2303702b7f2bf87826b4b1a44806f8659d0fd91b030b11`. The snapshot is `work/quote-audit/tardis-terms-current.md`, outside the public repository. This confirms the reviewed current text; it does not establish future terms or dataset coverage.

The terms modified 28 October 2026 permit internal research, AI-assisted processing and internally usable trained models. Section 9.3 allows qualifying non-reconstructive derived statistics, reports and academic papers to be shared. Raw/event-level datasets are not thereby publishable. Section 9.5 prohibits releasing trained ML models, their weights or access to outsiders; a public fitted AR model would require treating that restriction seriously. Free/sample downloads retain their license after access expires, subject to stated restrictions and licensor rights. Coinbase-specific restrictions are separate and are not a reason to infer the same permissions for Coinbase. [Tardis terms, definitions and §§9.1–9.7, 10.4, 23](https://docs.tardis.dev/legal/terms-of-service).

Consequently, a later study could keep observations and fitted parameters private while publishing independently written general code and permitted aggregate findings. Do not copy the previous Binance study's publication pattern automatically: coefficients, model-bearing JSON and event-level outputs need exclusion. This review grants no open-data license and does not establish that every proposed output meets the contractual definition of derived data.

### Clock and revision limitations

Tardis describes synchronized collector clocks and arrival-order retention, but explicitly denies a guaranteed exchange-wide ordering across independent channels. Same exchange timestamps do not identify a pre-trade book. CSV trades are deduplicated; export errors can cause revised CSVs. Captured gaps cannot be repaired retrospectively, and incident reports are incomplete as an outage census. [Timestamp, ordering, revision and quality FAQ](https://docs.tardis.dev/faq/data).

Our proposed guard is to join only quotes with strictly earlier collector timestamps, record equal-time ambiguity, and never use future quotes to populate a feature. Separate CSV row numbers do not resolve ties across files. Hashes pin the downloaded version; they do not independently certify the recorder's clock, completeness or historical availability. Without disconnect messages or equivalent evidence, stale quotes cannot be classified confidently as uninterrupted live coverage.

## Candidate 2: Kraken direct

Kraken's official downloadable history provides trades through 30 September 2026, with timestamp-ordered seven-column CSVs and build manifests. Its complete distribution uses approximately 2 GB parts. The reviewed page does not offer matching historical BBO files; neither its checksums nor subsequent live quotes supply those missing observations. [Historical time and sales](https://support.kraken.com/in/articles/360047543791-downloadable-historical-market-data-time-and-sales-).

The public v2 ticker supports BBO-triggered updates with bid/ask and a ticker timestamp; subscription acknowledgment clocks are different fields. The trade channel supplies book-specific trade IDs and trade timestamps. These can support a separately designed prospective capture, not reconstruct the required historical paired sample. [Ticker specification](https://docs.kraken.com/exchange/api-reference/spot-websocket-v2/ticker), [trade specification](https://docs.kraken.com/exchange/api-reference/spot-websocket-v2/trade).

Current global terms reserve content rights, allow use for one's own benefit and restrict third-party distribution. I did not establish a direct-feed grant covering public ML-derived research/model publication. Public unauthenticated access is insufficient evidence of those rights. The AI-tool annex concerns a different service and should not be misrepresented as a blanket market-data ML prohibition. [Kraken global terms, §§8–9 and Annex V](https://www.kraken.com/legal/global-terms).

## Smallest useful next action

Freeze a two-file Tardis access/schema audit with hard compressed and expanded byte caps, aborting if either cap is exceeded. Do not substitute a more convenient asset/date after examining outcomes. Record source terms/version, retrieval metadata, hashes, timestamp ties, quote gaps, invalid/crossed books, trade-ID behavior and paired coverage before defining any predictor test. Failure to obtain trustworthy timing or a complete enough quote history should remain an audit failure, not trigger silent filtering or provider shopping.

If that audit passes, matched trade-versus-midpoint targets could distinguish sensitivity to recorded transaction prices from persistence in quotes. This would be a fresh Kraken/product/period study, not retrospective validation of the 2017 Binance results. A midpoint is an observed book summary, not efficient-price ground truth. Neither source supplies independently established observation-error versus genuine-shock labels; future correction labels, if later found, would be valid outcomes only after maturity and never earlier features.
