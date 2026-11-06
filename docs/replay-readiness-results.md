# Replay boundary implementation and data-readiness outcome

This stage implements a causal processing boundary using invented fixtures. It also completes a bounded inspection of a preselected public trade archive. Neither activity is a real-market forecasting experiment or evidence of the original error-versus-shock mechanism.

## Assumptions fixed before implementation

The component receives an append-only stream in an already declared order. It does not infer original availability from timestamps or certify that a historical archive has retained its original values. The prototype has one positive recorded-price stream and qualifying correction notices. There is no receiver clock, multi-feed alignment, missing-book repair or source-specific adapter.

Every supplied message counts toward ordinal horizons and label windows. A notice can become a prospective feature, but cannot rewrite earlier snapshots or recorded prices. Its binary label means a qualifying notice arrived within a specified window; an absent notice does not identify a genuine shock. These choices and exact boundaries are derived in the [replay contract](replay-contract.md).

## Implemented behaviour

[The standard-library component](../ripplenet/replay.py) provides frozen price records, notices, snapshots and separate outcome objects. Prices use `Decimal`; log differences use a fixed 34-digit decimal context and are returned as floats. The implementation is deterministic and uses no random generator, so a seed is unnecessary for its fixtures.

The replay rejects nonpositive/nonfinite prices, duplicate message identifiers, missing or reordered ordinals, and notices referencing unknown price records. A rejected message does not change the accepted prefix. The module performs no sorting, deduplication, fitting or network access.

For origin `k` and horizon `H`, the target is the log change in the last as-recorded price between snapshots `k` and `k+H`. A notice leaves that price unchanged. This is a precisely defined recorded reference, not a clean latent price or executable profit.

Correction positives and negatives both wait until the end of their declared window. Open unfinished windows are pending; sealing before completion makes them censored, including windows with an early positive notice. The training-eligibility helper requires both target and label availability to be at or before the fit cutoff. It is a necessary timing check, not proof of matched example IDs, safe preprocessing or correct feature provenance. Historical fitting must use preserved origin features and the corresponding historical prefix.

## Verification performed

The [new tests](../tests/test_replay.py) cover future-tail changes, immutable snapshots, exact horizon and maturity endpoints, late notices, conservative censoring, fit cutoffs, invalid inputs, rejection without state corruption and numerical-context reproducibility.

The complete repository suite passed: **69 tests, including 11 new replay tests**, under Python 3.13.3. Commands:

```sh
python -m unittest discover -s tests -p test_replay.py -v
python -m unittest discover -s tests -v
```

An [independent subagent review](replay-review.md) reran the 11 targeted tests and found no blocking defect within the declared synthetic ordinal contract. It records the remaining source-adapter, example-alignment and coverage obligations.

These are correctness tests, not independent scientific replications, significance tests or an assessment of financial usefulness. Existing experimental code and frozen result files are unchanged.

## Actual archive inspection: a narrower success

The engineering subagent checked current official source terms, then inspected the preselected Binance spot daily individual-trades archive within fixed compressed and uncompressed limits. The [source audit](binance-readiness-audit.md) records selection, hashes, schema/coverage findings, attribution and the applicable document-specific license. Raw data and source snapshots remain outside this repository. No model was fitted, alternative date substituted, account created, provider contacted or paid resource used.

The source permits a bounded noncommercial recorded-file/schema investigation under its stated conditions. However, original receiver availability and trade-level revision history were not established. A publisher checksum verifies the retrieved file against its sidecar; it does not recover the original online information set. The source audit therefore retains a no-go for original as-of validation and error-versus-shock classification. Its primary links support those source-specific findings.

## Research decision

The replay boundary is usable for deterministic engineering checks. It does not remove the evidence gate in the [real-data feasibility decision](real-data-feasibility-decision.md). The inspected archive is insufficient to proceed with the proposed real-market mechanism comparison.

Do not launch a predictor search, inject synthetic corruption into the archive and call it empirical validation, or infer missing cause labels from extreme prices. A separately declared retrieved-file prediction task could be studied, but would answer a different question. An original as-of forecasting study still needs justified original sequencing/versions and admissible candidate inputs; the mechanism claim additionally needs defensible cause evidence. No statistical reliability, generalisation or novelty conclusion follows from this implementation stage.
