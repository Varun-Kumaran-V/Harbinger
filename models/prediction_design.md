# Prediction Architecture Design

## 1. Prediction Objective

**Target:** `warning_window` (Binary: 1 = Impending Failure, 0 = Healthy/Normal)
**Rationale:** Predicting the exact minute of a failure is practically impossible and operationally unnecessary. Instead, Harbinger predicts whether a node has entered a high-risk "warning window" preceding a known failure, enabling preemptive mitigation before the crash occurs.

## 2. Prediction Horizon

**Horizon:** 1 to 3 hours prior to failure.
**Rationale:** This provides sufficient lead time to execute mitigation actions (e.g., triggering an out-of-band checkpoint, migrating the job) without acting so early that false positives dominate and waste cluster resources.

## 3. Label Generation Logic

**Rule:** For any job in the Philly log where `status == "Failed"` or `"Killed"`:

* Let $T_f$ be the timestamp of failure.
* The label `warning_window = 1` is applied to all records where $T_f - 180 \le t \le T_f$.
* All other records are labeled `warning_window = 0`.

## 4. Feature Mapping (Inputs)

Derived from the Feature Registry, these signals feed the prediction model:

* `gpu_util` (Continuous)
* `cpu_util` (Continuous)
* `mem_pressure` (Continuous)
* `temperature` (Continuous)
* `ecc_event` (Binary/Count)
* `network_state` (Categorical)

## 5. Evaluation Metrics

Standard ML metrics (like Accuracy) are insufficient for operational intelligence. Harbinger will evaluate:

* **Precision/Recall (F1):** To measure base model separability on an imbalanced dataset.
* **Lead Time:** Average minutes of warning provided before the actual failure occurs.
* **False Positive Cost:** The penalty (in wasted operational time) of triggering unnecessary mitigations based on false alarms.
