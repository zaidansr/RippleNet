# Observable-target and information-set audit

The existing experiments do not support architecture expansion. Across the fixed observation-noise grid, exact mixture retention improved delayed conditional forecasting risk by at most about .134% at the reported point estimates; all primary adjusted upper bounds were below the 5% practical reference. A post-hoc category-oracle ceiling against projection remained below about 2.87% on the reported conditional-history averages. These findings concern a known-time, known-parameter, isolated Gaussian-event model. They are not a negative result for all markets or observation processes.

The next question is whether an observable, causally available information problem exists. Real quote or trade records and later corrections do not, by themselves, reveal latent true returns or identify every genuine market shock.

## 1. Define availability by receipt, not by an earlier event timestamp

For raw message `j`, retain at least its instrument, source, event timestamp \(e_j\), receipt/availability timestamp \(a_j\), source sequence or record identifier, payload, action and revision links. A correction is a new message with its own availability time. Preserve the original message and append the correction; do not rewrite the historical information set.

Let `t` be the prediction issue time on a declared receiver clock and let \(\ell\ge0\) be a fixed processing allowance. The permitted information set is

\[
\mathcal F_t=\sigma\{\text{messages }j:a_j\le t-\ell;\ \text{metadata already known by }t-\ell\}.
\]

A forecast \(g_t\) must be measurable with respect to \(\mathcal F_t\): changing messages received later must not change it. The origin-selection rule must also use available information. Backdating a later message to its event time does not make it available earlier.

For example, a record stamped 10:00:00 but received at 10:00:02 cannot enter a prediction issued at 10:00:01. A correction received at 10:05 can label or revise that record later; it cannot repair the input history of the 10:00:01 forecast. These are illustrative times, not claims about a particular feed.

Document how clocks are aligned and what each timestamp means. A historical file's final corrected values cannot establish original availability without supporting timestamp/version evidence. Missing client receipt times preclude a demonstrated client-latency backtest, but do not automatically prevent a causal **exchange-message-order benchmark**.

For that separate benchmark, let \(M_1,\ldots,M_k\) be the original sequenced exchange messages through ordinal `k`, preserving as-of payloads and later revision messages at their own positions. Define

\[
\mathcal G_k=\sigma(M_1,\ldots,M_k).
\]

A forecast using only \(\mathcal G_k\) is causal in that idealised sequence. It does not establish when a client actually received or processed those messages. Any multi-feed synchronisation, client latency or seconds-to-execution claim needs separate evidence. A reconstruction can supply valid ordinal features if each snapshot is demonstrably a function of its message prefix; a full book snapshot is not intrinsically leakage. Conversely, merely sorting final corrected records by their old timestamps does not create an as-of event stream.

## 2. Use an observable target

A defensible initial forecasting task is a **reference-source recorded return**, with the source and construction fixed before evaluation. Let \(P^{\mathrm{ref}}(u)\) be a strictly positive reference price computed by a deterministic rule from messages received by receiver time `u`. If quotes are available, the rule might use the latest eligible bid/ask midpoint; it must state freshness, invalid-record and missing-data rules. A trade-based reference is also possible, but defines a different observable.

For a fixed horizon \(h>0\), define

\[
Y_{t,h}=\log P^{\mathrm{ref}}(t+h)-\log P^{\mathrm{ref}}(t).
\]

This target is observed after the horizon, under the declared reference rule. It is not the latent return \(x_{t+h}-x_t\) of the synthetic model, an executable trading return, or a guarantee of reference accuracy. The target's time convention must match the forecast issue time, including any processing allowance.

With a verified as-of message sequence but no client receipt clock, an alternative is an **event-count recorded-midpoint return**. Let \(P_k\) be the eligible book midpoint after ordinal `k`, and fix an integer horizon \(H>0\):

\[
Y_{k,H}=\log P_{k+H}-\log P_k,\qquad g_k\text{ measurable with respect to }\mathcal G_k.
\]

Predeclare what messages count toward `H` and how instrument filtering, invalid books and sample boundaries are handled. `H` messages is not `H` seconds and implies no client execution latency. If only a reconstructed output table is available, call the horizon **recorded-row count** unless its correspondence to the complete raw message sequence is established. Audit snapshot causality and ordinal mapping before using either name.

When using a contemporaneous reference reading as an input, supply it consistently to every competing full-information method. Otherwise a gain may come from revealing the current reference state to one method only. If the reference is intentionally withheld from a primary-only information arm, describe that comparison as an information ablation.

An alternative target built from eventually corrected prices is permissible, but must be named **revised-record return**, with a fixed revision cut-off. It can change the starting price using information unavailable at `t`, so it answers a different question. Final corrected data must not silently substitute for as-received predictors.

Freshness matters. Stale repeated prices can generate many zero recorded returns without revealing forecast skill. Specify eligibility and target availability rules in advance, report missing/stale exclusions, and disclose if the resulting target population omits periods a deployed method would face. Filtering forecast origins retrospectively to retain only eventually confirmed-clean records is not an operational selection rule.

## 3. What late corrections identify

Let \(C_j(L)=1\) mean that a declared qualifying correction linked to record `j` arrives within a fixed label-maturity window `L`. Otherwise the label is “no qualifying correction observed by `L`,” not “verified genuine shock.” The definition must follow the dataset's documented correction semantics and distinguish price revisions from other administrative changes.

Late correction records can support a supervised **future-correction or data-quality** task. They do not make the labels contemporaneous. A training example may be used only after both its forecast target and correction label have become available; a chronological split by the original record time alone is insufficient. At each fit time, use only matured labels available then, with an appropriate maturity gap if needed.

An uncorrected large move is not automatically genuine. A corrected record is not a direct observation of the whole underlying market state. Observation problems and genuine moves can coexist, and some cases may remain unresolved. Keep ambiguous, mixed and unverified cases distinct instead of forcing every event into the simulator's two exhaustive categories.

The causal prediction question is whether an available feature forecasts \(Y_{t,h}\). The classification question is whether it forecasts \(C_j(L)\) or another auditable label. Success on one does not establish success on the other.

### Concrete distinction: raw ITCH trade breaks versus a reconstructed book

Nasdaq's TotalView-ITCH 5.0 specification, section 1.5.3, defines a `B` message for an execution that has been broken and identifies the earlier execution through its match number. The message does not change the current order book. These are trade/execution-history semantics, not an observation of a latent return or a generic bad-quote label. [Nasdaq ITCH specification](https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHSpecification.pdf)

LOBSTER's reconstruction documentation states that broken-trade messages are ignored in order-book reconstruction. A reconstructed message/book dataset must therefore not be assumed to preserve raw `B` events or their match-number linkage. Its book snapshots can still support an audited idealised ordinal forecast; they do not thereby provide late trade-break ground truth. Verify the actual sample schema rather than infer missing labels or receiver clocks from the fact that it contains a book. [LOBSTER reconstruction FAQ](https://php.lobsterdata.com/info/help_reconstruction.php)

Two uses of a break notice must remain separate:

- **Prospective quality tag:** once a `B` message is present in the allowed prefix, its existence may be an input for later origins. It cannot be attached retrospectively to the earlier execution as though the break had already been announced. For a receiver-time task, availability is determined by receipt; for an idealised sequence task, by the message's ordinal.
- **Ex-post label:** the later match-linked notice can label an earlier execution as eventually broken within a declared maturity window. Such a label supports a future-break prediction or quality-control task only if the raw linkage is actually retained. “No break observed by the cut-off” does not verify a genuine shock.

A lack of book impact from a `B` message is consistent with its specified role. It is not evidence that the book reconstruction has recovered the counterfactual market state or isolated the original synthetic observation-error mechanism.

## 4. Conditions for contemporaneous redundancy to help

Suppose an auxiliary observation is genuinely available by the prediction origin. An illustrative structural model is

\[
Y_t^{(1)}=H_1X_t+\epsilon_t^{(1)}+O_t^{(1)},\qquad
Y_t^{(2)}=H_2X_t+\epsilon_t^{(2)}+O_t^{(2)}.
\]

Here \(X_t\) is a shared latent state, \(H_1,H_2\) map that state into each observed channel, \(\epsilon\) represents ordinary measurement differences, and \(O\) represents a declared recording disturbance. This is a proposed model, not a verified description of any source.

For redundancy to distinguish causes, the audit must support all the following:

- The channels measure a sufficiently comparable quantity, with clock alignment and staleness controlled.
- A genuine state change affects the channels through known or estimable relationships; legitimate source differences are not automatically labelled bad records.
- Recording disturbances are not simply a common upstream failure copied into both channels.
- Independence or dependence assumptions for ordinary errors are documented and tested where possible.
- The auxiliary signal is available at the forecast origin, not reconstructed from later revisions.

Let \(D_t\) denote the permitted data prefix generating \(\mathcal F_t\). For category `Z`, a necessary condition for informative classification is that these data distributions differ:

\[
\mathcal L(D_t\mid Z=O)\ne\mathcal L(D_t\mid Z=S).
\]

If the likelihoods are identical, Bayes' rule cannot update the category prior. Distinct overlapping distributions permit uncertain inference; they do not guarantee an exact label for every event. Identifying structural causes further requires justified model restrictions or external verification: several latent explanations can induce the same observed law. A predictive score alone cannot resolve that equivalence.

Cross-asset correlation is not automatically a redundant measurement of the same state. Nor does agreement between two channels certify truth if their errors share an upstream cause.

## 5. Separate information value from architecture value

Let \(\mathcal F_t\) be primary-source history and let \(U_t\) be an auxiliary feature truly available at `t`. For the observable scalar target \(Y=Y_{t,h}\), define

\[
\mu_F=E[Y\mid\mathcal F_t],\qquad
\mu_{F,U}=E[Y\mid\mathcal F_t,U_t].
\]

Expanding the squared error and using conditional mean-zero residuals gives

\[
E[(Y-\mu_F)^2]-E[(Y-\mu_{F,U})^2]
=E[(\mu_{F,U}-\mu_F)^2]\ge0.
\]

Thus auxiliary data help squared-error forecasting only insofar as they change the conditional target mean. They may classify a historical correction well without changing that mean. This is the real-data counterpart of the synthetic gap between type scores and useful next-return headroom.

Use three distinct comparisons if data pass the availability audit:

1. A credible forecasting baseline using primary history.
2. A credible baseline using both primary history and the contemporaneous auxiliary information.
3. Only if warranted, a candidate using exactly the same full information as comparison 2.

Comparison 1 versus 2 investigates information value; comparison 2 versus 3 investigates model value. A future correction label may appear in a separately disclosed privileged diagnostic, but never in an ordinary prediction input. Such a diagnostic does not prove its extra information is attainable at the origin.

## 6. Small free-data feasibility experiment

First identify an already freely accessible sample whose documentation supports the chosen task. A correction-label task needs raw ordering, retained revision notices and original-record linkage. An idealised event-count forecasting task instead needs an audited as-of sequence or prefix-causal snapshot reconstruction, with no claim of client receipt latency. This mathematical audit does not establish that either suitable dataset has been found. Do not promise unavailable fields, invent receipt times, purchase access or launch paid compute to fill a gap.

Use one instrument and a fixed short consecutive interval—approximately five sessions or five fixed 24-hour periods if the data have no session boundary. This is a schema and causal-replay feasibility check, not a suitably powered forecasting study. Before inspecting outcomes:

- Freeze one reference-price rule and one justified horizon. Declare receiver time versus exchange-message/output-row ordinal explicitly. Use a processing allowance only where its timing interpretation is supported, and define any label-maturity window in the same declared units.
- Reconstruct immutable states under the declared receiver-time or sequence-prefix convention and log the message IDs or audited row ordinals behind every candidate feature and target. Where the raw data provide an audited correction, verify its original and revision versions.
- Inspect the earliest portion for schema and replay failures. Reserve the latest portion for a frozen availability/feature check; do not tune thresholds on it.
- Test that inserting or changing a later correction leaves an earlier feature vector and forecast unchanged. Check that channels are aligned using genuinely available readings.
- Count mature labelled cases, ambiguous cases, stale/missing references and auxiliary readings available in time. Report counts and coverage before attempting an effect-size claim.

Only if this passes should a subsequent predeclared, chronologically separated experiment compare the primary-history and full-information baselines. Fit only on then-matured labels, and use time/event blocks that respect dependence. Choose final sample size from development variability and event frequency before opening the final period. Five sessions of schema validation do not support a generalisation or significance claim.

An initial event-focused table can describe later-corrected versus other records, but must disclose retrospective stratification. It is not evidence that those categories could have been selected in real time.

## 7. Strict go/no-go criteria

**Availability gate:** proceed toward an operational receiver-time forecast only if raw values, revisions and client availability can be reconstructed at the origin. If client receipt evidence is missing but original sequenced as-of messages or audited prefix-causal snapshots survive, an explicitly idealised message-order or output-row benchmark may proceed. Do not attach operational latency claims to it. Without either form of prefix evidence, stop causal forecast claims; a final-record descriptive analysis is a different task.

**Target gate:** proceed only with a declared observable reference and horizon, reproducible missingness rules and a clear account of remaining reference error. If no auditable target exists, stop the claim of verified underlying-return accuracy.

**Mechanism gate:** proceed with an observation-error-versus-shock claim only if labels or justified redundant evidence distinguish those causes. Without them, relabel the task as predicting documented revisions, anomaly scores or observable returns. Do not convert missing verification into a shock label.

**Timeliness gate:** if the distinguishing signal arrives only after its potentially useful forecast origin, stop that origin-specific use claim. Longer-horizon or data-quality questions are separate hypotheses requiring explicit justification, not retrospective relabelling of success.

**Utility gate:** require a prespecified meaningful forecasting improvement over a credible full-information baseline, with uncertainty and a protected chronological test. Classification gains alone do not pass. A privileged oracle's useful headroom is necessary diagnostic evidence at most; it is not an attainable ordinary-model result. Retain the project's 5% reference only if it remains justified for the new observable task, and never lower it after observing a result.

**Research decision:** do not restart architecture growth unless these gates identify an independently motivated, timely information problem. If free data cannot support the availability, target or mechanism gates, stop the forecast-mechanism claim rather than continue synthetic parameter hunting. The existing negative practical results remain valid within their tested scope.

No new data or model runs, paid resources, or edits to other files were performed for this audit. The mathematical constraints and examples are original derivations, not claims about a particular market feed.
