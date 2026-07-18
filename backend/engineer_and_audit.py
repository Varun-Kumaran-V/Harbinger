"""
Harbinger Research Repository
File: engineer_and_audit.py

Purpose
-------
Transforms the canonical synthetic training dataset into a temporally
engineered feature set for downstream predictive modeling. This stage
derives rolling statistics, event accumulation metrics, temporal trend
features, and persistence-based features before exporting the engineered
dataset for baseline model evaluation.

Inputs
------
Input Files:
- data/processed/training_dataset.csv

Dependencies:
- pandas
- numpy

Outputs
-------
Generated Files:
- data/processed/engineered_training_dataset.csv

Functions
---------
This script executes as a sequential preprocessing pipeline and does not
define user-created functions.

Major Processing Stages
-----------------------
1. Rolling statistical feature generation.
2. Event accumulation feature generation.
3. Temporal trend feature generation.
4. Persistence feature generation.
5. Engineered dataset export.

Pipeline Role
-------------
Canonical Training Dataset
        ↓
Temporal Feature Engineering
        ↓
Engineered Dataset Export
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
import warnings
warnings.filterwarnings('ignore')

print("--- TEMPORAL FEATURE ENGINEERING ---")
print("Loading cumulative dataset...")
df = pd.read_csv('data/processed/training_dataset.csv')

# --- FAMILY 1: Rolling Statistics ---
df['gpu_util_mean_15m'] = df['gpu_util'].rolling(15, min_periods=1).mean()
df['gpu_util_mean_60m'] = df['gpu_util'].rolling(60, min_periods=1).mean()
df['gpu_util_mean_180m'] = df['gpu_util'].rolling(180, min_periods=1).mean()
df['gpu_util_std_60m'] = df['gpu_util'].rolling(60, min_periods=1).std().fillna(0)

df['temp_mean_15m'] = df['temperature'].rolling(15, min_periods=1).mean()
df['temp_mean_60m'] = df['temperature'].rolling(60, min_periods=1).mean()
df['temp_mean_180m'] = df['temperature'].rolling(180, min_periods=1).mean()
df['temp_std_60m'] = df['temperature'].rolling(60, min_periods=1).std().fillna(0)

df['mem_mean_60m'] = df['mem_pressure'].rolling(60, min_periods=1).mean()
df['throughput_mean_60m'] = df['throughput_factor'].rolling(60, min_periods=1).mean()

# --- FAMILY 2: Event Accumulation ---
df['ecc_count_15m'] = df['ecc_event'].rolling(15, min_periods=1).sum()
df['ecc_count_60m'] = df['ecc_event'].rolling(60, min_periods=1).sum()
df['ecc_count_180m'] = df['ecc_event'].rolling(180, min_periods=1).sum()

df['net_suboptimal'] = (df['network_state'] < 1.0).astype(int)
df['net_severe'] = (df['network_state'] == 0.4).astype(int)
df['degraded_mins_60m'] = df['net_suboptimal'].rolling(60, min_periods=1).sum()
df['severe_mins_180m'] = df['net_severe'].rolling(180, min_periods=1).sum()

# --- FAMILY 3: Trend Features ---
df['temp_delta_60m'] = df['temperature'] - df['temperature'].shift(60).fillna(df['temperature'])
df['gpu_delta_30m'] = df['gpu_util'] - df['gpu_util'].shift(30).fillna(df['gpu_util'])

# --- FAMILY 4: Persistence Features ---
df['gpu_above_90'] = (df['gpu_util'] > 90).astype(int)
df['temp_above_85'] = (df['temperature'] > 85).astype(int)
df['mins_above_90_gpu_180m'] = df['gpu_above_90'].rolling(180, min_periods=1).sum()
df['mins_above_85_temp_180m'] = df['temp_above_85'].rolling(180, min_periods=1).sum()

# Save engineered dataset
drop_cols = ['net_suboptimal', 'net_severe', 'gpu_above_90', 'temp_above_85']
df = df.drop(columns=drop_cols)
df.to_csv('data/processed/engineered_training_dataset.csv', index=False)
print("Engineered dataset saved to data/processed/engineered_training_dataset.csv\n")
