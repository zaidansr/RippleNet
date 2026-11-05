"""Render the saved held-out evaluation without rerunning or tuning models."""

from __future__ import annotations

import json
from pathlib import Path


def percent(value: float) -> str:
    return f"{100*value:+.1f}%"


def interval(values: list[float]) -> str:
    return f"[{percent(values[0])}, {percent(values[1])}]"


def render() -> str:
    path = Path("results/experiment-v1/summary.json")
    result = json.loads(path.read_text(encoding="utf-8"))
    primary = result["scenarios"]["nominal_moderate"]
    baseline = primary["selected_baseline"]
    comparisons = {category: primary["contrasts"][f"dual_vs_{baseline}_{category}"] for category in ("observation", "state", "clean")}
    practical = any(comparisons[c]["adjusted_ci"][0] >= .05 for c in ("observation", "state"))
    no_harm = all(comparisons[c]["adjusted_ci"][0] >= -.05 for c in comparisons)
    original_gain = any(comparisons[c]["relative_improvement"] >= .05 and comparisons[c]["ci95"][0] > 0 for c in ("observation", "state"))
    original_harm = all(comparisons[c]["relative_improvement"] >= -.05 for c in comparisons)
    lines = [
        "# Experiment v1: held-out synthetic findings", "",
        "This is a newly run synthetic feasibility experiment, not an analysis of pre-existing user results. The candidate is a small moment-matched Gaussian mixture filter, not a neural network or a validated financial model.", "",
        "## Design and provenance", "",
        "The public experiment specification and method code were committed before the final evaluation. Twenty clean training seeds fit OLS; twelve separate development seeds selected one ordinary baseline per persistence setting. The oracle gate passed on development data. Thirty new test seeds then evaluated the frozen methods with no post-test tuning. Each seed couples clean and two event worlds and is the unit of bootstrap resampling. Shift conditions share seeds and are not independent extra replications.", "",
        f"Frozen source tree: `{result['source_tree_at_run']}`. Runtime: Python {result['python']}, NumPy {result['numpy']}. [Specification](experiment-v1.md), [development losses](../results/development-v1.json), [full summary](../results/experiment-v1/summary.json).", "",
        "## Primary comparison: nominal, moderate persistence", "",
        f"Comparator selected on development data: **{baseline}**. Positive relative improvement means lower MSE. Category scores average five post-event one-step forecasts and three assets within each seed. Clean scores use an event-free control after warm-up; they are not all clean intervals surrounding events.", "",
        "| Category | Baseline MSE | Dual MSE | Improvement | Paired 95% interval | Adjusted interval |",
        "| --- | ---: | ---: | ---: | --- | --- |",
    ]
    for category, comparison in comparisons.items():
        lines.append(f"| {category} | {comparison['reference_mse']:.6f} | {comparison['method_mse']:.6f} | {percent(comparison['relative_improvement'])} | {interval(comparison['ci95'])} | {interval(comparison['adjusted_ci'])} |")
    lines += ["", "Adjusted intervals use per-contrast alpha=.05/9 for the prespecified nine nominal/moderate contrasts (three references, three categories). They are percentile bootstrap approximations using 9,999 paired resamples, not exact finite-sample guarantees.", "",
              f"Original exploratory point-estimate/95%-interval rule passes: **{original_gain and original_harm}**. At least one event improvement confidently exceeds the 5% practical margin under adjusted intervals: **{practical}**. All three baseline contrasts meet the uncertainty-aware no-more-than-5%-harm margin: **{no_harm}**.", "",
              "A positive point estimate is not sufficient evidence that the gain exceeds 5%. An interval crossing -5% cannot rule out practically important harm. MSE changes establish no trading profit or market transfer.", "",
              "## Scientific assessment", "",
              "- **Meaningful improvement:** the candidate fails the agreed continuation rule. Its baseline-relative event gains do not reach the 5% practical target.",
              "- **Statistical reliability:** the nominal state-shock gain is not established; its interval crosses zero. Recording-error deterioration is visible in the raw interval, but its adjusted interval reaches zero. The small clean-control gain is statistically stable under these assumptions but practically below the project's threshold.",
              "- **Generalisation:** no transferable advantage is demonstrated. The recording-error comparison deteriorates under the price-derived corruption shift, and larger anomaly magnitudes do not produce the required gain.",
              "- **Ablation:** the dual method beats observation-only handling on state shocks while losing on recording errors. It does not show a reliable advantage over pooled noise. This supports a robustness tradeoff, not successful event-type identification.",
              "- **Conclusion:** stop advancement of this collapsed candidate under the current gate. This does not establish that all disturbance-aware models are ineffective; it rejects the promised benefit for this frozen candidate and tested settings.", "",
              "## Mechanism ablations", "",
              "| Reference ablation | Category | Dual improvement | Adjusted interval |", "| --- | --- | ---: | --- |"]
    for reference in ("observation_only", "pooled"):
        for category in ("observation", "state", "clean"):
            comparison = primary["contrasts"][f"dual_vs_{reference}_{category}"]
            lines.append(f"| {reference} | {category} | {percent(comparison['relative_improvement'])} | {interval(comparison['adjusted_ci'])} |")
    lines += ["", "All variants use three branches, the same nominal dynamics, priors and scale, and no tuning on test data. The observation-only ablation duplicates the measurement-error branch. The pooled ablation duplicates a generic branch splitting anomaly variance between process and measurement noise.", "",
              "There is an analytical confound: with identical prior state moments, the dual and pooled variants have the same current posterior mean. The dual variant retains extra between-branch covariance; this can alter subsequent forecasts. Because the filter collapses event explanations after every update, an ablation difference supports a role for uncertainty propagation, not demonstrated recovery of true event identities. No event-classification score is asserted.", "",
              "## Declared shift tests", "",
              "These are secondary exploratory comparisons with raw paired 95% intervals. Magnitude-shift event standard deviation is .75 rather than .5; causal methods keep their original .5 scale. Price-error shift replaces one return spike with adjacent +d,-d recording errors. The oracle is omitted there because its covariance schedule would no longer be exact.", "",
              "| Condition | Persistence | Frozen baseline | Observation gain [95% interval] | State gain [95% interval] | Clean gain [95% interval] |",
              "| --- | --- | --- | --- | --- | --- |"]
    for name, scenario in result["scenarios"].items():
        shift, persistence = name.rsplit("_", 1)
        reference = scenario["selected_baseline"]
        cells = []
        for category in ("observation", "state", "clean"):
            comparison = scenario["contrasts"][f"dual_vs_{reference}_{category}"]
            cells.append(f"{percent(comparison['relative_improvement'])} {interval(comparison['ci95'])}")
        lines.append(f"| {shift} | {persistence} | {reference} | " + " | ".join(cells) + " |")
    max_gap = max(s["max_ordinary_prefix_forecast_gap"] for s in result["scenarios"].values())
    lines += ["", "Fresh seeds test repeatability under the generator. These two shifts test limited synthetic transfer, not robustness to arbitrary dynamics, estimated parameters, heavy tails, overlapping events or real markets. The zero-persistence control should erase the forecasting value of state propagation. Ratios at tiny absolute effect sizes should not be overinterpreted.", "",
              "## Causal checks and statistical limits", "",
              f"Maximum ordinary-method forecast difference across matched observed prefixes: {max_gap:.3g}. Per-origin MSE is saved in the summary. Matching predictions at delay zero is required; a privileged oracle may differ because it receives event metadata.", "",
              "All confidence intervals condition on the fixed generator and settings. Thirty seeds can leave substantial uncertainty; no seeds were added after inspecting intervals. The primary multiplicity family excludes secondary shifts and oracle comparisons, which remain exploratory. The three event worlds and all shift conditions share randomness by design.", "",
              "The oracle knows event time, category and true Gaussian impulse variance, but not realised amplitude or latent state. Baselines are simple, known-parameter methods. An established dual-disturbance approach such as CE-BASS remains necessary before any methodological-superiority or novelty claim. The simulated state itself is a prescribed latent return, not observed financial truth.", "",
              "## Most discriminating next experiment", "",
              "Separate event-history information from generic uncertainty adaptation. Compare (1) the collapsed dual model, (2) a filter retaining the previous event's competing explanations until new observations arrive, and (3) a Gaussian adaptive-covariance control matched for posterior mean/covariance propagation. Freeze their settings on new development seeds and use a new held-out seed set, since the v1 final seeds are now spent. Score by elapsed event time and include the price-derived corruption shift.", "",
              "If retaining event history adds no benefit over the covariance-matched control, explicit disturbance identification is unnecessary for the observed gains. If benefit appears only after divergent observations and transfers across the corruption shift, that is stronger evidence for the proposed mechanism. A larger neural network would not isolate these explanations.", "",
              "## Files and reproduction", "",
              "Per-seed category losses are saved as one CSV per condition/persistence in results/experiment-v1. Whole-path means and per-origin means are in summary.json. Run `python -m ripplenet.report` to regenerate this document from saved results. `python -m ripplenet.evaluate` refuses to overwrite an existing final evaluation directory. Reproducing frozen evaluation in a separate checkout is permissible; reusing its results for further tuning is not an independent new test.", ""]
    return "\n".join(lines)


if __name__ == "__main__":
    destination = Path("docs/experiment-v1-results.md")
    destination.write_text(render(), encoding="utf-8")
    print(destination)
