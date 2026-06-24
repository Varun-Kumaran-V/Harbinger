import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
import warnings
warnings.filterwarnings('ignore')

# 1. Load Data and Apply Temporal Split (0-1400 Train, 1401-2000 Test)
df = pd.read_csv('data/processed/training_dataset.csv')
train = df[df['minute'] <= 1400]
test = df[df['minute'] > 1400]

target = 'warning_window'
raw_features = ['gpu_util', 'cpu_util', 'mem_pressure']
synth_features = ['temperature', 'ecc_event', 'network_state', 'throughput_factor']
all_features = raw_features + synth_features

print("--- PHASE 3C: MODELING READINESS AUDIT ---\n")

# Test 1: Single Feature Feasibility
print("TEST 1: Single Feature AUC (Checking for Generative Coupling)")
for feature in all_features:
    model = LogisticRegression()
    model.fit(train[[feature]], train[target])
    preds = model.predict_proba(test[[feature]])[:, 1]
    auc = roc_auc_score(test[target], preds)
    print(f"{feature:>20}: {auc:.4f}")

# Test 2: Feature Ablation
print("\nTEST 2: Feature Ablation (Checking for Synthetic Value-Add)")
feature_sets = {
    "Raw Only": raw_features,
    "Synthetic Only": synth_features,
    "Combined": all_features
}

for name, features in feature_sets.items():
    model = LogisticRegression(max_iter=1000)
    model.fit(train[features], train[target])
    preds = model.predict_proba(test[features])[:, 1]
    auc = roc_auc_score(test[target], preds)
    print(f"{name:>15}: {auc:.4f}")