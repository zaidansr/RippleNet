# Conditional risk decomposition for the v2 diagnostic

This is a post-hoc mathematical precision diagnostic for the frozen v2 model. It does not modify the model, generate a new independent test set, or turn exploratory analysis into confirmation. The identities below are original derivations under v2's declared, correctly specified linear-Gaussian intervention model.

## Information and notation

At forecast origin `t`, let \(H_t\) contain observations through `t`, the known event time, known model parameters and declared category prior. It contains neither the actual category nor the realised amplitude. The target is the next **latent return** \(x_{t+1}\), not its noisy recording.

There are `n` assets and two event categories \(z\in\{O,S\}\): observation corruption and state shock. For each category, the frozen exact filter supplies

\[
\pi_z=P(Z=z\mid H_t),\qquad
m_z=E[x_t\mid H_t,Z=z],\qquad
P_z=\operatorname{Cov}(x_t\mid H_t,Z=z).
\]

Every quantity depends on `t`; subscripts are omitted to keep the equations readable. The mixture mean is \(\bar m=\pi_Om_O+\pi_Sm_S\). The known transition matrix is \(A\), and future ordinary state noise is independent \(w_{t+1}\sim N(0,Q)\). Since the only intervention has already occurred,

\[
x_{t+1}=Ax_t+w_{t+1},\qquad t\ge\tau.
\]

There is no future event term. There is also no future measurement covariance \(R\) in the target risk: the target is \(x_{t+1}\), not \(y_{t+1}\). Measurement noise still affects the posterior quantities through the observations.

## Derivation

Conditional on a category and the observed history,

\[
x_{t+1}\mid H_t,Z=z\sim N(\mu_z,V_z),
\qquad
\mu_z=Am_z,\quad V_z=AP_zA^\top+Q.
\]

For any forecast vector \(g\) calculated from \(H_t\), expand its error around \(\mu_z\). The conditional residual has mean zero, so its cross term vanishes:

\[
E[\|x_{t+1}-g\|^2\mid H_t,Z=z]
=\operatorname{tr}(V_z)+\|g-\mu_z\|^2.
\]

Average this expression using the **posterior** category probabilities \(\pi_z\). Define the exact Bayes forecast \(\mu=\sum_z\pi_z\mu_z=A\bar m\). The weighted mean-squared distance identity is

\[
\sum_z\pi_z\|g-\mu_z\|^2
=\|g-\mu\|^2+\sum_z\pi_z\|\mu_z-\mu\|^2.
\]

To see why, write \(g-\mu_z=(g-\mu)+(\mu-\mu_z)\), expand the square, and use \(\sum_z\pi_z(\mu-\mu_z)=0\). For two categories,

\[
\sum_z\pi_z\|\mu_z-\mu\|^2
=\pi_O\pi_S\|A(m_S-m_O)\|^2.
\]

Consequently the conditional mean squared error **per asset** is

\[
\boxed{
R(g\mid H_t)=
\underbrace{\frac{\operatorname{tr}Q}{n}}_{N:\ \text{future innovation}}
+\underbrace{\frac{\sum_z\pi_z\operatorname{tr}(AP_zA^\top)}{n}}_{W:\ \text{within-category state uncertainty}}
+\underbrace{\frac{\pi_O\pi_S\|A(m_S-m_O)\|^2}{n}}_{B:\ \text{category-information headroom}}
+\underbrace{\frac{\|g-A\bar m\|^2}{n}}_{E_g:\ \text{forecast excess risk}}
}.
\]

Here \(\operatorname{tr}\) is the sum of diagonal entries and \(\|\cdot\|\) is the Euclidean norm. All four terms are nonnegative in exact arithmetic. This integrates out **both** the unknown current latent state and future innovation, conditional on the recorded history and the assumed model. It is not merely an estimate that replaces the future innovation by zero while retaining an arbitrary realised latent state.

## What each arm means

The retained exact mixture uses \(g=\mu\), so

\[
R_{\mathrm{Bayes}}(H_t)=N+W+B.
\]

For projected or frozen-weight forecasts, the exact conditional difference is

\[
R(g\mid H_t)-R_{\mathrm{Bayes}}(H_t)=E_g\ge0.
\]

These excesses can be positive even when a finite-sample realised MSE comparison happens to favour a control. They measure distance from the correct conditional mean, without the random error cross term in realised losses. They do not establish that the declared model is correct for financial data.

An oracle that is additionally told the category uses \(\mu_z\). Averaging its risk over the category uncertainty **given this same history** gives

\[
R_{\mathrm{category\ oracle,\ averaged}}(H_t)
=\sum_z\pi_z\frac{\operatorname{tr}(V_z)}{n}
=N+W.
\]

Thus \(B\) is the expected reduction available from revealing category at this origin. It is not the realised loss of the actual-category oracle, and it is not the risk conditional on an actual true-category row. For a known particular category, the relevant expression is instead

\[
R(g\mid H_t,Z=z)=\frac{\operatorname{tr}(V_z)}{n}+\|g-\mu_z\|^2/n.
\]

The retained mixture need not beat every control separately conditional on a particular category and history. Its Bayes optimality and nonnegative excess identity refer to the posterior-averaged conditional problem.

A useful further identity explains the frozen-weight result. Let \(p=\pi_S\) and \(\Delta=\mu_S-\mu_O\). The frozen forecast is \((\mu_O+\mu_S)/2\), whereas the retained forecast is \((1-p)\mu_O+p\mu_S\). Therefore,

\[
E_{\mathrm{frozen}}=(p-1/2)^2\|\Delta\|^2/n,
\qquad B=p(1-p)\|\Delta\|^2/n.
\]

Accurate category probabilities alone cannot guarantee substantial next-return benefit: the two component **future means** may already be close. A probability can retain information about the historical event after current observations have made that event nearly irrelevant to forecasting the present state forward.

## Aggregation, signs and practical ratios

Each observed history uses its own posterior probabilities. Do not replace them by \(1/2,1/2\) after observing data merely because the unconditional category prior is balanced.

The experiment samples paired observation and state worlds with a shared seed. Equal averaging of the resulting two history-level risks estimates the balanced **marginal** intervention distribution: each world's marginal law is appropriate for its category. It is not the same operation as averaging conditional category risks equally at one fixed history. The paired worlds, assets, delays and zero-transition control are not independent extra replications. Preserve entire seed blocks for uncertainty calculations, and never give an arm the other world's counterfactual observations.

Positive excess is **control risk minus retained risk**, so positive means a benefit for retention. For the ratio-of-means convention used in the experiment, expected retained improvement over a control is

\[
1-\frac{\overline{R_{\mathrm{Bayes}}}}{\overline{R_g}}
=\frac{\overline{E_g}}{\overline{R_{\mathrm{Bayes}}}+\overline{E_g}},
\]

where bars denote the declared seed/world/delay average. Do not substitute the average of history-level ratios. Report ratios only when their denominators are positive.

The following quantities distinguish explanations for a small observed improvement:

- \(\overline{N}/\overline{R_{\mathrm{Bayes}}}\): how much conditional risk comes from independent future innovation.
- \(\overline{W}/\overline{R_{\mathrm{Bayes}}}\): residual state-estimation uncertainty even if category were supplied.
- \(\overline{B}/\overline{R_{\mathrm{Bayes}}}\): category-oracle headroom relative to retained risk.
- \(\overline{E_g}/\overline{R_g}\): the exact model-conditional fraction of control risk removed by the retained conditional mean.

If excess is tiny, the forecasts are already similar in the relevant squared-distance sense; a weak realised MSE difference is not merely a failure to collect enough future-noise draws. If excess is appreciable but realised contrasts are noisy, integrating the latent state and future innovation reveals headroom that raw outcomes estimate imprecisely. A dominant innovation floor alone does not prove excess is negligible: inspect both quantities. If type headroom is tiny despite good type scores, learning the historical category has little additional next-return value at that origin.

## Delay and negative controls

At event origin \(\tau\), the two event likelihoods match and \(p=1/2\). Retained, projected and frozen forecasts coincide, so both control excesses are zero. Category-information headroom \(B\) can nevertheless be positive: a privileged oracle knows which current state explanation to use before ordinary observations distinguish them.

Inspect \(\tau\) separately from the primary delayed origins \(\tau+1,\ldots,\tau+4\). New evidence can improve category probabilities while \(\Delta\), state uncertainty and the remaining forecasting value of that information decay. Averaging the two periods can conceal this timing constraint.

With \(A=0\), \(W=B=0\), all these next-return means and control excesses are zero, and risk is \(N=\operatorname{tr}(Q)/n\). Type probabilities remain balanced. No future measurement-noise term should appear. Numerical diagnostics should expose, rather than silently clip away, material negative variances or violated identities.

## API correspondence and scientific status

The diagnostic API uses these terms:

| Field | Mathematical quantity |
| --- | --- |
| `future_innovation_risk` | \(N\) |
| `within_type_state_risk` | \(W\) |
| `type_information_risk` | \(B\) |
| `bayes_risk` | \(N+W+B\) |
| `excess_risk['projected']`, `excess_risk['frozen']` | \(E_g\) for the respective forecast |
| `total_risk['retained']` | \(N+W+B\) |
| `total_risk['projected']`, `total_risk['frozen']` | \(N+W+B+E_g\) |
| `total_risk['category_oracle']` | \(N+W\), posterior-averaged rather than actual-category risk |

Arrays are indexed by forecast origin; entries before \(\tau\) are outside this diagnostic and may be `NaN`. These names do not license relabelling posterior-averaged quantities as observed losses.

The original saved aggregate losses cannot recover missing forecast vectors and posterior moments. A logged deterministic replay of the **existing frozen histories and source** can recover them without fitting a new model or acquiring independent data. It remains a post-hoc, model-conditional analysis. Keep the original v2 results and confirmatory decisions unchanged, disclose why replay was needed, and make no fresh independent-confirmation claim from the reused histories. Any later model selection or altered simulation hypothesis needs separately frozen validation and new final data.
