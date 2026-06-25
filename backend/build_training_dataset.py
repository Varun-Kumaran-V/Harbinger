import pandas as pd
import numpy as np
import os

def generate_risk_based_dataset(total_minutes=10000, warning_horizon=180):
    """
    Phase 3C.5: Causal Inversion.
    Simulates a cluster using a Hidden Risk Engine to decouple load from guaranteed failure.
    """
    np.random.seed(42)
    data = []
    
    # Initial States
    gpu_util = 50.0
    cpu_util = 40.0
    mem_pressure = 50.0
    prev_ecc = 0
    net_state = 1.0
    
    failures = []
    
    print(f"Simulating {total_minutes} minutes of cluster runtime...")
    
    for minute in range(total_minutes):
        # 1. Stochastic Load Generation (Random Walks)
        # Allows for long periods of 95%+ utilization WITHOUT forcing a failure
        rand_step = np.random.rand()
        if rand_step < 0.05:
            gpu_util = np.random.uniform(85, 100) # Jump to heavy load
        elif rand_step < 0.10:
            gpu_util = np.random.uniform(10, 40)  # Drop to idle
        else:
            gpu_util = np.clip(gpu_util + np.random.normal(0, 3), 0, 100) # Normal drift
            
        cpu_util = np.clip(gpu_util * 0.7 + np.random.normal(0, 10), 0, 100)
        mem_pressure = np.clip(gpu_util * 0.8 + np.random.normal(0, 5), 0, 100)
        
        # 2. Temperature
        temp = 40.0 + (gpu_util * 0.45) + (cpu_util * 0.10) + (mem_pressure * 0.05) + np.random.uniform(-1.0, 1.0)
        
        # 3. ECC Errors (Rare, driven by stress)
        stress = min(max((0.7 * (gpu_util / 100.0)) + (0.3 * (mem_pressure / 100.0)), 0.0), 1.0)
        p_ecc = 0.0001 + (0.005 * (stress ** 3)) + (0.15 if prev_ecc > 0 else 0.0)
        ecc_event = 1 if np.random.random() < p_ecc else 0
        prev_ecc = ecc_event
        
        # 4. Network
        if np.random.rand() < 0.02:
            net_state = np.random.choice([1.0, 0.7, 0.4], p=[0.8, 0.15, 0.05])
        throughput = gpu_util * net_state
        
        # 5. HIDDEN LATENT RISK ENGINE
        base_risk = 0.0001
        load_risk = 0.0005 * (stress ** 4) # Only extreme stress adds risk
        temp_risk = 0.005 if temp > 85 else 0.0
        ecc_risk = 0.02 if ecc_event == 1 else 0.0 # High risk multiplier
        
        latent_risk_score = base_risk + load_risk + temp_risk + ecc_risk
        
        # 6. Failure Trigger
        if np.random.random() < latent_risk_score:
            failures.append(minute)
            gpu_util = 10.0 # Node crashes and restarts at low load
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
            'warning_window': 0 # Placeholder, labeled retrospectively
        })
        
    df = pd.DataFrame(data)
    
    # 7. Retrospective Labeling (The Warning Window)
    for fp in failures:
        start_window = max(0, fp - warning_horizon)
        df.loc[start_window:fp, 'warning_window'] = 1
        
    return df, len(failures)

if __name__ == "__main__":
    df, fail_count = generate_risk_based_dataset(10000)
    out_path = 'data/processed/training_dataset.csv'
    df.to_csv(out_path, index=False)
    
    print(f"Dataset generated with {fail_count} stochastic failures.")
    print(f"Saved to {out_path}")