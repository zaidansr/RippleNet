# Single-origin auxiliary-information diagnostic: mathematics

This is a new synthetic information hypothesis. It asks whether a contemporaneous auxiliary measurement supplies useful information, and separately whether exact inference uses that information better than a full-input linear estimator. It is not a continuation that reopens the old delayed-origin 5% gate. No real independent channels, original receipt clocks or market calibration are established.

The derivations below are original calculations for the declared model. They are not equations attributed to a paper. This document contains no computed experimental results.

## 1. Model and fixed cases

Let the independent random variables be

\[
b\sim N(0,P),\quad d\sim N(0,T),\quad
\epsilon\sim N(0,R),\quad u\sim N(0,U),\quad w\sim N(0,Q).
\]

The balanced hidden category is \(K\in\{O,S\}\), independently chosen with probability one half for each type. `O` means an observation artifact; `S` means a state shock. Define the current state and primary recording by

\[
X=b+\mathbf1\{K=S\}d,\qquad
Y=X+\epsilon+\mathbf1\{K=O\}d.
\]

The single next-return target is

\[
F=aX+w.
\]

Thus \(b\) is an ordinary current-state draw, \(d\) is the event amplitude, \(\epsilon,u\) are measurement noises, and \(w\) is independent future state innovation. Every method knows an event occurs at this origin and knows the stated laws, but does not receive its type, amplitude, state or future innovation.

Freeze

\[
a=.6,\quad Q=.01,\quad R=.0025,\quad T=.25,\quad U=R,
\quad P=\frac{.01}{1-.6^2}=.015625.
\]

The formula for \(P\) supplies the nominal prior scale. There is no simulated prehistory or dynamic state-estimation stage in this single-origin diagnostic. Use exactly these five cases:

| Case | Auxiliary observation \(Z\) | Change from nominal |
| --- | --- | --- |
| Clean independent auxiliary | \(Z=X+u\) | None |
| Shared artifact | \(Z=X+u+\mathbf1\{K=O\}d\) | Artifact also enters auxiliary |
| Duplicate | \(Z=Y\) | No second independent observation |
| Perfect clean auxiliary | \(Z=X\) | \(U=0\) |
| Zero forecast propagation | \(Z=X+u\) | \(a=0\), while keeping \(P=.015625\) fixed |

In the zero-propagation control, do not recompute \(P\) from the changed `a`: this control changes only how the current state affects the future target. All ordinary noises and the event amplitude remain as declared.

## 2. Primary-only Bayes forecast is exactly linear

For both event categories,

\[
Y=b+d+\epsilon.
\]

Its category likelihoods are identical. Therefore \(P(K=O\mid Y)=P(K=S\mid Y)=1/2\). Define

\[
V=P+T+R,\qquad S_X=P+T/2=\operatorname{Var}(X).
\]

For category `O`, \(\operatorname{Cov}(X,Y\mid O)=P\); for category `S`, it is \(P+T\). Conditional Gaussian means and equal category weights give

\[
m_Y=E[X\mid Y]=\frac{P+T/2}{V}Y=\frac{S_X}{V}Y,
\qquad \mu_Y=E[F\mid Y]=a m_Y.
\]

Consequently the unconditional primary-only Bayes risk has the analytic expression

\[
\mathcal R_Y=E[(F-\mu_Y)^2]
=Q+a^2\left(S_X-\frac{S_X^2}{V}\right).
\]

No fitted regression is needed, and replacing this comparator with a weaker primary-only model would confound information and estimation quality.

## 3. Exact two-observation posterior

Write \(r=(y,z)^\top\). In the clean independent case, the observation covariance matrices are

\[
\Sigma_O=
\begin{pmatrix}P+R+T&P\\P&P+U\end{pmatrix},
\qquad
\Sigma_S=
\begin{pmatrix}P+R+T&P+T\\P+T&P+T+U\end{pmatrix}.
\]

Both category means are zero. Define category state variances and state/observation cross-covariances by

\[
V_X^O=P,\quad V_X^S=P+T,\qquad
C_O=(P,\ P),\quad C_S=(P+T,\ P+T).
\]

For \(c\in\{O,S\}\), Gaussian conditioning gives

\[
m_c=C_c\Sigma_c^{-1}r,\qquad
v_c=V_X^c-C_c\Sigma_c^{-1}C_c^\top.
\]

Here \(m_c=E[X\mid r,K=c]\) and \(v_c=\operatorname{Var}(X\mid r,K=c)\). Implement solves, not explicit inverses. The likelihood is \(\phi_2(r;0,\Sigma_c)\), and posterior category weights are

\[
\pi_c(r)=\frac{\tfrac12\phi_2(r;0,\Sigma_c)}
{\sum_j\tfrac12\phi_2(r;0,\Sigma_j)}.
\]

Compute normalised log weights with log-sum-exp. The exact state posterior moments are

\[
\bar m=\sum_c\pi_cm_c,\qquad
\bar v=\sum_c\pi_c\left[v_c+(m_c-\bar m)^2\right].
\]

Thus the full-input Bayes forecast and conditional target risk are

\[
\mu_{YZ}=a\bar m,\qquad
R_B(y,z)=Q+a^2\bar v.
\]

Its expected risk is \(\mathcal R_B=E[R_B(Y,Z)]\). No future measurement-noise variance belongs in this expression: the target is \(F=aX+w\), not a future recorded observation.

The clean channels have different category likelihoods. For example, \(Y-Z\) has variance \(R+U+T\) under `O` and \(R+U\) under `S`. This makes inference possible within the assumed model, but overlapping Gaussian supports do not permit certain category identification for every observation. Different real channels need not satisfy these stipulated error assumptions.

## 4. Full-input LMMSE comparator

The linear minimum mean squared error estimator receives the same `Y,Z` inputs and exact unconditional moments. Define

\[
\overline\Sigma=\tfrac12\Sigma_O+\tfrac12\Sigma_S,
\qquad \overline C=\tfrac12C_O+\tfrac12C_S=(S_X,S_X).
\]

For the clean case,

\[
\overline\Sigma=
\begin{pmatrix}P+T+R&S_X\\S_X&S_X+U\end{pmatrix}.
\]

The comparator is

\[
\mu_L=a\overline C\,\overline\Sigma^{-1}r,
\qquad
\mathcal R_L=Q+a^2\left(S_X-\overline C\,\overline\Sigma^{-1}\overline C^\top\right).
\]

This is an exact population linear comparator, not a regression whose coefficients were estimated from a finite training set. Its Gaussian pseudo-posterior variance must not be substituted for the true mixture's history-conditional variance. The analytic unconditional risk above remains valid from the moments.

## 5. Information value and architecture headroom are different

Because \(\sigma(Y)\subseteq\sigma(Y,Z)\), conditional expectation orthogonality gives

\[
I=E[(\mu_{YZ}-\mu_Y)^2]=\mathcal R_Y-\mathcal R_B\ge0.
\]

This measures the value of extra available information. For the same full inputs,

\[
A_{\mathrm{gap}}=E[(\mu_{YZ}-\mu_L)^2]
=\mathcal R_L-\mathcal R_B\ge0.
\]

This measures exact nonlinear inference headroom over the strongest linear moment comparator. Since the full linear class contains the primary-only Bayes forecast, \(0\le A_{\mathrm{gap}}\le I\). A useful auxiliary channel therefore need not justify a new architecture.

If relative summaries are reported, use the declared denominators:

\[
G_I=I/\mathcal R_Y,\qquad G_A=A_{\mathrm{gap}}/\mathcal R_L.
\]

Do not call \(G_I\) an architecture gain. These ratios concern a new single-origin endpoint and different comparators from the old delayed forecasts. There is no inherited 5% confirmation gate or newly calibrated practical margin.

At a particular full observation, the correct conditional risk of the primary forecast is \(R_B(y,z)+(\mu_Y-\mu_{YZ})^2\). The primary-only conditional variance given `y` alone need not equal that value for each `z`; the identity holds after averaging. This avoids incorrectly claiming a risk decrease at every individual auxiliary observation.

For a category oracle, posterior-averaged conditional risk is

\[
R_{K}(y,z)=Q+a^2\sum_c\pi_cv_c,
\]

and its category-information headroom is

\[
a^2\pi_O\pi_S(m_S-m_O)^2.
\]

The oracle receives extra information and must remain separate from the ordinary full-input comparison.

## 6. Why the controls matter

**Shared artifact.** Both observations become recordings of \(b+d\) with independent ordinary noises. Their identical category covariance is

\[
\Sigma_{\mathrm{shared}}=
\begin{pmatrix}P+T+R&P+T\\P+T&P+T+U\end{pmatrix}.
\]

Category weights stay one half, and the exact posterior mean is \(\overline C\Sigma_{\mathrm{shared}}^{-1}r\), exactly the full-input LMMSE mean. Architecture headroom is zero. Auxiliary information can still help by averaging ordinary measurement noise; positive information gain here is not successful event-type discrimination.

**Duplicate.** Since \(Z=Y\), it supplies no additional information. Reduce the problem to the one-dimensional observation; do not invert or add jitter to the singular two-observation covariance. Both information and architecture gaps are zero.

**Perfect clean auxiliary.** Since \(Z=X\), \(\mu_{YZ}=\mu_L=aZ\), conditional risk is \(Q\), and architecture and remaining category-oracle headroom are zero. Category inference may nevertheless be informative. Type information is unnecessary when the state itself is already known.

**Zero forecast propagation.** With `a=0` and nominal `P` held fixed, all forecasts are zero and all risks are \(Q\). Category likelihoods can remain informative, but no current-state information predicts the independent future target.

These controls separate current information, nonlinear state inference and historical category identification. They do not establish that any real auxiliary source is clean, independent or timely.

## 7. Fixed deterministic integration and convergence checks

Integrate functions of observations directly. For category `c`, let \(L_cL_c^\top=\Sigma_c\), so \(r=L_c\eta\) with \(\eta\sim N(0,I_2)\). For physicists' Gauss–Hermite nodes \(x_i\) and weights \(w_i\), which integrate against \(e^{-x^2}\), the order-`N` expectation is

\[
E[f(Y,Z)]\approx\frac12\sum_{c\in\{O,S\}}
\frac1\pi\sum_{i=1}^N\sum_{j=1}^N
w_iw_j\,f\!\left(L_c\sqrt2(x_i,x_j)^\top\right).
\]

Use orders **24, 48, 96 and 192 per axis**. The one-dimensional duplicate case uses the corresponding one-dimensional normal quadrature or its analytic identities; it must not be regularised into a different model. Perfect and zero-propagation checks should retain their exact mathematical identities rather than manufacture tiny effects from cancellation.

Freeze the following numerical acceptance rules before results:

- Every reported risk and gap integral differs by at most **1e-6** between orders 96 and 192.
- Every reported relative gain differs by at most **0.01 percentage point** between those orders, meaning at most .0001 in fraction units.
- Analytic/quadrature risk identities have absolute residual at most **1e-6**. In particular compare \(I\) with \(\mathcal R_Y-\mathcal R_B\), and \(A_{\mathrm{gap}}\) with \(\mathcal R_L-\mathcal R_B\).

Failure means **numerically inconclusive**. Do not extend orders adaptively, change parameters or select a favourable order after seeing results. Orders 24 and 48 provide the disclosed convergence path, not extra independent replications. Squared-distance gap integrals avoid subtracting nearly equal large risks, but all identity residuals must still be reported rather than hidden by clipping.

There is no random seed, Monte Carlo sample size or statistical significance test here. These are deterministic model expectations with a declared numerical convergence check. Numerical agreement is not evidence that the model describes a market. Report every fixed case and separate information gain, same-information inference gap, oracle headroom and future innovation risk.

No computations, data acquisition, model runs or paid resources were used in writing this specification. Any execution must follow the separately frozen experiment plan.
