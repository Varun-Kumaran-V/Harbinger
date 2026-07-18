"""
Harbinger Research Repository
File: baseline_audit.py

Purpose
-------
Evaluates the predictive expressiveness of engineered telemetry features
using multiple baseline machine learning models. Performs a strict
temporal train/test split, feature scaling, baseline model training,
and ROC-AUC evaluation while preventing target leakage.

Inputs
------
Input Files:
- data/processed/engineered_training_dataset.csv

Dependencies
------------
- pandas
- scikit-learn

Outputs
-------
Console Output:
- ROC-AUC performance for baseline prediction models.

Functions
---------
run_baseline_audit()
    Loads the engineered dataset, performs temporal model evaluation,
    and reports baseline predictive performance.

Models
------
- Logistic Regression
- Decision Tree
- Random Forest
- Histogram Gradient Boosting

Pipeline Role
-------------
Engineered Dataset
        ↓
Baseline Model Evaluation
        ↓
Baseline Performance Report
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
import warnings
warnings.filterwarnings('ignore')

def run_baseline_audit():
    print("--- BASELINE MODEL EXPRESSIVENESS AUDIT ---")
    print("Loading engineered dataset...")
    
    try:
        df = pd.read_csv('data/processed/engineered_training_dataset.csv')
    except FileNotFoundError:
        print("Error: 'data/processed/engineered_training_dataset.csv' not found.")
        print("Please ensure your dataset generation and feature engineering scripts have been run.")
        return

    print("VALIDATION: Engineered Model Expressiveness (Strict Temporal Split)")

    # Strict Temporal Split (70% Train, 30% Test)
    split_idx = int(len(df) * 0.7)
    train = df.iloc[:split_idx]
    test = df.iloc[split_idx:]

    # Exclude targets and hidden variables to prevent leakage
    exclude = ['warning_window', 'latent_risk_score', 'minute', 'checkpoint_event', 'recovery_loss_potential']
    features = [c for c in df.columns if c in df.columns and c not in exclude]

    X_train_raw = train[features]
    y_train = train['warning_window']
    X_test_raw = test[features]
    y_test = test['warning_window']

    # Scale the features for mathematical stability (crucial for Logistic Regression)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train_raw)
    X_test = scaler.transform(X_test_raw)

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Decision Tree": DecisionTreeClassifier(max_depth=5, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42),
        "Gradient Boosting": HistGradientBoostingClassifier(random_state=42)
    }

    for name, model in models.items():
        try:
            model.fit(X_train, y_train)
            preds = model.predict_proba(X_test)[:, 1]
            auc = roc_auc_score(y_test, preds)
            print(f"{name:>20}: {auc:.4f} AUC")
        except ValueError as e:
            print(f"{name:>20}: Error - {e}")

if __name__ == "__main__":
    run_baseline_audit()