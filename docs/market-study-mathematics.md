# Mathematics of the fixed recorded-market forecasting pilot

This document explains the [published study plan](market-study-plan.md), frozen in commit `ad52381d89716c20076d07333f8656c97fa415cd`. The plan supersedes the earlier five-date suggestion: it uses **30 consecutive UTC dates**, with 10 fitting, 5 validation and 15 protected test days. No prices or outcomes were read to write this document.

The target is a return recorded in a retrieved historical individual-trades archive. It is neither a latent true return nor a verified original receiver-time forecast target. The source supplies no correction/shock labels. This study tests a simple AR(5) predictor; it does not test a disturbance-identification architecture.

## 1. Fixed dates and daily sequences

Use BTCUSDT on these fixed dates:

- Fit: 2017-08-17 through 2017-08-26, 10 days.
- Validation: 2017-08-27 through 2017-08-31, 5 days.
- Protected test: 2017-09-01 through 2017-09-15, 15 days.

The first training date was already inspected for the source audit; do not describe every date as previously unseen. Missing or invalid dates stop the design. Do not replace dates or discard a day with no eligible origins.

Each file is a separate retrieved-row sequence. Within day `d`, let \(P_{d,k}>0\) be the recorded trade price at zero-based row `k`, for \(k=0,\ldots,N_d-1\). Preserve the importer-approved file order, including equal event timestamps and permitted trade-ID gaps. A row horizon is not a number of seconds or a claim of complete original-market trade coverage.

## 2. Target, causal features and coverage

Define adjacent recorded log returns for \(k\ge1\):

\[
r_{d,k}=\log P_{d,k}-\log P_{d,k-1}.
\]

At origin `k`, the five-dimensional feature vector is

\[
x_{d,k}=(r_{d,k},r_{d,k-1},r_{d,k-2},r_{d,k-3},r_{d,k-4})^\top.
\]

It needs prices through the current row, and no later price. Full features first exist at \(k=5\). Reset this history every day; the previous day's last price is not an initial lag.

The fixed ten-row target is

\[
Y_{d,k}=\log P_{d,k+10}-\log P_{d,k}
=\sum_{j=1}^{10}r_{d,k+j}.
\]

It is observed only after row \(k+10\) is consumed, and never crosses a date boundary. Its `available_at` is that endpoint under the retrieved-row convention. Both prices are recorded values, without hindsight correction or imputation.

Keep all origin records and their separate statuses. The first five origins lack a full feature history. The final ten lack a complete target; they are pending during open ingestion and censored at the end. On a short day these groups can overlap. For a valid day of `N` rows:

\[
n_{\mathrm{observed\ targets}}=\max(N-10,0),\qquad
n_{\mathrm{common\ eligible}}=\max(N-15,0).
\]

Compare all predictors on exactly these common eligible origins. A zero baseline could mathematically forecast earlier, but using its additional origins in the primary denominator would make the comparison unequal. Report target censoring and feature unavailability separately rather than dropping them without a count.

For a within-day fit boundary `f`, an example can enter fitting only if \(k+10\le f\), with its origin features frozen at `k`. Across dates, use the declared chronological date/row order. An availability check is necessary, but does not itself verify feature provenance or original exchange availability.

## 3. Equal-day training weights and preprocessing

Let \(\mathcal T\) contain the 10 fit dates, each with \(n_d>0\) eligible origins. Assign

\[
w_{d,k}=\frac1{10n_d}.
\]

Weights sum to one; each date has total weight one tenth. This prevents a high-trade-count day from dominating the fitting objective. It is a deliberate day-weighted task, not the distribution of a randomly selected trade.

For feature `j`, compute training-only weighted means and population variances:

\[
\mu_j=\sum_{d\in\mathcal T,k}w_{d,k}x_{d,k,j},\qquad
s_j^2=\sum_{d\in\mathcal T,k}w_{d,k}(x_{d,k,j}-\mu_j)^2.
\]

If \(s_j=0\), use scale one. The standardised vector is \(z_j=(x_j-\mu_j)/s_j\). Do not average daily standard deviations: that generally differs from the declared pooled weighted variance. Freeze the training feature means/scales for validation and test.

Also compute the training target mean

\[
\bar Y=\sum_{d\in\mathcal T,k}w_{d,k}Y_{d,k}.
\]

No test or validation target, variance, clipping threshold, normalisation constant or fitted quantity may enter these calculations.

## 4. Predictors and selection

The three fixed baselines are:

\[
g_0(x)=0,\qquad g_C(x)=\bar Y,\qquad
g_M(x)=10\left(\frac15\sum_{j=1}^{5}x_j\right).
\]

The last baseline extrapolates the mean of five **per-row** returns to the ten-row target. Omitting the factor ten would use the wrong horizon scale. It equals twice the log-price move over the preceding five rows; it is not a shock classifier.

For each fixed \(\alpha\in[0,.001,.01,.1,1,10,100]\), fit

\[
\min_{\beta_0,\beta}\;
\sum_{d\in\mathcal T,k}w_{d,k}
(Y_{d,k}-\beta_0-z_{d,k}^\top\beta)^2
+\alpha\|\beta\|^2.
\]

The intercept is not penalised. Since the weighted standardised features have mean zero, \(\beta_0=\bar Y\). With matrix `Z`, diagonal weight matrix `W` and centred target vector `y`,

\[
\widehat\beta=(Z^\top WZ+\alpha I)^{-1}Z^\top Wy
\]

for positive \(\alpha\); use least squares/pseudoinverse for \(\alpha=0\). Implement linear solves rather than an explicit inverse. The normalisation above matters: replacing weighted mean squared loss by an unnormalised sum changes what a numeric alpha means.

Select alpha by minimum **equal-day validation MSE**, with exact ties broken in the stated ascending alpha order. Separately select the best baseline on those same five validation dates, with ties in zero/constant/lag-mean order. Freeze both choices before test evaluation. Do not refit on validation or change the feature set.

Validation chooses a candidate, not an unbiased performance estimate. Test data evaluate that frozen choice. Reporting every test model is descriptive only; it must not become another selection stage.

## 5. Primary risk and contrasts

For model `m` on eligible origins of day `d`, define

\[
L_{m,d}=\frac1{n_d}\sum_k(Y_{d,k}-g_m(x_{d,k}))^2.
\]

The primary test risk is

\[
\widehat R_m=\frac1{15}\sum_{d\in\mathrm{test}}L_{m,d}.
\]

Report the alternative pooled-origin risk separately:

\[
\widehat R_{m,\mathrm{pooled}}
=\frac{\sum_dn_dL_{m,d}}{\sum_dn_d}.
\]

They need not rank predictors identically. Do not substitute the more favourable weighting after results. MAE is secondary, not a replacement primary endpoint.

For each of the two frozen reference comparisons—zero and the validation-selected baseline—define the paired daily improvement

\[
D_{b,d}=L_{b,d}-L_{\mathrm{AR},d},\qquad
\widehat\Delta_b=\frac1{15}\sum_dD_{b,d}.
\]

Positive means lower AR error. Relative improvement is the ratio of mean risks,

\[
\widehat G_b=1-\frac{\widehat R_{\mathrm{AR}}}{\widehat R_b}
=\frac{\widehat\Delta_b}{\widehat R_b},
\]

provided \(\widehat R_b>0\). It is not the mean of per-trade or per-day percentage errors. A zero denominator is undefined; do not hide it with an arbitrary epsilon. Keep the primary family size two even if validation selects zero and the two references coincide.

## 6. Fixed day-block bootstrap and its limits

Each bootstrap observation is the whole vector of all model losses for one test date. Rows have overlapping ten-row targets, lagged inputs and other potential dependence; they are not independent replications. Daily aggregation retains within-day comparisons without pretending those rows supply independent uncertainty units.

Use the frozen noncircular three-consecutive-day blocks. From the 15 dates, possible starts are `0` through `12`; each block contains its start and following two dates. Draw five starts with replacement per replicate, concatenate the five blocks, and evaluate the 15 resampled day vectors. Use identical resampled indices for every model and contrast, 9,999 replicates and seed **190011**. Recompute both numerator and denominator of every risk ratio jointly.

Report ordinary 95% percentile intervals and per-contrast 97.5% percentile intervals for the family of two contrasts. The latter use Bonferroni alpha .05/2. They do not give exact finite-sample family coverage, because bootstrap approximation and dependence assumptions remain.

There is an additional explicit boundary limitation. Across all 13 possible starts, test days have block-inclusion counts

\[
c=(1,2,3,3,3,3,3,3,3,3,3,3,3,2,1).
\]

Their expected bootstrap mean weights are \(c_d/39\), rather than the original equal weights \(1/15\). Thus endpoint days are underweighted. For a daily contrast, the replicate mean is centred in expectation at \(\sum_dc_dD_{b,d}/39\), which need not equal \(\widehat\Delta_b\). The discrepancy can matter with trends or unusual edge days. This affects centering, not merely interval width.

Noncircular blocks avoid creating a fictitious September-15-to-September-1 transition, but they do not eliminate endpoint effects or make the test dates exchangeable. Preserve the frozen procedure and disclose this weakness rather than choosing another resampler after seeing the outcome. Fifteen days and roughly five blocks offer limited evidence, especially if dependence or regime shifts extend beyond three days.

Accordingly these intervals are exploratory dependence diagnostics. They do not by themselves establish broad statistical reliability, original operational forecast validity or market generalisation.

## 7. Minimum honest interpretation

The narrow empirical question is whether a frozen lag-return AR predictor improves a declared recorded-price target over the frozen baselines on these 15 held-out retrieved days. Report absolute risks, relative changes, per-day consistency, status coverage and the dependence/availability limitations together.

An interval excluding zero addresses uncertainty under the stated bootstrap approximation; it does not establish economic usefulness. No market-specific useful-effect threshold, trading-cost model or execution assumption has been supplied. Do not reuse the old synthetic 5% reference as a financial criterion.

Beating zero alone does not show superiority to a simple causal extrapolation or training-mean predictor. That is why the independently validation-selected baseline is a second fixed comparison. If the candidate does not beat it, limit the conclusion accordingly. A null or adverse outcome must not trigger new dates, alpha grids or architectures on this protected test set.

These dates concern one instrument in a bounded early period, not a representative cross-market sample. There are no verified observation-error versus genuine-shock labels, so no mechanism or novelty conclusion follows. Neither a favourable score nor a successful prefix replay establishes original receiver availability or trading profit. The real recorded-data study and previous synthetic findings retain their separate scopes.

No trade bodies were read, models fit, data downloaded or paid resources used in writing this mathematical specification.
