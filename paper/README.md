# Research manuscript

[Read the research-paper PDF](RippleNet_research_report.pdf). The editable source is [research-paper.md](../docs/research-paper.md), with a separate [conclusion](../docs/conclusion.md).

The manuscript synthesizes the existing pilot; it adds no experiment or fit. It is an AI-assisted research draft, not an externally peer-reviewed publication. Source-specific attribution and publication conditions are explained in Section 8; no blanket data or manuscript license is asserted.

## Rebuild

Run `python tools/build_research_paper.py` from the repository root with ReportLab and pypdf installed. The builder embeds Windows Times New Roman when available, otherwise Linux DejaVu Serif. It reads only the public aggregate manuscript. A different runtime or fonts may change pagination and PDF bytes.

`build-metadata.json` records the manuscript and PDF SHA256 hashes, page count and build versions. PDF bytes include generation metadata, so a rebuild need not have an identical PDF hash. This is an export record, not a new experimental commitment.

## Checks for this export

- Scientific, mathematical and numeric synthesis checked by AI subagents against the stage reports; requested corrections incorporated. See [internal scientific review](../docs/manuscript-scientific-review.md).
- All ten pages rendered with Poppler and visually inspected. After correcting the appendix heading placement, the changed pages were rendered and inspected again; the remaining seven page images were byte-identical.
- Source and extracted PDF text checked for the expected sections, seven equation numbers, six numbered results tables and the appendix evidence table. Links preserve the cited evidence snapshot.
- No raw vendor records, fitted private parameters or per-origin predictions are included. Existing software tests are reported as implementation evidence, not newly run for this document export.
