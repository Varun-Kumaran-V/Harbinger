"""
===============================================================================
Harbinger: Temperature Signal Generator

Purpose
-------
Generates synthetic GPU temperature telemetry using a physics-inspired
heuristic model. The generator estimates operating temperature from GPU
utilization, CPU utilization, and memory pressure while introducing minor
thermal variance to emulate realistic environmental fluctuations.

Inputs
------
Function Inputs
---------------
- gpu_util : float
    GPU utilization percentage.

- cpu_util : float
    CPU utilization percentage.

- mem_pressure : float
    GPU memory utilization percentage.

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
- outputs/sample_output.csv
- outputs/temperature_plot.png

Returned Values
---------------
generate_temperature(...)
    Returns a floating-point temperature estimate (°C) rounded to two
    decimal places.

Functions
---------
generate_temperature(gpu_util, cpu_util, mem_pressure)
    Computes a synthetic GPU temperature using weighted system utilization
    metrics and stochastic thermal variation.

Model
-----
Physics-Inspired Temperature Estimation Model

Model Components
----------------
Stage 1 : Base Idle Temperature
Stage 2 : GPU Utilization Contribution
Stage 3 : CPU Utilization Contribution
Stage 4 : Memory Pressure Contribution
Stage 5 : Thermal Noise Injection

Pipeline Role
-------------
Synthetic signal generator responsible for producing temperature-related
telemetry used during synthetic dataset construction by
build_training_dataset.py. The generated signals contribute to downstream
feature engineering, baseline evaluation, and Harbinger decision modelling.
===============================================================================
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_temperature(gpu_util, cpu_util, mem_pressure):
    """
    Generates a physically plausible synthetic GPU temperature using a
    physics-inspired heuristic model.
    """
    base_temp = 40.0
    gpu_factor = 0.45
    cpu_factor = 0.10
    mem_factor = 0.05
    
    # Add minor thermal variance (-1.0C to 1.0C)
    noise = np.random.uniform(-1.0, 1.0)
    
    temp = base_temp + (gpu_util * gpu_factor) + (cpu_util * cpu_factor) + (mem_pressure * mem_factor) + noise
    return round(temp, 2)

if __name__ == "__main__":
    # 1. Run basic tests
    print(f"Test 1 [10, 5, 10]: {generate_temperature(10, 5, 10)} C")
    print(f"Test 2 [90, 60, 80]: {generate_temperature(90, 60, 80)} C")
    
    print("\nGenerating 100 sample rows and plot...")
    
    # Ensure the outputs directory exists in your Harbinger folder
    os.makedirs("outputs", exist_ok=True)

    # 2. Generate 100 random sample rows
    np.random.seed(42) # Ensures the graph looks the same every time
    gpus = np.random.uniform(0, 100, 100)
    cpus = np.random.uniform(0, 100, 100)
    mems = np.random.uniform(0, 100, 100)
    temps = [generate_temperature(g, c, m) for g, c, m in zip(gpus, cpus, mems)]

    df = pd.DataFrame({
        'GPU_Util': np.round(gpus, 2), 
        'CPU_Util': np.round(cpus, 2), 
        'Mem_Pressure': np.round(mems, 2), 
        'Estimated_Temp': temps
    })
    
    # Save the CSV
    csv_path = 'outputs/sample_output.csv'
    df.to_csv(csv_path, index=False)
    print(f"Saved: {csv_path}")

    # 3. Generate and save the scatter plot
    plt.figure(figsize=(8, 5))
    plt.scatter(df['GPU_Util'], df['Estimated_Temp'], alpha=0.7, color='firebrick')
    plt.title('Synthetic Signal: GPU Utilization vs. Estimated Temperature')
    plt.xlabel('GPU Utilization (%)')
    plt.ylabel('Estimated Temperature (°C)')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    
    plot_path = 'outputs/temperature_plot.png'
    plt.savefig(plot_path)
    print(f"Saved: {plot_path}")