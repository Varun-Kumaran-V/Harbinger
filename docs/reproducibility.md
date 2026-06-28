# Harbinger: Reproducibility and Evaluation Guide

## 1. Repository Layout

* `/backend/`: Core execution scripts (Dataset generation, ML tuning, Impact Estimation).
* `/backend/generators/`: Synthetic physics engines (Temperature, ECC, Network, Checkpoints).
* `/data/`: Raw Microsoft trace data and processed synthetic CSVs.
* `/docs/`: Architectural contracts and feature registries.
* `/models/`: Design documents for the risk engine and prediction modules.
* `/outputs/`: Generated plots, evaluation results, and baseline consolidation reports.

## 2. Environment & Seeds

* **Python Version:** Python 3.10+
* **Core Libraries:** `pandas`, `numpy`, `scikit-learn`
* **Random Seeds:** `np.random.seed(42)` is strictly enforced across all dataset generators and ML tuning splits (`build_training_dataset.py`, `evaluate_harbinger.py`, `tune_baselines.py`) to ensure exact reproducibility of the 203 GPU-hour savings metric.

## 3. Dataset Generation Pipeline

To regenerate the exact datasets used in this paper from scratch:

1. Run `python backend/build_training_dataset.py` (Generates the cumulative risk timeline).
2. Run `python backend/engineer_and_audit.py` (Applies 15m, 60m, 180m rolling temporal features).

## 4. Evaluation Pipeline

To reproduce the cluster-scale evaluation (Figure 5) and the baseline ML comparison:

1. Run `python backend/tune_baselines.py` (Validates Logistic Regression superiority).
2. Run `python backend/evaluate_harbinger.py` (Executes the 5,000-job cluster backtest).
