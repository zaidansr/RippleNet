# Observation errors, state shocks, and causal forecasting

These equations are an illustrative derivation for this pilot, not equations attributed to the reviewed paper.

## 1. Separate the underlying return from its recording

For one asset let t be an integer observation index. Let x_t be the underlying return and y_t the recorded return. Let a be a fixed persistence coefficient, w_t ordinary process noise, v_t ordinary measurement noise, s_t an exceptional state impulse, and o_t an exceptional recording error. The model is

\[
x_t=a x_{t-1}+w_t+s_t,\qquad y_t=x_t+v_t+o_t.
\]

The first equation describes evolution. The second describes measurement. Setting s_t=0 leaves ordinary evolution; setting o_t=0 leaves ordinary measurement. A genuine impulse changes x_t, which enters the next evolution equation. A recording error enters y_t only, so it cannot change the future underlying state in this model.

Assume w_t has mean zero and variance q, v_t has mean zero and variance r, and the ordinary noises are independent of each other, across times, and of the initial state. For ordinary stationary dynamics require |a|<1. Gaussian ordinary noises are a modelling assumption, not a discovered property of financial returns. Events are explicit interventions in the implemented simulator; their arrival probabilities are not estimated.

## 2. Derive propagation by subtracting two coupled worlds

Let tau be an event time and d its size. Compare a clean trajectory x^C with a state-shocked trajectory x^S. Use identical initial states and ordinary noise samples. At the event,

\[
x^S_\tau=a x^C_{\tau-1}+w_\tau+d,
\quad x^C_\tau=a x^C_{\tau-1}+w_\tau.
\]

Subtracting cancels the shared terms, giving delta_tau=x^S_tau-x^C_tau=d. There are no later impulses, so

\[
\delta_{\tau+1}=(a x^S_\tau+w_{\tau+1})-(a x^C_\tau+w_{\tau+1})=a\delta_\tau=ad.
\]

One more step gives delta_(tau+2)=a(ad)=a^2 d. Repeating gives delta_(tau+k)=a^k d for every nonnegative integer k. In contrast, an observation-error world O has x^O_t=x^C_t at every time, y^O_tau=y^C_tau+d, and no subsequent direct observation-error contribution.

## 3. Why the event cannot always be classified immediately

At tau, the state-shock world records

\[
y^S_\tau=x^C_\tau+d+v_\tau,
\]

while the observation-error world records

\[
y^O_\tau=x^C_\tau+v_\tau+d.
\]

They are equal. All earlier recordings also match. Therefore a function of only the observed history receives the same input in both worlds and must return the same output. With equal prior probabilities for these paired explanations and identical event-time likelihoods, the event-time observation cannot favour either explanation. Other assumptions or side information could change those probabilities; the equality is not a claim that every anomaly is forever unidentifiable.

At the next observation, the state-shock world has an additional ad; the observation-error world does not. New data can supply evidence, although ordinary noise prevents guaranteed classification. If a=0, the state effect disappears after the event: in this construction the complete observed paths match, and the distinction has no predictive effect on future states.

## 4. Numerical example

Take a=0.6, pre-event state zero, d=2, and set the ordinary noise samples to zero for this illustration.

| Time | Underlying state, observation error | Recorded return, observation error | Underlying state, genuine shock | Recorded return, genuine shock |
| --- | ---: | ---: | ---: | ---: |
| tau | 0 | 2 | 2 | 2 |
| tau+1 | 0 | 0 | 1.2 | 1.2 |
| tau+2 | 0 | 0 | 0.72 | 0.72 |
| tau+3 | 0 | 0 | 0.432 | 0.432 |

A privileged predictor knowing the event type and this noiseless setup predicts either 0 or 1.2 for x_(tau+1). A predictor given only the identical observed prefix must issue one forecast for both cases. If it assigns probability p to a genuine shock, its squared-error-optimal forecast is p*1.2+(1-p)*0. With p=0.5 this is 0.6. The two squared errors are (0.6-0)^2=0.36 and (0.6-1.2)^2=0.36. This irreducible ambiguity at that instant is not fixed by increasing model size.

## 5. Extend to several assets

Let x_t,y_t,w_t,v_t,s_t,o_t be vectors of length m, with m=3 in the pilot. Let A be an m-by-m transition matrix, and Q,R the ordinary process and observation covariance matrices. Then

\[
x_t=A x_{t-1}+w_t+s_t,\qquad y_t=x_t+v_t+o_t.
\]

Entry A_ij transfers previous return j into current expected return i. Off-diagonal innovation covariance describes simultaneous co-movement of ordinary noise; it is not the same mechanism as lagged propagation through A. Stability requires every eigenvalue of A to have magnitude below one. Nonzero off-diagonal entries alone do not establish real-world causality.

Subtracting coupled vector trajectories gives delta_(tau+k)=A^k d, where d is the injected vector and A^0 is the identity matrix. For A=[[0.6,0.1],[0,0.4]] and d=[0,2], the immediate effect is [0,2], the next effect is A d=[0.2,0.8], and the following effect is A[0.2,0.8]=[0.20,0.32]. Asset two's initial impulse therefore affects asset one at later times under this assumed model.

## 6. Derive the forecast and the implemented ordinary filter

Let H_t denote all observations y_0,...,y_t. The squared-error-optimal forecast is the conditional mean. Conditional expectation distributes over sums, so

\[
E[x_{t+1}\mid H_t]=A E[x_t\mid H_t]+E[w_{t+1}\mid H_t]+E[s_{t+1}\mid H_t].
\]

The middle term is zero under independent, zero-mean ordinary process noise. The last term is zero only when no future event is scheduled or its conditional mean is zero. Under that assumption the forecast is A m_t, where m_t=E[x_t|H_t]. An asymmetric predictable future event requires the extra conditional-mean term.

For the ordinary linear-Gaussian model, let P_(t-1) be uncertainty about the previous state after its observation. Predict the current state and uncertainty:

\[
m_t^-=A m_{t-1},\quad P_t^-=A P_{t-1} A^T+Q.
\]

Here superscript minus means before observing y_t; superscript T means transpose. With identity observation mapping, the residual is e_t=y_t-m_t^- and its covariance is S_t=P_t^-+R. The Kalman gain K_t=P_t^- S_t^{-1} determines the update m_t=m_t^-+K_t e_t. The implementation solves a linear system instead of explicitly forming S_t^{-1}.

The covariance uses Joseph's form:

\[
P_t=(I-K_t)P_t^-(I-K_t)^T+K_t R K_t^T.
\]

I is the identity matrix. The final forecast is A m_t. These are ordinary-model updates; exceptional disturbances make that model misspecified. The code does not implement a disturbance classifier or the proposed dual-mechanism method.

For the first scalar update in the unit test, a=0.5, q=0.1, r=0.2, previous mean zero and variance one. Thus P^-=0.5^2*1+0.1=0.35; S=0.35+0.2=0.55; K=0.35/0.55. With y=2, the updated mean is 2K and the next prediction is 0.5*2K=0.6363636. The test checks this hand calculation.

## 7. Implementation conventions and common mistakes

- Array index t contains x_t and y_t. Prediction row t targets x_(t+1), not x_t.
- Inject a state impulse once. Reapplying it at every future step creates a different process.
- Do not remove genuine shocks as though they were recording errors.
- Do not use y_(t+1) to revise a forecast originally issued at t. Historical smoothing is a different information set.
- Keep latent states and event logs outside the predictor's interface. The simulator returns separate public and scoring containers; this is an interface convention, not a security boundary.
- Use covariance matrices, not standard-deviation matrices, for Q and R. The simulator obtains a covariance square root through eigendecomposition and multiplies independent standard-normal draws by it.
- Burn-in reduces initialization effects but is not an exact stationary draw. The diagnostic filter's initial covariance is also an explicit approximation.
- A single bad log-price observation eta_t produces return error eta_t-eta_(t-1); a single return impulse models a different recording error.
- Multiple correlated timesteps are not independent research replications. Reproducible RNG seeds do not establish statistical significance.
