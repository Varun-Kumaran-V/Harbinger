import pandas as pd
import numpy as np
import os

def generate_unified_dataset(total_minutes=3000, warning_horizon=180):
    """
    Generates the canonical training dataset merging all Phase 2 signals.
    Simulates a continuous timeline with multiple failure/recovery cycles.
    """
    np.random.seed(42)
    data = []
    
    transitions = {1.0: [0.98, 0.02, 0.00], 0.7: [0.05, 0.90, 0.05], 0.4: [0.00, 0.05, 0.95]}
    net_state = 1.0
    impact_factors = {1.0: 1.00, 0.7: 0.85, 0.4: 0.60}
    last_ckpt = 0
    base_ckpt_interval = 120
    prev_ecc = 0
    
    # Simulate three distinct node crashes over the timeline
    failure_points = [1000, 2000, 3000]
    
    for minute in range(total_minutes):
        # 1. Target Label (Warning Window) - check if near ANY failure point
        warning_window = 0
        for fp in failure_points:
            if (fp - warning_horizon) <= minute <= fp:
                warning_window = 1
                break

        # 2. Base Utilizations
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
            
        # Reset checkpoint anchor after a failure occurs to simulate job restart
        if minute in failure_points:
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
            'warning_window': warning_window
        })
        
    return pd.DataFrame(data)

if __name__ == "__main__":
    print("Building canonical training dataset (Multi-Failure Simulation)...")
    df = generate_unified_dataset()
    os.makedirs('data/processed', exist_ok=True)
    df.to_csv('data/processed/training_dataset.csv', index=False)
    print("Done.")