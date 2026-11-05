"""Render exploratory model-conditional risk from saved reconstruction only."""

from __future__ import annotations

import json
from pathlib import Path


def render() -> str:
    summary = json.loads(Path("results/conditional-risk-v2/summary.json").read_text(encoding="utf-8"))
    moderate = summary["settings"]["moderate"]
    values = moderate["delayed_origins_1_to_4"]
    floor = values["future"]["mean"]
    projection = values["projected_total"]["mean"]
    ceiling = 1-floor/projection
    rows = [
        "# Conditional risk: little delayed forecasting headroom", "",
        "This is an exploratory reconstruction of the already-disclosed v2 histories, not a fresh test or a new forecasting model. Three subagents supplied mathematical review, instrumentation/tests, and an independent statistical audit; root integrated the replay and reporting. No parameter, observation, target, seed or original result was changed.", "",
        "## Main finding", "",
        f"Across the two balanced event worlds and delays 1–4, future innovations account for **{100*values['future_noise_fraction']['ratio_of_means']:.3f}%** of exact Bayes predictive risk. Retaining the exact mixture instead of the independently evolved Gaussian projection reduces conditional expected risk by **{100*values['projection_improvement_fraction']['ratio_of_means']:.5f}%**. Even perfect category information adds only **{100*values['category_information_fraction']['ratio_of_means']:.5f}%** over the retained forecast at these delayed origins.", "",
        "The negligible gain is therefore not merely an inconclusive realised-loss comparison. The approximation's conditional means are already close to the exact Bayes means on these histories, while future innovation noise dominates the total risk. Conditional excess is nonnegative by the Bayes-risk identity; that positivity is mathematical, not newly discovered statistical superiority.", "",
        "## Quantitative decomposition", "",
        "Values below are mean squared-return units per asset, averaged within each seed over two worlds and four origins before aggregating the 128 disclosed seed blocks.", "",
        "| Component | Mean risk |", "| --- | ---: |",
    ]
    for name, label in (("future", "Unpredictable future innovation"), ("within_type", "Current-state uncertainty within a type"),
                        ("type_information", "Remaining uncertainty about type"), ("bayes", "Total same-information Bayes risk"),
                        ("projected_excess", "Projection's excess above Bayes"), ("frozen_excess", "Frozen weights' excess above Bayes"),
                        ("projected_total", "Total projection risk"), ("category_oracle", "Posterior-averaged category-oracle risk")):
        rows.append(f"| {label} | {values[name]['mean']:.12f} |")
    rows += ["", "| Conditional risk reduction | Ratio of means | Descriptive 95% interval |", "| --- | ---: | --- |"]
    for name, label in (("projection_improvement_fraction", "Retained versus projection"), ("frozen_improvement_fraction", "Retained versus frozen weights"), ("category_information_fraction", "Category oracle versus retained")):
        item = values[name]
        lo, hi = item["descriptive_ci95"]
        rows.append(f"| {label} | {100*item['ratio_of_means']:.5f}% | [{100*lo:.5f}%, {100*hi:.5f}%] |")
    rows += ["", "Intervals resample entire paired seed blocks 9,999 times with fixed seed 678901. They describe these disclosed histories under the assumed model; they are not a new confirmatory family, a reopened gate, or market-generalisation evidence. The conditional reductions above use different information sets for the category oracle, which is reported explicitly.", "",
             "## Why the original 5% target is infeasible here", "",
             f"The Gaussian projection's delayed conditional risk is {projection:.12f}. Future process noise alone contributes {floor:.12f}. Even a hypothetical predictor additionally told the exact current state, but not the future innovation, could improve that projection by at most **{100*ceiling:.5f}%** on this observed-history average. A 5% reduction would require risk {0.95*projection:.12f}, below the future-noise floor.", "",
             "This ceiling is model-conditional expected risk averaged over the reconstructed histories. It is not a bound on each realised sample loss or a statement that 5% gains are impossible in other data regimes. With the actual shared information, the exact-Bayes ceiling is much tighter: approximately 0.036% over projection.", "",
             "## Timing explains the identification–forecasting gap", "",
             "| Origin delay | Bayes risk | Type-information risk | Value of perfect type information | Projection excess |",
             "| --- | ---: | ---: | ---: | ---: |"]
    for delay, item in moderate["by_origin"].items():
        rows.append(f"| {delay} | {item['bayes']:.9f} | {item['type_information']:.9f} | {100*item['type_information']/item['bayes']:.5f}% | {item['projected_excess']:.9f} |")
    rows += ["", "At the event origin, knowing the category would have substantial value, but the paired observed prefixes are identical and ordinary methods cannot identify it yet. Once subsequent observations arrive, type inference improves while current-state measurements already determine nearly the same next-return forecast. Remaining category uncertainty then has little predictive value. This explains why a strong historical type score need not imply a useful next-return MSE gain.", "",
             "## Verification and provenance", "",
             f"All five forecast-arm paths, state probabilities and normalized log-probabilities matched the actual frozen v2 implementation numerically exactly. Every saved v2 CSV metric reproduced with maximum absolute error **{moderate['max_frozen_metric_error']:.3g}**. The decomposition's maximum arithmetic residual was **{moderate['max_decomposition_identity_error']:.3g}**. The zero-persistence control retains risk .01 and has zero state/type/approximation headroom.", "",
             f"The replay loaded source from commit `{summary['frozen_commit']}` and verified its simulator/benchmark dependencies. Instrumented execution tree: `{summary['source_tree_at_run']}`. Frozen CSV canonical-text SHA256 hashes are saved in the summary; the old artifacts remain unchanged. The suite passes 53 tests.", "",
             "A post-run metadata wording correction renamed equality flags from `bitwise_equal` to `exactly_equal`, matching the actual `numpy.array_equal` check. The summary records that correction and the pre-correction hash. No numeric risk, score, prediction or original artifact changed; exact numerical equality does not claim byte-level equality of NaN payloads or signed zero.", "",
             "## Scope and next experiment", "",
             "These are known-time, known-parameter, single-Gaussian-event results. They establish neither operational detection nor financial usefulness, novelty or robust transfer. Posterior-averaged oracle risk integrates over the current category posterior; actual true-category realised losses are not samplewise lower bounds. Simply subtracting .01 from observed MSE would not yield this decomposition, which also integrates latent-state uncertainty.", "",
             "Do not enlarge the architecture to recover a missing 5% gain in this regime. The most efficient next experiment is an explicitly declared oracle-headroom map over externally justified measurement-noise regimes, with all cells reported. Keep dynamics and the noise floor controlled, then measure whether delayed same-information headroom becomes practically material before building another predictor. Synthetic favourable cells would establish possibility under their assumptions, not that markets occupy those cells. A new model chosen from that map needs fresh final data.", "",
             "## Artifacts", "",
             "- [Exploratory plan](conditional-risk-plan.md)",
             "- [Derivation](conditional-risk-mathematics.md)",
             "- [Audit plan](conditional-risk-audit-plan.md)",
             "- [Statistical review](conditional-risk-statistical-review.md)",
             "- [Engineering review](conditional-risk-engineering-review.md)",
             "- [Interpretation](conditional-risk-interpretation.md)",
             "- [Full summary](../results/conditional-risk-v2/summary.json)",
             "- [Moderate per-origin risks](../results/conditional-risk-v2/moderate.csv)",
             "- [Zero-control per-origin risks](../results/conditional-risk-v2/zero.csv)", "",
             "Run `python -m ripplenet.risk_report` to regenerate this document. Reconstructing into another directory is possible with `python -m ripplenet.risk_reconstruction --output work/risk-reproduction`; it repeats disclosed histories, not a fresh test. Existing directories are protected from overwrite. No paid resources were started.", ""]
    return "\n".join(rows)


if __name__ == "__main__":
    target = Path("docs/conditional-risk-results.md")
    target.write_text(render(), encoding="utf-8")
    print(target)
