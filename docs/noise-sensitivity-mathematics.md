# Mathematics of the fixed observation-noise sensitivity experiment

This experiment maps conditional forecasting headroom in five declared synthetic observation regimes. It introduces no architecture. A favourable cell would demonstrate possibility under that cell's assumptions, not that financial data occupy it. The grid is a synthetic bracket without external market calibration.

## 1. Fixed model and grid

Keep the v2 three-asset transition matrix

\[
A=\begin{pmatrix}.55&.10&0\\0&.45&.10\\.05&0&.35\end{pmatrix},
\qquad Q=.01I_3,\qquad T=.5^2 I_3
\]

fixed. Here \(Q\) is ordinary process-innovation covariance and \(T\) is the single intervention's amplitude covariance. Use exactly the existing known-time, balanced-category model, Gaussian noise laws, 180 retained observations, 128 burn-in steps, and one event time uniform over indices 40–149. The event's type and realised amplitude remain hidden; all arms know its time, prior and amplitude law. There are no later events.

Vary only the scalar \(r\) in

\[
R_r=rQ=.01rI_3,
\qquad r\in\{0,\ .25,\ 1,\ 4,\ 16\}.
\]

| Cell \(r\) | Measurement variance per asset | Role |
| --- | ---: | --- |
| 0 | 0 | Exact-current-state delayed-origin control |
| .25 | .0025 | Fresh-seed replication of the original v2 regime |
| 1 | .01 | Intermediate observation uncertainty |
| 4 | .04 | Noisier observations |
| 16 | .16 | Coarse high-noise bracket |

The ratio is measurement-noise variance divided by **process-innovation variance**. It is not measurement variance divided by unconditional latent-return variance. The latter also depends on \(A\), through the stationary covariance equation \(\Sigma=A\Sigma A^\top+Q\).

Use the confirmed new seeds **70000–70127**, shared across every cell. The grid and count are fixed before opening results. Report all five cells, including failures. Do not move endpoints, insert extra settings or increase sample size after examining the map.

## 2. What changes, and what must not

For each seed, couple ordinary process innovations, event time, realised amplitude and standardised measurement innovations across cells. If \(u_t\sim N(0,I_3)\) is the shared measurement stream, the declared coupling is

\[
v_t(r)=\sqrt{.01r}\,u_t.
\]

Generate the two counterfactual event worlds with that same seed, amplitude and ordinary noise. Latent paths do not change with \(r\); observed paths do. Sharing randomness reduces noise in cell comparisons but does not make the cells independent experiments.

Every method receives the correct \(R_r\) for its cell. Its clean-history filtering and event-time posterior must therefore use that covariance. Do not reuse an event-time posterior, gain or projection covariance calculated at the original \(R=.0025I_3\). Project once at the event using the cell's own exact mixture moments, then evolve the projected filter independently. Re-copying retained moments later would invalidate the comparison.

The scalar intervention does more than alter how precisely the current state is observed: it also changes how informative subsequent observations are about event category. Holding \(A,Q,T\) fixed prevents a simultaneous change of persistence, future innovation floor or latent event size, but the event's observation signal-to-noise ratio necessarily changes. Interpret the total effect of measurement uncertainty; use posterior-risk terms and type scores to investigate the channels rather than claiming one channel was independently manipulated.

The model still assumes independent measurement errors and correct known parameters. It does not cover misspecified noise laws, overlapping events, unknown timing or price-derived paired return errors.

## 3. Conditional-risk terms

At origin `t`, let \(H_t(r)\) denote the observation history and shared metadata in cell `r`. For category \(z\in\{O,S\}\), let

\[
\pi_z=P(Z=z\mid H_t(r)),\quad
m_z=E[x_t\mid H_t(r),Z=z],\quad
P_z=\operatorname{Cov}(x_t\mid H_t(r),Z=z).
\]

The retained forecast is \(\mu=A\bar m\), where \(\bar m=\sum_z\pi_zm_z\). With \(n=3\), define

\[
N=\operatorname{tr}(Q)/n=.01,
\]

\[
W=\sum_z\pi_z\operatorname{tr}(AP_zA^\top)/n,
\qquad
B=\pi_O\pi_S\|A(m_S-m_O)\|^2/n,
\]

\[
E_P=\|g_P-\mu\|^2/n,
\]

where \(g_P\) is the independently evolved projected forecast. These give

\[
R_B=N+W+B,\qquad
R_P=R_B+E_P,\qquad
R_{\mathrm{type\ oracle}}=N+W.
\]

The last expression averages oracle risk over the **current posterior category probabilities**. It is not a true-category row's realised loss. For the derivation and information-set caveats, see [conditional-risk mathematics](conditional-risk-mathematics.md).

Since the retained model supplies the exact conditional mean under the declared generator, \(E_P\ge0\) is a mathematical property. The experiment estimates its size over a distribution of histories; it does not discover that exact Bayesian conditioning is population-MSE optimal.

## 4. Three different headroom quantities

Within each seed and cell, average equally over the two paired event worlds and the four primary origins \(\tau+1,\ldots,\tau+4\). Then average seed-level quantities equally across the 128 seeds. Write an overbar for this declared average. Use identical averaging for every risk component.

The **primary same-information retention gain** is

\[
G_{\mathrm{ret}}(r)
=1-\frac{\overline{R_B}}{\overline{R_P}}
=\frac{\overline{E_P}}{\overline{R_B}+\overline{E_P}}.
\]

This is the relative conditional-risk reduction from projection to retention. It is the appropriate quantity for asking whether preserving this mixture offers the 5% practical benefit against this projected comparator.

The **additional category-information headroom** is

\[
G_{\mathrm{type}}(r)=\frac{\overline B}{\overline{R_B}}.
\]

Its comparator and information set differ: an oracle is additionally told the category. A large oracle quantity does not imply that an ordinary same-information method can obtain it, and it does not imply that retention beats projection by 5%.

The **perfect-current-state ceiling against projection** is

\[
C_{\mathrm{state}}(r)=1-\frac{N}{\overline{R_P}}.
\]

Even a predictor additionally given the exact current state, but not future innovation, cannot remove \(N=.01\). Consequently \(G_{\mathrm{ret}}(r)\le C_{\mathrm{state}}(r)\). If that ceiling is below 5%, the target is infeasible even with this privileged extra information on the averaged conditional histories. A ceiling above 5% only leaves room; it does not show retention can use it.

Also report \(N/\overline{R_B}\), absolute \(\overline{E_P}\), \(\overline B\), \(\overline{R_B}\) and \(\overline{R_P}\). Across-noise percentages have different risk denominators. A percentage alone cannot distinguish a larger absolute approximation error from a changed denominator. With \(A,Q\) and the latent-return units fixed, absolute risks are directly comparable across cells.

These are **ratios of pooled means within a cell**, not averages of per-history ratios. Nor should the five cells be pooled into one headline percentage: no probability distribution describing market occupancy over the grid has been supplied. Compute ratios only with positive denominators, which the present positive \(Q\) ensures.

## 5. Timing and the exact-observation control

At \(\tau\), category likelihoods match in every cell. Both category priors remain .5, and retained, projected and frozen-weight mixture means coincide. Their same-information event-origin retention gains are zero. Oracle category headroom may nevertheless be large. Preserve this origin separately; do not move delayed evidence backwards into its forecast or change the primary window after viewing results.

For \(r=0\), the measurement at \(\tau\) can still be corrupted. At every later origin, however, the event is over and \(y_t=x_t\). All correctly implemented state estimators then know the current state exactly. Their one-step forecasts are

\[
g_t=Ay_t,\qquad t>\tau,
\]

and their latent-next-return conditional risk is exactly \(N=.01\). Thus, at the primary delayed origins,

\[
W=B=E_P=0,
\quad G_{\mathrm{ret}}=G_{\mathrm{type}}=C_{\mathrm{state}}=0.
\]

This remains true even if inference about the historical category is imperfect: its identity is no longer needed to forecast from the exactly observed present state. Zero \(R\) is allowed here because the positive process covariance preserves positive innovation covariances in the required updates. Tests should expose material deviations rather than conceal them by clipping risk terms.

There is no monotonicity guarantee for intermediate-noise retention gains. Greater measurement noise leaves more current-state uncertainty, but can also obscure the evidence needed to infer category. In the idealised limit of arbitrarily large \(R\), for fixed finite history and fixed \(A,Q,T\), observations carry vanishing information and conditional component forecast means approach each other. This motivates a bracket rather than assuming the highest-noise cell must be best. The finite five-cell grid cannot locate a continuous optimum or rule out unsampled regimes.

## 6. Comparisons, uncertainty and conclusions

The same 128 seed blocks appear in every cell. Pair comparisons within seed and preserve those blocks jointly across cells when resampling. The five cells are not 640 independent replications, and the coupled worlds, assets and delays are not extra independent samples. Across-cell contrasts compare different observation histories; they do not condition on one identical history under five noise laws.

Any claim that **at least one** grid cell exceeds 5% needs a multiplicity rule fixed before opening results, such as simultaneous intervals or a declared Bonferroni family for the primary cell gains. Raw cell intervals followed by selecting the most favourable cell do not provide that protection. Approximate bootstrap intervals retain their finite-sample limitations.

Interpret the map without changing the architecture:

- If the same-information upper bounds remain below 5% throughout the grid, the selected regimes do not support the promised gain. This is not a statement about every possible noise law or dynamics.
- If a lower simultaneous bound exceeds 5% in a cell, that establishes material conditional headroom for the exact retained representation against this projected approximation in that cell. It does not establish an operational disturbance detector or a market-relevant model.
- If an interval crosses 5%, retain the uncertainty. Do not silently extend the sample or tune the grid until a cell passes.
- If only the category oracle has headroom, investigate the information constraint rather than treating privileged-category performance as attainable retention gain.

The map is a gate on further research, not permission to enlarge the architecture. Even a favourable synthetic cell requires external justification of a relevant observation regime before model growth, and any model subsequently selected from the map needs separately frozen evaluation on new final data. No data or model runs, architecture changes, paid tools or new spending were performed in writing this document.
