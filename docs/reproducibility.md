# Harbinger: Reproducibility and Evaluation Guide

## 1. Repository Layout

- `/backend/` – Core implementation of the Harbinger pipeline, including dataset generation, feature engineering, baseline evaluation, decision optimization, and performance assessment.
- `/backend/generators/` – Synthetic signal generators for temperature, ECC activity, network behaviour, and checkpoint events.
- `/data/processed/` – Generated datasets used throughout the repository.
- `/docs/` – Documentation describing the system architecture, modules, datasets, and reproducibility.
- `/models/` – Design specifications for the prediction model, decision engine, and training dataset.
- `/outputs/` – Generated evaluation reports, plots, and sample outputs.

---

## 2. Environment

### Python Version

- Python 3.10 or later

### Core Libraries

- pandas
- numpy
- scikit-learn
- matplotlib

---

## 3. Reproducibility

Harbinger is designed to generate its datasets and evaluation artifacts internally. The repository does not require external datasets to reproduce the implemented pipeline.

Where stochastic behaviour is present, deterministic random seeds are used to ensure reproducible dataset generation and evaluation under the same software environment.

---

## 4. Dataset Generation Pipeline

The complete dataset can be regenerated from scratch using the following sequence.

### Step 1 – Generate the Base Dataset

```bash
python backend/build_training_dataset.py
```

Output:

- `data/processed/training_dataset.csv`

This stage combines the synthetic infrastructure signals into a structured training dataset.

---

### Step 2 – Engineer Temporal Features

```bash
python backend/engineer_and_audit.py
```

Output:

- `data/processed/engineered_training_dataset.csv`

This stage derives temporal and statistical features used by the machine learning models.

---

## 5. Model Development Pipeline

### Learnability Audit

```bash
python backend/learnability_audit.py
```

Verifies that the engineered dataset contains meaningful predictive structure before model training.

---

### Baseline Evaluation

```bash
python backend/baseline_audit.py
```

Evaluates baseline machine learning models on the engineered dataset.

---

### Baseline Optimization

```bash
python backend/tune_baselines.py
```

Output:

- `outputs/baseline_consolidation_report.md`

Performs hyperparameter tuning and summarizes baseline model performance.

---

## 6. Harbinger Decision Pipeline

Execute the complete operational decision pipeline.

```bash
python backend/harbinger_pipeline.py
```

This stage integrates:

- Failure prediction
- Recovery loss estimation
- Intervention cost modelling
- Operational decision optimization

---

## 7. Evaluation

Run the complete evaluation pipeline.

```bash
python backend/evaluate_harbinger.py
```

Outputs:

- `outputs/evaluation_results.csv`
- `outputs/cluster_impact_summary.md`
- `outputs/recovery_loss_report.md`

These artifacts summarize Harbinger's operational performance using metrics such as recovery loss, intervention cost, and overall operational effectiveness.

---

## 8. Expected Execution Order

For a complete reproduction of the repository workflow, execute the scripts in the following order:

1. `build_training_dataset.py`
2. `engineer_and_audit.py`
3. `learnability_audit.py`
4. `baseline_audit.py`
5. `tune_baselines.py`
6. `harbinger_pipeline.py`
7. `evaluate_harbinger.py`

Following this sequence reproduces the synthetic datasets, baseline evaluations, decision pipeline, and evaluation artifacts included in the repository.
