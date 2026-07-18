# Harbinger Architecture & Execution Pipeline

## Repository Purpose

Harbinger is a decision-oriented framework for predicting failures in distributed GPU training clusters and recommending economically optimal interventions.

Unlike conventional predictive maintenance systems that stop after estimating failure probability, Harbinger continues by estimating operational consequences and selecting the action that minimizes expected operational cost.

---

# Complete Repository Architecture

```
                    OFFLINE RESEARCH PIPELINE
══════════════════════════════════════════════════════════════════════

                 Synthetic Signal Generation
──────────────────────────────────────────────────────────────────────

 checkpoint_generator.py
 ecc_generator.py
 network_generator.py
 temperature_generator.py

                 │
                 ▼

          build_training_dataset.py

                 │
                 ▼

         training_dataset.csv

                 │
        ┌────────┴────────┐
        │                 │
        ▼                 ▼

learnability_audit.py   engineer_and_audit.py

                          │
                          ▼

          engineered_training_dataset.csv

                          │
             ┌────────────┴─────────────┐
             │                          │
             ▼                          ▼

      baseline_audit.py         tune_baselines.py

                                      │
                                      ▼

                    baseline_consolidation_report.md

══════════════════════════════════════════════════════════════════════

                     ONLINE DECISION PIPELINE
══════════════════════════════════════════════════════════════════════

                 Live Cluster Telemetry

                          │
                          ▼

                  Prediction Adapter

                          │
                          ▼

                 Failure Probability

                          │
                          ▼

                  Decision Engine

                          │
                          ▼

                 Recovery Engine

                          │
                          ▼

            Intervention Cost Model

                          │
                          ▼

             Recommended Operator Action

══════════════════════════════════════════════════════════════════════

                  EXPERIMENTAL EVALUATION
══════════════════════════════════════════════════════════════════════

               evaluate_harbinger.py

                          │
             ┌────────────┼──────────────┐
             │            │              │
             ▼            ▼              ▼

evaluation_results.csv

cluster_impact_summary.md

recovery_loss_report.md
```

---

# Understanding Harbinger

The repository is divided into **two completely different pipelines**.

Many people confuse these.

---

# Pipeline 1 — Offline Research Pipeline

Purpose

Develop Harbinger.

Generate data.

Train models.

Evaluate methods.

Everything from

```
checkpoint_generator.py
```

through

```
tune_baselines.py
```

belongs here.

This pipeline is executed during development.

It is **never executed on a production cluster.**

---

# Pipeline 2 — Runtime Decision Pipeline

Purpose

Make operational decisions.

During deployment,

Harbinger receives

```
Live GPU telemetry
```

not synthetic telemetry.

The runtime pipeline begins at

```
Prediction Adapter
```

and ends with

```
Recommended Action
```

---

# Where Synthetic Generators Fit

This is probably the most misunderstood part of the repository.

The generators

DO NOT

predict failures.

They

DO NOT

make decisions.

They

DO NOT

run during deployment.

Instead,

they provide the synthetic infrastructure signals required to create the training dataset.

Think of them as

```
Laboratory Equipment
```

rather than

```
Production Software.
```

Once

```
training_dataset.csv
```

has been created,

their job is finished.

---

# Data Flow

Raw Infrastructure Behaviour

↓

Synthetic Signals

↓

Training Dataset

↓

Engineered Dataset

↓

Prediction Model

↓

Failure Probability

↓

Decision Engine

↓

Recovery Analysis

↓

Cost Optimization

↓

Recommended Action

↓

Evaluation

---

# Complete File Dependency

```
checkpoint_generator.py
ecc_generator.py
network_generator.py
temperature_generator.py
                │
                ▼
build_training_dataset.py
                │
                ▼
training_dataset.csv
        ┌───────┴────────┐
        │                │
        ▼                ▼
learnability_audit.py engineer_and_audit.py
                         │
                         ▼
engineered_training_dataset.csv
         ┌───────────────┴────────────────┐
         │                                │
         ▼                                ▼
baseline_audit.py              tune_baselines.py
                                         │
                                         ▼
                         baseline_consolidation_report.md

engineered_training_dataset.csv
                │
                ▼
harbinger_pipeline.py
                │
                ▼
recovery_engine.py
                │
                ▼
intervention_cost_model.py
                │
                ▼
evaluate_harbinger.py
```

---

# Research Contribution

Harbinger does **not** claim

"We built another failure predictor."

Instead,

its contribution is

```
Prediction

↓

Economic Decision Optimization
```

Most existing systems answer

```
Will failure occur?
```

Harbinger answers

```
Should intervention occur?
```

Those are fundamentally different research questions.

---

# Why Every Module Exists

Synthetic Signal Generation

↓

Create reproducible infrastructure behaviour.

Dataset Construction

↓

Convert signals into structured observations.

Feature Engineering

↓

Transform telemetry into informative ML features.

Baseline Validation

↓

Establish fair comparison models.

Decision Engine

↓

Convert predictions into actions.

Evaluation

↓

Measure operational benefit.

---

# Repository Philosophy

Harbinger follows one simple philosophy.

Prediction alone does not reduce downtime.

Only

Prediction

Operational Decision

reduces wasted computation.

Everything in the repository ultimately supports this objective.

---

# Reading Order

A new developer should read the repository in this order.

README.md

↓

architecture.md

↓

execution_pipeline.md

↓

Synthetic Signal Generation Module

↓

Dataset Construction Module

↓

Baseline Validation Module

↓

Decision Engine Module

↓

Evaluation Module

↓

Research Design Documents

↓

Individual Python files

This progression moves from high-level concepts to implementation details, making the repository much easier to understand than starting directly with source code.

---

# Questions Every Contributor Should Be Able to Answer

After reading the documentation, a contributor should be able to explain:

- Why synthetic data is used instead of production telemetry.
- Why two datasets (`training_dataset.csv` and `engineered_training_dataset.csv`) exist.
- Why feature engineering is necessary.
- Why baseline models are evaluated before Harbinger.
- Why Harbinger optimizes operational cost rather than prediction accuracy.
- Why recovery loss is measured in GPU-hours.
- Why intervention cost must be considered alongside failure probability.
- How the runtime pipeline differs from the research pipeline.
- Which files generate data, which files transform data, which files make decisions, and which files evaluate the system.

If someone can answer those questions, they understand not only how Harbinger is implemented, but also why it was designed the way it was.
