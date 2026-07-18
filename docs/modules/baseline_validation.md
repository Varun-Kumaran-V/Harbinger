# Baseline Validation Module

## Module Overview

The **Baseline Validation Module** verifies that the engineered dataset is suitable for machine learning and establishes performance benchmarks before introducing Harbinger.

A common criticism of research projects is:

> "Your proposed method performs well because you never compared it against strong baseline models."

This subsystem addresses that criticism by evaluating multiple conventional machine learning algorithms on the same engineered dataset used by Harbinger.

The goal is **not** to outperform Harbinger. The goal is to establish a fair reference point so that any improvement achieved by Harbinger can be justified scientifically.

---

# Why This Module Exists

Suppose Harbinger achieves an AUC of 0.91.

Without baseline comparisons, a reviewer might ask:

> "Is 0.91 actually good?"

Maybe Logistic Regression already achieves 0.90.

Maybe Random Forest achieves 0.92.

Without baseline evaluation, Harbinger's contribution cannot be measured objectively.

This subsystem provides that comparison.

---

# Position in Overall Architecture

```
engineered_training_dataset.csv
            │
            ▼
baseline_audit.py
            │
            ▼
Feature Evaluation
            │
            ▼
tune_baselines.py
            │
            ▼
Optimized Baseline Models
            │
            ▼
baseline_consolidation_report.md
            │
            ▼
Harbinger Comparison
```

---

# File 1 — baseline_audit.py

## Purpose

Evaluates the predictive quality of the engineered dataset before hyperparameter tuning.

Think of this as a **baseline health check**.

Rather than finding the best possible model, this file determines whether the engineered features already contain useful predictive information.

---

## Why It Exists

Feature engineering can easily introduce:

- noisy features,
- redundant features,
- weak predictors,
- information leakage.

Before investing computational effort in tuning models, we first verify that the engineered dataset behaves as expected.

---

## Inputs

```
engineered_training_dataset.csv
```

---

## Processing

### Step 1

Load the engineered dataset.

---

### Step 2

Separate:

Features

↓

Prediction labels

---

### Step 3

Train baseline models using default or lightly configured settings.

Examples include:

- Logistic Regression
- Random Forest
- Gradient Boosting (depending on implementation)

---

### Step 4

Evaluate performance.

Metrics typically include:

- ROC-AUC
- Precision
- Recall
- Accuracy

---

## Outputs

Performance summaries printed during execution.

The purpose is diagnostic rather than producing permanent repository artifacts.

---

## Why These Results Matter

This file answers:

> "Did feature engineering improve the dataset?"

If performance improves significantly compared with the raw dataset, feature engineering has successfully extracted meaningful temporal behaviour.

---

## Consumer

Human researcher.

The observations guide further tuning but are not consumed automatically by another script.

---

## Important Technical Terms

Baseline

A reference model used for comparison.

ROC-AUC

Measures ranking quality independent of threshold.

Feature Importance

Contribution of each feature to prediction.

Diagnostic Evaluation

Evaluation intended to guide development rather than represent final results.

---

## Presentation Notes

If someone asks:

"Why evaluate before tuning?"

Answer:

Because tuning a poor dataset wastes time. This module first verifies that the engineered features already contain meaningful predictive information.

---

# File 2 — tune_baselines.py

## Purpose

Optimizes conventional machine learning models and identifies the strongest baseline against which Harbinger will be compared.

---

## Why It Exists

Default model settings rarely produce optimal performance.

Hyperparameter tuning ensures that every baseline receives a fair opportunity before concluding that Harbinger performs better.

This strengthens the scientific credibility of the comparison.

---

## Inputs

```
engineered_training_dataset.csv
```

---

## Processing

### Step 1

Load the engineered dataset.

---

### Step 2

Split data chronologically.

Training observations

↓

Testing observations

This preserves temporal realism.

---

### Step 3

Train multiple baseline algorithms.

Current implementation includes:

- Logistic Regression
- Random Forest
- HistGradientBoostingClassifier

---

### Step 4

Perform hyperparameter optimization.

Rather than manually selecting parameters,

RandomizedSearchCV explores combinations such as:

Random Forest

- number of trees
- tree depth
- minimum split size

Logistic Regression

- regularization strength

Gradient Boosting

- learning rate
- maximum iterations
- tree depth

---

### Step 5

Evaluate optimized models.

Performance metrics are collected and compared.

---

### Step 6

Generate a consolidated report.

---

## Outputs

### baseline_consolidation_report.md

A Markdown report summarizing baseline performance.

---

## Why This Output Matters

This report becomes the primary evidence supporting statements such as:

- Logistic Regression achieved the highest ROC-AUC.
- Gradient Boosting underperformed.
- Random Forest benefited from hyperparameter tuning.

These observations justify the baseline selected for comparison with Harbinger.

---

## Consumer

Human researcher.

The report is later referenced during evaluation and paper writing.

---

# Generated Artifact

---

## baseline_consolidation_report.md

### Purpose

Summarizes the performance of every optimized baseline model.

---

### Typical Contents

For each model:

- evaluation metrics
- optimized hyperparameters
- comparison ranking
- strengths
- weaknesses

---

### Interpretation

Example

```
Model AUC

Logistic Regression

0.724

Random Forest

0.646

Gradient Boosting

0.646
```

Interpretation

Although Random Forest is more complex,

the engineered features appear to be nearly linearly separable, allowing Logistic Regression to perform best.

---

### Conclusions

The report establishes the strongest conventional benchmark.

Harbinger must demonstrate improvement relative to this benchmark rather than an untuned baseline.

---

# Important Technical Terms

Baseline Model

A conventional machine learning algorithm used for comparison.

Hyperparameter

Configuration chosen before training.

RandomizedSearchCV

Randomly samples hyperparameter combinations to efficiently search the optimization space.

Temporal Validation

Training on earlier observations while testing on later observations.

ROC Curve

Relationship between true positive rate and false positive rate.

ROC-AUC

Area under the ROC curve.

Higher values indicate better discrimination.

---

# Common Questions

### Why compare multiple algorithms?

Different datasets favor different model families.

Comparing several algorithms ensures conclusions are not biased toward one particular model.

---

### Why tune hyperparameters?

Default settings are designed for general use.

Optimization provides each model with a fair opportunity to achieve its best performance.

---

### Why use Logistic Regression if more complex models exist?

Simple models provide strong interpretability and often perform surprisingly well on well-engineered features.

If a simple model performs as well as a complex one, it may be preferred due to lower computational cost and easier explanation.

---

### Why perform temporal validation?

Random shuffling can leak future information into the training set.

Temporal validation better represents how the model would behave in real deployments.

---

# Overall Module Summary

This subsystem validates the quality of the engineered dataset and establishes scientifically credible machine learning baselines.

Its workflow is:

```
engineered_training_dataset.csv
            │
            ▼
baseline_audit.py
            │
            ▼
Initial Feature Validation
            │
            ▼
tune_baselines.py
            │
            ▼
Optimized Baseline Models
            │
            ▼
baseline_consolidation_report.md
```

By the end of this subsystem, Harbinger has demonstrated that:

- the engineered dataset contains meaningful predictive information,
- multiple conventional machine learning algorithms have been fairly evaluated,
- hyperparameters have been optimized,
- and a strong baseline benchmark has been established.

These results provide the reference against which Harbinger's decision-oriented framework will be evaluated in the next subsystem.
