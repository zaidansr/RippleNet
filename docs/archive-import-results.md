# Offline archive import and target attachment

This stage implements the bounded importer described by the [source contract](archive-import-contract.md) and [target contract](archive-target-contract.md). It performs a retrieved-file-order engineering check, not a forecasting comparison or original online backtest.

## Assumptions and implementation

Before coding, the subagent contracts and review identified the main risks: timestamp-unit confusion, mixing source IDs with row positions, sorting away anomalies, dropping incomplete origins, treating missing correction evidence as negative labels, and using whole-file metadata in origin features.

[The implementation](../ripplenet/archive_import.py) reads only the declared seven-column, headerless Binance spot individual-trades format. The caller supplies symbol, UTC date and timestamp unit. That declaration does not itself verify that the symbol was listed or certify the file's source. Expected input hashes must come from independently retained provenance.

Prices and quantities remain exact `Decimal` values. The parser rejects invalid fields, duplicate/backward IDs, backward timestamps and out-of-day values without sorting or silently skipping rows. Equal timestamps preserve file order. Source-ID gaps are recorded as diagnostics; they neither create rows nor prove recording corruption. Quote quantity is not required to equal price times quantity exactly.

The lazy CSV iterator emits immutable records before reading later CSV records. A malformed later record raises with its zero-based record ordinal; previously emitted records and origin snapshots remain unchanged. Caller-owned streams remain open. CSV record ordinals need not equal physical line numbers.

The offline CLI accepts an explicit local CSV/ZIP and expected SHA256. It has no network client. It limits input to 2 MiB and ZIP expansion to 20 MiB, accepts one stored/deflated CSV member without extraction, and records input/CSV hashes solely as provenance. Integrity, decoding and decompression preflight are separate from lazy record parsing; an artifact failure at that boundary can stop ingestion before any origin is emitted.

## Targets and unsupported labels

Every accepted raw trade row creates one immediate origin. For row `k` and fixed positive `H`, the separate target is `log(price[k+H]) - log(price[k])`, available at row `k+H`. Horizons count retrieved rows, regardless of trade-ID gaps or timestamp ties. Examples retain the horizon and immutable origin snapshot; future values and whole-file hashes are not origin features.

Every accepted origin remains in the output. At normal EOF, incomplete future-row targets are censored. If CSV validation fails, accepted origins remain accessible, unfinished targets remain pending, and the CLI reports `validation_error` with nonzero exit status rather than declaring a clean end. Empty input reports zero origins; it is not a usable training corpus or evidence of adequate coverage.

The source provides no correction ledger. Examples explicitly carry `correction_status='unsupported'`, and requests for a correction label raise `NotImplementedError`. The generic replay's price-only no-notice calculation is not exposed as a fabricated real negative label. No model fitting, correction classifier or training dataset split is implemented.

## Validation

All **82 repository tests pass**, including **13 new importer/attachment tests**, under Python 3.13.3. Deterministic invented CSV and ZIP fixtures require no random seed or vendor data. Tests cover precise units/day boundaries, gaps/ties, malformed tails, prefix invariance, retained censoring, unsupported labels, input identity, checksums and structured failures for unsupported or damaged ZIP compression.

```sh
python -m unittest discover -s tests -p test_archive_import.py -v
python -m unittest discover -s tests -q
```

The previously downloaded, checksum-pinned archive was also processed locally without another download. Input and CSV hashes matched the earlier audit; the importer completed normally and retained its incomplete suffix targets. Attributed data-derived coverage findings are recorded in the separately licensed [source-audit supplement](binance-readiness-audit.md#offline-import-revalidation). The local JSON report and raw archive remain outside this repository.

To run the offline tool on a separately acquired permitted file, substitute its local path and independently established input hash:

```sh
python -m ripplenet.archive_import LOCAL_ARCHIVE.zip --symbol BTCUSDT --date 2017-08-17 --timestamp-unit ms --horizon 2 --expected-sha256 INPUT_SHA256
```

The horizon of two rows is an engineering fixture choice, not a selected forecasting horizon. The command prints coverage and provenance, not predictions or performance scores. The input's use conditions still apply; this tool grants no additional data rights.

## Research implication

This completes an offline parser and target-alignment boundary. Passing its checks establishes consistency with a chosen retrieved artifact, not original dissemination order, receiver availability, economic truth or correction/shock ground truth. The [previous feasibility decision](real-data-feasibility-decision.md) remains in force. No real-data performance, significance, generalisation, novelty or profitability conclusion follows.

Three subagents supplied the import contract, target mathematics and [independent review](archive-import-review.md). No provider was contacted, account created, paid resource used, or new market data downloaded. Existing synthetic experiments and frozen numerical results are unchanged.
