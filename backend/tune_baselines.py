"""
===============================================================================
Harbinger: Baseline Hyperparameter Tuning Framework

Purpose
-------
Evaluates and compares optimized baseline machine learning models using the
engineered training dataset. The module performs hyperparameter optimization,
benchmarks predictive performance, records computational characteristics, and
generates a consolidated baseline comparison report for model selection.

Inputs
------
- data/processed/engineered_training_dataset.csv
    Engineered feature dataset produced by engineer_and_audit.py.

Dependencies
------------
- pandas
- scikit-learn
- time
- os

Outputs
-------
Repository Files
----------------
- outputs/baseline_consolidation_report.md

Console Reports
---------------
- Model training progress
- Best hyperparameters
- ROC-AUC scores
- Training durations
- Baseline comparison table

Functions
---------
Main Script
    Executes the complete baseline evaluation workflow.

Processing Stages
-----------------
1. Load engineered dataset.
2. Perform temporal train-test split.
3. Train Logistic Regression baseline.
4. Tune Random Forest using RandomizedSearchCV.
5. Tune HistGradientBoostingClassifier.
6. Compare predictive performance and computational cost.
7. Generate consolidated Markdown report.

Models
------
- Logistic Regression
- Random Forest
- HistGradientBoostingClassifier

Pipeline Role
-------------
Provides optimized baseline performance benchmarks used to justify the
selection of predictive models within the Harbinger framework before
integration into the operational decision pipeline.
===============================================================================
"""

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import roc_auc_score
import time
import os
import warnings
warnings.filterwarnings('ignore')

print("--- BASELINE MODEL CONSOLIDATION ---")
print("Loading engineered dataset...")
df = pd.read_csv('data/processed/engineered_training_dataset.csv')

# Use the same strict temporal split
train = df[df['minute'] <= 7000]
test = df[df['minute'] > 7000]

exclude = ['warning_window', 'latent_risk_score', 'minute', 'checkpoint_event', 'recovery_loss_potential']
features = [c for c in df.columns if c not in exclude]

X_train, y_train = train[features], train['warning_window']
X_test, y_test = test[features], test['warning_window']

results = []

# 1. Logistic Regression (Baseline)
print("Training Logistic Regression (Default)...")
start_time = time.time()
lr = LogisticRegression(max_iter=1000)
lr.fit(X_train, y_train)
train_time_lr = time.time() - start_time
preds_lr = lr.predict_proba(X_test)[:, 1]
auc_lr = roc_auc_score(y_test, preds_lr)
results.append({"Model": "Logistic Regression", "AUC": auc_lr, "Train Time (s)": round(train_time_lr, 2), "Inference Cost": "Very Low", "Interpretability": "Very High"})
print(f"Result: {auc_lr:.4f} AUC\n")

# 2. Random Forest (Tuned)
print("Tuning Random Forest...")
rf_param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [5, 10, None],
    'min_samples_leaf': [1, 5, 10]
}
rf = RandomForestClassifier(random_state=42)
start_time = time.time()
# Note: cv=3 since this is a timeseries, RandomizedSearchCV randomly splits folds, 
# but this is just to find params, the final test is on the strict temporal test set.
rf_search = RandomizedSearchCV(rf, rf_param_grid, n_iter=10, scoring='roc_auc', cv=3, random_state=42, n_jobs=-1)
rf_search.fit(X_train, y_train)
train_time_rf = time.time() - start_time
preds_rf = rf_search.predict_proba(X_test)[:, 1]
auc_rf = roc_auc_score(y_test, preds_rf)
results.append({"Model": "Random Forest (Tuned)", "AUC": auc_rf, "Train Time (s)": round(train_time_rf, 2), "Inference Cost": "Medium", "Interpretability": "Medium"})
print(f"Result: {auc_rf:.4f} AUC")
print(f"Best Params: {rf_search.best_params_}\n")

# 3. Gradient Boosting (Tuned)
print("Tuning Gradient Boosting (XGBoost Equivalent)...")
gb_param_grid = {
    'learning_rate': [0.01, 0.05, 0.1],
    'max_iter': [100, 200, 300],
    'max_depth': [3, 5, 10],
    'min_samples_leaf': [20, 50]
}
gb = HistGradientBoostingClassifier(random_state=42)
start_time = time.time()
gb_search = RandomizedSearchCV(gb, gb_param_grid, n_iter=10, scoring='roc_auc', cv=3, random_state=42, n_jobs=-1)
gb_search.fit(X_train, y_train)
train_time_gb = time.time() - start_time
preds_gb = gb_search.predict_proba(X_test)[:, 1]
auc_gb = roc_auc_score(y_test, preds_gb)
results.append({"Model": "Gradient Boosting (Tuned)", "AUC": auc_gb, "Train Time (s)": round(train_time_gb, 2), "Inference Cost": "Low", "Interpretability": "Low"})
print(f"Result: {auc_gb:.4f} AUC")
print(f"Best Params: {gb_search.best_params_}\n")

# Consolidation Report
print("--- BASELINE CONSOLIDATION REPORT ---")
results_df = pd.DataFrame(results)
markdown_table = results_df.to_markdown(index=False)
print(markdown_table)

# Save to documentation
out_path = 'outputs/baseline_consolidation_report.md'
os.makedirs('outputs', exist_ok=True)
with open(out_path, 'w') as f:
    f.write("# Baseline Consolidation Report\n\n")
    f.write(markdown_table)