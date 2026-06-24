# Synthetic Signal Design

## Signal: Temperature
* **Inputs:** GPU Util, CPU Util, Memory Pressure
* **Output:** Estimated Temperature (°C)
* **Reason:** Public traces (like Microsoft Philly) systematically lack hardware telemetry due to NDA constraints. We derive physically plausible temperatures from utilization loads to test the downstream impact estimation pipeline.