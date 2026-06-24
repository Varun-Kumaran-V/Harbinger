# Training Dataset Specification

## 1. Unit of Prediction

**Sample Level:** One Minute.
**Rationale:** All telemetry in the Philly dataset and all our synthetic generators operate at a per-minute granularity. A minute-level prediction allows the model to act as a continuous streaming inference engine in a live cluster.

## 2. Label Assignment

**Strategy:** Fixed Pre-Failure Horizon.

* For a job that fails at minute $T_f$:
* Rows where $t < (T_f - 180)$ are labeled `warning_window = 0`
* Rows where $(T_f - 180) \le t \le T_f$ are labeled `warning_window = 1`

## 3. Class Balance

**Expected Distribution:** Highly Imbalanced.

* Given a typical 2000-minute job with a 180-minute warning horizon, the positive class represents ~9.0% of the dataset.
* This imbalance is operationally realistic and will dictate our model evaluation metrics (e.g., F1-score and PR-AUC instead of standard Accuracy).

## 4. Strict Feature Isolation (Anti-Leakage)

* **Features ($X$):** `gpu_util`, `cpu_util`, `mem_pressure`, `temperature`, `ecc_event`, `network_state`, `throughput_factor`, `recovery_loss_potential`
* **Target ($y$):** `warning_window`
* **Forbidden:** `warning_window` must strictly be dropped from the feature matrix before any `model.fit()` or `model.predict()` operation.
