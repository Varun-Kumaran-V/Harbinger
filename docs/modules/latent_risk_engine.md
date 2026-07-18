# Latent Risk Engine Desi

## 1. The Core Problem: Generative Coupling

Earlier iterations of the synthetic dataset suffered from target leakage because the warning labels were too strongly coupled to the generated infrastructure signals. As a result, machine learning models learned the simulation rules rather than meaningful failure patterns, producing unrealistically high predictive performance.

## 2. Latent Risk Framework

To solve this, Harbinger introduces a Hidden Latent Risk Engine.
**New Pipeline:**

```text
Infrastructure Signals
        ↓
Latent Risk Score
        ↓
Stochastic Failure Event
        ↓
Warning Window Assignment
```

## 3. Risk Engine Mechanics

A hidden variable, `latent_risk_score` $\in [0, 1]$, is calculated every minute. It is **never** exposed to the training dataset.

**Latent Risk Formula:**

* **Base Risk:** $0.0001$ (background noise)
* **Load Stress:** Scales non-linearly with GPU/Memory. High load increases risk, but *does not guarantee* failure.
* **Thermal Penalty:** Added risk if temperature exceeds 85°C.
* **Hardware Fault:** Massive risk spike if an `ecc_event` occurs.

## 4. Failure Trigger & Labeling

* **Trigger:** At each simulation step, the latent risk score is interpreted as the probability of failure. A stochastic sampling process determines whether a failure occurs.
* **Labeling:** Once the complete simulation timeline has been generated, the simulator identifies each failure timestamp ($T_f$) and retrospectively assigns `warning_window = 1` to the preceding 180-minute prediction horizon.

This approach allows the dataset to contain instances of healthy high utilization alongside failures caused by independent hardware events (such as ECC faults), encouraging the prediction model to learn meaningful interactions rather than deterministic simulation rules.

## Design Rationale

The latent risk engine separates the hidden failure mechanism from the observable infrastructure telemetry. This prevents direct feature-label coupling while preserving realistic relationships between system behaviour and failure probability. As a result, the generated datasets provide a more challenging and representative environment for evaluating failure prediction and operational decision-making algorithms.
