"""
Harbinger Research Repository
File: build_training_dataset.py

Purpose
-------
Generates Harbinger's canonical synthetic training dataset by simulating
long-running AI training jobs under stochastic operating conditions. The
simulation models hardware utilization, temperature, ECC events, network
degradation, checkpoint progression, cumulative latent risk, and multiple
failure events before retrospectively labeling prediction warning windows.

Inputs
------
External Inputs:
- None

Function Parameters:
- max_minutes (int): Total simulated runtime.
- warning_horizon (int): Number of minutes preceding each simulated failure
  labeled as the prediction warning window.

Dependencies:
- pandas
- numpy
- os

Outputs
-------
Generated Files:
- data/processed/training_dataset.csv

Returns:
- pandas.DataFrame containing simulated telemetry and warning-window labels.

Functions
---------
generate_unified_dataset()
    Simulates synthetic AI cluster telemetry, accumulates latent system
    degradation, generates multiple stochastic failures, retrospectively
    labels warning windows, and constructs the canonical training dataset.

Pipeline Role
-------------
Canonical Dataset Generation
        ↓
training_dataset.csv
        ↓
Temporal Feature Engineering
        ↓
Predictive Modeling
"""

import pandas as pd
import numpy as np
import os

def generate_unified_dataset(max_minutes=10000, warning_horizon=180):
    """
    Generates the canonical training dataset using Causal Inversion.
    Tuned to produce a failure roughly every 1500-2000 minutes, creating
    a realistic class imbalance (5-10% positive labels).
    """
    np.random.seed(42)
    data = []
    
    transitions = {1.0: [0.98, 0.02, 0.00], 0.7: [0.05, 0.90, 0.05], 0.4: [0.00, 0.05, 0.95]}
    net_state = 1.0
    impact_factors = {1.0: 1.00, 0.7: 0.85, 0.4: 0.60}
    last_ckpt = 0
    base_ckpt_interval = 120
    prev_ecc = 0
    
    latent_risk_score = 0.0
    failure_minutes = []
    
    for minute in range(max_minutes):
        # 1. Base Utilizations (Noisy with random stress spikes)
        gpu_util = np.random.uniform(30, 80)
        cpu_util = np.random.uniform(20, 70)
        mem_pressure = np.random.uniform(30, 80)
        
       # ... inside the for loop ...
        
        # 10% chance of a high-stress spike
        if np.random.random() < 0.10:
            gpu_util = np.random.uniform(90, 100)
            mem_pressure = np.random.uniform(85, 100)
            
        # NEW: As risk builds, the machine shows symptoms (runs hotter, more errors)
        degradation_penalty = latent_risk_score * 15.0 
            
        # 2. Synthetic Temperature (Add MASSIVE random noise to confuse the model)
        temp = 40.0 + (gpu_util * 0.4) + (cpu_util * 0.1) + np.random.normal(0, 15.0) + degradation_penalty
        
        # 3. Synthetic ECC Errors (Make the degradation penalty highly unpredictable)
        stress = (gpu_util / 100.0)
        noisy_degradation = latent_risk_score * np.random.uniform(0.01, 0.10)
        p_ecc = 0.001 + (0.05 * (stress ** 3)) + noisy_degradation + (0.1 if prev_ecc > 0 else 0.0)
        ecc_event = 1 if np.random.random() < p_ecc else 0
        prev_ecc = ecc_event
        
        # 4. Synthetic Network Degradation
        net_state = np.random.choice([1.0, 0.7, 0.4], p=transitions[net_state])
        throughput = gpu_util * impact_factors[net_state]
        
        # 5. Synthetic Checkpoints & Recovery Loss
        ckpt_event = 0
        if minute > 0 and (minute - last_ckpt) >= base_ckpt_interval:
            ckpt_event = 1
            last_ckpt = minute
        recovery_loss = minute - last_ckpt
        
        # 6. CAUSAL LATENT RISK ENGINE (Tuned for ~1800 min lifespans)
        if gpu_util > 90 or temp > 85 or ecc_event == 1:
            latent_risk_score += np.random.uniform(0.003, 0.008) # Slower accumulation
        else:
            latent_risk_score = max(0.0, latent_risk_score - 0.0002) # Gentle decay
            
        latent_risk_score += 0.0002 # Constant baseline aging
            
        data.append({
            'minute': minute,
            'gpu_util': round(gpu_util, 2),
            'cpu_util': round(cpu_util, 2),
            'mem_pressure': round(mem_pressure, 2),
            'temperature': round(temp, 2),
            'ecc_event': ecc_event,
            'network_state': net_state,
            'throughput_factor': round(throughput, 2),
            'recovery_loss_potential': recovery_loss,
            'latent_risk_score': latent_risk_score,
            'warning_window': 0 # Placeholder
        })
        
        # 7. MULTIPLE FAILURES TRIGGER
        if latent_risk_score >= 1.0:
            failure_minutes.append(minute)
            latent_risk_score = 0.0 # Reset risk after failure
            last_ckpt = minute      # Reset checkpoint after failure
            
    df = pd.DataFrame(data)
    
    # 8. RETROSPECTIVE LABELING for all failures
    for f_min in failure_minutes:
        df.loc[(df['minute'] > f_min - warning_horizon) & (df['minute'] <= f_min), 'warning_window'] = 1
        
    return df

if __name__ == "__main__":
    print("--- CANONICAL TRAINING DATASET GENERATION ---")
    df = generate_unified_dataset()
    
    os.makedirs('data/processed', exist_ok=True)
    out_path = 'data/processed/training_dataset.csv'
    df.to_csv(out_path, index=False)
    
    print(f"\nDataset saved to {out_path}")
    print("-" * 40)
    print("DATASET VALIDATION")
    print("-" * 40)
    print(f"Total Rows: {len(df)}")
    positives = df['warning_window'].sum()
    print(f"Positive Labels (warning_window=1): {positives} ({positives/len(df)*100:.1f}%)")