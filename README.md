# RippleNet: work-in-progress AI-assisted research

Work-in-progress quantitative research project using AI to investigate observation distortions, market shocks, and robust financial time-series forecasting.

This repository tests a proposed distinction between observation corruption and genuine state shocks. It provides a simulator, causal filtering diagnostics, a frozen synthetic benchmark, matched ablations, tests, and a critical research review. It does not contain a trained neural RippleNet model or evidence of superiority in financial markets.

## Current results

The next stage audits a fixed free paired Kraken trade/quote sample before any forecasting comparison. Data rights and collector-clock limits are explicit; no quote-based model has been fitted. [Source decision and bounded acquisition plan](docs/quote-acquisition-plan.md).

The fresh-period paired-target control finds 13.44% MSE improvement for an origin-start return and 3.24% when the return starts one trade later, on matched October 2017 test origins. MAE is worse for both (0.62% and 4.14%). The result supports substantial near-origin concentration of recorded-price predictability, without identifying its cause. [Fresh-period control, uncertainty and audit](docs/market-delay-results.md).

The first real recorded-market study uses 30 days of historical BTCUSDT trades with a 10/5/15-day train/validation/test split. A validation-selected AR(5) baseline improves held-out equal-day MSE by 7.98% versus the selected constant baseline, while MAE is 0.95% worse. Exploratory dependence-aware intervals and the early-period/archive limits are explicit. This does not validate RippleNet's cause mechanism or profitability. [Real-data findings and independent review](docs/market-study-results.md).

Market-data-derived findings are attributed to Binance Vision and distributed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), with computed changes and source links documented in the report. This notice does not relicense independent project code.

The new scalar information diagnostic finds a 68.68% optimal-risk reduction from a stipulated clean second measurement. A linear predictor with those same inputs captures 99.16% of that improvement; exact nonlinear inference adds 1.81% relative to the full-input linear risk. All frozen numerical checks pass. This conditional synthetic result validates no real market sensor or architecture. [Results, controls and review](docs/information-diagnostic-results.md). The current archive's evidence gaps remain unmet.

The offline archive importer now preserves retrieved row order, explicit units, provenance and incomplete targets while refusing unsupported correction labels. It passed a local check on the already inspected sample; all 82 repository tests pass. This is engineering validation, with no real-data model fitted. [Importer and target-attachment results](docs/archive-import-results.md).

The earlier engineering stage added an immutable replay component with delayed-label and censoring checks, passing 69 tests at that stage. A bounded public trade-archive inspection supports schema work but does not establish original online availability or error/shock labels. [Replay implementation and readiness outcome](docs/replay-readiness-results.md).

The real-data feasibility audit does not establish a valid test of the original error-versus-shock mechanism. Three subagents reviewed public sources, target/availability mathematics, and an actual bounded sample's schema. An observable-target replay is a separate conditional engineering step; no real-data model was fitted. [Research decision and next discriminating experiment](docs/real-data-feasibility-decision.md).

The complete five-cell observation-noise sensitivity reports retention gains of approximately 0%, 0.0217%, 0.1116%, 0.1342%, and 0.0784%. Every five-cell-adjusted upper bound is below 0.23%, far below the 5% target. Increasing observation noise does not justify growing the architecture for this frozen task. [Full sensitivity report, figure and independent audits](docs/noise-sensitivity-results.md).

An exploratory conditional-risk reconstruction explains the v2 outcome: future innovations account for 95.763% of delayed Bayes risk, while exact retention improves conditional risk over projection by only 0.03564%. Even perfect current-state information would permit at most 4.27116% improvement over projection on these disclosed histories under the assumed model, below the 5% target. Original forecasts and stored scores were reproduced exactly. [Risk decomposition and independent reviews](docs/conditional-risk-results.md).

The subagent-reviewed v2 diagnostic gives every method the true intervention time. Posterior type inference improves, but retaining the full mixture shows essentially no forecast gain over a Gaussian projected once and updated independently: -0.0013%, with an adjusted interval of [-0.1449%, +0.1642%], on 128 new paired seed blocks. It fails the 5% practical target. [V2 report and independent audits](docs/experiment-v2-results.md).

The first causal mixture candidate failed the practical improvement gate on 30 held-out seeds. Against the development-selected baseline in the nominal moderate-persistence setting, its MSE was 1.4% worse for recording errors and 1.2% better for genuine shocks; the latter uncertainty interval includes zero improvement. It did not reliably beat the pooled-noise ablation and was 13.6% worse on recording errors under the price-derived corruption shift. [Full results and limitations](docs/experiment-v1-results.md).

## Run locally

Requires Python 3.11+ and NumPy. No PyTorch, paid services, or cloud resources are required.

```sh
python -m unittest discover -s tests -v
python -m ripplenet.diagnostic
python -m ripplenet.report
python -m ripplenet.history_report
python -m ripplenet.risk_report
python -m ripplenet.noise_sensitivity_report
```

The diagnostic checks mathematical identities and causal timing. Its output is not a forecasting benchmark, a statistical significance test, or a mechanism ablation.

To reproduce the frozen benchmark into a separate directory, run `python -m ripplenet.evaluate --output work/reproduction-v1`. This uses the same now-disclosed test seeds and is reproduction, not a new independent evaluation. The default output directory already contains the original results and is protected against overwrite.

## Research documents

- [Protocol](docs/protocol.md): agreed pilot and amendments recommended by review.
- [Peer review](docs/peer-review.md): threats to valid conclusions.
- [Results audit](docs/results-analysis.md): available evidence and analysis requirements.
- [Mathematics](docs/math-tutorial.md): equations, assumptions, derivations, and numerical example.
- [Paper analysis](docs/paper-analysis.md): a relevant primary-source paper selected for this review.
- [Implementation notes](docs/implementation-notes.md): assumptions, interfaces, tests, and current limits.
- [Experiment specification](docs/experiment-v1.md): settings and conditional decision rules frozen before final testing.
- [Held-out experiment report](docs/experiment-v1-results.md): comparative results, intervals, ablations, and shift tests.
- [V2 shared-time specification](docs/experiment-v2.md): the exact two-component diagnostic and five contrasts.
- [V2 mathematics](docs/experiment-v2-mathematics.md): exact updates, risk limitations, and the v1 covariance-interpretation correction.
- [V2 results](docs/experiment-v2-results.md): 128-seed findings with independent statistical and engineering reviews.
- [Exploratory conditional-risk analysis](docs/conditional-risk-results.md): noise floor, approximation excess, timing, and oracle headroom; this reuses disclosed histories and is not a fresh test.
- [Observation-noise sensitivity](docs/noise-sensitivity-results.md): all five fixed cells, 128 new paired seed blocks, source checks, scientific figure, and independent audits.
- [Real-data feasibility decision](docs/real-data-feasibility-decision.md): limits of the current evidence, the data-readiness contract, and the next information ablation.
- [Public-data source audit](docs/public-data-audit.md): official exchange/book candidates, correction semantics, timing and use constraints.
- [Observable-target audit](docs/observable-target-audit.md): causal information sets, delayed labels, observable returns and information-versus-model comparisons.
- [Data-engineering feasibility](docs/data-engineering-feasibility.md): bounded sample schema inspection, private-data handling and additional documented sources.
- [Replay implementation and readiness](docs/replay-readiness-results.md): implemented prefix boundary, 69-test validation and the remaining evidence gate.
- [Replay mathematical contract](docs/replay-contract.md): ordinal horizons, fixed-window labels, training cutoffs and censoring.
- [Binance recorded-file audit](docs/binance-readiness-audit.md): preselected bounded inspection, provenance and source-specific attribution/license notice.
- [Offline archive importer](docs/archive-import-results.md): strict source parsing, retained target coverage, 82-test validation and the independent review.
- [Research frontier](docs/research-frontier.md): why the current evidence gate remains unmet and which new questions could follow.
- [Auxiliary-information diagnostic](docs/information-diagnostic-results.md): frozen new scalar question, information versus same-input approximation gaps, analytic controls and all quadrature orders.
- [Real recorded-market study](docs/market-study-results.md): 30 fixed BTCUSDT dates, protected test comparison, source provenance, uncertainty and competing explanations.
- [Fresh-period delayed-start control](docs/market-delay-results.md): matched origins and features, target-specific fits, common-reference contrast and all paired losses.

To reproduce v2 into a separate directory, run `python -m ripplenet.history_experiment --stage final --output work/v2-reproduction`. This repeats disclosed seeds and does not supply a new independent test.

The exploratory moment reconstruction can be repeated with `python -m ripplenet.risk_reconstruction --output work/risk-reproduction`. It checks the actual frozen v2 source and original CSV metrics before reporting new conditional moments.

Repeat the noise sensitivity with `python -m ripplenet.noise_sensitivity --output work/noise-reproduction`. Optional figure rendering uses Matplotlib (`requirements-plot.txt`): `python -m ripplenet.noise_sensitivity_report --plot`. Plotting only reads saved results and records its versions separately.

The work is AI-assisted. All scientific claims require reproducible evidence and checked sources. Explicit owner approval is required before any spending.
