# Agreed pilot and review recommendations

## Agreed scope

Seven days, approximately 10–15 focused hours. Three synthetic assets; next-step latent returns predicted using observations available by the forecast origin. Known stable dynamics and ordinary noise parameters for the initial filters. Disturbances are isolated, with matched distributions of initial magnitudes and affected assets. Moderate, weak, and zero persistence are tested.

Comparators: zero prediction, fitted linear model, standard Kalman filter, observation-robust filter, and a separately reported privileged oracle. A causal dual-mechanism filter is conditional on evidence of useful oracle headroom. This repository's first component and diagnostic do not yet implement that complete comparison.

Development data select methods and settings. Freeze the configuration before evaluating on 30 independent shared test seeds and unseen event magnitudes. Measure errors over the first five one-step forecasts beginning at the event origin, separately for both event categories; also report overall and clean periods. An event at index t scores predictions of x[t+1] through x[t+5]. The simulator requires all those targets to exist.

Agreed exploratory gates: develop a causal filter if the oracle reduces development event-window MSE by at least 10% in either category. A promising causal result needs at least 5% held-out improvement in either category, paired 95% uncertainty supporting improvement, and at most 5% deterioration in the other category or clean periods. The comparator is chosen before final testing.

Deliver a runnable experiment, saved seeds/settings, figures/tables, and a report even if the gate fails. No spending without explicit approval.

## Review amendments requiring explicit interpretation

The original gates are exploratory: passing either of two categories is a multiple-comparison opportunity. A confidence interval excluding zero does not show improvement exceeds 5%, and a point estimate of harm below 5% does not establish noninferiority. Confirmatory claims need prespecified multiplicity handling and appropriate bounds against the actual decision margins.

New seeds are same-generator replication. Unseen magnitudes are a limited distribution shift. Neither establishes transfer to real markets. Estimated parameters, heavy tails, alternative propagation, event rates, and price-derived quote corruption are later external validity tests.

An oracle is an optimal benchmark only if it computes the conditional mean under the actual data-generating law and stated information. A covariance-inflation heuristic with labels is a label-informed comparator, not an automatic upper bound on forecasting performance.

## Most informative first experiment

Couple two worlds with identical ordinary noises and pre-event histories. Inject the same vector into the observation in one world and the latent state in the other. Their observed histories match through the event instant. A causal method must give the same forecast then; later differences can use newly arrived observations. Repeat with zero and moderate persistence, report each forecast-origin delay, and compare a dual-mechanism method with observation-only and generic adaptive-noise alternatives using equal information and tuning budgets.

The shipped diagnostic verifies the paired-world construction and a standard causal filter. It does not yet test the mechanism's benefit against those alternatives.
