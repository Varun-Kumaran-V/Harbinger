# Harbinger Feature Taxonomy

This document defines the formal contract between the data layer and the modeling layer. It categorizes how each signal is utilized across the Prediction, Impact, and Decision phases of Harbinger.

## 1. Prediction Features
**Core Question:** *Will a failure occur?*
These features feed directly into the failure-risk model to estimate the probability of an impending fault.
* **`gpu_util`**: Volumetric load on the GPU.
* **`cpu_util`**: Volumetric load on the CPU.
* **`mem_pressure`**: Memory allocation stress.
* **`temperature`**: Thermal stress proxy.
* **`ecc_event`**: Hardware instability burst marker.
* **`network_state`**: System connectivity health.
* **`warning_window`**: Pre-failure cascade indicator (Label/Target).

## 2. Impact Features
**Core Question:** *How bad would the failure be if we do nothing?*
These features calculate the economic exposure and wasted compute.
* **`last_checkpoint_time`**: The anchor for recovery calculations.
* **`recovery_loss_potential`**: The minutes of un-saved training progress.
* **`throughput_factor`**: The performance penalty active during network degradation.
* **`gpu_count`**: The hardware multiplier for converting time into total GPU-hours lost.

## 3. Decision Features
**Core Question:** *What should we do?*
These features combine risk and impact to output a recommended mitigation action.
* **`failure_probability`**: Output from the prediction model.
* **`impact_score`**: Output from the impact estimator (Wasted GPU-Hours).
* **`checkpoint_interval`**: The tunable mitigation lever.
* **`mitigation_cost`**: The operational cost of taking action (e.g., pausing to checkpoint).