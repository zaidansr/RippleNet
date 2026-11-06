# Strict offline spot-trade archive import contract

This is a narrow parsing contract, not an as-of-data certification, forecast model, network client or correction-feed adapter. It permits deterministic iteration over a caller-supplied Binance spot individual-trades CSV in its recorded file order. No new download or dataset is needed to implement or test it.

## Evidence and supported scope

The [official archive README](https://raw.githubusercontent.com/binance/binance-public-data/master/README.md) specifies seven individual-trade columns and the spot timestamp change to microseconds from 1 January 2025. It also warns that historical archives can be revised. The [official historical-trade schema](https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market#old-trade-lookup) supplies the corresponding integer IDs/timestamps, decimal-valued strings and boolean meanings. The prior [readiness audit](binance-readiness-audit.md) verified a small headerless sample, but did not establish original dissemination/receipt or correction history.

This contract deliberately accepts headerless seven-column individual-trade CSV only. It does not automatically adapt aggregate trades, candles, futures formats, headers or a newly changed vendor schema. An unsupported layout fails clearly rather than being guessed from column names or digit counts.

## Proposed API

```python
@dataclass(frozen=True)
class ArchiveSpec:
    symbol: str           # explicit, e.g. "BTCUSDT"
    session_date: date    # declared UTC calendar day
    timestamp_unit: Literal["ms", "us"]

    @property
    def namespace(self) -> str:
        # fixed format: binance.spot.trades:SYMBOL:YYYY-MM-DD
        ...

@dataclass(frozen=True)
class ArchiveTrade:
    spec: ArchiveSpec
    row_ordinal: int
    trade_id: int
    event_time: int
    price: Decimal
    quantity: Decimal
    quote_quantity: Decimal
    is_buyer_maker: bool
    is_best_match: bool
    id_gap_before: int

iter_spot_trades(stream: TextIO, spec: ArchiveSpec) -> Iterator[ArchiveTrade]
```

This is the root-frozen interface. `trade_id` is the source trade identifier; it must remain distinct from `row_ordinal`. Each returned record and its context are immutable. Fail with a `ValueError` subclass such as `ArchiveFormatError`, including the zero-based CSV record ordinal and offending field/reason where available.

The stream is already open and text-decoded by its caller. The iterator does not open URLs, decompress/download archives, fit parameters, create directories, or close the caller's stream. A separate bounded offline CLI may open local CSV/ZIP inputs and record byte hashes. Such hashes belong to provenance, not origin identifiers or predictive features, and do not prove historical availability. The CLI has no network client and reports an accepted-prefix validation failure distinctly from clean EOF.

## Context and timestamp validation

Require a nonempty canonical symbol, an actual calendar date and an explicit supported unit. The namespace property is deterministically `binance.spot.trades:SYMBOL:YYYY-MM-DD`, using the caller's declared context. A practical symbol lexical rule is uppercase ASCII letters/digits; validating that a pair was genuinely listed is outside an offline parser. Do not infer symbol or date from a nearby directory, or silently reuse metadata from another file.

Require nonnegative ASCII integer timestamps. Interpret them using the explicit unit and check the half-open UTC-day interval `[session_date midnight, next midnight)`, using integer arithmetic. Never use the host timezone or a float epoch conversion for this check.

The declared unit must match the supported archive regime: pre-2025 milliseconds under this adapter's stated convention, and microseconds from 2025 onward. The selected 2017 sample verified the former; the README documents the latter transition. A conflicting unit fails rather than being silently rescaled. Acceptance of a timestamp inside the declared day still does not prove full-day coverage or contemporaneous availability.

## Per-record lexical and value checks

Parse one CSV record at a time with strict CSV syntax. A physical newline is not necessarily a CSV record boundary, so keep the CSV-record ordinal separate from any diagnostic physical line number.

| Field | Required behaviour |
| --- | --- |
| Width | Exactly seven columns; reject blank records and headers. A normal final newline is not a blank record. |
| Source trade ID | Nonnegative ASCII integer; zero is valid. Preserve its integer value. Reject missing values, signs, fractional notation and scientific notation. |
| Price and base quantity | Parse directly from finite decimal strings into `Decimal`; require strictly positive values. |
| Quote quantity | Parse directly into finite `Decimal`; require nonnegative value. |
| Numeric spelling | Require a documented plain fixed-point grammar, e.g. `[0-9]+(?:\.[0-9]+)?`; reject whitespace padding, commas, exponents, NaN and infinities. Do not pass through binary floats. |
| Flags | Accept only the explicitly enumerated literals `True`, `False`, `true`, `false`, mapping to actual booleans. Reject `1`, `0`, empty strings, `yes` and arbitrary case variants. |
| Time | Nonnegative ASCII integer satisfying the explicit unit/day checks above. |

No price/quantity rounding, quantization or global Decimal-context change is needed merely to parse values. Do not require `quote_quantity == price * quantity` as a universal format rule: the audited sample's arithmetic agreement is not proof that every product/date has identical rounding conventions. Any such consistency check must be a separately documented diagnostic that leaves recorded values untouched.

## Source identifiers, ordinals and order

`row_ordinal` is contiguous and zero-based in accepted file order. `trade_id` is an exchange identifier, not an ordinal and not a message counter. A synthetic fixture with IDs 1000 and 1003 must emit ordinals 0 and 1. Never create records 1001/1002, divide a target horizon by ID differences, or assume the audited early sample's coincident ID/ordinal values are a general property.

A cross-file source key uses the declared namespace and source trade ID. An external provenance manifest can associate that context and row ordinal with a versioned source-file identity; hashes remain in the manifest rather than origin identifiers or features. Alternative archive versions must not be silently merged as though they were independent observations.

For this strict iterator, require source IDs to increase and event times not to decrease. Gaps in source IDs are allowed without imputation; they do not independently establish lost trades. Duplicate/backward IDs or backward timestamps raise an order/format error. They are not automatically deduplicated, sorted, discarded, or relabeled as recording errors. Equal timestamps are allowed and retain the original file tie order. This is a declared archive-order constraint, not a proof of original feed sequencing.

Set `id_gap_before=0` for the first row, because the input alone provides no preceding source reference. For each later accepted row use `trade_id - previous_trade_id - 1`. The synthetic IDs 1000 then 1003 therefore produce flags 0 then 2. This diagnostic records absent numeric IDs between successive input rows without inventing their meaning or synthesizing missing trades.

Do not silently skip any blank, invalid, duplicate or otherwise inconvenient record: doing so would change later event-count horizons and the meaning of an inclusive prefix.

## Lazy prefix and failure behaviour

The iterator must not scan the complete file before emitting its first trade. Given a valid prefix followed by malformed data, requesting the valid prefix emits exactly those records; requesting the next malformed record raises. Already emitted immutable records remain unchanged, and no later record is yielded after that failure.

Two files identical through record k must produce identical output through k, regardless of whether their tails differ, are missing, or are malformed. Do not require an invalid future suffix to be harmless when the caller explicitly consumes it. A caller requesting `list(iterator)` may receive an exception instead of a complete list; streaming consumers retain the records they previously received.

EOF after a complete valid row ends iteration normally. EOF inside malformed CSV or an incomplete record raises; it must not synthesize a trade. A total-row-count or whole-file-coverage audit can be implemented separately, without contaminating the iterator's valid-prefix emission guarantee.

## Information boundary and prohibited conversions

Every output is explicitly **archive-order only**. The iterator produces no receiver time, correction notice, original-publication guarantee, clean latent price or error/shock label. Sorting by event time, checking a hash, assigning ordinals or satisfying this contract cannot upgrade that status.

The parser must not automatically convert this stream into an approved as-of replay feed. In particular, an archive with no correction column must not become a stream of fabricated no-correction labels. Correction outcomes are structurally unavailable for this source unless an independently audited correction feed is supplied; they are not observed zero merely because the CSV has no notices.

Any later recorded-return exercise must define a file-order horizon, target availability and tail censoring explicitly, retaining the historical-file limitation. Operational online claims require the separate source-availability evidence in the [causal replay contract](replay-contract.md).

## Minimal deterministic tests

Use literal synthetic CSV strings, not new network downloads or model runs:

1. Correct seven-field parsing, exact Decimal preservation, accepted flag literals and immutable outputs.
2. Source ID zero is accepted; nonzero/gapped source IDs still yield contiguous ordinals starting at zero.
3. Explicit symbol/date/unit retention and deterministic namespace; empty/invalid symbol, invalid date/unit and timestamps outside the declared UTC day fail.
4. Millisecond/microsecond unit mismatches fail; there is no digit-count unit guessing.
5. Bad width, blank record, header, NaN/infinite/zero/negative price, nonpositive base quantity, negative quote quantity, exponent/whitespace spellings and invalid booleans fail clearly.
6. Equal times preserve row order; backward times, duplicate IDs and backward IDs raise without repair.
7. Requesting only a valid prefix does not inspect a malformed future tail. Consuming the tail raises without mutating or retracting previously emitted records.
8. No caller-stream close, sorting, deduplication, interpolation, gap filling, correction-label creation or as-of certification occurs.

These tests establish an offline parser's declared behaviour. They establish neither original online causality nor scientific validity of a financial forecasting result.
