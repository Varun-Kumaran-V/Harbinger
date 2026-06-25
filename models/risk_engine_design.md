# Latent Risk Engine Architecture (Phase 3C.5)

## 1. The Core Problem: Generative Coupling

Previous synthetic datasets suffered from target leakage because the `warning_window` deterministically forced high hardware load. The model learned to predict the simulation rules rather than failure risk, resulting in artificial 1.000 AUC scores.

## 2. Causal Inversion

To solve this, Harbinger introduces a Hidden Latent Risk Engine.
**New Pipeline:** `System Load -> Latent Risk Score -> Stochastic Failure Event -> Retrospective Warning Label`

## 3. Risk Engine Mechanics

A hidden variable, `latent_risk_score` $\in [0, 1]$, is calculated every minute. It is **never** exposed to the training dataset.

**Latent Risk Formula:**

* **Base Risk:** $0.0001$ (background noise)
* **Load Stress:** Scales non-linearly with GPU/Memory. High load increases risk, but *does not guarantee* failure.
* **Thermal Penalty:** Added risk if temperature exceeds 85°C.
* **Hardware Fault:** Massive risk spike if an `ecc_event` occurs.

## 4. Failure Trigger & Labeling

* **Trigger:** Every minute, $rand() < latent\_risk\_score$. If true, the node crashes.
* **Labeling:** Only *after* the timeline finishes, the simulator looks at crash timestamps ($T_f$) and retroactively applies `warning_window = 1` to the preceding 180 minutes.

This ensures the dataset contains instances of healthy 99% GPU utilization, and instances of failure at 50% utilization (due to random ECC hardware faults), forcing the model to learn interactions.
