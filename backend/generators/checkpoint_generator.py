"""
===============================================================================
Harbinger: Checkpoint Signal Generator

Purpose
-------
Generates synthetic checkpoint scheduling signals for AI training workloads
using a four-layer economic checkpoint model. The generator simulates
checkpoint intervals based on job duration, dynamically escalates checkpoint
frequency during warning windows, and estimates recovery loss potential to
support downstream risk-aware decision making.

Inputs
------
Function Inputs
---------------
- total_minutes : int
    Total simulated job duration.
- warning_start : int
    Minute at which the warning window begins.

Dependencies
------------
- pandas
- numpy
- matplotlib
- os

Outputs
-------
Repository Files
----------------
- outputs/checkpoint_sample.csv
- outputs/checkpoint_plot.png

Returned Values
---------------
generate_checkpoint_data(...)
    Returns a pandas DataFrame containing:
    - Minute
    - Warning_Window
    - Current_Interval
    - Checkpoint_Event
    - Last_Checkpoint_Time
    - Recovery_Loss_Potential

Functions
---------
generate_checkpoint_data(total_minutes, warning_start)
    Simulates checkpoint scheduling, escalation policy, and recovery-loss
    accumulation over the lifetime of a training job.

Model
-----
Four-Layer Checkpoint Economic Signal Model

Pipeline Role
-------------
Synthetic signal generator responsible for producing checkpoint-related
features used during synthetic dataset construction by
build_training_dataset.py.
===============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def generate_checkpoint_data(total_minutes, warning_start):
    """
    4-Layer Checkpoint Economic Signal Model
    """
    # Layer 1 & 2: Base Interval based on Job Duration Classification
    if total_minutes < 120:
        base_interval = float('inf') # Short: None
    elif total_minutes <= 720:
        base_interval = 240          # Medium: 4 hours
    elif total_minutes <= 2880:
        base_interval = 120          # Long: 2 hours
    else:
        base_interval = 60           # Very Long: 1 hour

    data = []
    last_ckpt = 0

    for minute in range(total_minutes):
        warning = 1 if minute >= warning_start else 0
        
        # Layer 3: Escalation (Dynamically reduce interval during risk windows)
        current_interval = 30 if warning else base_interval
        
        # Layer 4: Trigger Checkpoint and Calculate State
        ckpt_event = 0
        if minute > 0 and (minute - last_ckpt) >= current_interval:
            ckpt_event = 1
            last_ckpt = minute
            
        recovery_loss = minute - last_ckpt # Wasted compute potential
        
        data.append({
            'Minute': minute,
            'Warning_Window': warning,
            'Current_Interval': current_interval,
            'Checkpoint_Event': ckpt_event,
            'Last_Checkpoint_Time': last_ckpt,
            'Recovery_Loss_Potential': recovery_loss
        })
        
    return pd.DataFrame(data)

if __name__ == "__main__":
    # Simulate a "Long" job of 20 hours (1200 minutes)
    # The Warning Window opens at minute 1000
    df = generate_checkpoint_data(1200, 1000)

    os.makedirs('outputs', exist_ok=True)
    df.to_csv('outputs/checkpoint_sample.csv', index=False)

    # Plotting the Economic Signal (Sawtooth pattern)
    plt.figure(figsize=(12, 6))

    # Plot Recovery Loss Potential
    plt.plot(df['Minute'], df['Recovery_Loss_Potential'], color='darkorange', linewidth=2, label='Recovery Loss Potential (mins)')

    # Highlight Warning Window
    plt.axvspan(1000, 1200, color='red', alpha=0.1, label='Warning Window Active')

    # Mark Checkpoint Events
    ckpt_times = df[df['Checkpoint_Event'] == 1]['Minute']
    plt.vlines(ckpt_times, ymin=0, ymax=df['Recovery_Loss_Potential'].max(), color='green', linestyles='dashed', alpha=0.6, label='Checkpoint Event')

    plt.title('Economic Signal: Checkpoint Escalation & Recovery Loss Potential')
    plt.xlabel('Job Runtime (Minutes)')
    plt.ylabel('Wasted Compute Risk (Minutes)')
    plt.legend(loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('outputs/checkpoint_plot.png')

    print("Checkpoint Generation Complete.")
    print(f"Total Checkpoints Generated: {sum(df['Checkpoint_Event'])}")
    print(f"Max Loss Risk before Warning: {df[df['Warning_Window']==0]['Recovery_Loss_Potential'].max()} mins")
    print(f"Max Loss Risk during Warning: {df[df['Warning_Window']==1]['Recovery_Loss_Potential'].max()} mins")