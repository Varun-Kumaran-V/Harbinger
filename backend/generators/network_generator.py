import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def generate_network_degradation(total_minutes):
    """
    3-Layer Network Degradation Model (Markov State -> Impact -> Throughput)
    """
    # Layer 1: States (Healthy, Degraded, Severe)
    states = [1.0, 0.7, 0.4]
    impact_factors = {1.0: 1.00, 0.7: 0.85, 0.4: 0.60}
    
    # Layer 2: Markov Transition Matrix
    # Order: [Healthy, Degraded, Severe]
    transitions = {
        1.0: [0.98, 0.02, 0.00],
        0.7: [0.05, 0.90, 0.05],
        0.4: [0.00, 0.05, 0.95]
    }
    
    current_state = 1.0
    data = []
    
    # Generate constant high GPU load to clearly visualize the throughput drop
    gpu_utils = np.random.uniform(85, 100, total_minutes)
    
    for minute in range(total_minutes):
        # Apply State Transition
        probs = transitions[current_state]
        current_state = np.random.choice(states, p=probs)
        
        # Layer 3: Performance Impact Calculation
        impact_factor = impact_factors[current_state]
        gpu_util = gpu_utils[minute]
        effective_throughput = gpu_util * impact_factor
        
        data.append({
            'Minute': minute,
            'Network_State': current_state,
            'Network_Impact_Factor': impact_factor,
            'Nominal_GPU_Util': gpu_util,
            'Effective_Throughput': effective_throughput
        })
        
    return pd.DataFrame(data)

if __name__ == "__main__":
    np.random.seed(42)
    df = generate_network_degradation(1000)

    os.makedirs('outputs', exist_ok=True)
    df.to_csv('outputs/network_sample.csv', index=False)

    # Plotting
    plt.figure(figsize=(12, 6))

    plt.plot(df['Minute'], df['Nominal_GPU_Util'], color='lightgrey', label='Nominal GPU Utilization (No Degradation)', alpha=0.8)
    plt.plot(df['Minute'], df['Effective_Throughput'], color='dodgerblue', label='Effective Throughput', linewidth=1.5)

    plt.fill_between(df['Minute'], 0, 100, where=df['Network_State']==0.7, color='yellow', alpha=0.2, label='Degraded State (0.85x)')
    plt.fill_between(df['Minute'], 0, 100, where=df['Network_State']==0.4, color='red', alpha=0.2, label='Severe State (0.60x)')

    plt.title('Performance Signal: Network Degradation via Markov State Transitions')
    plt.xlabel('Time (Minutes)')
    plt.ylabel('GPU Utilization / Throughput (%)')
    plt.legend(loc='lower left')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('outputs/network_plot.png')

    healthy = len(df[df['Network_State'] == 1.0])
    degraded = len(df[df['Network_State'] == 0.7])
    severe = len(df[df['Network_State'] == 0.4])

    print("Network Degradation Generation Complete.")
    print(f"Total Minutes: 1000")
    print(f"Healthy: {healthy} | Degraded: {degraded} | Severe: {severe}")
    print(f"Average Effective Throughput: {df['Effective_Throughput'].mean():.2f}% vs Nominal: {df['Nominal_GPU_Util'].mean():.2f}%")