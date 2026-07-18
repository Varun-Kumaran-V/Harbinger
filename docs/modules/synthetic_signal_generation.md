
# Synthetic Signal Generation Module

## Module Overview

The **Synthetic Signal Generation Module** is responsible for producing realistic infrastructure telemetry that mimics the behavior of GPUs, compute nodes, and distributed AI training jobs. These signals are not collected from a real cluster; instead, they are generated using deterministic and probabilistic models that represent how modern GPU clusters behave under normal operation and as failures begin to develop.

The outputs of this module serve two purposes:

1. **Generate the synthetic training dataset** used to train and evaluate Harbinger.
2. **Produce standalone visualizations and CSV files** that validate each signal model individually.

This subsystem executes **offline** during research and experimentation. It is **not part of the runtime prediction pipeline**. Once the synthetic dataset has been created, the generators are no longer required during inference.

---

# Why This Module Exists

Obtaining large-scale GPU failure logs is difficult because:

- Most organizations do not publish infrastructure telemetry.
- Production cluster logs often contain confidential information.
- Hardware failures are relatively rare events, making balanced datasets difficult to obtain.
- Collecting months of telemetry would significantly delay research.

To overcome these challenges, Harbinger generates synthetic infrastructure signals that follow realistic operational patterns. These signals provide a controlled, reproducible environment for developing and evaluating the prediction system.

---

# Position in the Overall Architecture

```
Checkpoint Generator
ECC Generator
Network Generator
Temperature Generator
          │
          ▼
build_training_dataset.py
          │
          ▼
training_dataset.csv
          │
          ▼
Entire Harbinger Pipeline
```

The generators **do not interact directly with the prediction model**.

Instead, they provide the raw telemetry required to build the synthetic dataset.

---

# File 1 — checkpoint_generator.py

## Purpose

Simulates checkpoint scheduling during AI training.

A checkpoint represents a saved copy of the model's state so that training can resume after a failure without starting from the beginning.

---

## Why It Exists

Suppose a GPU fails after eight hours of training.

If the last checkpoint was saved one hour earlier, only one hour of work is lost.

If the last checkpoint was saved six hours earlier, six hours of work must be repeated.

Checkpoint frequency therefore has a direct impact on recovery cost.

This generator models that relationship.

---

## Inputs

```
total_minutes
warning_start
```

- **total_minutes** – Total simulation duration.
- **warning_start** – Time when Harbinger predicts an elevated failure risk.

---

## Processing

The generator follows a **4-Layer Checkpoint Economic Model**.

### Layer 1

Determine the normal checkpoint interval based on job duration.

Longer jobs naturally checkpoint more frequently than shorter jobs.

---

### Layer 2

Monitor whether the simulation has entered the warning window.

---

### Layer 3

If a warning window exists:

Checkpoint interval decreases.

Example:

```
Normal operation

Checkpoint every 2 hours

↓

Warning window

Checkpoint every 30 minutes
```

---

### Layer 4

Calculate recovery loss.

Recovery Loss =

```
Failure Time

−

Last Checkpoint Time
```

---

## Outputs

### checkpoint_sample.csv

Contains every checkpoint event.

Important columns include:

- checkpoint time
- interval
- recovery loss

---

### checkpoint_plot.png

Shows checkpoint timing over the simulation.

### X-axis

Simulation time.

### Y-axis

Checkpoint progression.

### Interpretation

Widely spaced checkpoints indicate normal operation.

Closely spaced checkpoints indicate adaptive protection.

### Conclusion

The graph demonstrates that Harbinger reduces expected recovery loss by increasing checkpoint frequency before anticipated failures.

---

## Consumer

```
build_training_dataset.py
```

The generated checkpoint signal becomes one column within the synthetic training dataset.

---

## Important Terms

Checkpoint

A saved model state.

Recovery Loss

Training time lost after failure.

Checkpoint Interval

Time between consecutive checkpoints.

Warning Window

Time period immediately before a predicted failure.

---

## Presentation Notes

If someone asks:

"Why adaptive checkpoints?"

Answer:

> Frequent checkpoints reduce recovery loss but increase overhead. Harbinger attempts to balance these competing costs by increasing checkpoint frequency only when failure probability becomes sufficiently high.

---

# File 2 — ecc_generator.py

## Purpose

Generates synthetic ECC (Error Correcting Code) memory errors.

ECC errors often appear before GPU hardware failures.

---

## Why It Exists

Memory faults are one of the strongest indicators of deteriorating GPU health.

Rather than using random errors, this model attempts to simulate realistic error escalation.

---

## Inputs

Internally generated:

- GPU utilization
- Memory pressure
- Previous ECC activity
- Warning window

---

## Processing

Uses a **5-Layer ECC Probability Model**.

### Layer 1

Compute hardware stress.

---

### Layer 2

Generate background ECC noise.

Healthy hardware occasionally experiences isolated ECC events.

---

### Layer 3

Increase ECC probability as stress rises.

---

### Layer 4

Within the warning window,

ECC activity increases sharply.

---

### Layer 5

Burst persistence.

Recent ECC events increase the probability of subsequent ECC events.

---

## Outputs

### ecc_sample_output.csv

Contains simulated ECC counts.

---

### ecc_plot.png

Visualizes ECC activity over time.

### X-axis

Simulation time.

### Y-axis

ECC event count.

### Interpretation

Small isolated spikes represent normal background errors.

Clusters of increasing errors indicate hardware deterioration.

### Conclusion

The graph demonstrates that failures are usually preceded by increasing ECC activity rather than occurring completely randomly.

---

## Consumer

```
build_training_dataset.py
```

---

## Important Terms

ECC

Error Correcting Code memory.

Burst Persistence

ECC events occurring close together.

Stress Score

Estimated hardware stress.

---

## Presentation Notes

ECC events are not deterministic predictors.

Instead,

Harbinger learns that sustained increases in ECC activity often precede failures.

---

# File 3 — network_generator.py

## Purpose

Simulates network degradation during distributed AI training.

---

## Why It Exists

Distributed training depends on communication between multiple GPUs.

Network degradation reduces effective throughput even when GPU utilization remains high.

---

## Inputs

```
total_minutes
```

---

## Processing

Uses a **3-LLayer Markov Network Model**.

### Layer 1

Current network state.

States:

Healthy

↓

Degraded

↓

Severe

---

### Layer 2

Markov transition.

Each minute,

the next network state is selected probabilistically.

---

### Layer 3

Throughput calculation.

Each network state has an impact factor.

Example:

Healthy

100%

↓

Degraded

85%

↓

Severe

60%

---

## Outputs

### network_sample.csv

Network state for every simulated minute.

---

### network_plot.png

Shows throughput degradation.

### X-axis

Simulation time.

### Y-axis

GPU throughput.

Gray line

Nominal throughput.

Blue line

Effective throughput.

Yellow region

Degraded network.

Red region

Severe degradation.

### Conclusion

The graph demonstrates that communication bottlenecks reduce useful training throughput even when GPUs remain busy.

---

## Consumer

```
build_training_dataset.py
```

---

## Important Terms

Markov Chain

Future state depends only on the current state.

Effective Throughput

Actual useful work completed.

Network State

Current communication quality.

---

## Presentation Notes

Network degradation is modeled probabilistically because communication quality fluctuates rather than changing deterministically.

---

# File 4 — temperature_generator.py

## Purpose

Generates synthetic GPU temperatures.

---

## Why It Exists

Temperature is one of the most common indicators of hardware stress.

High utilization generally produces higher temperatures.

---

## Inputs

```
GPU utilization

CPU utilization

Memory pressure
```

---

## Processing

Uses a **Physics-Inspired Heuristic Model**.

Estimated temperature is calculated as:

Base temperature

GPU contribution

CPU contribution

Memory contribution

Small random thermal noise.

---

## Outputs

### sample_output.csv

Estimated temperatures.

---

### temperature_plot.png

Scatter plot of GPU utilization versus estimated temperature.

### X-axis

GPU utilization.

### Y-axis

Estimated GPU temperature.

### Interpretation

Higher GPU utilization generally corresponds to higher temperatures.

Small scatter reflects natural environmental variation.

### Conclusion

The graph demonstrates that thermal behavior follows expected physical trends rather than remaining constant.

---

## Consumer

```
build_training_dataset.py
```

---

## Important Terms

Thermal Noise

Small random environmental variation.

Base Temperature

Idle operating temperature.

Heuristic Model

Rule-based approximation rather than a learned model.

---

## Presentation Notes

The model is intentionally simple because temperature is only one signal among many. Harbinger combines it with utilization, ECC activity, checkpoint behavior, and network health instead of relying on temperature alone.

---

# Overall Module Summary

The Synthetic Signal Generation subsystem does **not** make predictions.

Its responsibility is to generate realistic infrastructure telemetry that can be fused into a complete synthetic dataset.

Each generator models a different aspect of cluster behavior:

- **checkpoint_generator.py** models recoverability and checkpoint economics.
- **ecc_generator.py** models memory reliability and error escalation.
- **network_generator.py** models communication quality and throughput degradation.
- **temperature_generator.py** models thermal behavior under system load.

Together, these signals are consumed by `build_training_dataset.py`, which integrates them into `training_dataset.csv`. That dataset becomes the foundation for feature engineering, baseline validation, model training, and evaluation throughout the remainder of the Harbinger pipeline.
