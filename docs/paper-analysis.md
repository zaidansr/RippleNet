# Selected paper: CE-BASS

Selected for relevance; no paper was specified. Source: Fisch, Eckley and Fearnhead, [CE-BASS paper](https://arxiv.org/pdf/2007.03238), July 2020 preprint; full text inspected.

1. **Question:** Robust filtering with both observation and process outliers, including delayed visibility (Section 1).
2. **Framework:** Linear state-space dynamics; separate observation/process variance inflations and anomaly indicators (Section 2).
3. **Architecture:** Rao–Blackwellised particle-mixture Kalman filtering, specialised proposals and back-sampling (Sections 3–4).
4. **Data:** Simulations, NAB machine temperatures, and router throughput (Sections 5–6).
5. **Design:** Four simulated models, 1,000 observations each, four anomaly regimes; predictive log-likelihood and MSE comparisons. Anomaly observations and selected following observations are excluded from scoring (Section 5).
6. **Results:** Authors report favourable simulated comparisons and detection of labelled machine anomalies; additional detections remain uncertain (Sections 5–6).
7. **Limitations:** The model restricts simultaneous anomalies; router evaluation lacks labels. These demonstrations do not establish financial forecasting performance.
8. **RippleNet relevance — our interpretation:** A necessary related-method comparison. Disturbance separation alone cannot establish novelty. Its scoring exclusions differ materially from our event-window objective.

No precise effect size is asserted. No equations are reconstructed from imperfect PDF extraction.
