# Evaluation & Reporting Module

## Module Overview

The **Evaluation & Reporting Module** is the final stage of the Harbinger pipeline.

All previous modules answer one of the following questions:

- Can realistic infrastructure data be generated?
- Can a useful dataset be constructed?
- Can failures be predicted?
- Can better operational decisions be made?

This subsystem answers the final question:

> **"Did Harbinger actually improve cluster operation?"**

Instead of evaluating only machine learning metrics, Harbinger evaluates **operational outcomes**.

This is an important distinction because a highly accurate model is not necessarily the most useful model in production.

---

# Why This Module Exists

Traditional ML projects usually stop after reporting:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC

However, cluster operators care about questions like:

- How much computation was saved?
- How many GPU-hours were recovered?
- How much operational cost was reduced?
- Was checkpointing actually worthwhile?

The Evaluation Module converts prediction performance into operational impact.

---

# Position in Overall Architecture

```
Decision Engine
        │
        ▼
evaluate_harbinger.py
        │
        ├──────────────► evaluation_results.csv
        ├──────────────► cluster_impact_summary.md
        └──────────────► recovery_loss_report.md
```

---

# File — evaluate_harbinger.py

## Purpose

Evaluates Harbinger's complete decision pipeline using simulated workloads and summarizes its operational effectiveness.

Unlike previous modules, this file does **not** build datasets or train models.

Instead, it measures how well the complete Harbinger framework performs.

---

# Why It Exists

Suppose Harbinger predicts failures correctly.

That alone does not prove usefulness.

The real questions become:

- Did checkpointing reduce recovery loss?
- Did interventions save GPU-hours?
- Was operational cost reduced?
- Was Harbinger better than static policies?

This module answers those questions.

---

# Inputs

Receives outputs from

```
harbinger_pipeline.py

recovery_engine.py

intervention_cost_model.py
```

along with simulated workloads.

---

# Processing

## Step 1

Execute the Harbinger pipeline.

Obtain

- prediction
- recovery loss
- intervention cost
- recommended action

---

## Step 2

Run multiple workload simulations.

Example

```
5000 jobs

varying

duration

GPU count

checkpoint intervals
```

---

## Step 3

Evaluate different policies.

Example

Static checkpoint policy

↓

Adaptive Harbinger policy

↓

Compare operational outcomes

---

## Step 4

Collect evaluation metrics.

Examples

GPU-hours saved

Recovery loss

Operational cost

Checkpoint overhead

Policy efficiency

---

## Step 5

Generate reports.

---

# Outputs

```
evaluation_results.csv

cluster_impact_summary.md

recovery_loss_report.md
```

---

# Why These Outputs Matter

These reports become the experimental evidence supporting the research paper.

Instead of claiming

"Harbinger is better"

the repository contains quantitative evidence explaining why.

---

# Generated Artifact

---

## evaluation_results.csv

### Purpose

Stores numerical evaluation results for every simulated workload.

---

### Typical Columns

Depending on implementation, examples include

- Job ID
- GPU Count
- Failure Probability
- Recovery Loss
- Intervention Cost
- Total Operational Cost
- Recommended Action

---

### Interpretation

Each row represents one simulated experiment.

Comparing rows allows researchers to evaluate how Harbinger behaves under different cluster conditions.

---

### Conclusions

This dataset provides the raw evidence used to compare different operational strategies.

---

# Generated Artifact

---

## cluster_impact_summary.md

### Purpose

Provides a human-readable summary of Harbinger's overall performance.

---

### Why Generate It?

CSV files are useful for analysis.

Markdown reports are useful for

- reviewers
- developers
- paper writing

---

### Typical Contents

Overall observations such as

- GPU-hours saved
- reduction in recovery loss
- policy comparisons
- operational improvements

---

### Interpretation

Rather than reading thousands of simulated experiments,

the summary highlights the important findings.

---

### Conclusions

This report is often the easiest place to understand whether Harbinger achieved its design goals.

---

# Generated Artifact

---

## recovery_loss_report.md

### Purpose

Explains how much training work would have been lost under different policies.

---

### Typical Contents

Examples

Checkpoint interval

↓

Recovery loss

↓

GPU-hours lost

↓

Cost comparison

---

### Interpretation

Large recovery losses indicate infrequent checkpoints.

Smaller losses indicate more effective intervention.

---

### Conclusions

Demonstrates whether Harbinger successfully reduced wasted computation.

---

# Important Technical Terms

Evaluation

Measuring system performance after implementation.

Operational Impact

Real-world effect on cluster efficiency.

Policy

Strategy followed by the system.

Static Policy

Always follows the same rule.

Adaptive Policy

Changes behaviour based on current conditions.

GPU-Hours Saved

Amount of computation preserved.

Recovery Loss

Training work requiring recomputation.

Operational Cost

Combined cost of failures and interventions.

Sensitivity Analysis

Evaluating behaviour under different operating conditions.

---

# Common Questions

## Why isn't ROC-AUC enough?

ROC-AUC measures prediction quality.

Cluster operators care about

- downtime
- wasted computation
- operational cost

Harbinger therefore evaluates both prediction and operational impact.

---

## Why compare policies?

A decision-support system should be compared against realistic alternatives.

Examples include

- fixed checkpoint intervals
- adaptive checkpointing
- no intervention

This demonstrates whether Harbinger provides measurable improvements.

---

## Why produce Markdown reports?

Markdown is

- easy to read,
- easy to version-control,
- easy to reference in papers,
- easy to inspect during code reviews.

---

## Why produce CSV files?

CSV files preserve raw experimental data.

Researchers can

- verify calculations,
- create new plots,
- reproduce published results,
- perform additional statistical analysis.

---

# Presentation Notes

If someone asks

> "How do you know Harbinger actually helps?"

Answer:

"We evaluate the complete decision pipeline rather than only prediction accuracy. Harbinger is assessed using operational metrics such as recovery loss, GPU-hours saved, checkpoint overhead, and total operational cost. These results are recorded in evaluation reports that compare Harbinger's adaptive policy against conventional strategies."

---

If someone asks

> "What is the final output of Harbinger?"

Answer:

"The runtime output is a recommended operational action, such as whether to checkpoint or continue training. The research output is a set of evaluation reports demonstrating how those decisions affect operational cost and recovery loss."

---

# Overall Module Summary

This subsystem validates the complete Harbinger framework from an operational perspective.

Its workflow is:

```
Prediction
        │
        ▼
Decision Engine
        │
        ▼
evaluate_harbinger.py
        │
        ├──────────────► evaluation_results.csv
        ├──────────────► recovery_loss_report.md
        └──────────────► cluster_impact_summary.md
```

By the end of this subsystem, Harbinger has completed its full lifecycle:

```
Synthetic Signals
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
Decision Optimization
        │
        ▼
Operational Evaluation
```

The final outcome is **not just a prediction model**, but a **decision-support framework** whose effectiveness is demonstrated through reproducible experiments and measurable operational improvements.

---

# Complete Repository Summary

The Harbinger repository can now be understood as five interconnected subsystems:

## 1. Synthetic Signal Generation

**Goal:** Generate realistic infrastructure telemetry.

**Produces:**

- Checkpoint signals
- ECC signals
- Network degradation signals
- Temperature signals

**Output:** Raw synthetic telemetry.

---

## 2. Dataset Construction & Feature Engineering

**Goal:** Build machine-learning-ready datasets.

**Produces:**

- `training_dataset.csv`
- `engineered_training_dataset.csv`

**Output:** Structured datasets for modelling.

---

## 3. Baseline Validation

**Goal:** Establish strong conventional ML benchmarks.

**Produces:**

- Baseline performance metrics
- `baseline_consolidation_report.md`

**Output:** Scientifically fair comparison baseline.

---

## 4. Decision Engine

**Goal:** Convert predictions into economically optimal actions.

**Produces:**

- Recovery loss estimates
- Intervention cost estimates
- Recommended operational actions

**Output:** Decision-support recommendations.

---

## 5. Evaluation & Reporting

**Goal:** Measure real operational benefits.

**Produces:**

- `evaluation_results.csv`
- `cluster_impact_summary.md`
- `recovery_loss_report.md`

**Output:** Experimental evidence supporting Harbinger's research contribution.

---

# One-Sentence Description of Harbinger

> **Harbinger is a decision-oriented AI infrastructure management framework that combines synthetic data generation, machine learning, and operational cost optimization to predict failures and recommend economically optimal interventions for distributed GPU training clusters.**
