# Independent review: paired Kraken sample

This review concerns only the two files specified by the [frozen acquisition plan](quote-acquisition-plan.md), commit `6fed87f6b17d930d721b1c7387a0f56cf81638e2`: Tardis Kraken spot XBT/USD trades and quotes for 1 June 2026. No other date, asset, target, predictor or model was evaluated.

**Source attribution and publication scope:** These aggregate inspection findings derive from [Tardis Kraken data](https://docs.tardis.dev/historical-data-details/kraken). Raw records, aligned observations and vendor snapshots remain private. [Current Tardis terms](https://docs.tardis.dev/legal/terms-of-service) govern use; this report grants no Creative Commons or other open-data license. No trained parameters were produced.

## Independent verification

Independently reread both compressed files and reproduced their sizes, SHA256 hashes and advertised MD5 checks against the private manifest. Fully decompressed both through CRC-verified EOF, reproduced expanded CSV hashes and sizes, and checked exact headers, row widths and identities. The pair totals 12,460,410 compressed bytes and 78,513,685 expanded bytes, within the declared limits. A checksum match establishes the retrieved version's integrity, not its original availability or economic correctness.

Reproduced 73,704 trade rows and 862,680 quote rows. Both identify `kraken` and `XBT/USD`. Integer microsecond timestamps fall within the requested UTC day. Exact Decimal parsing found positive finite prices/amounts and no locked/crossed quotes. Neither clock steps backward within either file. These are structural checks, not observation-error labels.

All trade IDs are empty. Preserved 381 consecutive identical trade rows: they cannot be classified as duplicate executions merely from equality. There are 37,564 adjacent collector-time ties among trades and 8,798 among quotes. No deduplication, sorting or inferred global sequence was applied.

## Alignment result and limits

A separate vectorized reconstruction reproduces every reported age band under the frozen rule: choose the last supplied-file quote with collector time strictly before the trade. Counts are 39,911 at most 100 ms; 27,080 over 100 ms through 1 s; 6,423 over 1 s through 5 s; 289 over 5 s; and one missing predecessor. They account for all trades. For 2,688 trades, same-time quotes exist and are excluded. Code inspection confirms an invalid latest predecessor would be counted rather than replaced by an older valid quote; these all-valid files do not exercise that failure branch.

The audit establishes a structurally usable paired sample under a declared collector-clock convention. Separate-file ties do not reveal cross-channel causality. Missing IDs impede execution-uniqueness checks. CSVs omit disconnect records, so neither observed gaps nor quote ages prove uninterrupted coverage or stale economic prices. Reconstructed BBO, provider-clock assumptions, export revisions and deduplication remain material [source limitations](quote-data-source-review.md).

No forecasting or error-versus-shock conclusion follows. One session supplies no cross-session generalization evidence, and a midpoint would remain an observable reference rather than latent-price ground truth. A subsequent experiment requires its own frozen timing, gap, coverage and target rules before scoring.
