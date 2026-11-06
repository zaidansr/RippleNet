"""Render every frozen observation-noise cell; plotting never reruns the model."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

SUMMARY = Path("results/noise-sensitivity-v1/summary.json")


def render(summary: dict[str, object]) -> str:
    cells = summary["cells"]
    above = [cell["ratio"] for cell in cells if cell["delayed_origins_1_to_4"]["projection_improvement_fraction"]["adjusted_ci99"][0] > .05]
    rows = ["# Observation-noise sensitivity: all five declared cells", "",
            "This is a synthetic, known-intervention-time sensitivity study, informed by prior experiments. It is not market calibration or optimisation of a chosen setting. The complete five-cell grid and the new 128 seed blocks were fixed before the run; no fitted model or parameter tuning was introduced.", "",
            "Engineering, mathematical and statistical subagents reviewed the design. The engineering subagent implemented the runner and fixture tests; root integrated plotting and reporting. The experiment runtime and plotting runtime are separate.", "",
            "## Conditional headroom", "",
            "Each quantity first averages four delayed forecast origins and both event worlds within a seed. Reported fractions are ratios of pooled means. The same 128 paired seed blocks and bootstrap indices span every cell; neither cells nor worlds multiply independent sample size.", "",
            "| R/Q variance ratio | Bayes risk | Projection risk | Retention gain | Five-cell interval | Category-oracle headroom | Future-noise share | Perfect-state ceiling |",
            "| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: |"]
    for cell in cells:
        value = cell["delayed_origins_1_to_4"]
        gain = value["projection_improvement_fraction"]
        lo, hi = gain["adjusted_ci99"]
        rows.append(f"| {cell['ratio']:g} | {value['bayes']['mean']:.8f} | {value['projected_total']['mean']:.8f} | {100*gain['ratio_of_means']:.4f}% | [{100*lo:.4f}%, {100*hi:.4f}%] | {100*value['category_information_fraction']['ratio_of_means']:.3f}% | {100*value['future_noise_fraction']['ratio_of_means']:.2f}% | {100*value['perfect_current_state_ceiling_fraction']['ratio_of_means']:.2f}% |")
    rows += ["", "The primary intervals are 99% individual percentile intervals (Bonferroni alpha=.05/5), using 9,999 paired seed resamples with seed 789012. Their joint coverage is approximate. The fractions other than retention gain have descriptive 95% intervals in the summary. Conditional Bayes optimality is assumed by the correctly specified model; the empirical issue is effect size, not a new theorem.", "",
             f"Cells whose entire adjusted retention-gain interval exceeds the 5% practical reference: **{above if above else 'none'}**. This reports the full grid and does not select an optimal cell or establish that any financial series has its assumed observation noise.", "",
             "## Absolute risk and realised losses", "",
             "| R/Q | Absolute conditional projection excess | Retained realised MSE | Projected realised MSE |", "| --- | ---: | ---: | ---: |"]
    for cell in cells:
        value = cell["delayed_origins_1_to_4"]
        rows.append(f"| {cell['ratio']:g} | {value['projected_excess']['mean']:.10f} | {value['retained_mse']['mean']:.8f} | {value['projected_mse']['mean']:.8f} |")
    rows += ["", "Higher relative gain can coexist with higher absolute prediction error. Conditional risks integrate latent-state and future-innovation uncertainty, while realised MSE contains the particular sampled innovations; they need not rank methods identically on a finite sample.", "",
             "## Scientific limits", "",
             "Only R changes. Every method receives the true intervention time, true noise parameters, fixed dynamics, known Gaussian impulse law and the guarantee of no further events. Unknown timing, parameter error, other corruption mechanisms, overlapping events, real-market transfer, trading utility and methodological novelty are not established.", "",
             "The R=0 cell is a delayed perfect-observation control, not a claim that event type stays unknowable. Once y[tau+1] reveals the exact current state, delayed forecasts agree and conditional risk equals the .01 future-noise floor. Historical type probabilities may still change; realised MSE is random.", "",
             "Any promising synthetic cell requires external justification for its observation quality before it can motivate a market-facing project. Do not tune another architecture to the disclosed cells and call that a new test. An operational candidate selected from this study requires a separate design and fresh evaluation.", "",
             "## Figure", "",
             "![Complete observation-noise sensitivity](../figures/noise-sensitivity.svg)", "",
             "The figure shows every declared cell with the same categorical axis. The left panel displays primary headroom and uncertainty; the right displays absolute conditional risk. It does not interpolate a market-calibrated optimum.", "",
             "## Provenance and reproduction", "",
             f"Executed model source tree: `{summary['source_tree_at_run']}`. Model runtime: Python {summary['python']}, NumPy {summary['numpy']}. Full matrices, actual source-file SHA256 values and coupling/control residuals are stored in the [summary](../results/noise-sensitivity-v1/summary.json). Local commit identity is distinguished from the public source-tree identity.", "",
             "Run `python -m ripplenet.noise_sensitivity_report` to render tables from saved results. Optional figure rendering requires Matplotlib: `python -m ripplenet.noise_sensitivity_report --plot`. The figure provenance records plotting versions and input-summary hash separately; plotting does not run the simulator. Full reproduction into another directory uses `python -m ripplenet.noise_sensitivity --output work/noise-reproduction`; these then-disclosed seeds are not a new independent test.", "",
             "[Declared plan](noise-sensitivity-plan.md), [mathematics](noise-sensitivity-mathematics.md), [audit plan](noise-sensitivity-audit-plan.md). No paid resources were started.", ""]
    return "\n".join(rows)


def plot(summary: dict[str, object], png: Path | None = None) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    cells = summary["cells"]
    x = np.arange(len(cells))
    settings = [cell["delayed_origins_1_to_4"] for cell in cells]
    gains = np.array([v["projection_improvement_fraction"]["ratio_of_means"]*100 for v in settings])
    bounds99 = np.array([v["projection_improvement_fraction"]["adjusted_ci99"] for v in settings])*100
    bounds95 = np.array([v["projection_improvement_fraction"]["ci95"] for v in settings])*100
    plt.rcParams.update({"font.size": 10, "svg.hashsalt": "ripplenet-noise-sensitivity-v1"})
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.7), layout="constrained")
    left, right = axes
    left.errorbar(x, gains, yerr=np.array([gains-bounds99[:, 0], bounds99[:, 1]-gains]), fmt="o-", color="#2463a6", ecolor="#8baeca", capsize=5, linewidth=1.6, label="Retention gain; five-cell intervals")
    left.errorbar(x, gains, yerr=np.array([gains-bounds95[:, 0], bounds95[:, 1]-gains]), fmt="none", color="#2463a6", linewidth=3, label="Pointwise 95% intervals")
    left.axhline(5., color="#a14b30", linestyle="--", linewidth=1.3, label="5% practical reference")
    left.set(title="Same-information conditional headroom", ylabel="MSE reduction versus projection (%)", ylim=(0, max(5.6, float(bounds99[:, 1].max())*1.15)))
    left.legend(fontsize=8, loc="upper left")
    for field, label, color, style in (("bayes", "Exact Bayes risk", "#2463a6", "o-"), ("projected_total", "Projection risk", "#d48429", "s--"), ("future", "Future-innovation floor", "#555555", ":")):
        right.plot(x, [v[field]["mean"] for v in settings], style, label=label, color=color, linewidth=1.6)
    right.set(title="Absolute conditional risk", ylabel="Mean squared-return units per asset", ylim=(0, max(v["projected_total"]["mean"] for v in settings)*1.12))
    right.legend(fontsize=8, loc="upper left")
    for axis in axes:
        axis.set_xticks(x, [f"{cell['ratio']:g}" for cell in cells])
        axis.set_xlabel("Measurement/process variance ratio R/Q")
        axis.grid(axis="y", alpha=.22)
        axis.spines[["top", "right"]].set_visible(False)
    fig.suptitle("Synthetic observation-noise sensitivity · known intervention time", fontsize=13)
    fig.supxlabel("128 shared paired seed blocks · forecast delays 1–4 · all five cells · not market calibrated", fontsize=9)
    directory = Path("figures")
    directory.mkdir(exist_ok=True)
    fig.savefig(directory/"noise-sensitivity.svg", metadata={"Date": None})
    if png:
        png.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(png, dpi=180)
    plt.close(fig)
    provenance = {"matplotlib": matplotlib.__version__, "plotting_numpy": np.__version__,
                  "model_numpy": summary["numpy"], "input_summary_sha256_canonical_text": hashlib.sha256(SUMMARY.read_text(encoding="utf-8").encode()).hexdigest(),
                  "simulator_rerun": False}
    (directory/"noise-sensitivity-provenance.json").write_text(json.dumps(provenance, indent=2)+"\n", encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plot", action="store_true")
    parser.add_argument("--png", type=Path)
    args = parser.parse_args()
    data = json.loads(SUMMARY.read_text(encoding="utf-8"))
    target = Path("docs/noise-sensitivity-results.md")
    target.write_text(render(data), encoding="utf-8")
    if args.plot:
        plot(data, args.png)
    print(target)
