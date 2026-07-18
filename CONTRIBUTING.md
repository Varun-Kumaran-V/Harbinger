# Contributing to Harbinger

Thank you for your interest in contributing to Harbinger.

Harbinger is a research framework for decision-oriented AI infrastructure failure prediction. The project emphasizes reproducibility, modular design, and transparent experimentation. Contributions that improve research quality, reproducibility, or code maintainability are welcome.

---

# Repository Structure

```
Harbinger/
│
├── backend/            # Core pipeline, models, evaluation, and decision logic
├── data/               # Raw and processed datasets
├── docs/               # Design documents and methodology
├── outputs/            # Generated reports, figures, and evaluation results
│
├── README.md
├── LICENSE
├── requirements.txt
└── Dockerfile
```

---

# Development Principles

Contributions should preserve the modular pipeline architecture.

```
Synthetic Signal Generation
            │
            ▼
Training Dataset Construction
            │
            ▼
Feature Engineering
            │
            ▼
Model Training
            │
            ▼
Failure Prediction
            │
            ▼
Recovery Loss Estimation
            │
            ▼
Intervention Cost Modelling
            │
            ▼
Decision Recommendation
```

Each stage should remain as independent as practical.

---

# Coding Guidelines

Please follow these principles when contributing:

- Keep modules focused on a single responsibility.
- Prefer readability over unnecessary optimization.
- Document assumptions behind simulations and heuristics.
- Avoid hard-coded constants without explanation.
- Use descriptive variable and function names.
- Add comments only where they improve understanding of non-obvious logic.

---

# Adding New Components

## Signal Generators

New telemetry generators should be placed in:

```
backend/generators/
```

Each generator should produce deterministic, reproducible synthetic telemetry consistent with the existing data generation pipeline.

---

## Machine Learning Models

Additional prediction models should:

- operate on the engineered dataset
- use the existing evaluation workflow
- report performance using the same evaluation metrics where possible

Avoid modifying existing benchmark implementations unless correcting a verified issue.

---

## Evaluation

When introducing new algorithms or heuristics:

- compare against existing baselines
- explain methodological differences
- include quantitative evaluation where appropriate

Maintaining reproducible comparisons is preferred over maximizing performance.

---

# Documentation

Significant architectural or methodological changes should also update the relevant documentation under:

```
docs/
```

This helps maintain consistency between the implementation and the research methodology.

---

# Pull Requests

A good pull request should include:

- a clear description of the change
- motivation for the modification
- any affected modules
- evidence that the code executes successfully
- updates to documentation if required

Small, focused pull requests are preferred over large unrelated changes.

---

# Reporting Issues

If you discover a bug or identify an opportunity for improvement, please open a GitHub Issue with:

- a clear description
- reproduction steps (if applicable)
- expected behavior
- observed behavior
- relevant logs or screenshots

---

# Research Philosophy

Harbinger is designed as a decision-support framework rather than solely a prediction benchmark.

Contributions should prioritize:

- reproducibility
- interpretability
- modularity
- sound experimental methodology

over maximizing predictive performance alone.
