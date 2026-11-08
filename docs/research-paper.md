# Observation Distortions, Market Shocks, and Forecast Value

*A reproducible pilot study of the RippleNet research hypothesis*

RippleNet research project | Maintainer zaidansr | 8 November 2026

Completed research pilot. Final report. Not peer reviewed. AI-assisted research and writing.

## Abstract

Distinguishing an erroneous observation from a genuine state shock may improve state inference without materially improving the next forecast. We investigate this distinction through sequential synthetic diagnostics and retrospective recorded-market studies. A collapsed-mixture candidate failed its synthetic practical-improvement gate. An exact known-time mixture improved event-type inference but had essentially no realised forecasting advantage over a strong Gaussian projection control across 128 paired seed blocks. An exploratory risk decomposition attributed 95.763% of delayed Bayes risk to future innovations; a five-cell observation-noise sensitivity found retention gains below 0.14%. A separate, favorable auxiliary-sensor model produced substantial information value, while a same-input linear predictor captured 99.16% of that benefit. Two early-period BTCUSDT studies found trade-return MSE improvements, attenuating when the target began one trade later, with worse MAE. Finally, a twelve-session Kraken trade/quote pilot found no aggregate trade-MSE benefit beyond a fixed starting-gap correction. Its midpoint MSE improvement was 0.761%, accompanied by worse MAE, only three test sessions and 17.73% scoring coverage. The evidence does not validate RippleNet as a financial forecasting architecture, establish observation-error versus market-shock identification, or demonstrate profitability. It supports separating information value, reference-price effects and model value before expanding complexity.

**Keywords:** financial time series; observation error; state shocks; robust filtering; forecast evaluation; market microstructure; reproducibility.

## 1 Introduction

A large recorded price movement can reflect changing market state, a recording problem, ordinary measurement differences or several effects together. A model that reacts identically to these explanations may appear unnecessarily fragile. The RippleNet hypothesis was therefore that maintaining competing observation-error and genuine-shock explanations could improve financial time-series forecasting. This report evaluates the evidence accumulated while testing that hypothesis, including negative and mixed findings. RippleNet names the completed research pilot; its implemented candidates are classical filtering and linear prediction methods, with no validated neural architecture claimed.

Three questions must be separated. First, can the available observations distinguish event types? Second, does any resulting information change the conditional mean of the target enough to improve the intended loss? Third, does a specialised predictor outperform a strong method receiving the same information? An improvement against a weaker information set or a deliberately limited ablation does not answer the third question.

The study proceeds from a controlled linear-Gaussian simulator to exact conditional-risk diagnostics, a separately declared auxiliary-information experiment, and retrospective market-record benchmarks. Each later design was informed by earlier disclosed results. They are distinct studies with different targets, privileges and comparison margins; their percentages are not pooled into one performance claim. Methods and settings were frozen before their protected numerical outputs, subject to the qualifications recorded below. This synthesis introduces no new model fit or experiment.

Relevant prior work already distinguishes additive observation outliers from innovative state disturbances. Fisch, Eckley and Fearnhead's CE-BASS uses a robust particle-mixture Kalman filter and revisits past states to handle delayed visibility [1]. Their reported applications include machine temperature and server data. That work motivates an established-method comparison, but it does not validate financial forecasting by this project. We did not implement a full CE-BASS benchmark, and make no novelty or superiority claim based on separating disturbances alone.

## 2 Mathematical framework

### 2.1 Synthetic state and observation mechanisms

The multivariate simulator uses a stable transition matrix and isolated interventions:

```math
% eq1
x_t=A x_{t-1}+w_t+s_t, \qquad y_t=x_t+v_t+o_t. \tag{1}
```

Here t is the discrete observation index; x_t is the n-dimensional latent return prescribed by the simulator; A is an n by n stable transition matrix; y_t is the observed vector; w_t and v_t are independent zero-mean Gaussian noises with covariances Q and R; and s_t and o_t are state and observation interventions. A state impulse enters once and subsequently propagates through A. An observation impulse changes the recorded return without changing the latent state. Gaussian impulse magnitudes are matched across paired worlds. These are assumptions of a controlled generator, not observations of financial truth.

Ordinary noises and pre-event histories are coupled across the two worlds. At intervention time tau, adding the same vector to the state or to the observation yields the same observed prefix. A causal ordinary method must then issue the same forecast in both worlds. It can distinguish them only when later observations or genuinely additional information become available. A category oracle receives a different information set and must be reported separately.

### 2.2 Conditional risk and information value

Let H be the allowed observation history, Z the event category, pi_z its posterior probability, and m_z and P_z the conditional mean and covariance of the current state given H and category z. Write mbar for the posterior-weighted mean. For this decomposition, assume no further intervention before the target, so x_(t+1)=A x_t+w_(t+1), with independent zero-mean innovation covariance Q. This is the exact known-time diagnostic's future law, not every possible continuation of Equation 1. For a candidate vector forecast g of that next return, conditional MSE per asset decomposes as:

```math
% eq2
\mathcal R(g\mid H)=\frac{\operatorname{tr}Q}{n}
+\sum_z\pi_z\frac{\operatorname{tr}(A P_z A^\top)}{n}
+\frac{\pi_O\pi_S\|A(m_S-m_O)\|^2}{n}
+\frac{\|g-A\bar m\|^2}{n}. \tag{2}
```

O and S denote observation corruption and state shock. The terms are future innovation risk, within-category state uncertainty, residual between-category uncertainty and approximation excess relative to the exact conditional mean. The third term can be small after new observations reveal the current state, even when identifying the historical event remains an interesting classification task. All ceilings derived from this equation are model-conditional expected risks. They are not bounds on every realised loss.

For a scalar target F, let mu_H=E[F|H] and mu_HU=E[F|H,U], where U is an auxiliary observation available at the origin. Conditional-mean orthogonality gives:

```math
% eq3
E[(F-\mu_H)^2]-E[(F-\mu_{H,U})^2]
=E[(\mu_{H,U}-\mu_H)^2]. \tag{3}
```

This is information value. A separate squared-distance identity compares the full-information Bayes mean with a linear minimum-MSE predictor using exactly H and U. The two gaps have different references and percentage denominators. The linear predictor need not be a conditional mean, but its excess risk still equals its squared disagreement with the full-information conditional mean.

### 2.3 Recorded prices and mechanical reference effects

Market experiments use observed reference prices rather than latent returns. If P(t) is the last recorded trade price, M(t) the bid/ask midpoint and g(t)=log P(t)-log M(t), define Y_P(t,h)=log P(t+h)-log P(t) and Y_M(t,h)=log M(t+h)-log M(t). These log returns obey:

```math
% eq4
Y_P(t,h)=Y_M(t,h)+g(t+h)-g(t). \tag{4}
```

Thus predicting trade return as -g(t), and midpoint return as zero, is a meaningful fixed diagnostic baseline when the conditional expected midpoint log return and terminal log gap are both zero given origin information. It can correct a known starting-price displacement without predicting future midpoint movement. A midpoint is still an observable book summary, not an independently verified efficient price or executable fill.

## 3 Experimental design and evaluation

### 3.1 Sequential synthetic studies

V1 evaluates a small moment-matched mixture candidate with observation-only and pooled-noise ablations. Its mixture settings are stipulated, not learned; twenty clean training seeds fit the OLS baseline. Twelve development seeds select ordinary baselines; thirty protected seed blocks evaluate nominal and shift conditions. Ordinary methods do not receive realised event labels. The mixture collapses after each update rather than retaining the full event-history hypotheses. The primary nominal moderate-persistence comparison uses five one-step forecasts beginning at the event origin. Shift conditions share seed randomness and are not independent additional replications [D1].

V2 is an easier representation diagnostic. Every ordinary arm knows the true intervention time, dynamics, noise covariances, Gaussian impulse distribution and the guarantee of no further events. It compares an exact retained two-component mixture, a Gaussian projected once at the event and then updated independently, and identical conditional filters with weights frozen at one half. Its 128 new paired blocks average both categories, three assets and delayed origins tau+1 through tau+4. It has no clean-event population and does not test operational detection [D2].

Conditional-risk reconstruction reuses V2's disclosed histories and exactly reproduces its saved forecasts and scores before computing missing conditional moments. It is exploratory, not a fresh confirmation. The subsequent noise sensitivity fixes five R/Q variance ratios, all other settings, and 128 new paired blocks. Every cell is reported; none is selected as a market-calibrated optimum [D3, D4].

A separately frozen scalar experiment supplies a hypothetical auxiliary observation. Let C be a balanced O/S category and let b, d, e, u and w be mutually independent zero-mean Gaussians: base state, disturbance, primary noise, auxiliary noise and future innovation. Define X=b+1{C=S}d, Y=X+e+1{C=O}d, clean auxiliary Z_aux=X+u, and future target F=aX+w. Consequently Y=b+d+e in both categories; its marginal likelihood alone cannot identify C. Base-state variance is 0.015625, disturbance variance 0.25, primary and auxiliary ordinary-noise variances 0.0025, forecast multiplier a=0.6 and future innovation variance 0.01. The shared-artifact control adds 1{C=O}d to Z_aux; the duplicate sets Z_aux=Y; the perfect clean case sets u=0; the zero-multiplier case sets a=0 while holding the base prior fixed. Gaussian-mixture expectations are integrated at all four declared Gauss-Hermite orders 24, 48, 96 and 192. This is deterministic numerical integration, not a sampling significance test [D5].

### 3.2 Retrospective recorded-market studies

The first two market studies use official Binance BTCUSDT individual-trade archives. Prices are retained in retrieved-file order with explicit units, strict parsing and source hashes. The first study fixes August 17-September 15, 2017, partitioned into ten training, five validation and fifteen test days. Five lagged adjacent returns predict the next ten retrieved-trade return. The second uses fresh September 16-October 15 dates and the same split lengths, comparing origin-start and delayed-start labels on a common mask [D6, D7].

```math
% eq7
Y_{A,k}=\log P_{k+10}-\log P_k,\qquad
Y_{B,k}=\log P_{k+11}-\log P_{k+1}. \tag{5}
```

k is the retrieved trade-row index. The delayed target's starting price is future label information only, never an input. Both labels span ten retrieved intervals and share nine increments; exchanging the first and last increment changes the forecasting task. Attenuation cannot uniquely identify bid/ask bounce. The paired study uses N-16 common eligible origins per valid day, whereas the first study uses N-15.

The quote study uses Tardis Kraken spot XBT/USD pairs for twelve first-of-month sessions, June 2025-May 2026. Six sessions train, three validate and three test. The already inspected June 2026 audit session is excluded. That later audit informed source/QC choices, so this remains a retrospectively designed research holdout, not a prospectively deployed historical trading process. A documented November 2025 server relocation lies inside training [D8].

Each quote-study session has a one-second UTC collector-clock grid, with strictly earlier trade and quote records at every snapshot and endpoint. Maximum observed-record ages are five seconds for trades and one second for quotes. Six immutable historical snapshots supply five trade returns, five midpoint returns, current relative spread and current log trade/midpoint gap: twelve shared inputs. Invalid latest states cannot be bypassed to older clean-looking states. Targets are ten-second trade and midpoint returns. These are clock horizons, not the earlier ten-trade horizon.

Forecasts are issued using current/past feature eligibility only. Losses use the common subset with both future reference labels available under frozen rules; future validity never decides whether to issue a forecast. Coverage and censoring remain explicit. Consequently, results concern a conditional active/fresh subset, not the whole trading day or an operational selection rule.

### 3.3 Fitting baselines and metrics

For D training sessions with n_d scorable examples in session d, row weights are w_di=1/(D n_d). The classical predictors minimise:

```math
% eq5
\sum_{d,i}w_{di}(y_{di}-b-z_{di}^{\top}\beta)^2
+\alpha\|\beta\|^2,\qquad w_{di}=\frac{1}{D n_d}. \tag{6}
```

z is the feature vector standardised with training-only weighted means and population standard deviations; b is an unpenalised intercept; beta is the coefficient vector. Zero-variance feature scales are set to one. Alpha is selected from the fixed grid 0, 0.001, 0.01, 0.1, 1, 10, 100 using validation equal-session MSE. Alpha zero is weighted least squares. No validation refit or test tuning is used. The quote study also fits equal-session weighted median constants for MAE context; its mechanical gap baseline has no fitted coefficient.

Primary market risks average each session's eligible-origin MSE equally. MAE and pooled-origin risk are secondary. Relative improvement is a ratio of mean risks:

```math
% eq6
G=1-\frac{\overline{\mathrm{MSE}}_{\mathrm{model}}}
{\overline{\mathrm{MSE}}_{\mathrm{reference}}}. \tag{7}
```

Different targets and references have different denominators. Raw lower midpoint variance is not forecast skill. The original synthetic 5% criterion is not transferred to market studies because no market-purpose-specific practical margin or execution model has been established.

### 3.4 Statistical and numerical interpretation

Synthetic inference resamples entire coupled seed blocks, not individual assets, worlds or times. V1 uses a nine-contrast primary adjustment; V2 uses five contrasts; the noise grid uses five cells. Percentile bootstrap intervals and Bonferroni adjustments are approximate. The conditional reconstruction's intervals are descriptive because the histories were already disclosed.

The two 2017 market studies use 9,999 paired noncircular three-day block resamples over fifteen test-day loss vectors. Their adjusted interval levels are 97.5% for two contrasts and 98.333333% for three contrasts. Few blocks, nonstationarity and endpoint underweighting limit coverage; the reported intervals are exploratory dependence-assumption diagnostics, not guaranteed market-level confidence.

The quote study has only three nonadjacent test sessions. Its plan prohibits confidence intervals, p-values, power, significance and broad-generalisation claims. Deterministic quadrature convergence in the auxiliary experiment is numerical reliability, not statistical evidence about an unknown market process.

## 4 Results

### 4.1 Initial candidate and exact-history diagnostic

The V1 candidate failed its practical-improvement gate. Against the development-selected adaptive baseline in nominal moderate persistence, observation-error MSE deteriorated by about 1.4%, while state-shock MSE improved by about 1.2% with uncertainty crossing zero. Its recording-error comparison worsened by 13.6% under price-derived corruption. The dual candidate did not reliably outperform pooled-noise handling. It traded robustness between categories rather than demonstrating useful event identification [D1].

| Synthetic contrast | Relative MSE reduction or score change | Adjusted interval |
| --- | ---: | --- |
| V1 observation errors vs adaptive | -1.4% | [-3.0%, approximately 0.0%] |
| V1 state shocks vs adaptive | +1.2% | [-0.9%, +3.3%] |
| V2 retained vs projection | -0.0013% | [-0.1449%, +0.1642%] |
| V2 retained vs frozen weights | +0.3375% | [+0.1839%, +0.5079%] |
| V2 type negative-log-score reduction | +0.4749 nats | [+0.3926, +0.5443] nats |

Table 1. Distinct synthetic designs and uncertainty families; these rows are not pooled. Positive reductions favour the candidate. Rounded zero endpoints must not be interpreted as exact equivalence.

V2 learns event category: its mean type negative log score is 0.218254 rather than 0.693147 for frozen half probabilities. However, the stronger independently updated Gaussian projection forecasts almost identically. The retained-versus-projection upper adjusted bound is far below the prespecified 5% practical margin. Beating frozen weights supports evidence-responsive inference under the stipulated model; it does not establish a useful advantage over projection [D2].

### 4.2 Risk reconstruction and noise sensitivity

On the reused V2 histories, exact Bayes risk is 0.010442449182 per asset. Future innovation risk is 0.01, or 95.763% of that total. Projection excess above Bayes is 0.000003723471; exact retention reduces projection conditional risk by 0.03564%. Perfect category information would add only 0.02888% over the retained predictor at these delayed origins. Even perfect current-state information, without the future innovation, permits at most 4.27116% improvement over projection on this history average. The actual future-noise floor is 0.01, not 4.27116% [D3].

This explanation is conditional on the model and disclosed histories. It is not a bound on realised finite-sample errors or a universal forecasting impossibility result. At the event origin, category information could have large value but is unavailable from the matched ordinary prefix. After informative observations arrive, current-state inference already makes the forecast means similar.

| Measurement variance ratio R/Q | Retention gain over projection | Adjusted 99% interval |
| --- | ---: | --- |
| 0 | Numerical zero | Numerical zero |
| 0.25 | 0.0217% | [0.0160%, 0.0283%] |
| 1 | 0.1116% | [0.0756%, 0.1528%] |
| 4 | 0.1342% | [0.0730%, 0.2274%] |
| 16 | 0.0784% | [0.0408%, 0.1348%] |

Table 2. All five declared sensitivity cells, with common paired seeds. The largest adjusted upper bound is below 0.23%; none establishes the 5% reference gain.

At higher measurement noise, the perfect-state ceiling exceeds 5% while actual retention gains remain tiny. Therefore the result cannot be explained only by the future-noise floor: the Gaussian approximation is also already close to the Bayes forecast mean. A post-hoc category-oracle bound reaches at most 2.8691% versus projection across the reported cells; this is an exploratory model-conditional history-average bound, not a prespecified simultaneous market claim [D4].

### 4.3 Additional information versus nonlinear inference

The clean auxiliary experiment reduces optimal risk by 68.6824% relative to primary-only Bayes. Exact nonlinear inference reduces risk by 1.80895% relative to the full-input linear predictor. The latter captures 99.16% of the absolute primary-to-full improvement. The percentages have different denominators and must not be added [D5].

| Auxiliary condition | Information reduction vs primary | Nonlinear reduction vs full-input linear |
| --- | ---: | ---: |
| Clean independent sensor | 68.6824% | 1.80895% |
| Shared disturbance | 0.364986% | Numerical zero |
| Exact duplicate | Zero | Numerical zero |
| Perfect clean sensor | 70.6516% | Zero |
| Zero forecast multiplier | Zero | Zero |

Table 3. Conditional scalar information experiment. A trusted simultaneous clean sensor is assumed rather than discovered in market data.

Shared corruption makes the two categories' observation laws identical, while ordinary noise averaging can still improve forecasts. A duplicate reading adds nothing. A perfect clean sensor reveals the state, leaving only future innovation risk; further category information has no forecast value. A zero forecast multiplier removes next-return value even if current classification is informative. All fixed numerical convergence checks pass; clean-case final identity residuals are about 1e-12. This establishes properties of the supplied information model, not market availability, statistical significance or an architectural innovation.

### 4.4 Early-period recorded trade forecasts

The first Binance study selects weighted AR(5) without regularisation. On September 1-15, 2017, its equal-day MSE is 1.849151e-5, versus 2.009438e-5 for the selected training-mean constant: a 7.9767% reduction. MAE is 0.9468% worse. The adjusted exploratory interval is [4.124%, 12.200%], and daily MSE improves on 14 of 15 days. This is a recorded ten-trade target, not a trading strategy [D6].

In the fresh paired study, both labels use identical origins and past inputs with separate target-specific fits. On October 1-15, origin-start MSE improves by 13.4384% versus its selected constant; delayed-start improvement is 3.2387%. MAE is worse by 0.6240% and 4.1422%. The paired absolute zero-relative improvement contrast is 5.43028e-7 squared-log-return units, with adjusted exploratory interval [3.73563e-7, 7.09654e-7]. It is not a percentage-point effect [D7].

| Held-out recorded trade task | MSE reduction vs selected constant | MAE change vs reference | Adjusted exploratory MSE interval |
| --- | ---: | ---: | --- |
| First study September 2017 | +7.977% | +0.947% worse | [4.124%, 12.200%] |
| Fresh origin-start October 2017 | +13.438% | +0.624% worse | [9.104%, 16.216%] |
| Fresh delayed-start October 2017 | +3.239% | +4.142% worse | [0.929%, 5.177%] |

Table 4. Distinct test cohorts and targets. The valid paired target comparison is between the two fresh October tasks, not between September's original result and October's delayed result.

The attenuation is consistent with near-origin concentration, but delayed predictability remains. Legitimate short-lived return dependence, trade-price reversal, serial measurement effects and target changes can all contribute. These controls do not independently identify bid/ask bounce or prove that every gain comes from the shared origin price. Closely related zero and constant baselines are not independent confirmations.

### 4.5 Quote availability and the stronger mechanical baseline

A bounded source audit acquired real Kraken spot trades and reconstructed BBO quotes for June 1, 2026: 73,704 trade rows and 862,680 quote rows. All trade IDs are missing; 381 consecutive identical trade rows are preserved rather than presumed duplicates. A strict-earlier collector-time join finds a preceding quote within one second for 90.89% of trades. Missing IDs, tied clocks, omitted disconnect markers and reconstruction/revision policies remain limitations. This single inspected day supplies no generalisation or forecast result and is excluded from the multi-session study [D9].

The protected quote-study test uses March 1, April 1 and May 1, 2026. On the paired scored subset, the linear predictor's trade MSE is 1.324942e-7, slightly worse than the fixed gap baseline's 1.324140e-7. Comparing only against zero would show a 10.11% gain, but the simple gap correction slightly exceeds that aggregate benefit. The midpoint model improves MSE by 0.7606% versus its selected constant while worsening MAE by 1.0829%. Trade MAE is 3.2337% worse than the selected mechanical reference [D8].

| Quote-study target | Linear MSE | Selected-reference MSE | Relative MSE reduction | MAE change vs reference |
| --- | ---: | ---: | ---: | ---: |
| Trade | 1.324942e-7 | 1.324140e-7 gap | -0.0606% | +3.234% worse |
| Midpoint | 1.417716e-7 | 1.428581e-7 constant | +0.7606% | +1.083% worse |

Table 5. Equal-session conditional risks on three test dates. The reference is mechanically stronger for trade returns; no inferential interval is justified by this design.

Trade relative MSE changes are -1.984%, +2.387% and +5.258% across the three sessions; midpoint changes are -0.533%, +2.244% and +4.305%. Two positive sessions do not establish a robust edge. Equal-session risk still gives high-variance sessions larger absolute loss contributions; it is not an average of session percentage gains.

| Quote-study test session | Clock origins | Issued feature-eligible origins | Paired scorable origins |
| --- | ---: | ---: | ---: |
| March 1 2026 | 86,400 | 22,485 | 16,094 |
| April 1 2026 | 86,400 | 25,904 | 18,755 |
| May 1 2026 | 86,400 | 16,020 | 11,109 |
| Total | 259,200 | 64,409 | 45,958 |

Table 6. Coverage is part of the finding, not an implementation footnote.

Only 17.73% of all clock origins are scored, and 71.35% of issued forecasts have both required future references. Among 18,451 unscored issued origins, two hit the session boundary and 18,449 lack a qualifying future reference. On the scored subset, 15.29% of trade targets and 30.79% of midpoint targets are unchanged. Age, activity, update frequency and retrospective label availability can change the evaluated population. Lower loss on this subset is not full-day deployment performance.

## 5 Discussion

### 5.1 Identification information and forecast value are separate

The synthetic diagnostics support evidence-responsive type inference under their specified law, while rejecting the proposed practical retention benefit for the tested delayed forecasts. A low-dimensional approximation can forecast accurately even when its representation does not preserve a full historical causal narrative. The conditional-risk analysis explains why, and the noise sensitivity shows that the explanation includes both innovation uncertainty and small approximation error.

The auxiliary study supplies a different lesson: genuinely new information can dominate predictor sophistication. However, placing a clean simultaneous sensor in the generator installs a favorable distinction by construction. No real sensor with these properties was established, and the result cannot rescue the earlier null or validate a market mechanism. Most benefit was already captured by a classical full-input linear method.

### 5.2 Reference choice and baseline strength change the claim

Recorded trade returns can be predictable because the target shares an observed starting price or because the last trade differs from a current book reference. The first real studies established a narrow held-out MSE effect, with metric tradeoffs and weak references. The delayed-start experiment reduced but did not remove that effect. The quote comparison adds a stronger, explicit mechanical explanation and finds no aggregate trade-MSE advantage beyond it.

This is a limitation of the claim supported by the benchmark, not proof that its predictions contain no information. It also does not prove that the earlier Binance effects had the same cause: venues, quote currencies, horizons, dates, reference prices and fitted pipelines differ. The remaining midpoint result is small, mixed across sessions, adverse under MAE and conditional on restrictive coverage. It does not establish a reliable financial edge.

### 5.3 Ablations do not establish real causal categories

V1 observation-only and pooled variants test robustness and covariance propagation; V2 frozen weights test whether posterior evidence updates matter. Neither substitutes for independent real event labels. Shared and duplicate auxiliary controls check mathematical information assumptions; delayed targets and mechanical gap forecasts check alternative recorded-price explanations. Collectively they strengthen interpretation while leaving the original market identification problem unresolved. No uncorrected record is labelled a genuine shock, and no quote disagreement is automatically labelled an erroneous observation.

## 6 Limitations and threats to validity

**Synthetic specification and privileges.** Known timing, parameters, isolated Gaussian events and correctly specified observation laws make V2 and sensitivity experiments easier than an operational detector. V2 has no clean-event case or false-alarm population. Price-derived corruption exposed a V1 robustness failure. Estimated dynamics, heavy tails, overlapping events and different measurement mechanisms remain untested.

**Finite samples and adaptive research sequence.** Later experiments follow disclosed earlier findings; these are not a single preregistered confirmatory program. Designs and code were frozen for their own protected outputs, but the overall research path is adaptive. Synthetic paired seed blocks are the unit of replication. Market days and overlapping origins are dependent; bootstrap coverage is approximate. Three monthly quote-study test sessions support descriptive evidence only.

**Retrospective availability and coverage.** Archive hashes verify retrieved bytes, not original publication or client receipt. The Kraken comparison uses provider collector clocks with reconstruction and missing-disconnect limitations. Its June 2026 source audit informed rules for earlier calendar test dates, although its records are excluded from the study. Future-label validity restricts scoring and may select an active/fresh subset. We do not describe these studies as prospective execution tests.

**Baselines objectives and generalisation.** Zero/constant comparisons can exaggerate specialised-model value when a simple reference-gap correction captures the effect. The tested candidates are classical filters or linear predictors, not a completed neural RippleNet. MSE and MAE can disagree, and no real-market minimum useful margin, transaction-cost model or executable-fill target is established. No broad cross-market, contemporary deployment, causal, profitability or novelty claim follows.

**Audit independence and access restrictions.** AI subagents separately checked code, mathematics and numerical reproductions, including raw-file reconstructions for the market studies. These checks belong to one AI-assisted workflow, not independent external peer review. Source-specific restrictions keep Tardis raw data, weights and fitted preprocessing private. General code, provenance, commitments and eligible aggregate findings remain public; exact model-bearing artifacts are available only within permitted use.

## 7 Conclusion

The completed pilot does not validate RippleNet as a financial forecasting architecture or establish separation of recording errors from genuine market shocks. Its strongest synthetic diagnostics show that improved event-type inference can coexist with negligible useful forecasting headroom beyond a strong same-information Gaussian control. A hypothetical clean auxiliary signal has substantial information value, but a linear predictor captures almost all of the available benefit under that assumption.

Real recorded-price experiments show that an MSE gain is not enough to establish the intended scientific claim. The trade-return gains depend on target timing and reference choice, can coexist with worse MAE, and in the quote pilot are matched or slightly exceeded by a fixed starting-gap correction. The remaining midpoint MSE reduction is small, mixed across only three sessions and evaluated on a limited paired-coverage subset. It warrants neither a robust market-edge claim nor architecture expansion.

The justified outcome is a reproducible set of scoped negative and mixed results, together with a stronger evaluation discipline: separate information value from model value; test plausible mechanical references; expose coverage and metric tradeoffs; and distinguish numerical reproduction from statistical and causal evidence. Further work should begin only with a concrete intended use, an independently motivated falsifiable hypothesis, defensible observations or cause evidence, a meaningful metric requirement and genuinely protected evaluation. A larger architecture alone would not resolve the present evidence gaps.

## 8 Data code and research transparency

The public repository contains simulator and forecasting code, frozen plans, source/version hashes, numerical synthetic artifacts, permissible aggregate reports, model-selection commitments and review records [D0]. The current integrated suite passes 118 software tests; these test implementation behavior, not financial validity. No new experiment or data acquisition was performed for this manuscript.

The Binance Vision findings adapted in Section 4.4 and Table 4 are attributed to Binance and distributed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), with source [2, 3]. Changes comprise computed return targets, forecasts, loss summaries and resampling statistics; no raw trades are reproduced and no endorsement is implied. Tardis-derived findings are published only as eligible aggregate research under its separate terms [5]; no blanket open-data license is applied to this mixed-source manuscript. Raw observations and restricted fitted artifacts are not included. No paid data, cloud compute or additional credits were purchased. AI assistants implemented, checked and documented the work; human scholarly review is needed before external submission.

## References

[1] Fisch, A. T. M., Eckley, I. A., and Fearnhead, P. (2020). *Innovative and Additive Outlier Robust Kalman Filtering With a Robust Particle Filter*. arXiv:2007.03238. https://arxiv.org/abs/2007.03238

[2] Binance. *Binance Public Data*. Official dataset documentation and archive schema. https://github.com/binance/binance-public-data

[3] Binance. *Binance Vision Dataset Terms*, version 1.0, updated 26 August 2026; access-time snapshots retained in the research archive. https://github.com/binance/binance-public-data/blob/master/TERMS_AND_CONDITIONS.md

[4] Tardis.dev. *Kraken historical data details*. Source coverage, feed transitions and sample documentation. https://docs.tardis.dev/historical-data-details/kraken

[5] Tardis.dev. *Terms of Service*, reviewed version modified 28 October 2026. Private access-time snapshot SHA256 ea5901192dce12c72f2303702b7f2bf87826b4b1a44806f8659d0fd91b030b11. https://docs.tardis.dev/legal/terms-of-service

[6] Tardis.dev. *CSV data types and construction*. Quote reconstruction, field definitions and timestamp semantics. https://docs.tardis.dev/downloadable-csv-files/data-types

[7] Tardis.dev. *Data FAQ*. Collector clocks, ordering, revisions and quality limitations. https://docs.tardis.dev/faq/data

[D0] RippleNet project archive. Evidence snapshot for this synthesis: commit ce6ea73e071cb2b736a984a82153e360b573c339. https://github.com/zaidansr/RippleNet/tree/ce6ea73e071cb2b736a984a82153e360b573c339

[D1] [Synthetic V1 protocol results and ablations](https://github.com/zaidansr/RippleNet/blob/ce6ea73e071cb2b736a984a82153e360b573c339/docs/experiment-v1-results.md).

[D2] [Exact-history V2 results and audits](https://github.com/zaidansr/RippleNet/blob/ce6ea73e071cb2b736a984a82153e360b573c339/docs/experiment-v2-results.md).

[D3] [Exploratory conditional-risk reconstruction](https://github.com/zaidansr/RippleNet/blob/ce6ea73e071cb2b736a984a82153e360b573c339/docs/conditional-risk-results.md).

[D4] [Complete observation-noise sensitivity](https://github.com/zaidansr/RippleNet/blob/ce6ea73e071cb2b736a984a82153e360b573c339/docs/noise-sensitivity-results.md).

[D5] [Auxiliary-information diagnostic](https://github.com/zaidansr/RippleNet/blob/ce6ea73e071cb2b736a984a82153e360b573c339/docs/information-diagnostic-results.md).

[D6] [First real recorded-market study](https://github.com/zaidansr/RippleNet/blob/ce6ea73e071cb2b736a984a82153e360b573c339/docs/market-study-results.md).

[D7] [Fresh-period delayed-start control](https://github.com/zaidansr/RippleNet/blob/ce6ea73e071cb2b736a984a82153e360b573c339/docs/market-delay-results.md).

[D8] [Multi-session trade-versus-midpoint study](https://github.com/zaidansr/RippleNet/blob/ce6ea73e071cb2b736a984a82153e360b573c339/docs/quote-study-results.md).

[D9] [Paired quote/trade access and readiness audit](https://github.com/zaidansr/RippleNet/blob/ce6ea73e071cb2b736a984a82153e360b573c339/docs/quote-readiness-results.md).

## Appendix A Evidence and reproducibility map

| Stage | Evidence unit | Status of inference | Main scope restriction |
| --- | --- | --- | --- |
| V1 | 30 paired final seed blocks | Approximate adjusted bootstrap | Fixed synthetic generator and candidate |
| V2 | 128 new paired final blocks | Approximate five-contrast bootstrap | Known event timing and parameters |
| Conditional reconstruction | Same disclosed V2 histories | Exploratory conditional risk | No fresh confirmation |
| Noise sensitivity | 128 new paired blocks across five cells | Approximate adjusted cell intervals | No market calibration or best-cell selection |
| Auxiliary information | Five fixed conditions and four quadrature orders | Numerical integration | Clean sensor supplied by assumption |
| First Binance study | 15 held-out days | Exploratory paired day blocks | Early-period retrieved trade prices |
| Delayed-start study | 15 fresh paired held-out days | Exploratory paired day blocks | Different target increments and fitted pipelines |
| Quote readiness | One inspected session | Access and structural checks | No predictive evaluation |
| Kraken quote study | Three held-out monthly sessions | Descriptive only | Conditional coverage and source rights |

Source plans, source-freeze identities, input hashes and review records are linked from each stage report. Fresh seed counts do not establish market transfer; repeated quadrature orders and exact reproductions are not independent experiments. Reproduction uses disclosed settings and observations and must respect the original source conditions. Public general code can recreate permitted private fits; model-bearing outputs must remain outside the repository where the source requires it.
