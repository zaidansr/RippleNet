# Contract for a matched trade/quote forecasting comparison

This is a bounded design outline while sources are audited. It does not certify that suitable trade and quote data, original sequencing, receiver clocks or independent price references are available. No data or model run is authorised by this document alone. Freeze the source-specific parameters listed below before opening study outcomes.

The question is whether recorded-return predictability persists for a contemporaneously observable midpoint reference on matched clock horizons. Midpoint is an observable reference, not latent truth. A difference between trade and midpoint scores cannot, by itself, identify recording error or bid/ask bounce.

## 1. The most serious alignment error

Never match a trade to the nearest quote in absolute time. A nearest match can select a quote published after the forecast cutoff, including a book update caused by that trade. That can manufacture apparent denoising or predictability.

Use a **backward as-of** prefix under a declared clock and tie rule. Quote and trade updates have unequal counts: ten trades and ten quote updates are different horizons. Use the same clock origins and future clock endpoints for both reference series.

## 2. Admit one declared clock interpretation

The source audit must establish which interpretation is supported:

- **Receiver-time study:** messages have verified receiver availability times on a comparable clock. Features use only messages actually received before the cutoff. Event timestamps do not override a later receipt time.
- **Idealised source-time study:** original as-of messages and ordering are supported, but client receipt is not. Declare source clock alignment and any assumed publication delay. Conclusions concern that idealised source prefix, not client latency or executable availability.
- **Retrieved-clock study:** only the retrieved records and their timestamp convention are supported. The comparison may follow that explicitly limited convention, but cannot claim original source-as-of or receiver availability merely because code sorts timestamps.

For a source message `j`, let \(a_j\) denote its eligible time under the selected interpretation. It is an actual availability time only in the first case. A documented or assumed source delay must be stated per stream; it cannot be tuned to improve scores. Missing cross-stream clock evidence is a source limitation, not a parameter to guess silently.

Use the conservative default prefix

\[
\mathcal F_u=\sigma\{\text{eligible messages }j:a_j<u\}.
\]

The strict-before rule excludes timestamp ties at the cutoff. Preserve source sequence within ties where known. Do not infer quote-before-trade ordering from price changes or an arbitrary merge order. A different inclusive rule requires verified joint ordering or a clearly defined complete timestamp batch and must be frozen before evaluation. Nanosecond-looking timestamps alone do not establish publication order or synchronised clocks.

Reconstructed snapshots are admissible only under their documented prefix convention. A snapshot created from later corrections must not be treated as the book originally available at the earlier timestamp. A checksum proves retrieved bytes, not historical availability.

## 3. Recorded references and fixed validity rules

Let \(P(u)\) be the last eligible recorded trade price in \(\mathcal F_u\). Let the current eligible best bid and ask be \(b(u),a(u)\), and define

\[
M(u)=\frac{b(u)+a(u)}2.
\]

This midpoint describes the supplied quote reference. It need not equal a latent efficient price, an executable transaction price or a consolidated-market reference.

Use these logical rules, with source-specific age limits fixed before outcomes:

1. Trade prices and both quote sides must be finite and strictly positive.
2. Require \(b(u)<a(u)\). Locked or crossed quotes are unavailable for this reference definition, not automatically labelled erroneous. Report them separately.
3. Quote and trade age limits apply separately in the declared clock units. A reference passes when its observation age is nonnegative and at most its declared maximum, including equality. For individually observed sides, audit both sides; a fresh bid does not automatically supply a fresh ask observation. Age concerns the last supported observation/reconfirmation, not merely the last price change: a documented full quote snapshot can reconfirm an unchanged side.
4. The current as-of quote must pass the rules. Do not search backwards past an invalid current quote for a more favourable historical spread, or forward for the next valid quote.
5. Missing/stale references are unavailable, never zero or silently interpolated. Carry-forward is permitted only within the fixed age limit.
6. If the source provides sizes, decide the eligible-size rule from its schema before results. Do not infer a valid book from price fields whose documented semantics do not support it.

The numerical maximum ages remain blocking parameters until the source audit. Absence of actual receipt clocks must not be hidden by calling event-time age receiver staleness.

## 4. Common origins, horizons and delayed labels

Choose a deterministic clock grid \(t_j=t_0+j\Delta\) within a fixed supported daily/session interval. Origins must not be selected using future quote availability, a profitable future move or eventual correction status. Let \(h>0\) be the fixed forecast duration and \(\delta\ge0\) a separately declared target-start delay.

For reference \(S\in\{P,M\}\), define

\[
Y^S_{j,\delta,h}
=\log S(t_j+\delta+h)-\log S(t_j+\delta).
\]

All features stop at \(\mathcal F_{t_j}\). If \(\delta>0\), the starting reference is future label information and cannot be an input or forecast anchor. A clock delay does not establish execution or receipt latency.

Freeze one grid spacing, one horizon and at most one delayed-start value for this small comparison. A zero-delay reference can be a declared secondary control; do not search many durations until a target changes significance. Specify which tasks are primary before opening outcomes.

Keep the same origins, \(h\) and \(\delta\) for trade and midpoint comparisons. Use common eligibility based on adequate past input history and valid declared reference endpoints for both tasks. Preserve every scheduled origin's status and reason:

- `pending`: required future coverage has not yet arrived in an open replay.
- `observed`: required references and feature history satisfy the frozen rules.
- `censored`: an endpoint extends beyond supported coverage of either stream.
- `unavailable`: a covered endpoint or required input lacks a valid fresh reference.

Supported coverage is not automatically the last trade timestamp. Use documented file/session coverage; otherwise restrict conclusions to the supported interval. Do not forward-fill beyond known coverage and call the endpoint observed.

Final common eligibility can depend on future missingness. That defines a selected evaluation population, not an origin-time trading rule. Report retention rates, excluded intervals and reasons per day so a claim about all market times is not inferred from only active, fully quoted periods.

## 5. Hold available inputs constant

A trade-target model seeing the current trade reference and a midpoint-target model lacking the current midpoint/gap would not have equivalent starting-state information. To prevent this, a modest shared full-information candidate vector can contain:

- Five adjacent clock-grid log returns of \(P\).
- Five adjacent clock-grid log returns of \(M\).
- Current relative spread \((a-b)/M\).
- Current log trade–midpoint gap \(\log P-\log M\).

Every value must come from the backward as-of prefix and pass the same freshness rules. This is a proposed bounded 12-feature set to freeze after source verification, not permission to add features after results. If a smaller set is chosen, explicitly account for which current reference information is withheld.

Give every flexible baseline and candidate the identical available inputs when making an architecture comparison. Zero or training-mean baselines may ignore those inputs by definition. A full-input linear/ridge baseline is essential before attributing value to a specialised model. Comparing a quote-informed candidate with a trade-only predictor measures an information change as well as any model change.

Fit the two reference targets separately with frozen model/regularisation choices. Compute scaling, constants and coefficients from training only; validate before the protected test. Identical common features, masks and weights should produce identical feature scalers. Different target means and coefficients are allowed. No-event or correction labels are invented from quote disagreement.

## 6. Scores that do not confuse different targets

Use held-out MSE for each reference with a credible target-specific baseline, and MAE as a declared secondary score. Report absolute risks, reference-risk denominators and ratios of mean risks. A lower raw midpoint MSE than trade MSE can arise from different target variance or piecewise-constant quote updates; it is not itself superior prediction.

Report the fraction of unchanged trade/midpoint references, update counts, ages, spread and missingness diagnostics. Several zero midpoint returns in a stale or infrequently updated stream must not be presented as evidence that a model learned market dynamics.

Any cross-reference contrast must state whether it compares absolute zero-relative improvement or normalised gains with different denominators. Pair the same day/time blocks across all models and references; unequal update counts are not additional independent replications. Overlapping clock windows and common latent market activity create dependence.

The intended use must determine a meaningful effect margin before evaluation. There is no automatically valid 5% threshold from the old synthetic task. Statistical nonzero improvement does not establish economic utility; no trading-cost or execution model has been specified.

Persistence on midpoint targets would weaken an explanation confined to a shared trade-price term, but would not prove efficient-price predictability. Attenuation could also reflect changed update frequency, noise, target variance, information timing or model suitability. Without independently verified labels or a stronger structural design, neither outcome proves bid/ask bounce or genuine shocks.

## 7. Smallest execution gate

Before any experiment, publish a source-specific plan fixing:

- Instrument, venue/reference scope, dates and chronological development/test split.
- Supported clock interpretation, cross-stream alignment and strict tie/latency rules.
- Grid spacing, horizon, target delay and supported coverage boundaries.
- Quote/trade age limits, validity rules and treatment of missing/locked/crossed observations.
- Shared features, baselines, model-selection procedure, origin weighting and primary contrasts.
- Dependence-aware uncertainty procedure, numerical/practical margin and all planned coverage diagnostics.

If the source cannot support matched trade/quote prefixes, stop the original-as-of claim. A separately named retrieved-clock comparison may remain possible if its limited alignment is defensible, but it must not silently pass the stronger evidence gate. If a source omits required quote data, do not reconstruct future quotes from trades or treat a bar high/low as a contemporaneous bid/ask.

Use one bounded comparison after these gates, with all targets and exclusions reported. Do not turn missing evidence into another synthetic calibration or a larger architecture. No data, network access, models or paid resources were used in writing this contract; no particular source facts are assumed.
