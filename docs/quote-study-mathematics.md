# Mathematics of the fixed multi-session trade/midpoint study

This specification follows the [published final plan](quote-study-plan.md), commit `6993f9a12311d759b8e5d3370fcac8dc2ade6ed7`. It compares recorded trade and midpoint targets using identical available inputs. It does not identify latent efficient prices, client receipt latency or error/shock categories. No study prices were read or models run to prepare this document.

## 1. Sessions and clock

Use the fixed Kraken spot XBT/USD trade/quote pairs for the first day of each month from June 2025 through May 2026. Fit June–November 2025, validate December 2025–February 2026 and protect March–May 2026. These are six, three and three sessions, respectively. The previously inspected June 2026 session is excluded. A missing or invalid required session, or one without common scorable origins, stops the fixed design.

The clock is the supplied collector `local_timestamp` in integer UTC microseconds. It is not the research user's receipt clock. Preserve each stream's supplied order and ties; do not sort or infer exchange-wide ordering. Source clock, coverage and revision limitations remain those stated in the plan and audit.

For session midnight \(T_0\), define exactly 86,400 snapshots

\[
t_j=T_0+10^6j\text{ microseconds},\qquad j=0,\ldots,86399.
\]

At snapshot `j`, only records with collector time **strictly less than** \(t_j\) may contribute. A record exactly at the cutoff is excluded. The supplied order determines the last record within any eligible timestamp tie. No nearest-time join or future quote is permitted.

Do not carry state from the preceding day. The zero-second snapshot therefore has no earlier same-day reference. Endpoints at the next midnight are not in this grid; the last ten origin clocks have out-of-grid target endpoints.

## 2. Validity belongs to each snapshot's own time

Let the latest eligible trade record contain price \(p\), amount \(v\) and collector time \(a_P\). Its state is valid at \(t_j\) only if the numeric fields are finite and positive and

\[
0\le t_j-a_P\le5\times10^6.
\]

Let the latest eligible quote contain bid \(b\), ask \(a\), positive finite amounts and collector time \(a_Q\). It is valid only if all required values are finite and positive, \(b<a\), and

\[
0\le t_j-a_Q\le10^6.
\]

The age limits include equality. Age is since the latest supported observation, not the latest price change. An unchanged quote can be refreshed by a new observed record. Conversely, a later record cannot refresh an earlier snapshot retrospectively.

An invalid latest observation blocks the reference until another update supplies a valid state. Do not bypass it to an older clean-looking trade or quote. Missing, stale, locked/crossed and otherwise invalid states are recorded, not assigned a zero price or repaired with a later observation. These exclusions define study eligibility; they do not label a quote erroneous or identify a genuine shock.

Where valid, define

\[
P_j=p,\qquad M_j=(b+a)/2,
\qquad s_j=(a-b)/M_j,
\qquad g_j=\log P_j-\log M_j.
\]

The midpoint is a recorded reference, not latent truth or an executable return. Missing disconnect messages also prevent certification of continuous observation merely because values look valid.

## 3. Common causal features

For each reference \(S\in\{P,M\}\), define adjacent one-second grid returns

\[
r_j^S=\log S_j-\log S_{j-1}.
\]

Both fitted predictors receive the same 12-dimensional input

\[
x_j=(r_j^P,\ldots,r_{j-4}^P,
      r_j^M,\ldots,r_{j-4}^M,s_j,g_j)^\top.
\]

This needs six immutable reference snapshots, from \(j-5\) through `j`. Validate each history snapshot against its **own** clock and age limits. Applying the current clock's one-second quote limit to every older history point would incorrectly reject ordinary lagged history. Replacing an invalid historical snapshot with a later valid quote would leak future information.

Let \(V_j^P,V_j^M\) indicate valid reference states. Define origin-time feature eligibility

\[
I_j=\mathbf1\{j\ge5\}\prod_{i=0}^{5}V_{j-i}^PV_{j-i}^M.
\]

This depends solely on information available by the origin under the collector-prefix convention. The first five clocks lack a complete history; even `j=5` requires the unavailable midnight reference. Do not manufacture a fixed warm-up count in place of actual eligibility.

Issue forecasts at **all** \(I_j=1\) origins. Keep source ages and statuses privately even if the future outcome will be missing. The same features for both targets prevent a comparison in which only one task knows its current reference state.

## 4. Labels and retrospective scoring coverage

The two ten-second targets are

\[
Y_j^P=\log P_{j+10}-\log P_j,\qquad
Y_j^M=\log M_{j+10}-\log M_j.
\]

Each endpoint uses the same strict-before, validity and inclusive-age rules at \(t_{j+10}\). There are no delayed-start labels or overnight endpoints in this pilot.

The common scorable indicator is

\[
J_j=I_j\,\mathbf1\{j+10\le86399\}\,V_{j+10}^PV_{j+10}^M.
\]

Unlike \(I_j\), \(J_j\) is not known at an ordinary origin because it includes future reference validity. It is an evaluation mask, not an operational decision rule. All reported losses condition on this disclosed paired coverage.

Preserve the distinction between:

- No prediction: insufficient or invalid origin/history inputs, \(I_j=0\).
- Issued but session-censored: \(I_j=1\), endpoint outside the fixed grid.
- Issued but future-unscorable: endpoint inside the grid but one or both references invalid/unavailable.
- Issued and jointly scored: \(J_j=1\).

These main statuses partition the scheduled origins; detailed invalidity reasons may overlap. Report issued-to-scorable attrition, each reference's exclusions and per-session counts. Do not infer performance at all eligible origins from only those with future fresh trade and quote observations. Depending on activity or outages, that subgroup can differ systematically from the full issued population.

The last ten clocks are censored by the grid definition, even if external data would extend into the next day. Never invent targets by silently loading another session or carrying the last value beyond coverage.

## 5. Why the mechanical gap baseline is necessary

On every common scorable origin,

\[
\boxed{Y_j^P=Y_j^M+g_{j+10}-g_j.}
\]

The current gap \(g_j\) is already an admissible input. If future midpoint movement and terminal gap both had conditional mean zero, the trade conditional mean would be \(-g_j\). Thus trade-return predictability can arise from a known starting gap without predicting future midpoint movement.

The fixed diagnostic therefore predicts

\[
g_{\mathrm{mech}}^P(x_j)=-g_j,\qquad
g_{\mathrm{mech}}^M(x_j)=0.
\]

It fits no parameters and receives no future reference. Its assumptions need not hold; that is why its losses are reported. The midpoint mechanical baseline duplicates zero and supplies no additional independent evidence.

The identity alone does not prove bid/ask bounce. The gap can also reflect asynchronous observations, state freshness, venue/reference scope or other recorded-price differences. A fitted coefficient on the gap is not a verified causal mechanism.

## 6. Training-only equal-session estimation

For a fitting session `d`, let \(n_d=\sum_jJ_{d,j}>0\). Assign each matched origin weight

\[
w_{d,j}=1/(6n_d).
\]

Each session has equal total influence. All fitting statistics use these weights on the common matched subset, without test or validation preprocessing. For feature `l`, compute

\[
\mu_l=\sum_{d,j}w_{d,j}x_{d,j,l},\qquad
\sigma_l^2=\sum_{d,j}w_{d,j}(x_{d,j,l}-\mu_l)^2.
\]

Use unit scale if variance is zero and standardise by \(z_l=(x_l-\mu_l)/\sigma_l\). The common `X` and weights imply identical feature scalers for the two targets. Their target means and fitted coefficients can differ.

For target \(q\in\{P,M\}\), fit

\[
\min_{\beta_{0,q},\beta_q}
\sum_{d,j}w_{d,j}(Y^q_{d,j}-\beta_{0,q}-z_{d,j}^\top\beta_q)^2
+\alpha\|\beta_q\|^2.
\]

The intercept is unpenalised and equals the weighted target mean. Use alpha in the frozen order \([0,.001,.01,.1,1,10,100]\), with weighted least squares for zero. Select separately by equal-session validation MSE, exact ties in stated order; do not refit on validation. Every flexible fitted comparator receives the same admissible full inputs.

The constants are the target-specific equal-session training mean and weighted training median. The median is the first sorted target whose cumulative training weight reaches .5. This is a weighted median for the declared session-weighted MAE task, not the pooled-row median. With an exact half-weight interval of minimisers, the stated rule selects its lower endpoint.

Baseline tie order is zero, training mean, weighted median, mechanical gap. Validation MSE selects a baseline separately for each target. A median can be useful for MAE, but the plan's selection objective remains MSE; preserve disagreements between the two loss functions.

Keep all learned coefficients, intercepts, scalers, constants, medians, model-bearing selections and per-origin predictions private under the source-specific publication boundary. Publish only the permitted one-way artifact hashes, provenance and aggregate findings. The generic equations here are not fitted model artifacts.

## 7. Descriptive test estimands

For test session `d`, model `m` and target `q`, define

\[
L^q_{m,d}=\frac1{n_d}\sum_{j:J_{d,j}=1}(Y^q_{d,j}-\widehat Y^q_{m,d,j})^2,
\qquad R^q_m=\frac13\sum_{d\in\mathrm{test}}L^q_{m,d}.
\]

MAE and the origin-count-weighted pooled risk are secondary. Report every test date, every baseline, the selected reference identity, denominator risks and coverage. A high-activity date must not silently receive more weight in the primary summary.

For each target, report relative improvement over its validation-selected baseline,

\[
G_q=1-R^q_{\mathrm{fit}}/R^q_{b_q},
\]

when the denominator is positive. It is a ratio of averaged risks, not an average of individual percentage errors. Undefined zero-risk ratios remain undefined rather than being stabilised with an arbitrary epsilon.

Also report the change in absolute zero-relative improvement,

\[
\mathcal A=(R^P_0-R^P_{\mathrm{fit}})-(R^M_0-R^M_{\mathrm{fit}}),
\]

in squared-log-return units. This uses a common zero reference, but still compares distinct labels and separately selected pipelines. Normalised gains across targets have different denominators. Raw lower midpoint MSE may simply reflect a different target second moment or unchanged quotes, not greater predictive skill.

**Only three nonadjacent monthly test sessions exist. Report no bootstrap confidence intervals, p-values, significance, power or broad generalisation claims.** Many scored seconds do not turn those three selected sessions into independent replications of market regimes. Per-session signs and magnitudes describe consistency within this cohort; they do not establish population reliability.

No practical economic margin or execution-cost model has been established. The old synthetic 5% criterion is not reused. Report point effects, absolute MSE/MAE, their disagreements and the coverage on which they depend.

## 8. Minimum conclusion and stop boundary

This study can describe whether a frozen classical full-input predictor improves recorded trade and midpoint forecasts relative to the fixed baselines on three protected matched sessions. Comparison with the mechanical gap baseline checks whether simple starting-gap correction accounts for trade skill. Persistence on midpoint targets would weaken an explanation confined to that starting term; attenuation would not uniquely prove its cause.

Other explanations include changed target variance, quote update patterns, asynchronous capture, missing/disconnected intervals, the retrospective scorable cohort and separate model selections. The plan's documented collector-infrastructure change within training can also affect age/coverage patterns. No result establishes efficient-price drift, error/shock labels, client-time availability or profit.

The earlier trade-row studies use different periods, venue/source and horizons; they are not the paired control for this question. Keep the within-study trade target as the contemporaneous comparison. Publish bounded acquisition failures and null/adverse results without new dates, age thresholds, horizons or features chosen after outcomes.

No source bodies were accessed, prices inspected, models run or spending incurred in writing this specification.
