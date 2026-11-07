# Private fitted-selection commitment before protected test

The [frozen plan](quote-study-plan.md) was published as `6993f9a12311d759b8e5d3370fcac8dc2ade6ed7`. Executable source was published as `45684955d4ab62e558c9d79992b2ff612e23ca5e`, tree `9ea90338d151a52f6242a5c3a75c427c5d8a261f`, before development prices were parsed. The full suite passed 118 tests, including ten new quote-study fixtures.

Training used only the six June–November 2025 sessions; validation used only December 2025–February 2026. Both target-specific fitted pipelines, preprocessing, constants, weighted medians and validation selections were saved privately. No validation refit occurred. The protected March 1, April 1 and May 1, 2026 records have not yet been parsed or scored by this study at this commitment.

The private selection artifact SHA256 is:

`9bf603799dcdb57e08aabed70c15e43b7c625d00b4ec428c5fc92989b2353a61`

This publication contains no fitted parameters or model-bearing configuration. The source terms restrict public trained-model weights; the artifact stays outside the public repository. Test execution must match this exact hash, executable hashes, acquisition-manifest hash and protected date list before loading test records. It must not refit. Publish only eligible aggregate results after evaluation; this commitment itself is not a performance result.
