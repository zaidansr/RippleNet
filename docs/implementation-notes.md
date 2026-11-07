# Component choice and implementation assumptions

**Collector-clock quote pilot:** `quote_study.py` enforces streamed byte/row limits, strict backward joins, own-time freshness and shared historical inputs. It separates issued origins from paired scoring coverage and keeps all fitted artifacts outside the repository. Ten fixtures bring the suite to 118. See [mechanical-control findings](quote-study-results.md); only source-permitted aggregate reports and original general code are public.

**Paired-target real-market control:** `market_delay.py` adds matched origin-start/delayed-start labels in a fresh nonoverlapping 30-day period, reusing the existing fitting routine unchanged. It freezes both pipelines before protected test parsing and reports three jointly resampled contrasts. Seven new fixtures bring the suite to 108; see [fresh-period findings](market-delay-results.md).

**Real-market pilot:** `market_study.py` separates development and protected test execution, fits equal-day weighted AR(5) with training-only scaling, freezes validation choices and reports day-level losses/paired exploratory bootstrap intervals. Nine tests bring the suite to 101. See [the real recorded-market study](market-study-results.md); no neural RippleNet or cause labels are introduced.

**Information diagnostic:** `information.py` computes exact scalar mixture posteriors, same-input LMMSE and deterministic risk integrals. `information_experiment.py` executes five fixed conditions at four frozen quadrature orders, records provenance and checks numerical convergence. Ten new tests bring the suite to 92. No model is trained; see [the new conditional findings](information-diagnostic-results.md).

**Offline archive update:** `archive_import.py` adds a bounded local CLI, strict lazy spot-trade parsing and one target attachment per origin. It preserves source IDs separately from replay row ordinals, retains pending/censored outcomes, and refuses correction labels without a ledger. Thirteen new tests bring the suite to 82. This is retrieved-file-order engineering validation, not a real-data forecasting experiment. See [implementation and independent review](archive-import-results.md).

**Replay update:** `replay.py` adds immutable prefix snapshots, delayed fixed-window correction labels, explicit censoring and a necessary training-availability check, initially validated with 11 deterministic synthetic tests. See [replay results](replay-readiness-results.md).

**Noise-sensitivity update:** `noise_sensitivity.py` varies only ordinary measurement covariance across five declared cells, using 128 fresh paired seed blocks and coupling checks. Five fixture tests bring the suite to 58. `noise_sensitivity_report.py` renders all cells and an optional Matplotlib scientific figure from saved results; plotting is isolated from the pinned model runtime. See the [complete report](noise-sensitivity-results.md).

**Conditional-risk update:** added posterior risk traces and `history_risk.py`; the existing forecast/log-weight calculations are unchanged. `risk_reconstruction.py` compares every path with the actual frozen v2 function and reproduces all frozen CSV metrics before exposing missing moments. `risk_report.py` labels the analysis exploratory. Eight new tests bring the suite to 53. See [risk findings and independent audits](conditional-risk-results.md).

**V2 update:** the subagent-built `history.py` retains an exact two-component posterior under shared known timing; `history_statistics.py` implements five-contrast paired inference. Root integration is in `history_experiment.py`, with reporting in `history_report.py`. New invariant tests bring the suite to 45. See [v2 results](experiment-v2-results.md) and its independent audits. V1 data and numerical findings remain unchanged.

No existing component implementation was located, and the request left [COMPONENT] unspecified. The selected first component is the seeded synthetic simulator, with an ordinary causal Kalman filter as a diagnostic consumer. The mathematical concept selected for tutoring is the distinction between observation corruption and state shocks. The selected paper is explicitly identified in paper-analysis.md.

Before writing code, the engineering review identified these requirements: stable transitions; finite symmetric positive-semidefinite covariances; explicit return-versus-price corruption semantics; one-time impulse application; known parameter privileges; correct next-step indexing; independent ordinary noise streams; private event metadata; complete separated scoring windows; and a declared burn-in convention. Those assumptions are documented in the simulator before its implementation.

## Modules

- `simulation.py`: validated typed dataclasses, independent SeedSequence-derived process/measurement streams, Gaussian covariance square roots, explicit interventions, paired counterfactual worlds.
- `filtering.py`: online standard Kalman baseline using linear solves and Joseph covariance updates. No smoothing or label input.
- `diagnostic.py`: two scenarios checking identical prefixes, causal forecast equality and the A^k impulse identity. Saves parameters, RNG seed, versions and source Git tree.
- `tests/test_simulation.py`: 14 unittest cases covering mathematical effects, isolation, boundaries, validation, a hand-computed filter step, and future-data invariance.

NumPy is sufficient for these low-dimensional linear operations. PyTorch would add installation and complexity without a current learning requirement. unittest is used because it is in the Python standard library; no test dependency download is necessary.

## Deliberate limits

**Update after experiment v1:** `benchmark.py` now includes OLS fitting, clipped/adaptive heuristics, and an exact label-informed Gaussian comparator for the declared Gaussian impulses. `mixture.py` adds the collapsed causal mixture and matched branch-count ablations; `statistics.py` provides paired run-level intervals; `evaluate.py` saves the frozen held-out comparison, and `report.py` renders the saved results. The original omissions listed below describe the first diagnostic-only release. No neural network or full CE-BASS implementation has been added.

The simulator has explicit intervention times, not a random event scheduler. It uses a zero initial state before finite burn-in; this approximates an ordinary stationary process. The diagnostic filter has a declared approximate initial covariance. Read-only NumPy arrays discourage accidental mutations but are not a security mechanism. Reproducibility is checked in the recorded environment; cross-version bitwise equality is not promised.

The repository does not yet implement an OLS benchmark fit, robust filter, exact event-informed conditional mean, causal dual-mechanism filter, development selection, held-out statistical comparison, or trained neural network. These omissions prevent interpreting the diagnostic as the complete pilot.

## Reproduce

Use Python 3.13.3 with the recorded NumPy version in requirements-reproduce.txt, then run:

```sh
python -m unittest discover -s tests -v
python -m ripplenet.diagnostic
```

The stored diagnostic's `source_tree_at_run` identifies the exact repository content used; the corresponding remote code commit has that same Git tree. If running the command from a later documentation commit, the reported source tree naturally differs.
