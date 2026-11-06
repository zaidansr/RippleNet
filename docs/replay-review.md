# Independent review: recorded-data readiness and synthetic replay boundary

Reviewed `ripplenet/replay.py`, its fixture tests, the [replay contract](replay-contract.md), and the [Binance readiness audit](binance-readiness-audit.md). Ran only the targeted replay test suite: all 11 tests passed. No source code, data, other documents or provider searches were changed for this review.

## Functional and information-set assessment

No blocking defect was found within the declared synthetic ordinal contract. Validation occurs before ordinary rejected inputs can advance or corrupt the accepted prefix. Message IDs are globally unique across both message types; a notice's reference deliberately points to an earlier price record and is not treated as a new ID. No sorting, silent deduplication or retrospective price replacement occurs.

Snapshots contain immutable values and depend only on messages consumed so far. Price-to-price return persists across a notice, whereas an exact-message-horizon recorded-return target can be zero when its endpoint merely carries the latest price forward. These are different quantities, explicitly distinguished by the contract. Neither represents executable profit or latent efficient-price accuracy.

Completed return targets and shorter-window correction labels remain unchanged after later notices. Both positive and negative correction labels wait for the full declared maturity boundary. Sealing an interval with an incomplete window yields censoring, including an early known positive under the explicitly conservative common-maturity policy. Censoring is not converted into a negative label or zero return.

The training helper checks that both supplied outcomes are observed and mature at the fit cursor. It does not certify that a supplied feature snapshot, target and label belong to the same intended example, and the contract correctly assigns that verification to the caller. No fitted model or historical backtest is implemented.

## Scientific and data-use boundaries

The readiness audit distinguishes a retrieved file's ordinal/ID order and checksum integrity from original publication order, revision history and receiver availability. Its bounded noncommercial schema inspection does not certify an online as-of sequence. This is consistent with the contract: assigning consecutive integers to an archive cannot create missing historical availability evidence.

The inspected Binance schema supplies no correction lineage. `CorrectionNotice` is therefore a synthetic interface for testing delayed outcomes, not a claim that maker/best-match flags can be converted into verified error labels. No genuine-shock ground truth or real-data mechanism validation follows.

The dataset-derived readiness findings carry their own attribution/share-alike notice and do not purport to relicense independent project code. This review introduces no broader data-use permission claim. The bounded early trading day is a plumbing sample, not an empirically justified training or generalisation corpus.

## Constraints on a subsequent adapter

1. Keep this stage's narrow label: synthetic prefix-boundary checks or retrieved-record-order analysis. A real market-as-of claim needs separate availability evidence; current archive ordering is insufficient.
2. Freeze explicit source schema, timestamp units, product identity and ID namespace. Distinguish contiguous replay ordinals from source trade identifiers. Do not infer missing-message or corruption labels from ID gaps or timestamp ties.
3. Enforce example alignment in any future training builder: retain the immutable origin snapshot and the exact source IDs underlying each outcome. `training_eligible` alone is not an end-to-end leakage guarantee.
4. Retain every accepted origin and explicit incomplete-outcome status. Do not retrospectively filter origins because a later notice, missing target or interval boundary makes them inconvenient. Report coverage/censoring separately.
5. Before adding an adapter, add a fixture for its actual boundary risks: source-order preservation, timestamp-unit changes, cross-type/source ID namespaces, malformed future tails leaving prior emissions usable, and feature/outcome alignment. Do not use vendor rows as fixtures without an applicable publication basis.

This review supports the module's stated software behaviour only. It supplies no predictive performance result, statistical test, market-latency validation or reason to resume architecture expansion.
