"""
===============================================================================
Harbinger: ECC Error Signal Generator

Purpose
-------
Generates synthetic GPU Error Correcting Code (ECC) events using a six-layer
probabilistic reliability model. The generator simulates realistic ECC error
bursts by modelling background hardware noise, workload-induced stress,
pre-failure escalation, and temporal burst persistence to produce synthetic
telemetry for Harbinger's training dataset.

Inputs
------
Function Inputs
---------------
- gpu_util : float
    GPU utilization percentage.

- mem_pressure : float
    GPU memory utilization percentage.

- warning_window : int
    Binary indicator specifying whether the system is currently inside the
    pre-failure warning window.

- prev_ecc : int
    Previous timestep ECC event used to model burst persistence.

Dependencies
------------
- numpy
- pandas
- matplotlib
- os

Outputs
-------
Repository Files
----------------
- outputs/ecc_sample_output.csv
- outputs/ecc_plot.png

Returned Values
---------------
generate_ecc_errors(...)
    Returns:
    - 1 : ECC event occurred.
    - 0 : No ECC event occurred.

Functions
---------
generate_ecc_errors(gpu_util, mem_pressure, warning_window, prev_ecc)
    Computes ECC event probability using a hierarchical probabilistic model
    and generates synthetic ECC events for a single timestep.

Model
-----
Six-Layer ECC Error Probability Model

Model Components
----------------
Layer 1 : Volumetric Stress Score
Layer 2 : Background Base Noise
Layer 3 : Stress Amplification
Layer 4 : Pre-Failure Cascade
Layer 5 : Burst Persistence

Pipeline Role
-------------
Synthetic signal generator responsible for producing ECC-related telemetry
used during synthetic dataset construction within build_training_dataset.py.
The generated signals contribute to feature engineering, baseline evaluation,
and downstream Harbinger decision modelling.
===============================================================================
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_ecc_errors(gpu_util, mem_pressure, warning_window, prev_ecc):
    """
    5-Layer ECC Error Probability Model
    """
    # Layer 1: Volumetric Stress Score
    stress = (0.7 * (gpu_util / 100.0)) + (0.3 * (mem_pressure / 100.0))
    stress = min(max(stress, 0.0), 1.0)
    
    # Layer 2: Background Base Noise
    p_base = 0.0005
    
    # Layer 3: Stress Amplification
    p_stress = 0.01 * (stress ** 3)
    
    # Layer 4: Pre-Failure Cascade
    p_cascade = 0.03 if warning_window else 0.0
    
    # Layer 5: Burst Persistence
    p_burst = 0.15 if prev_ecc > 0 else 0.0
    
    # Total Probability
    p_total = p_base + p_stress + p_cascade + p_burst
    p_total = min(p_total, 1.0)
    
    # Generate event (1 = Error, 0 = No Error)
    return 1 if np.random.random() < p_total else 0

if __name__ == "__main__":
    # Simulate a 1000-minute GPU lifecycle
    np.random.seed(42)
    minutes = 1000
    
    # 0-600: Normal load | 601-800: Heavy load | 801-1000: Warning Window
    gpus = np.concatenate([np.random.uniform(40, 60, 600), np.random.uniform(80, 100, 200), np.random.uniform(80, 100, 200)])
    mems = np.concatenate([np.random.uniform(30, 50, 600), np.random.uniform(70, 90, 200), np.random.uniform(70, 90, 200)])
    warnings = np.concatenate([np.zeros(800), np.ones(200)])
    
    ecc_events = []
    prev_e = 0
    for g, m, w in zip(gpus, mems, warnings):
        e = generate_ecc_errors(g, m, w, prev_e)
        ecc_events.append(e)
        prev_e = e
        
    df = pd.DataFrame({
        'Minute': range(minutes),
        'GPU_Util': np.round(gpus, 2),
        'Mem_Pressure': np.round(mems, 2),
        'Warning_Window': warnings.astype(int),
        'ECC_Event': ecc_events
    })
    
    os.makedirs('outputs', exist_ok=True)
    df.to_csv('outputs/ecc_sample_output.csv', index=False)
    
    plt.figure(figsize=(12, 6))
    plt.plot(df['Minute'], df['GPU_Util'], label='GPU Util (%)', alpha=0.3, color='blue')
    plt.fill_between(df['Minute'], 0, 100, where=df['Warning_Window']==1, color='red', alpha=0.1, label='Warning Window')
    
    ecc_times = df[df['ECC_Event'] == 1]['Minute']
    plt.vlines(ecc_times, ymin=0, ymax=100, color='firebrick', label='ECC Error Burst', linewidth=2)
    
    plt.title('Synthetic ECC Errors: 6-Layer Probability Model')
    plt.xlabel('Time (Minutes)')
    plt.ylabel('GPU Utilization / Events')
    plt.legend(loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('outputs/ecc_plot.png')
    
    print("ECC Generation Complete.")
    print(f"Total ECC Events: {sum(ecc_events)}")