# RippleNet: work-in-progress AI-assisted research

Work-in-progress quantitative research project using AI to investigate observation distortions, market shocks, and robust financial time-series forecasting.

This repository tests a proposed distinction between observation corruption and genuine state shocks. It currently provides a simulator, causal filtering diagnostics, tests, and a critical research review. It does not contain a trained RippleNet model or evidence of superiority in financial markets.

## Run locally

Requires Python 3.11+ and NumPy. No PyTorch, paid services, or cloud resources are required.

```sh
python -m unittest discover -s tests -v
python -m ripplenet.diagnostic
```

The diagnostic checks mathematical identities and causal timing. Its output is not a forecasting benchmark, a statistical significance test, or a mechanism ablation.

## Research documents

- [Protocol](docs/protocol.md): agreed pilot and amendments recommended by review.
- [Peer review](docs/peer-review.md): threats to valid conclusions.
- [Results audit](docs/results-analysis.md): available evidence and analysis requirements.
- [Mathematics](docs/math-tutorial.md): equations, assumptions, derivations, and numerical example.
- [Paper analysis](docs/paper-analysis.md): a relevant primary-source paper selected for this review.
- [Implementation notes](docs/implementation-notes.md): assumptions, interfaces, tests, and current limits.

The work is AI-assisted. All scientific claims require reproducible evidence and checked sources. Explicit owner approval is required before any spending.
