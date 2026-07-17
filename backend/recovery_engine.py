"""
Harbinger Research Repository
File: recovery_engine.py

Purpose
-------
Implements Harbinger's Recovery Loss Engine for estimating computational work
lost following training job failures. The engine performs counterfactual
analysis by comparing the active checkpoint policy against alternative
checkpoint intervals to quantify potential GPU-hour savings.

Inputs
------
Initialization Parameters:
- gpu_count

Evaluation Parameters:
- failure_time
- last_checkpoint_time
- job_start_time
- current_interval
- alternative_intervals

Dependencies:
- pandas
- os

Outputs
-------
Generated Files:
- outputs/recovery_loss_report.md

Returns:
- pandas.DataFrame containing recovery-loss and counterfactual policy
  comparisons.

Console Output:
- Markdown summary of recovery-loss analysis.

Classes
-------
RecoveryLossEngine
    Estimates recovery loss and evaluates counterfactual checkpoint
    strategies.

Methods
-------
calculate_loss()
    Computes recovery loss and GPU-hours lost for a failure event.

evaluate_counterfactuals()
    Compares the current checkpoint policy against alternative policies and
    reports potential GPU-hour savings.

Pipeline Role
-------------
Failure Event
        ↓
Recovery Loss Estimation
        ↓
Counterfactual Policy Analysis
        ↓
Recovery Impact Report
"""

import pandas as pd
import os

class RecoveryLossEngine:
    def __init__(self, gpu_count):
        """
        Initializes the engine with the hardware footprint of the job.
        """
        self.gpu_count = gpu_count

    def calculate_loss(self, failure_time, last_checkpoint_time):
        """
        Calculates the physical and economic loss of a failure.
        """
        recovery_loss_min = failure_time - last_checkpoint_time
        gpu_hours_lost = (recovery_loss_min * self.gpu_count) / 60.0
        return recovery_loss_min, gpu_hours_lost

    def evaluate_counterfactuals(self, failure_time, job_start_time, current_interval, alternative_intervals):
        """
        Compares the actual checkpoint policy against alternative mitigation policies.
        """
        results = []

        # Calculate baseline (what actually happened / is happening)
        last_ckpt_actual = job_start_time + ((failure_time - job_start_time) // current_interval) * current_interval
        actual_loss_min, actual_gpu_hours = self.calculate_loss(failure_time, last_ckpt_actual)

        results.append({
            'Policy': f'Current ({current_interval}m)',
            'Interval (min)': current_interval,
            'Last Checkpoint': last_ckpt_actual,
            'Recovery Loss (min)': actual_loss_min,
            'GPU-Hours Lost': round(actual_gpu_hours, 2),
            'GPU-Hours Saved': 0.0
        })

        # Calculate counterfactuals (what if we intervened?)
        for alt in alternative_intervals:
            last_ckpt_alt = job_start_time + ((failure_time - job_start_time) // alt) * alt
            alt_loss_min, alt_gpu_hours = self.calculate_loss(failure_time, last_ckpt_alt)
            saved_gpu_hours = actual_gpu_hours - alt_gpu_hours

            results.append({
                'Policy': f'Counterfactual ({alt}m)',
                'Interval (min)': alt,
                'Last Checkpoint': last_ckpt_alt,
                'Recovery Loss (min)': alt_loss_min,
                'GPU-Hours Lost': round(alt_gpu_hours, 2),
                'GPU-Hours Saved': round(saved_gpu_hours, 2)
            })

        return pd.DataFrame(results)

if __name__ == "__main__":
    print("--- PHASE 4.1: RECOVERY LOSS ENGINE ---\n")
    
    # Simulating a job on 8 GPUs that fails at minute 850
    engine = RecoveryLossEngine(gpu_count=8)
    failure_time = 850
    job_start = 0
    current_policy = 120 # Standard 2-hour checkpoint
    alternatives = [60, 30, 15] # More aggressive mitigation options

    print(f"Simulating Job Failure at Minute {failure_time} on {engine.gpu_count} GPUs.")
    
    df_results = engine.evaluate_counterfactuals(failure_time, job_start, current_policy, alternatives)
    
    print("\nImpact Estimation & Counterfactual Analysis:")
    markdown_table = df_results.to_markdown(index=False)
    print(markdown_table)
    
    # Save output for documentation
    os.makedirs('outputs', exist_ok=True)
    with open('outputs/recovery_loss_report.md', 'w') as f:
        f.write("# Phase 4.1: Recovery Loss Counterfactuals\n\n")
        f.write(markdown_table)