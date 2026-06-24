# Modeling Readiness Audit

## 1. Single-Feature Feasibility (The "Too Easy" Test)

*Goal: Ensure no single synthetic feature perfectly predicts the target, which would indicate generative coupling.*

* **Temperature Only AUC:** [Pending]
* **ECC Only AUC:** [Pending]
* **GPU Util Only AUC:** [Pending]
* **Network State Only AUC:** [Pending]

## 2. Feature Ablation (The "Value Add" Test)

*Goal: Prove that the synthetic hardware signals actually improve prediction over raw utilization data alone.*

* **Raw Features Only (GPU, CPU, Mem):** [Pending]
* **Synthetic Features Only (Temp, ECC, Network):** [Pending]
* **Combined Dataset:** [Pending]

## 3. Temporal Split (The "Reality" Test)

*Goal: Prevent inflated metrics from random shuffling by enforcing a strict time-series split.*

* **Train:** Minutes 0–1400
* **Validation:** Minutes 1401–1700
* **Test:** Minutes 1701–2000
