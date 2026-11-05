# Experiment v2: mathematics of the shared-time diagnostic

These are original derivations for a controlled diagnostic, not equations or results attributed to a research paper. V2 asks whether retaining two possible disturbance explanations has a practically useful effect on later forecasts. Every method is explicitly told that one event occurred at the same time. This privilege removes event detection from the question; it does not represent an operational forecasting system.

## 1. Data model and information

Let there be `n` assets, with vectors written as columns. At integer time `t`,

\[
x_t=A x_{t-1}+w_t+\mathbf 1\{t=\tau,Z=S\}d,
\qquad
y_t=x_t+v_t+\mathbf 1\{t=\tau,Z=O\}d.
\]

The variables are:

- \(x_t\in\mathbb R^n\): underlying returns, hidden from ordinary methods.
- \(y_t\in\mathbb R^n\): recorded returns supplied to those methods.
- \(A\in\mathbb R^{n\times n}\): known transition matrix; the simulator requires spectral radius below one.
- \(w_t\sim N(0,Q)\): ordinary state innovation, with known covariance \(Q\).
- \(v_t\sim N(0,R)\): ordinary measurement noise, with known covariance \(R\).
- \(\tau\): the known time of the single event.
- \(Z\in\{O,S\}\): hidden event category, observation error or state shock.
- \(d\sim N(0,T)\): hidden event amplitude, with known covariance \(T\).
- \(\mathbf1\{\cdot\}\): one when its condition holds, zero otherwise.

Assume \(P(Z=O)=P(Z=S)=1/2\). The initial state is Gaussian; ordinary noises are independent across time and mutually independent of the initial state, category and amplitude. There are no other events. Innovation covariances used below must be positive definite so their densities and inverses are well-defined.

Methods know \(A,Q,R,T,\tau\), the prior and initialisation. They receive observations only through the current time, never latent states, realised amplitudes or future observations. The type oracle additionally knows \(Z\). Knowing \(\tau\) is shared privileged information and must be disclosed in every interpretation of v2.

An observation error adds \(d\) to one recording. A state shock adds it once to the underlying state; its subsequent contribution is \(A^k d\) after \(k\) steps. Repeatedly adding \(d\) would define a different process.

## 2. Conditional Gaussian filtering

Condition on a particular category \(z\). The model is then linear Gaussian. Write

\[
m_{t-1}^z=E[x_{t-1}\mid y_{0:t-1},Z=z],
\qquad
P_{t-1}^z=\operatorname{Cov}(x_{t-1}\mid y_{0:t-1},Z=z).
\]

The notation \(y_{0:t}\) means all observations from zero through `t`, inclusive. Define category-specific noise covariances

\[
Q_t^z=Q+\mathbf1\{t=\tau,z=S\}T,
\qquad
R_t^z=R+\mathbf1\{t=\tau,z=O\}T.
\]

The amplitude is integrated out as extra Gaussian noise. Its realised value is never supplied to the filter.

First predict the state before seeing \(y_t\):

\[
m_{t|-}^z=A m_{t-1}^z,
\qquad
P_{t|-}^z=A P_{t-1}^z A^\top+Q_t^z.
\]

The observed innovation and its covariance are

\[
e_t^z=y_t-m_{t|-}^z,
\qquad
S_t^z=P_{t|-}^z+R_t^z.
\]

For this identity observation equation, the state/observation cross-covariance is \(P_{t|-}^z\). Conditioning their joint Gaussian distribution therefore gives

\[
K_t^z=P_{t|-}^z(S_t^z)^{-1},
\qquad
m_t^z=m_{t|-}^z+K_t^z e_t^z.
\]

Here \(K_t^z\) is the Kalman gain: it determines how strongly the state estimate responds to the innovation. With \(I\) the `n` by `n` identity matrix, a numerically preferable covariance update is

\[
P_t^z=(I-K_t^z)P_{t|-}^z(I-K_t^z)^\top
       +K_t^zR_t^z(K_t^z)^\top.
\]

This is the Joseph form. Implement matrix solves rather than explicitly constructing an inverse.

## 3. Type probabilities and proper log scores

Let \(\pi_{t-1}^z=P(Z=z\mid y_{0:t-1})\). The likelihood of the next observation under component `z` has log density

\[
L_t^z=-\tfrac12\left[
n\log(2\pi)+\log\det S_t^z
 +(e_t^z)^\top(S_t^z)^{-1}e_t^z\right].
\]

Bayes' rule multiplies the previous probability by this likelihood. Implement the operation in log space:

\[
a_t^z=\log\pi_{t-1}^z+L_t^z,
\qquad
\log\pi_t^z=a_t^z-\operatorname{LSE}(a_t^O,a_t^S),
\]

where

\[
\operatorname{LSE}(a,b)=h+\log(e^{a-h}+e^{b-h}),
\qquad h=\max(a,b).
\]

Subtracting the maximum prevents overflow. Store the **normalised log probabilities** as well as ordinary probabilities. For a realised true category \(z_*\), the negative log score is

\[
\ell_t=-\log\pi_t^{z_*}.
\]

Lower is better. Calculate it directly from the normalised log weight. Exponentiating a very negative log weight and then taking its logarithm can underflow to zero and produce a spurious infinite score. Clipping probabilities changes the score and can conceal overconfident errors. An unnormalised log likelihood is not a posterior type log score.

A binary Brier score can also be reported, with the convention

\[
b_t=(\pi_t^S-\mathbf1\{z_*=S\})^2.
\]

This is the single-probability binary convention; summing squared errors over both categories would give twice this number. The uninformative balanced prior has Brier score \(1/4\) and negative log score \(\log 2\).

## 4. Forecasts and the three ordinary controls

The exact posterior is a two-component Gaussian mixture. Its mean and covariance are

\[
\bar m_t=\sum_z\pi_t^z m_t^z,
\qquad
\bar P_t=\sum_z\pi_t^z\left[
P_t^z+(m_t^z-\bar m_t)(m_t^z-\bar m_t)^\top\right].
\]

After the event there are no future interventions, and future ordinary state noise has conditional mean zero. Consequently, the exact one-step return forecast is

\[
\widehat x_{t+1}=A\bar m_t,\qquad t\ge\tau.
\]

Compare these procedures:

1. **Exact mixture:** retain both component distributions and update their probabilities using each new observation.
2. **Project once:** at \(\tau\), replace the exact posterior by the Gaussian \(N(\bar m_\tau,\bar P_\tau)\). Thereafter run an independent ordinary Kalman filter with \(A,Q,R\). Do not copy any subsequent moments from the exact mixture.
3. **Frozen weights:** retain and update the same two component filters, but form forecasts with weights fixed at \(1/2,1/2\). Its components are identical to the exact mixture's components; only category reweighting is removed.

The type oracle uses the component for the known true category and is reported separately.

Exact versus projected filtering tests the forecasting effect of retaining distribution shape beyond mean and covariance. Exact versus frozen weights more narrowly tests evidence-responsive reweighting while preserving the component trajectories. Neither comparison uniquely establishes real causal identification: the result is conditional on the simulator's category definitions and correctly specified laws.

Giving a Gaussian control the exact mixture's mean at **every** origin would force its linear point forecast to equal \(A\bar m_t\). Matching MSE would then be a construction, not an empirical discovery. Matching moments once and subsequently updating independently avoids this tautology. A pooled-noise control alone removes both mixture shape and reweighting, so it does not isolate their separate contributions.

## 5. Causal and zero-transition checks

Before \(\tau\), both categories describe the same clean process. Let \(m,P\) be the common predicted state mean and covariance at \(\tau\), before adding any event variance. Both event explanations give

\[
E[y_\tau\mid Z=z,y_{0:\tau-1}]=m,
\qquad
\operatorname{Cov}(y_\tau\mid Z=z,y_{0:\tau-1})=P+R+T.
\]

Their event-time likelihoods match. Thus \(\pi_\tau^O=\pi_\tau^S=1/2\). Their conditional state estimates can differ, but the observation itself has not revealed which explanation is correct.

For paired worlds sharing pre-event history, ordinary noises and amplitude, observed prefixes match through \(\tau\). Every deterministic causal method must issue the same forecast in those worlds at that origin. The exact, projected and frozen procedures also have the same mixture mean at \(\tau\), so their delay-zero forecasts coincide. The oracle can differ because it receives extra information.

The first potentially distinguishing observation is \(y_{\tau+1}\). Record type scores and forecast errors by elapsed event time. Nonzero \(A\) does not guarantee useful separation in every direction; a shock in a direction annihilated by \(A\) need not leave subsequent evidence.

With \(A=0\), future states forget the event immediately. All event-type observation laws coincide, type posteriors stay balanced, and next-return conditional means are zero. This is a negative control for leakage and unjustified category confidence. It is not evidence that useful inference is impossible when propagation is present.

Renaming both category labels and their associated component definitions must leave forecasts unchanged. A label rename alone is not a mechanism ablation. Treat coupled counterfactual worlds as one seed-level inferential block, not two independent replications.

## 6. Exact Bayes optimality limits the claim

Let \(X=x_{t+1}\), let \(\mathcal I\) contain the allowed observations and shared metadata, and write \(\mu=E[X\mid\mathcal I]\). For any other forecast \(g\) computed from the same information,

\[
X-g=(X-\mu)+(\mu-g).
\]

Expanding its squared norm and conditioning on \(\mathcal I\) removes the cross term because \(E[X-\mu\mid\mathcal I]=0\). Taking expectations gives

\[
E\|X-g\|^2-E\|X-\mu\|^2=E\|g-\mu\|^2\ge0.
\]

Divide both sides by `n` if scoring mean squared error per asset. Under the correct generator, exact mixture filtering supplies \(\mu\). Its population-MSE optimality follows from conditioning; it is not a novel experimental discovery. A finite test sample can still favour another method by chance.

V2 measures the size of the practical headroom, checks implementation, and separates reweighting from immediate moment projection. Any conclusion remains conditional on shared event-time knowledge, known parameters, Gaussian amplitudes, one isolated event and the tested dynamics. It does not establish operational detection, real-market transfer or methodological novelty.

## 7. Analytic interpretation correction for v1

This section changes no v1 data, numerical results or decisions. It clarifies what the covariance terms mean.

At one update, suppose observation and state anomaly branches share a Gaussian prior and equal category priors. Define \(P\) as ordinary predicted state covariance, \(R\) as ordinary measurement covariance, \(T\) as anomaly covariance, \(S=P+R+T\), and \(e\) as the current innovation. Their innovation likelihoods are equal. The mean of the two anomaly posterior means equals the posterior mean of the pooled branch that allocates \(T/2\) to state noise and \(T/2\) to measurement noise.

Let \(D=\tfrac12 TS^{-1}\). The two anomaly posterior means differ from their common average by \(+De\) and \(-De\). Their average within-component covariance is the pooled posterior covariance minus \(DSD^\top\). Adding their between-component covariance \(Dee^\top D^\top\) yields

\[
P_{\mathrm{dual,anomaly}}-P_{\mathrm{pooled,anomaly}}
=D(ee^\top-S)D^\top.
\]

When the identical normal branch is included, multiply this difference by the common posterior probability of an anomaly. The between-component term itself is positive semidefinite, but the **total dual-minus-pooled difference need not be**: the within-component covariances also differ. In one dimension it is proportional to \(e^2-S\), which can be positive or negative.

Therefore, referring to an extra between-branch covariance term does not imply that the dual filter always has greater total covariance than the pooled control. The substantive v1 limitation remains: collapsing explanations at every update does not demonstrate persistent event-type identification.
