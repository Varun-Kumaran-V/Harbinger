import pandas as pd
import numpy as np
import os

print("--- PHASE 6: EXPERIMENTAL EVALUATION FRAMEWORK ---")
print("Initializing Cluster Simulation Harness...\n")

# Set seed for reproducible research
np.random.seed(42)
NUM_JOBS = 5000

# 1. Generate Synthetic Job Workload (Sensitivity Parameters)
jobs = []
for i in range(NUM_JOBS):
    gpu_count = np.random.choice([8, 16, 32, 64, 128])
    duration = np.random.uniform(500, 2000) # Job length in minutes
    p_failure = np.random.uniform(0.01, 0.95) # Ranging from totally safe to doomed
    failure_time = np.random.uniform(100, duration) # When the crash occurs
    
    jobs.append({
        'job_id': i,
        'gpu_count': gpu_count,
        'duration': duration,
        'p_failure': p_failure,
        'failure_time': failure_time
    })

df_jobs = pd.DataFrame(jobs)

# 2. Cost Engine Logic
def calc_cost(job, interval):
    base_time_min = 1.0
    k_time_per_gpu = 0.5
    t_ckpt = base_time_min + (k_time_per_gpu * job['gpu_count'])
    pause_gpu_hours = (job['gpu_count'] * t_ckpt) / 60.0
    
    ckpt_count = job['duration'] // interval
    overhead = ckpt_count * pause_gpu_hours
    
    last_ckpt = (job['failure_time'] // interval) * interval
    recovery_loss_min = job['failure_time'] - last_ckpt
    gpu_hours_lost = (recovery_loss_min * job['gpu_count']) / 60.0
    expected_loss = job['p_failure'] * gpu_hours_lost
    
    return overhead + expected_loss

# 3. Evaluate Policies (Experiment 3 & 4)
results = []
print(f"Simulating {NUM_JOBS} jobs across static and adaptive policies...")

for _, job in df_jobs.iterrows():
    cost_120 = calc_cost(job, 120)
    cost_60 = calc_cost(job, 60)
    cost_30 = calc_cost(job, 30)
    
    # Harbinger dynamic optimizer (Phase 5 logic: selects minimum cost policy)
    cost_harbinger = min(cost_120, cost_60, cost_30)
    
    results.append({
        'Static-120': cost_120,
        'Static-60': cost_60,
        'Static-30': cost_30,
        'Harbinger': cost_harbinger
    })

df_results = pd.DataFrame(results)

# 4. Aggregate & Output
summary = {
    'Policy': ['Static-120 (Standard)', 'Static-60 (Aggressive)', 'Static-30 (Ultra-Aggressive)', 'Harbinger (Adaptive)'],
    'Total Operational Cost (GPU-Hours)': [
        df_results['Static-120'].sum(),
        df_results['Static-60'].sum(),
        df_results['Static-30'].sum(),
        df_results['Harbinger'].sum()
    ]
}

df_summary = pd.DataFrame(summary)
df_summary['Total Operational Cost (GPU-Hours)'] = df_summary['Total Operational Cost (GPU-Hours)'].round(2)

baseline_cost = df_summary.loc[0, 'Total Operational Cost (GPU-Hours)']
harbinger_cost = df_summary.loc[3, 'Total Operational Cost (GPU-Hours)']
savings = baseline_cost - harbinger_cost

print("\nAggregate Cluster-Scale Impact (5,000 Simulated Jobs):")
markdown_table = df_summary.to_markdown(index=False)
print(markdown_table)
print(f"\n*** Total Expected GPU-Hours Saved by Harbinger vs Standard Baseline: {savings:,.2f} ***\n")

# Export for paper figures
os.makedirs('outputs', exist_ok=True)
df_results.to_csv('outputs/evaluation_results.csv', index=False)
with open('outputs/cluster_impact_summary.md', 'w') as f:
    f.write("# Phase 6: Cluster-Scale Impact\n\n")
    f.write(markdown_table)