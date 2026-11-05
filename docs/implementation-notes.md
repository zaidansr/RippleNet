# Component choice and implementation assumptions

No existing component implementation was located, and the request left [COMPONENT] unspecified. The selected first component is the seeded synthetic simulator, with an ordinary causal Kalman filter as a diagnostic consumer. The mathematical concept selected for tutoring is the distinction between observation corruption and state shocks. The selected paper is explicitly identified in paper-analysis.md.

Before writing code, the engineering review identified these requirements: stable transitions; finite symmetric positive-semidefinite covariances; explicit return-versus-price corruption semantics; one-time impulse application; known parameter privileges; correct next-step indexing; independent ordinary noise streams; private event metadata; complete separated scoring windows; and a declared burn-in convention. Those assumptions are documented in the simulator before its implementation.

## Modules

- `simulation.py`: validated typed dataclasses, independent SeedSequence-derived process/measurement streams, Gaussian covariance square roots, explicit interventions, paired counterfactual worlds.
- `filtering.py`: online standard Kalman baseline using linear solves and Joseph covariance updates. No smoothing or label input.
- `diagnostic.py`: two scenarios checking identical prefixes, causal forecast equality and the A^k impulse identity. Saves parameters, RNG seed, versions and source Git tree.
- `tests/test_simulation.py`: 14 unittest cases covering mathematical effects, isolation, boundaries, validation, a hand-computed filter step, and future-data invariance.

NumPy is sufficient for these low-dimensional linear operations. PyTorch would add installation and complexity without a current learning requirement. unittest is used because it is in the Python standard library; no test dependency download is necessary.

## Deliberate limits

The simulator has explicit intervention times, not a random event scheduler. It uses a zero initial state before finite burn-in; this approximates an ordinary stationary process. The diagnostic filter has a declared approximate initial covariance. Read-only NumPy arrays discourage accidental mutations but are not a security mechanism. Reproducibility is checked in the recorded environment; cross-version bitwise equality is not promised.

The repository does not yet implement an OLS benchmark fit, robust filter, exact event-informed conditional mean, causal dual-mechanism filter, development selection, held-out statistical comparison, or trained neural network. These omissions prevent interpreting the diagnostic as the complete pilot.

## Reproduce

Use Python 3.13.3 with the recorded NumPy version in requirements-reproduce.txt, then run:

```sh
python -m unittest discover -s tests -v
python -m ripplenet.diagnostic
```

The stored diagnostic's `source_tree_at_run` identifies the exact repository content used; the corresponding remote code commit has that same Git tree. If running the command from a later documentation commit, the reported source tree naturally differs.
