# Minimal causal replay contract

This contract covers a small pure-Python prototype using deterministic synthetic fixtures. It does not establish that an external archive preserves as-of data. There is no network client, forecasting model, receiver-time API, exchange adapter or order-book reconstruction in this stage.

## 1. Input and public API

Use two frozen message types, with prices represented by Python `Decimal`:

```python
PriceRecord(ordinal: int, record_id: str, price: Decimal)
CorrectionNotice(ordinal: int, notice_id: str, record_id: str)

Replay.consume(message) -> Snapshot
Replay.snapshot -> Snapshot
Replay.seal() -> None
Replay.recorded_return(origin_ordinal: int, horizon: int) -> Outcome
Replay.correction_label(record_id: str, window: int) -> Outcome
training_eligible(return_outcome, label_outcome, fit_ordinal: int) -> bool
```

These signatures specify behaviour, not a general-purpose market-data framework. `CorrectionNotice` means a notice already declared to qualify for the prototype's binary outcome. Interpreting a particular source's correction semantics belongs in a separately audited adapter.

Ordinals are **contiguous, zero-based integers**: 0, 1, 2, and so on. Every accepted price record or correction notice consumes one ordinal. Horizons and maturity windows count these messages, not price updates, source timestamps, seconds or trades. Reject duplicate, missing, tied or out-of-order ordinals; do not sort them into a preferred order. An adapter with a verified original tie-breaking order may assign consecutive ordinals before replay. Without that evidence, sorting equal event timestamps does not prove arrival order.

Require nonempty identifiers and **global uniqueness of message IDs**: neither a new price's `record_id` nor a notice's `notice_id` may reuse any earlier message identifier, including one of the other message type. A notice's reference field `record_id` deliberately repeats an earlier price ID; it is not that notice's new identifier. Do not silently deduplicate records or reinterpret an identifier. A notice must refer to an already accepted price record. Repeated qualifying notices for the same price record may exist only with distinct notice IDs; the binary label remains one. Reject unknown references rather than invent the earlier record.

Require actual finite, strictly positive `Decimal` prices. Missing, nonnumeric, infinite, `NaN` and nonpositive prices must not become zero, a guessed replacement price or a valid return. Invalid input fails before advancing the prefix or changing state. The adapter must declare how source-level missing observations are handled; silently dropping a message would change every later event-count horizon.

`seal()` marks the observed stream complete for this replay object and prohibits further consumption. Sealing a truncated sample does not establish that no later correction existed outside it.

## 2. Prefix and snapshot invariants

Let \(M_0,\ldots,M_k\) be accepted messages through ordinal `k`. The allowed information is the inclusive prefix

\[
\mathcal G_k=\sigma(M_0,\ldots,M_k).
\]

Before any messages the replay has an empty snapshot. After `consume(M_k)`, it returns a frozen snapshot containing the current ordinal, last **as-recorded** price and its record ID, the most recent price-to-price log return when defined, and prefix counts. Missing initial price/return fields are `None`, not numerical zero. A consumer cannot mutate a snapshot or its contained metadata.

For a price record, update the last price and ID. If the preceding price was \(p\) and the new price is \(q\), the new price-to-price return is \(\log(q)-\log(p)\). The implementation uses a local Decimal context with precision 34, independent of ambient caller settings, then returns the result as a finite Python float. For a notice, increase notice-related counts but preserve the last as-recorded price, ID and price-to-price return. A notice does not supply a replacement price. Its arrival can become a prospective feature for later origins; it cannot backfill old snapshots.

In particular, a notice referring to an earlier price record must not change:

- Any previously returned snapshot or feature.
- The historical as-recorded price at that earlier ordinal.
- An already fixed recorded-return target.
- A fixed-window label whose window ended before the notice.

The last as-recorded price is a defined recorded reference, not a claim that it remains economically correct after a notice. Studying a revised-price reference would require a separate target contract. Order-book validity, bid/ask crossing, multi-feed synchronisation and replacement-price semantics are outside this prototype.

## 3. Distinct recorded-return and correction outcomes

Use an immutable `Outcome` with `status`, `value` and `available_at`. The statuses are:

| Status | Meaning |
| --- | --- |
| `pending` | Required boundary has not been observed and the replay remains open. |
| `observed` | Full required window is observed; value and availability ordinal are fixed. |
| `censored` | Replay was sealed before the required boundary; no completed-window value may be assigned. |
| `unavailable` | A required reference is structurally unavailable; no numerical target is supplied. |

Only `observed` outcomes have a usable value and availability ordinal. Do not use a numeric value for pending, censored or unavailable outcomes. Invalid arguments, including nonpositive horizons/windows and invalid ordinals, should fail clearly rather than masquerade as an observed outcome. Structural unavailability and a not-yet-observed future boundary must remain distinct.

Observed returns are floats; correction labels are integer 0 or 1. The missing-reference `unavailable` branch is reserved for an absent recorded price. Under the current strict message contract, the first valid message must be a positive price record, since a notice cannot refer to an unseen record; that branch is not normally reached after valid consumption. It does not imply that an invalid-book or missing-source adapter has been implemented.

### Recorded return

Let \(P_k\) be the latest as-recorded price in snapshot `k`. For origin `k` and positive integer horizon `H`, the endpoint is **exactly** \(k+H\). Define

\[
Y_{k,H}=\log P_{k+H}-\log P_k.
\]

Origins and endpoints may be notice messages; notices still count toward `H`, while leaving the recorded reference unchanged. A window containing no new price can therefore have return zero by definition. That is a stale-reference possibility, not evidence of forecasting skill. No interpolation or future backfill is allowed.

At current ordinal \(c\ge k+H\), return `observed`, with `available_at=k+H`, provided both references exist. The stored as-recorded snapshots determine both values even if later notices arrive. If the replay is open and the endpoint is not yet reached, return `pending`; if sealed first, return `censored`. If a required price reference does not exist, return `unavailable`, not a guessed return. Reject origins that do not denote an accepted message rather than silently clamping them to a valid prefix.

### Fixed-window correction label

Suppose price record `r` arrived at ordinal `i`. For positive window `L`, define

\[
C_{r,L}=\mathbf1\{\text{a qualifying notice for }r\text{ occurs at some }j
\text{ with }i<j\le i+L\}.
\]

The endpoint is inclusive: a notice at \(i+L\) counts. A notice after it does not. A zero label means no qualifying notice **within that observed window**, not that the original record was a genuine market shock or permanently correct.

**Both positives and negatives mature only at \(i+L\).** Before then, return `pending`, even if a qualifying notice has already arrived. If sealed before the boundary, return `censored`, even after an early positive notice. At maturity return the binary label with `available_at=i+L`. Uniform maturity avoids admitting early-known positives into training while comparable negatives are still unresolved. The already observed notice remains usable as a prospective feature for other origins; the label-release policy does not erase that prefix information.

A different window defines a different label. Do not enlarge `L` after seeing a later notice and claim the original fixed-window label was wrong. Unknown record IDs are errors, not negative labels.

## 4. Training availability and historical fitting

For an example with origin `k`, return horizon `H`, and correction record `r` at ordinal `i` with window `L`, supervised fitting requires both outcomes to be observed. Its earliest joint availability is

\[
a=\max(k+H,\ i+L).
\]

`training_eligible(return_outcome, label_outcome, fit_ordinal=f)` is true only when both statuses are `observed` and both `available_at` values are at most `f`. Equality is allowed: this means fitting **after** consuming message `f`. If the intended fit occurs before that message, the cutoff is `f-1`.

This helper checks outcome availability, not the entire absence of leakage. It does not verify that the target, label and feature snapshot belong to the intended record/example. The caller must verify that alignment. The feature snapshot must also be the immutable origin snapshot, and no fitting, normalisation or threshold choice may use a later prefix. For a historical fit, replay only the historical prefix and request its outcomes there. A full final stream plus a numerical cutoff is not a substitute for verifying how features and outcomes were constructed.

Chronological splits must respect maturity. Splitting solely by the original price-record ordinal can leak later labels into an earlier fit. Censored and unavailable examples do not become negatives or zero returns; retain their counts and reasons in any later analysis.

## 5. Numerical fixture

Use exact decimal literals and this deterministic sequence:

| Ordinal | Message |
| --- | --- |
| 0 | Price `a`, 100 |
| 1 | Price `b`, 102 |
| 2 | Notice `n1`, referring to `a` |
| 3 | Price `c`, 101 |
| 4 | Notice `n2`, referring to `b` |
| 5 | Price `d`, 103 |

After ordinal 1, the snapshot has price 102, last price ID `b`, and price-to-price return \(\log(102/100)\). Consuming notice `n1` does not change those values or the saved ordinal-1 snapshot. Its prospective notice count increases.

The return from origin 1 with `H=2` matures at ordinal 3 and is

\[
\log(101/102)\approx-0.0098522964.
\]

The return from origin 0 with `H=2` ends on a notice. Its recorded reference is still 102, so it is \(\log(102/100)\), not a retrospectively corrected return based on price `a`.

For record `a`, `L=3` ends at ordinal 3. The label is still pending at ordinal 2 despite notice `n1`; at ordinal 3 it is observed one, available at 3. For record `b`, `L=3` ends at ordinal 4, and notice `n2` at that exact endpoint counts. Its label is one, available at 4.

For record `a` with the separately defined `L=1`, the label is observed zero at ordinal 1. The later notice at ordinal 2 cannot alter it. For record `c` with `L=3`, the endpoint is 6; sealing after ordinal 5 produces a censored label, never zero. A second fixture consisting only of price `a` at 0 and its notice at 1, sealed at 1, must also produce a censored `L=3` label despite the early positive notice.

With return origin 1/`H=2` and correction record `b`/`L=3`, fitting at ordinal 3 is ineligible because the label is pending. Fitting after consuming ordinal 4 is eligible, assuming origin features were preserved correctly.

## 6. Minimal tests

1. **Snapshot immutability:** saved snapshots and any nested fields cannot change after consumption of later prices/notices.
2. **Prefix/future mutation:** two streams identical through `k` produce identical snapshots and features through `k`; changing future prices or notices does not change any target or label whose full boundary is at most `k`.
3. **No backfill:** the fixture's late notices leave old prices, returns and shorter-window labels unchanged.
4. **Maturity boundaries:** exact-endpoint notices count; one-message-late notices do not. Early positives remain pending until the same boundary as negatives.
5. **Censoring:** seal before a boundary yields no observed target or label, including for an early positive. Seal exactly at a boundary allows the completed outcome.
6. **Availability:** equal-to-fit boundaries are eligible after consumption; later boundaries and all nonobserved statuses are ineligible.
7. **Input rejection:** unknown references, duplicate IDs, noncontiguous ordinals, invalid prices and append-after-seal fail without corrupting the accepted prefix.
8. **Empty/missing state:** initial missing price/return is explicit; no zero, interpolation, or fabricated current book is returned.
9. **Recorded-return arithmetic:** fixture values agree under a documented Decimal precision/tolerance; notice messages count toward horizons without becoming price updates.
10. **Deterministic reproduction:** the same literal fixture produces the same snapshots/outcomes. No random generator is used, so no random seed is needed for these tests.

Future message changes may legitimately change outcomes whose required window extends into that future. The prefix test must not demand invariance of an outcome that was not yet mature at the tested cutoff.

## 7. Evidence boundary

An integer named `ordinal` represents the caller's declared order. Passing this prototype's tests proves adherence to that declared prefix, not that the order reproduces original publication or receipt. Checksums prove byte integrity, not availability, revision completeness or historical ordering.

An archive sorted by event time must not automatically pass an as-of gate. Any later real-data adapter must separately document original sequencing, revision policy, correction linkage, source semantics and what was available when. Missing receiver clocks permit, at most, a justified idealised source-message-order task where the raw as-of sequence is supported; they do not support client-latency claims. If even original as-of values/order are unsupported, the prototype must not convert the archive into an operational backtest by assigning integers.

No source-specific archive or Binance schema is assumed to preserve receiver availability or revision history. Inspecting such an archive cannot silently relax this contract. This stage requires no downloads, new data/model runs, paid resources or architecture changes.
