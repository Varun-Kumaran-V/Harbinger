"""
Harbinger Research Repository
File: build_training_dataset.py

Purpose
-------
Generates a synthetic training dataset representing AI training cluster
telemetry through stochastic workload simulation, cumulative latent risk
modeling, probabilistic failure generation, and retrospective warning-window
label assignment. The generated dataset serves as the primary input for
subsequent feature engineering and predictive modeling stages.

Inputs
------
External Inputs:
- None

Function Parameters:
- total_minutes (int): Total simulation duration in minutes.
- warning_horizon (int): Number of minutes preceding each simulated failure
  that are labeled as the prediction warning window.

Dependencies:
- pandas
- numpy

Outputs
-------
Generated Files:
- data/processed/training_dataset.csv

Returns:
- pandas.DataFrame containing simulated telemetry and labels.
- int representing the total number of simulated failure events.

Functions
---------
generate_cumulative_risk_dataset()
    Simulates synthetic cluster telemetry, accumulates latent system risk,
    generates stochastic failures, retrospectively labels warning windows,
    and constructs the training dataset.

Pipeline Role
-------------
Synthetic Dataset Generation
    ↓
Training Dataset Export
    ↓
Feature Engineering
    ↓
Predictive Modeling
"""

import pandas as pd
import numpy as np
import os

def generate_cumulative_risk_dataset(total_minutes=10000, warning_horizon=180):
    """
    Phase 3C.6: Cumulative Risk Engine.
    Stress builds up latent risk over time. High latent risk triggers failure.
    """
    np.random.seed(42)
    data = []
    
    gpu_util = 50.0
    cpu_util = 40.0
    mem_pressure = 50.0
    prev_ecc = 0
    net_state = 1.0
    latent_risk = 0.0  # Now cumulative
    
    failures = []
    
    print(f"Simulating {total_minutes} minutes with Cumulative Risk...")
    
    for minute in range(total_minutes):
        # 1. Stochastic Load (Random Walks)
        rand_step = np.random.rand()
        if rand_step < 0.05:
            gpu_util = np.random.uniform(85, 100)
        elif rand_step < 0.10:
            gpu_util = np.random.uniform(10, 40)
        else:
            gpu_util = np.clip(gpu_util + np.random.normal(0, 3), 0, 100)
            
        cpu_util = np.clip(gpu_util * 0.7 + np.random.normal(0, 10), 0, 100)
        mem_pressure = np.clip(gpu_util * 0.8 + np.random.normal(0, 5), 0, 100)
        
        temp = 40.0 + (gpu_util * 0.45) + (cpu_util * 0.10) + (mem_pressure * 0.05) + np.random.uniform(-1.0, 1.0)
        
        # 2. ECC & Network
        stress = min(max((0.7 * (gpu_util / 100.0)) + (0.3 * (mem_pressure / 100.0)), 0.0), 1.0)
        p_ecc = 0.0001 + (0.005 * (stress ** 3)) + (0.15 if prev_ecc > 0 else 0.0)
        ecc_event = 1 if np.random.random() < p_ecc else 0
        prev_ecc = ecc_event
        
        if np.random.rand() < 0.02:
            net_state = np.random.choice([1.0, 0.7, 0.4], p=[0.8, 0.15, 0.05])
        throughput = gpu_util * net_state
        
        # 3. CUMULATIVE LATENT RISK ENGINE
        # Risk increases if stress is high, decreases if system rests
        risk_delta = (stress - 0.70) * 0.015 
        if temp > 85: risk_delta += 0.005
        if ecc_event == 1: risk_delta += 0.05
        if net_state < 1.0: risk_delta += 0.002
        
        latent_risk = max(0.0, min(1.0, latent_risk + risk_delta))
        
        # 4. Failure Trigger (Probability scales heavily with cumulative risk)
        failure_prob = (latent_risk ** 3) * 0.05 # Max 5% chance per min when fully degraded
        
        if np.random.random() < failure_prob:
            failures.append(minute)
            latent_risk = 0.0 # Reset after crash
            gpu_util = 10.0
            prev_ecc = 0
            
        data.append({
            'minute': minute,
            'gpu_util': round(gpu_util, 2),
            'cpu_util': round(cpu_util, 2),
            'mem_pressure': round(mem_pressure, 2),
            'temperature': round(temp, 2),
            'ecc_event': ecc_event,
            'network_state': net_state,
            'throughput_factor': round(throughput, 2),
            'latent_risk_score': latent_risk, # Added for auditing only
            'warning_window': 0 
        })
        
    df = pd.DataFrame(data)
    
    # Retrospective Labeling
    for fp in failures:
        start_window = max(0, fp - warning_horizon)
        df.loc[start_window:fp, 'warning_window'] = 1
        
    return df, len(failures)

if __name__ == "__main__":
    df, fail_count = generate_cumulative_risk_dataset(10000)
    out_path = 'data/processed/training_dataset.csv'
    df.to_csv(out_path, index=False)
    print(f"Dataset generated with {fail_count} stochastic failures.")