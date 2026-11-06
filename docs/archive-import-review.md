# Independent review: offline archive import and row-target attachment

Reviewed the [import contract](archive-import-contract.md), [target contract](archive-target-contract.md), `ripplenet/archive_import.py` and its synthetic fixture tests. Independently ran the current targeted suite: all 13 tests passed. This reviewer performed no vendor-data download, model fitting or broader provider search, and edited only this review document.

## Assessment

No blocking defect remains within the declared bounded, retrieved-file-order scope. The implementation does not turn the archive into verified historical as-of data or revive the error-versus-shock claim.

The specification fixes product, UTC day and timestamp unit before row processing. Date boundaries use integer epoch arithmetic, including the documented 2025 unit transition. Integer source trade IDs remain distinct from contiguous row ordinals; gaps are recorded without inventing rows or treating them as error labels. Tied timestamps retain supplied order. Numeric fields are parsed as finite Decimals, with no assumed universal price-times-quantity identity.

The lazy CSV iterator validates before yielding and rejects malformed, blank, duplicate or backward records rather than sorting, skipping or repairing them. A malformed later record leaves previously emitted immutable trades and replay origins usable. Whole-file integrity and ZIP decompression are a separate bounded preflight; those failures need not produce CSV prefix emissions.

Feature identities use the predetermined source/product/date namespace and trade ID. Whole-file hashes, last timestamps and total row counts do not enter features or origin IDs. Changing a later valid row therefore leaves earlier origin identities and snapshots unchanged.

Every accepted trade origin is retained. Targets use exactly H subsequent retrieved trade rows, not H source-ID increments, market messages or seconds. `TradeExample` preserves the fixed horizon alongside its immutable origin and separate outcome. Repeated prices legitimately give zero recorded returns. Normal EOF seals the supplied interval and censors unresolved suffix targets; validation failure reports a failed partial read and leaves unresolved targets pending, without falsely asserting normal completion.

The archive supplies no correction ledger. The public wrapper marks correction supervision unsupported and raises `NotImplementedError` if requested. It does not obtain fabricated zero labels from its internal price-only replay. Return-only outcome timing must not be confused with the generic two-outcome training helper, which requires a genuine correction outcome.

## CLI error paths reviewed

The CLI reads only caller-provided local files, requires an expected SHA256, enforces fixed 2 MiB input and 20 MiB expanded limits, and does not extract ZIP members or access the network. It accepts a single CSV member using supported stored/deflated compression and rejects encrypted archives. Hashes remain provenance, not evidence of original publication or receiver availability.

An initial synthetic unsupported-compression fixture exposed an uncaught ZIP `NotImplementedError`. The implementation now rejects unsupported compression explicitly and has a regression test. Current hardening also handles damaged DEFLATE/EOF failures. Independently checked a tiny deliberately corrupted DEFLATE fixture: it returns structured `validation_error` JSON and exit status 2 rather than an uncaught traceback. The targeted suite covers hash mismatch, expansion bounds and malformed-tail coverage as well.

## Remaining limits

- A validated archive prefix is a structural prefix of this retrieved artifact, not proof that its values or ordering existed at a historical forecast time. Trade IDs, monotone timestamps and hashes cannot supply absent revision/receipt evidence.
- Failure metadata and pending/censored coverage must remain visible in downstream reports. Silently selecting only completed targets or relabelling a partial failure as EOF would defeat the implemented boundary.
- This single-file in-memory research wrapper does not reconstruct a book, merge venues or archive versions, establish complete market coverage, or certify event semantics. Cross-file provenance must keep alternative versions distinguishable without leaking full-file metadata into features.
- Exact positivity of prices, valid flags and source-order checks are format conditions, not independently verified economic truth. The adapter creates no recording-error, genuine-shock or latent-price ground truth.
- Any later training builder must align origin snapshots, source identities and matured outcomes explicitly. Passing parser and target tests does not establish predictive validity, market generalisation or the absence of leakage in a future model.

The stage supports its stated engineering calculation only. No prediction-quality, statistical-significance, operational-latency or financial-usefulness conclusion follows from it.
