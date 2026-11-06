# Retrieved-archive row and target contract

This stage attaches recorded trade-price targets to a retrieved file's row order. It is a schema, prefix and outcome-availability exercise using deterministic development fixtures. It does not fit a model, certify original publication order or receiver availability, or supply correction labels that the source lacks.

## 1. Two identifiers, one declared prefix

A frozen `ArchiveTrade` carries these fields under the confirmed API:

- `row_ordinal`: contiguous zero-based position in the accepted trade rows of this retrieved file.
- `trade_id`: the source's trade identifier, distinct from the row position.
- `event_time`: the source timestamp as an integer, with its declared unit retained in provenance.
- `price`, `quantity` and `quote_quantity`: finite `Decimal` values under the declared schema.
- The source Boolean fields, parsed as actual Booleans rather than truthiness of nonempty strings.
- `spec`: `ArchiveSpec(symbol, session_date, timestamp_unit)`, where `session_date` is a Python date and the time unit is explicitly `ms` or `us`.
- `id_gap_before`: a diagnostic for nonconsecutive source trade identifiers, not a synthetic row or a correction flag.

The predetermined namespace is `binance.spot.trades:SYMBOL:DATE`. Do not include a whole-file hash or other future-dependent quantity in predictive features. For this single-file adapter, every accepted raw trade row counts. The lazy reader uses a strict seven-column row schema; headers or schema changes must not be silently skipped or autodetected into a different schema. Blank or invalid rows must not be used to compress a failed file into an apparently valid complete sequence.

`row_ordinal` and `trade_id` are not interchangeable. Require strictly increasing trade IDs, but allow gaps and record them as diagnostics. A gap does not insert missing rows or alter the horizon. It is evidence of nonconsecutive IDs, not by itself proof of a particular missing-record cause. Duplicate or decreasing trade IDs fail validation.

For row `k`, the only declared feature prefix is rows `0` through `k`, inclusive, in **retrieved file order**. Event times must be nonnegative integers in the declared unit and nondecreasing. Equal event timestamps retain file order; do not sort or average them. A timestamp decrease is rejected rather than repaired by reordering. Event time is a field, not a replacement for the row cursor.

The ordinal convention is deliberately weaker than verified as-of exchange sequencing. Contiguous row numbers, increasing trade IDs and checksums do not prove when a record's current contents first became available or whether an archive was revised later.

## 2. Streaming validation and failure behaviour

Use a small iterator that validates a row before yielding its immutable record. Validation covers the seven columns, numeric/Boolean types, identifier/time order and valid finite prices/quantities. Prices and quantities must be strictly positive; quote quantities may be zero but not negative. Do not require exact price-times-quantity equality, since this contract supplies no such source rounding guarantee. The timestamp unit comes from `ArchiveSpec`, not an inference from integer magnitude.

At a bad row, raise a clear error identifying the zero-based CSV record ordinal and reason, without accepting that row or continuing past it. A CSV record may span physical lines. Previously yielded records remain usable as a validated structural prefix. They do not become proof that the entire artifact is valid. No sorting, renumbering past the failure, guessed field values or silent deduplication is allowed.

Do not label a failed partial read as successful complete-file ingestion. If retaining partial diagnostic output, mark the read failure and distinguish its truncation from a normally completed file. In either case, unobserved future endpoints cannot become zero returns or negative correction labels.

## 3. Reuse the existing replay narrowly

The public wrapper is:

```python
TradeReplay(spec, horizon)
TradeReplay.consume(trade: ArchiveTrade) -> TradeOrigin
TradeReplay.examples() -> tuple[TradeExample, ...]
TradeReplay.seal() -> None
TradeReplay.correction_label(...)  # raises NotImplementedError
```

`TradeOrigin` freezes the trade and its origin snapshot. Each `TradeExample` carries that origin, a separate target `Outcome`, the fixed `horizon`, and `correction_status='unsupported'`. Internally, each accepted archive row maps to the existing `PriceRecord` with the same row ordinal and a unique namespaced ID. Every archive row is a price update; equal timestamps do not merge updates. No `CorrectionNotice` is invented. Reject a trade from a different `ArchiveSpec` rather than mix namespaces or timestamp units in one replay.

Store the immutable origin `Snapshot` returned at that point. It contains only the current and preceding as-recorded price information and prefix counts. Do not populate an origin snapshot from a future full-file statistic, a revised reference or a target column. Whole-file hashes, file length, last timestamp and other retrospective metadata are provenance, not predictive features.

The recorded price is the trade price present in this retrieved row. It is not a book midpoint, latent efficient price, executable liquidation value or verified original uncorrected price. There is no order-book or receiver-clock API in this adapter.

## 4. One target attachment per origin

For a fixed positive integer `H`, let \(P_k\) be the retrieved trade price at row `k`. Define

\[
Y_{k,H}=\log P_{k+H}-\log P_k.
\]

The endpoint is exactly `origin row ordinal + H`. `H` counts subsequent retrieved trade rows, not source-ID increments, all original exchange messages, seconds or receiver latency. If the file omits source trades, the target still means the next `H` retrieved rows. Do not relabel it the next `H` complete-market trades without separate coverage evidence.

Each attachment should retain the origin ordinal, namespaced source identity, immutable origin snapshot, fixed horizon and an explicit `Outcome`. Future target values belong in the separate outcome field, never the feature snapshot.

Use the existing outcome meanings:

| Status | Meaning for this target |
| --- | --- |
| `pending` | Endpoint `k+H` has not been consumed and the input remains open. |
| `observed` | Both required prices exist; value is fixed and `available_at=k+H`. |
| `censored` | The observed file/prefix was closed before the endpoint. |
| `unavailable` | A required reference cannot be supplied under the declared contract. |

With strictly positive validated trade rows, the missing-price branch should not normally occur for an accepted origin. Invalid data are rejected, not turned into an `observed` target. Nonobserved outcomes have neither value nor availability. Retain their rows; do not drop the final `H` origins and conceal their censoring. Record observed/pending/censored/unavailable counts separately from input-validation failures.

For a completed valid file of `N` rows and `N>=H`, there are `N-H` observed targets and `H` censored targets. If `N<H`, every accepted origin is censored. An empty core iterator produces zero records and zero examples; it does not manufacture outcomes. A CLI may reject emptiness as an explicit input failure. In an open prefix, unresolved suffix targets are pending instead. Sealing exactly at an endpoint permits that completed target; sealing one row earlier does not.

An offline builder may fill a separate future outcome after reading the file. That is legitimate label attachment, not proof that the outcome was available to the origin's feature computation. Preserve `available_at` and keep the feature-generation boundary explicit.

## 5. Correction labels are unsupported, not zero

This archive adapter supplies no correction notices or independently verified correction ledger. Consequently, it must not call a price-only replay's fixed-window `correction_label` and interpret the resulting no-notice value as a source label. An empty supplied notice stream is not evidence of an exhaustive real notice stream.

Expose the limitation through `correction_status='unsupported'` on examples and `NotImplementedError` from `TradeReplay.correction_label`. Do not manufacture `Outcome('observed', 0, ...)`, prospective quality flags, shock labels or break-notice lineage. Increasing trade IDs, small price changes and unmodified downloaded bytes supply none of those labels.

The replay's correction API remains meaningful for synthetic fixtures or a later separately audited adapter with qualifying notices. That does not make it meaningful for this price-only archive.

## 6. Training cutoff is a necessary timing check

For a return-only example from row `k`, the target can enter a fit after consuming row `f` only when

\[
\text{target.status=observed}\quad\text{and}\quad k+H\le f.
\]

This is timing relative to the retrieved-row replay convention, not a receiver-time claim. Equality means the fit occurs after row `f` has been consumed.

The existing `training_eligible(target, label, fit_ordinal)` requires both an actual target and an actual matured correction label. It must not be satisfied here by supplying a fabricated zero label. The return-only timing expression above is sufficient to state this contract; no extra training helper or fitted-model API is required in this stage.

No availability helper alone verifies feature provenance, row/target alignment, source admissibility or correct fitting. Replay the intended historical prefix for a historical fit, preserve origin features, and fit any transformations solely on eligible development examples. Training targets crossing a split boundary are not available before that boundary. Dependent overlapping windows would require appropriate blocking in a later statistical experiment; this stage makes no fitted-model or significance claim.

## 7. Frozen numerical development fixture

Use the following literal fixture to test the schema and target boundary, not to choose a horizon or fit a model. Prices and quantities are exact Decimal literals. Boolean fields are illustrative actual Boolean values. If constructing a dated `ArchiveSpec`, these artificial millisecond timestamps correspond to 1970-01-01; the fixture does not claim that an actual market archive exists for that date.

| Row ordinal | Source ID | Event time | Price | Quantity | Quote quantity | Buyer-maker | Best-match |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 10 | 1000 | 100 | 1 | 100 | true | true |
| 1 | 11 | 1000 | 102 | 2 | 204 | false | true |
| 2 | 14 | 1001 | 101 | 1.5 | 151.5 | true | true |
| 3 | 15 | 1002 | 103 | 1 | 103 | false | true |

The equal timestamps at rows 0 and 1 preserve order. The source-ID jump from 11 to 14 is flagged but creates no extra rows. For the fixed fixture horizon `H=2`:

- Origin 0 is pending after row 1, then observed at row 2 with \(\log(101/100)\approx.0099503309\).
- Origin 1 becomes observed at row 3 with \(\log(103/102)\approx.0097561749\).
- Origins 2 and 3 remain pending while the stream is open and become censored when sealed after row 3.
- At a fit cutoff of 2, only origin 0 has a matured return. No correction label is available for any row.

Existing replay return calculation uses a fixed local Decimal context before producing a float; tests should use its documented numerical tolerance. These fixtures are deterministic, so no random seed is required.

## 8. Required boundary tests

1. IDs, types and ordering: accept and flag the fixture's source-ID gap; preserve equal event times; reject duplicate/decreasing source IDs and malformed rows without silently continuing.
2. Prefix immutability: changing a later row cannot change an earlier numeric feature snapshot. Provenance identifying changed artifact bytes may differ, but must not enter predictive features.
3. Target maturity: test exactly at, one row before and one row after `k+H`; future changes may alter an unmatured target but not one whose endpoint is already in the unchanged prefix.
4. Suffix retention: keep one attachment per accepted origin, including pending/censored records; verify the complete-file counts above, including a file shorter than `H`.
5. Availability: a target ending exactly at the fit row is eligible only after consuming that row; later, pending, censored and unavailable targets are not.
6. Unsupported labels: a request for archive correction supervision fails explicitly; no absent notice stream becomes observed negative labels.
7. Failure transparency: a bad later row leaves earlier emitted records intact but prevents a complete successful ingestion claim.
8. Identity separation: horizon arithmetic uses row ordinals, never source IDs or timestamp differences.

No future numerical feature, final-file length or hindsight correction should appear in an origin snapshot. Offline target fields must remain visibly separate from those snapshots.

## 9. Scientific boundary

This adapter can establish that calculations respect the chosen retrieved-file prefix. It cannot establish that those rows were present in that form at the original historical forecast time. An archive may have a revision policy without a retained historical revision ledger or original receipt clock. A checksum certifies the retrieved artifact, not its earlier availability.

Do not let a successful parser, target test or replay test change an unsupported as-of evidence gate to passed. A later study may honestly analyse a retrieved-row recorded-return task under that limitation, but it cannot present the resulting features as verified original receiver-time information or claim the original RippleNet observation-error mechanism was identified.

No data access, downloads, network calls, fitted models or paid resources are required to implement and test this contract. No new data or model runs were performed in writing it.
