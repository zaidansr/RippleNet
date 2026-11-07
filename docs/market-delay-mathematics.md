# Mathematics of the fresh-period delayed-start control

This document follows the [published final plan](market-delay-plan.md), commit `1cdfb3d0fe3eed36e1892d10c4c7c78ec84be3c6`. It describes a new, protected period and paired recorded-price targets. No prices were read or models run to write it.

The study does not identify original receiver availability, efficient prices or an observation-error mechanism. It compares two forecasting tasks in retrieved-file order, using separately selected predictors and a common evaluation mask.

## 1. Fresh dates and the two labels

Fix BTCUSDT UTC dates 2017-09-16 through 2017-10-15. Fit September 16–25, validate September 26–30 and protect October 1–15 for evaluation. There is no overlap with the previous period. Missing, invalid or empty-eligible days stop the design; no date substitution or outcome-based exclusion is permitted.

Within each day, write the recorded prices as \(P_0,\ldots,P_{N-1}>0\), preserving file order. Define adjacent returns

\[
r_k=\log P_k-\log P_{k-1},\qquad k\ge1.
\]

At origin `k`, both predictors receive exactly

\[
x_k=(r_k,r_{k-1},r_{k-2},r_{k-3},r_{k-4})^\top.
\]

The two labels are

\[
Y_k^A=\log P_{k+10}-\log P_k=\sum_{j=1}^{10}r_{k+j},
\]

\[
Y_k^B=\log P_{k+11}-\log P_{k+1}=\sum_{j=2}^{11}r_{k+j}.
\]

Thus

\[
Y_k^B=Y_k^A-r_{k+1}+r_{k+11}.
\]

Both labels span ten retrieved trade intervals and share nine increments. Delaying the start removes one increment and introduces another; it does not simply remove a known noise term.

The price \(P_{k+1}\) is future label information. It must never enter features, scaling, prediction construction or a supposed origin-time forecast anchor. Predicting a future-start return is mathematically legitimate; treating its unknown starting price as available to the model would be leakage. “One trade later” is a retrieved-row shift, not an execution-latency or seconds claim.

## 2. Common origins and maturity

Full input history requires \(k\ge5\). Both labels are available only if \(k+11<N\). The common origins are

\[
k=5,\ldots,N-12,
\qquad n_{\mathrm{common}}=\max(N-16,0).
\]

Use this mask for both tasks in fitting, validation and test. Do not let A use an additional origin that B cannot score. Reset all features and targets every day; no overnight return or target is constructed.

For a valid nonempty-eligible day, retain separate coverage counts:

- Five origins lack complete input history.
- Ten A labels lack the full future endpoint.
- Eleven B labels lack the full future endpoint.
- A has one additional complete, feature-eligible label excluded solely to align with B.

That last A label is **not censored**: it is complete but outside the common comparison mask. A day with \(N\le16\) has no common eligible origin and must stop the fixed design rather than disappear from an average.

Label A matures at ordinal \(k+10\); label B at \(k+11\). Features remain the immutable prefix through `k`. At a historical fit boundary `f`, an A example needs \(k+10\le f\), and a B example needs \(k+11\le f\). This study uses common completed daily masks, so neither task uses a target crossing a day boundary. Availability under the retrieved-row convention does not verify original historical publication or receipt.

## 3. Target-specific fitting without different feature information

For each task \(q\in\{A,B\}\), assign every fitting day equal total weight. If day `d` has \(n_d\) common origins, each origin receives

\[
w_{d,k}=\frac1{10n_d}.
\]

Compute training-only feature means and population scales,

\[
\mu_j=\sum_{d,k}w_{d,k}x_{d,k,j},\qquad
s_j^2=\sum_{d,k}w_{d,k}(x_{d,k,j}-\mu_j)^2,
\]

using scale one for zero variance. Since both tasks have identical features, origins and weights, these feature means and scales must agree between the two fitted pipelines. Separate fit artifacts do not justify different feature masks. Disagreement would signal an implementation or weighting problem.

The target means, coefficients and selected regularisation strengths may differ. Let

\[
\bar Y_q=\sum_{d,k}w_{d,k}Y^q_{d,k},\qquad
z_j=(x_j-\mu_j)/s_j.
\]

For each target independently, fit

\[
\min_{\beta_{0,q},\beta_q}
\sum_{d,k}w_{d,k}(Y^q_{d,k}-\beta_{0,q}-z_{d,k}^\top\beta_q)^2
+\alpha\|\beta_q\|^2.
\]

The intercept is unpenalised and equals \(\bar Y_q\). Use the fixed grid \([0,.001,.01,.1,1,10,100]\), with zero corresponding to weighted least squares/pseudoinverse. Select each alpha by equal-day validation MSE and break exact ties in listed order. Do not refit on validation.

Each task has the fixed baselines zero, its own training target mean and

\[
g_M(x)=10\left(\frac15\sum_{j=1}^5x_j\right).
\]

The lag-mean baseline has the same ten-interval scale for both labels; delaying the starting interval does not change the label's duration. Select each task's strongest baseline on validation only, with ties in zero/constant/lag-mean order. Freeze both fitted pipelines and selected references before opening protected test prices.

This fits the appropriate label for each task. It also means the eventual comparison is between separately trained and selected pipelines, not one fixed predictor with a single input removed.

## 4. Risks and the three primary contrasts

For model `m`, task `q` and test day `d`, define

\[
L^q_{m,d}=\frac1{n_d}\sum_k(Y^q_{d,k}-g^q_m(x_{d,k}))^2,
\qquad
R^q_m=\frac1{15}\sum_dL^q_{m,d}.
\]

The common-origin count is the same for A and B within each day. Primary averaging gives every test date equal weight. Pooled-origin risk and MAE remain secondary and must not replace the primary weighting after outcomes.

Let \(b_A,b_B\) be the separately validation-selected baselines. The first two primary contrasts are

\[
G_A=1-\frac{R^A_{\mathrm{candidate}}}{R^A_{b_A}},
\qquad
G_B=1-\frac{R^B_{\mathrm{candidate}}}{R^B_{b_B}}.
\]

These are ratios of averaged risks, not averages of rowwise percentage errors. Report all reference identities and denominators. Zero reference risk makes a ratio undefined, not an invitation to add an arbitrary epsilon.

For the third primary contrast use a **common zero reference in absolute units**:

\[
D_A=R^A_0-R^A_{\mathrm{candidate}},\qquad
D_B=R^B_0-R^B_{\mathrm{candidate}},\qquad
\mathcal A=D_A-D_B.
\]

Positive \(\mathcal A\) means less zero-relative predictive improvement for B, in squared-log-return units. The common zero reference avoids changing baseline identities and risk-ratio denominators within this contrast. It does not make the tasks identical or isolate a physical cause. For a row, zero-relative improvement is \(Y_q^2-(Y_q-g_q)^2=2Y_qg_q-g_q^2\): both the target and its fitted predictor can change the contrast.

Report \(G_A-G_B\) only descriptively. It compares normalised gains with potentially different selected references and denominators. Express it in **percentage points** when multiplying fraction units by 100; do not call it a relative percentage attenuation or use it as the primary attenuation test.

## 5. Joint day-block uncertainty

Use the same test-day resampling indices for every target, model and contrast. The A/B labels overlap heavily, their origins coincide and their methods are correlated. Independent bootstraps for A and B would discard the pairing.

The frozen rule draws five noncircular three-day blocks from the 15 test dates. Starts are `0` through `12`; concatenate each start and its following two dates. Use 9,999 replicates and seed **190012**. Recompute all day-mean risks, both ratios and \(\mathcal A\) jointly for each replicate.

Report ordinary 95% percentile intervals and the fixed family-three intervals with tails

\[
\frac{.05}{2\cdot3}=\frac1{120},\qquad 1-\frac1{120}=\frac{119}{120}.
\]

Their individual nominal coverage is 98.333333%. They are approximate Bonferroni-adjusted bootstrap intervals, not exact familywise guarantees. Overlapping rows and correlated targets do not multiply the number of independent replications.

The noncircular endpoint limitation remains: across all possible starts, day inclusion counts are \((1,2,3,\ldots,3,2,1)\), summing to 39. Expected replicate mean weights are those counts divided by 39, not the original \(1/15\). Endpoint underweighting can shift the bootstrap centre, especially under trends; report the shift. Do not recenter or tune block length after seeing these outcomes. Fifteen adjacent dates and roughly five blocks provide weak protection against longer dependence or regime changes.

## 6. What the control can establish

A favourable A result with little B improvement, especially with positive \(\mathcal A\), would support sensitivity of this pipeline's recorded-return predictability to removing the first future increment and adding a later one. It would not identify bid/ask bounce, recording errors or origin-price noise as the cause. Short-lived genuine predictability, changed target variance/dependence and model suitability can also produce attenuation—even if prices were measured perfectly.

Persisting B improvement would weaken a narrow explanation based solely on a shared origin-price term. It would not prove efficient-price drift, executable entry at \(P_{k+1}\), economic profit or original as-of availability. A crossing interval is inconclusive, not evidence that effects are equal or absent.

Fresh-period A supplies the contemporaneous control. Comparing old-period A directly with new-period B would mix target delay with period changes; it is not this experiment's attenuation contrast. If neither fresh pipeline improves, limit claims about transfer of the earlier result rather than replacing dates or settings.

There is no calibrated economic minimum effect or cost model, and the synthetic 5% reference is not reused. Keep all three scopes separate: recorded-market forecast comparisons, hypothetical mechanism explanations and trading usefulness. None of the latter two follows from the first alone.

No trade bodies were read, data downloaded, models run or spending incurred in preparing this specification.
