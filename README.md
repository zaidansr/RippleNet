# RippleNet: work-in-progress AI-assisted research

Work-in-progress quantitative research project using AI to investigate observation distortions, market shocks, and robust financial time-series forecasting.

This repository tests a proposed distinction between observation corruption and genuine state shocks. It provides a simulator, causal filtering diagnostics, a frozen synthetic benchmark, matched ablations, tests, and a critical research review. It does not contain a trained neural RippleNet model or evidence of superiority in financial markets.

## Current result

The first causal mixture candidate failed the practical improvement gate on 30 held-out seeds. Against the development-selected baseline in the nominal moderate-persistence setting, its MSE was 1.4% worse for recording errors and 1.2% better for genuine shocks; the latter uncertainty interval includes zero improvement. It did not reliably beat the pooled-noise ablation and was 13.6% worse on recording errors under the price-derived corruption shift. [Full results and limitations](docs/experiment-v1-results.md).

## Run locally

Requires Python 3.11+ and NumPy. No PyTorch, paid services, or cloud resources are required.

```sh
python -m unittest discover -s tests -v
python -m ripplenet.diagnostic
python -m ripplenet.report
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

The work is AI-assisted. All scientific claims require reproducible evidence and checked sources. Explicit owner approval is required before any spending.
