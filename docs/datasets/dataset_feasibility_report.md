# Dataset Feasibility Report: Microsoft Philly Trace

## Dataset Summary
The Microsoft Philly Trace is a 6.6 GB (uncompressed) log dataset containing details for 117,325 deep learning jobs and corresponding cluster hardware utilization metrics. 

## Known Issues
* **Trailing Commas:** The utilization CSV files (e.g., `cluster_gpu_util`) contain trailing commas on data rows but not on header rows. This causes standard `pd.read_csv()` parsing to fail. A custom chunked CSV loader will be required.
* **Memory Constraints:** The dataset is too large for naive in-memory ingestion. Attempting to load `cluster_job_log` via standard JSON methods caused a critical system RAM overflow. Strict chunked processing (e.g., `ijson`) is mandatory.

## Signals Available
* Job status (Pass, Failed, Killed)
* Job attempts / retry counts
* Per-minute GPU utilization
* Per-minute CPU utilization
* Per-minute Memory utilization (total and free)
* Machine inventory and GPU capacity mapping

## Signals Missing
* Hardware temperature telemetry
* ECC memory errors
* Specific checkpoint events
* Detailed node health metrics
* Network/switch telemetry

## Harbinger Impact
* **Can use directly:** Job outcome labels, base hardware utilization time series, and machine mappings.
* **Can derive:** Job failure history, platform retry patterns, and resource starvation indicators.
* **Must simulate:** Because temperature, ECC errors, and network telemetry are missing, these critical Harbinger failure signals must be artificially simulated and injected during later phases.