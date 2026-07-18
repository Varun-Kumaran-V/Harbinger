
# Synthetic Signal Design

## Overview

Harbinger generates synthetic infrastructure telemetry to construct a reproducible training environment for failure prediction and operational decision optimization.

Each signal models a different aspect of distributed GPU cluster behaviour. Together, these signals form the foundation of the synthetic training dataset used throughout the repository.

---

# Temperature Signal

## Inputs

- GPU Utilization
- CPU Utilization
- Memory Pressure

## Output

Estimated GPU Temperature (°C)

## Design Rationale

Temperature is one of the strongest indicators of hardware stress. Since real-world hardware telemetry is generally unavailable in public datasets, Harbinger estimates thermally plausible temperatures from resource utilization patterns.

---

# ECC Signal

## Inputs

- GPU Utilization
- Memory Pressure
- Previous ECC Activity
- Warning Window

## Output

ECC Event Count

## Design Rationale

ECC errors frequently increase before hardware failures. The synthetic model generates realistic escalation behaviour while preserving temporal consistency across the simulation.

---

# Network Signal

## Inputs

- Simulation Timeline

## Output

Network State

Throughput Factor

## Design Rationale

Distributed AI training depends heavily on communication between compute nodes. The network model simulates probabilistic degradation using discrete operating states to represent changing communication quality.

---

# Checkpoint Signal

## Inputs

- Simulation Timeline
- Warning Window

## Output

Checkpoint Events

Recovery Loss

## Design Rationale

Checkpoint scheduling directly affects recovery cost after failures. Harbinger models adaptive checkpoint intervals to balance checkpoint overhead against expected recovery loss.

---

# Design Principles

The synthetic generators follow four principles:

1. Internal consistency across all generated signals.
2. Temporal evolution rather than independent random samples.
3. Reproducibility through deterministic simulation.
4. Support for downstream prediction, impact estimation, and operational decision optimization.

Together, these generators provide a complete synthetic infrastructure environment for developing and evaluating Harbinger.
