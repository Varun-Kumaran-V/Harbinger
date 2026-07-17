"""
Harbinger Research Repository
File: intervention_cost_model.py

Purpose
-------
Implements Harbinger's intervention cost model for evaluating checkpoint
policies. The model estimates checkpoint overhead, expected recovery loss,
and total operational cost, enabling comparison of candidate checkpoint
intervals under different workload and failure-risk scenarios.

Inputs
------
Initialization Parameters:
- gpu_count
- base_time_min
- k_time_per_gpu

Evaluation Parameters:
- failure_time
- job_duration
- checkpoint interval
- failure probability

Dependencies:
- pandas

Outputs
-------
Returns:
- pandas.DataFrame containing policy comparisons and the recommended
  checkpoint interval.

Console Output:
- Markdown tables for predefined evaluation scenarios.

Classes
-------
InterventionCostModel
    Evaluates candidate checkpoint policies using an operational cost model.

Methods
-------
calculate_costs()
    Computes checkpoint overhead, expected recovery loss, and total
    operational cost.

evaluate_policies()
    Compares candidate checkpoint intervals and identifies the
    minimum-cost strategy.

Pipeline Role
-------------
Operational Cost Analysis
        ↓
Checkpoint Policy Evaluation
        ↓
Optimal Intervention Recommendation
"""

import pandas as pd
import os

class InterventionCostModel:
    def __init__(self, gpu_count, base_time_min=1.0, k_time_per_gpu=0.5):
        self.gpu_count = gpu_count
        # T_ckpt = BaseTime + (k * GPUCount)
        self.t_ckpt = base_time_min + (k_time_per_gpu * gpu_count)
        self.pause_gpu_hours = (self.gpu_count * self.t_ckpt) / 60.0

    def calculate_costs(self, failure_time, job_duration, interval, p_failure):
        # 1. Frequency Cost (Overhead)
        ckpt_count = job_duration // interval
        overhead_cost = ckpt_count * self.pause_gpu_hours
        
        # 2. Expected Failure Loss
        last_ckpt = (failure_time // interval) * interval
        recovery_loss_min = failure_time - last_ckpt
        gpu_hours_lost = (recovery_loss_min * self.gpu_count) / 60.0
        expected_loss = p_failure * gpu_hours_lost
        
        # 3. Total Operational Cost
        total_cost = overhead_cost + expected_loss
        
        return overhead_cost, expected_loss, total_cost

    def evaluate_policies(self, failure_time, job_duration, p_failure, candidates=[120, 60, 30, 15]):
        results = []
        for interval in candidates:
            overhead, exp_loss, total = self.calculate_costs(failure_time, job_duration, interval, p_failure)
            results.append({
                'Interval (m)': interval,
                'Overhead (GPU-hrs)': round(overhead, 2),
                'Expected Loss (GPU-hrs)': round(exp_loss, 2),
                'Total Cost (GPU-hrs)': round(total, 2)
            })
        
        df = pd.DataFrame(results)
        # Find the argmin of Total Cost
        best_idx = df['Total Cost (GPU-hrs)'].idxmin()
        df['Recommendation'] = ['*** OPTIMAL ***' if i == best_idx else '' for i in df.index]
        return df

if __name__ == "__main__":
    print("--- PHASE 4.3: INTERVENTION COST MODEL ---\n")
    
    # Scenario A: Standard Job, High Risk (P=0.85)
    model_a = InterventionCostModel(gpu_count=8)
    df_a = model_a.evaluate_policies(failure_time=950, job_duration=1000, p_failure=0.85)
    
    # Scenario B: Standard Job, Low Risk (P=0.15)
    model_b = InterventionCostModel(gpu_count=8)
    df_b = model_b.evaluate_policies(failure_time=950, job_duration=1000, p_failure=0.15)
    
    # Scenario C: Massive Job (High Overhead), High Risk (P=0.85)
    model_c = InterventionCostModel(gpu_count=64)
    df_c = model_c.evaluate_policies(failure_time=950, job_duration=1000, p_failure=0.85)

    print("Scenario A: 8 GPUs, High Risk (P=0.85)")
    print(df_a.to_markdown(index=False), "\n")
    
    print("Scenario B: 8 GPUs, Low Risk (P=0.15)")
    print(df_b.to_markdown(index=False), "\n")

    print("Scenario C: 64 GPUs (High Checkpoint Overhead), High Risk (P=0.85)")
    print(df_c.to_markdown(index=False), "\n")