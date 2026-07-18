# Harbinger

**Harbinger** is a decision-oriented AI infrastructure management framework that combines synthetic infrastructure simulation, machine learning, and operational cost optimization to predict failures and recommend economically optimal interventions for distributed GPU training clusters.

Unlike conventional predictive maintenance systems that stop after estimating the probability of failure, Harbinger extends the pipeline by estimating recovery impact, intervention cost, and recommending the operational action that minimizes expected cost.

---

# Repository Overview

Harbinger is organized as a complete research pipeline consisting of five interconnected subsystems:

1. **Synthetic Signal Generation**

   - Generates realistic infrastructure telemetry including temperature, ECC activity, network behaviour, and checkpoint events.
2. **Dataset Construction & Feature Engineering**

   - Integrates synthetic signals into structured datasets suitable for machine learning.
3. **Baseline Validation**

   - Establishes conventional machine learning benchmarks for scientific comparison.
4. **Decision Engine**

   - Combines prediction outputs with recovery and intervention cost models to recommend economically optimal operational actions.
5. **Evaluation & Reporting**

   - Measures operational effectiveness using metrics such as recovery loss, GPU-hours saved, and total operational cost.

---

# Repository Architecture

```
Synthetic Signal Generation
            │
            ▼
Dataset Construction
            │
            ▼
Feature Engineering
            │
            ▼
Baseline Validation
            │
            ▼
Decision Engine
            │
            ▼
Operational Evaluation
```

---

# Repository Structure

```
Harbinger
│
├── backend/
│   ├── generators/
│   ├── build_training_dataset.py
│   ├── engineer_and_audit.py
│   ├── baseline_audit.py
│   ├── tune_baselines.py
│   ├── harbinger_pipeline.py
│   ├── recovery_engine.py
│   ├── intervention_cost_model.py
│   ├── evaluate_harbinger.py
│   └── learnability_audit.py
│
├── data/
│   ├── processed/
│   └── trace-data/
│
├── docs/
│   ├── architecture.md
│   ├── reproducibility.md
│   ├── datasets/
│   └── modules/
│
├── models/
├── outputs/
└── tests/
```

---

# Execution Pipeline

The repository follows a sequential workflow.

## 1. Generate the Synthetic Dataset

```bash
python backend/build_training_dataset.py
```

Produces:

- `training_dataset.csv`

---

## 2. Engineer Temporal Features

```bash
python backend/engineer_and_audit.py
```

Produces:

- `engineered_training_dataset.csv`

---

## 3. Validate Dataset Learnability

```bash
python backend/learnability_audit.py
```

Verifies that the generated dataset contains meaningful predictive patterns.

---

## 4. Evaluate Conventional Baselines

```bash
python backend/baseline_audit.py
```

Provides initial baseline performance.

---

## 5. Optimize Baseline Models

```bash
python backend/tune_baselines.py
```

Produces:

- `baseline_consolidation_report.md`

---

## 6. Execute the Decision Pipeline

```bash
python backend/harbinger_pipeline.py
```

Integrates:

- prediction
- recovery estimation
- intervention cost modelling
- operational decision making

---

## 7. Evaluate Harbinger

```bash
python backend/evaluate_harbinger.py
```

Produces:

- `evaluation_results.csv`
- `cluster_impact_summary.md`
- `recovery_loss_report.md`

---

# Documentation

The repository documentation is organized into three complementary sections.

## Architecture

High-level overview of the complete system.

```
docs/architecture.md
```

---

## Module Documentation

Detailed explanations of each subsystem.

```
docs/modules/

├── synthetic_signal_generation.md
├── dataset_construction.md
├── baseline_validation.md
├── decision_engine.md
└── evaluation_pipeline.md
```

---

## Dataset Documentation

Reference material describing generated signals, features, and schema.

```
docs/datasets/

├── feature_registry.csv
├── feature_taxonomy.md
├── schema_dictionary.csv
├── signal_coverage_matrix.csv
└── synthetic_signal_design.md
```

---

## Model Design Documents

Design specifications for the prediction and decision components.

```
models/

├── prediction_design.md
├── risk_engine_design.md
├── training_dataset_design.md
└── modeling_readiness.md
```

---

# Outputs

Example generated artifacts are stored in:

```
outputs/
```

These include:

- evaluation reports
- baseline summaries
- generated datasets
- plots
- sample outputs

---

# Research Contribution

Traditional failure prediction systems answer:

> **Will a failure occur?**

Harbinger addresses the broader operational question:

> **Given the probability of failure, the expected recovery loss, and the cost of intervention, what action minimizes the total operational cost?**

This shift from prediction to decision optimization forms the central contribution of the project.

---

# Reproducibility

The repository generates synthetic infrastructure telemetry and datasets internally.

The complete workflow for reproducing the datasets, baseline experiments, and evaluation pipeline is documented in:

```
docs/reproducibility.md
```

---

# License

This project is distributed under the terms of the MIT License.

See the `LICENSE` file for details.
