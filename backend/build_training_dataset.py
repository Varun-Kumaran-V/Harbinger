import pandas as pd
import numpy as np
import os

def generate_unified_dataset(total_minutes=2000, failure_minute=2000, warning_horizon=180):
    """
    Generates the canonical training dataset merging all Phase 2 signals.
    Simulates a long-running job that ends in failure.
    """
    np.random.seed(42)
    data = []
    
    # States for Markov Network & Checkpoints
    transitions = {1.0: [0.98, 0.02, 0.00], 0.7: [0.05, 0.90, 0.05], 0.4: [0.00, 0.05, 0.95]}
    net_state = 1.0
    impact_factors = {1.0: 1.00, 0.7: 0.85, 0.4: 0.60}
    last_ckpt = 0
    base_ckpt_interval = 120
    prev_ecc = 0
    
    for minute in range(total_minutes):
        # 1. Target Label (Warning Window)
        warning_window = 1 if (failure_minute - warning_horizon) <= minute <= failure_minute else 0

        # 2. Base Utilizations (Ramp up stress during warning window)
        if warning_window == 0:
            gpu_util = np.random.uniform(40, 80)
            cpu_util = np.random.uniform(20, 60)
            mem_pressure = np.random.uniform(30, 60)
        else:
            gpu_util = np.random.uniform(85, 100)
            cpu_util = np.random.uniform(60, 90)
            mem_pressure = np.random.uniform(70, 95)
            
        # 3. Synthetic Temperature
        temp = 40.0 + (gpu_util * 0.45) + (cpu_util * 0.10) + (mem_pressure * 0.05) + np.random.uniform(-1.0, 1.0)
        
        # 4. Synthetic ECC Errors
        stress = min(max((0.7 * (gpu_util / 100.0)) + (0.3 * (mem_pressure / 100.0)), 0.0), 1.0)
        p_ecc = 0.0005 + (0.01 * (stress ** 3)) + (0.03 if warning_window else 0.0) + (0.15 if prev_ecc > 0 else 0.0)
        ecc_event = 1 if np.random.random() < p_ecc else 0
        prev_ecc = ecc_event
        
        # 5. Synthetic Network Degradation
        net_state = np.random.choice([1.0, 0.7, 0.4], p=transitions[net_state])
        throughput = gpu_util * impact_factors[net_state]
        
        # 6. Synthetic Checkpoints & Recovery Loss
        current_ckpt_interval = 30 if warning_window else base_ckpt_interval
        ckpt_event = 0
        if minute > 0 and (minute - last_ckpt) >= current_ckpt_interval:
            ckpt_event = 1
            last_ckpt = minute
        recovery_loss = minute - last_ckpt
        
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
            'warning_window': warning_window # TARGET Y
        })
        
    return pd.DataFrame(data)

if __name__ == "__main__":
    print("Building canonical training dataset...")
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
    print(f"Negative Labels (warning_window=0): {len(df) - positives} ({(len(df) - positives)/len(df)*100:.1f}%)")
    print(f"Missing Values:\n{df.isnull().sum().sum()} total missing")
    
    print("\nFeature Correlations with Target (Leakage Check):")
    corrs = df.corr()['warning_window'].sort_values(ascending=False)
    print(corrs)