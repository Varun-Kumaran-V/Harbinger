
# Harbinger

Predict failure risk in AI training clusters, estimate operational impact before failure occurs, and recommend the lowest-cost mitigation action to reduce wasted compute and training disruption.

## Idea

Harbinger is a predictive reliability intelligence system for AI training clusters.

The goal is to identify jobs, nodes, or GPUs that are likely to fail, estimate the expected impact, and recommend the best mitigation action before compute resources are wasted.

## Current Status

**Phase 3A – Prediction Architecture Design**

## Architecture Overview

Harbinger bridges the gap between raw cluster telemetry and operational decision-making through a multi-stage pipeline:

1. **Data & Signal Layer:** Real telemetry (Philly trace) augmented with a mathematically rigorous synthetic hardware fault layer (Temperature, ECC, Network, Checkpoints).
2. **Prediction Layer:** Forecasts the probability of an impending failure warning window.
3. **Impact Layer:** Estimates the economic exposure (wasted GPU-hours) based on checkpoint timestamps.
4. **Decision Layer:** Recommends cost-aware mitigation actions.

## Completed Milestones

* [X] **Phase 0:** Problem Lock and Repo Setup
* [X] **Phase 1:** Data Acquisition, Signal Verification and Feasibility Analysis (Microsoft Philly)
* [X] **Phase 2A:** Hardware Fault Simulation (Temperature & ECC Errors)
* [X] **Phase 2B:** Economic & Performance Simulation (Checkpoints & Network Degradation)
* [X] **Phase 2C:** Feature Registry & Taxonomy (Separating Prediction, Impact, and Decision features)

## Roadmap

- [X] Phase 0 – Problem Lock and Repo Setup
- [X] Phase 1 – Data Acquisition, Signal Verification and Feasibility Analysis
- [X] Phase 2 – Failure Scenario Modeling and Label Generation
- [ ] Phase 3 – Failure-Risk Prediction Model
- [ ] Phase 4 – Impact Estimation Module
- [ ] Phase 5 – Decision Intelligence Engine
- [ ] Phase 6 – End-to-End Simulation Harness
- [ ] Phase 7 – Backend API
- [ ] Phase 8 – Dashboard
- [ ] Phase 9 – Evaluation and Paper Writing
