import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('data/processed/training_dataset.csv')

print("--- PHASE 3C.6: LEARNABILITY VALIDATION ---\n")

# Validation 1: Risk Calibration
print("VALIDATION 1: Risk Calibration (Latent Risk vs Warning Window Rate)")
df['risk_bucket'] = pd.cut(df['latent_risk_score'], bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0])
calibration = df.groupby('risk_bucket', observed=False)['warning_window'].mean() * 100
for bucket, rate in calibration.items():
    print(f"Risk {bucket}: {rate:.1f}% in warning window")

# Validation 2: Feature-Risk Relationship
print("\nVALIDATION 2: Feature Correlations with Latent Risk")
features = ['gpu_util', 'cpu_util', 'mem_pressure', 'temperature', 'ecc_event', 'network_state', 'throughput_factor']
corrs = df[features].corrwith(df['latent_risk_score']).sort_values(ascending=False)
print(corrs)

# Validation 3: Non-Linear Separability
print("\nVALIDATION 3: Model Expressiveness (Temporal Split)")
train = df[df['minute'] <= 7000]
test = df[df['minute'] > 7000]

X_train = train[features]
y_train = train['warning_window']
X_test = test[features]
y_test = test['warning_window']

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree": DecisionTreeClassifier(max_depth=5, random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
}

for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, preds)
    print(f"{name:>20}: {auc:.4f} AUC")