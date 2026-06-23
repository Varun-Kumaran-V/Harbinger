import pandas as pd
import json
import os

# Define paths
data_dir = './data/trace-data/'
docs_dir = './docs/datasets/'

print("--- PHILLY DATASET EXPLORATION ---")

# 1. cluster_job_log (JSON)
print("\n1. cluster_job_log")
with open(os.path.join(data_dir, 'cluster_job_log')) as f:
    job_data = json.load(f) 
    
job_df = pd.DataFrame(job_data)
print(f"Number of rows: {len(job_df)}")
print(f"Number of columns: {len(job_df.columns)}")
print(f"Column names: {list(job_df.columns)}")
print(f"Missing values:\n{job_df.isnull().sum()}")
if 'status' in job_df.columns:
    print(f"Job status values: {job_df['status'].unique()}")

# Helper function for CSV utilization files (Crash-proof version)
def inspect_util_csv(filename):
    print(f"\n--- {filename} ---")
    file_path = os.path.join(data_dir, filename)
    
    print("Raw Data Sample (First 3 lines):")
    try:
        with open(file_path, 'r') as f:
            for i in range(3):
                line = f.readline().strip()
                print(f"Line {i+1} ({len(line.split(','))} columns): {line}")
    except Exception as e:
        print(f"Error reading file: {e}")

# 2, 3, 4. Utilization Files (CSVs)
inspect_util_csv('cluster_gpu_util')
inspect_util_csv('cluster_cpu_util')
inspect_util_csv('cluster_mem_util')

# 5. cluster_machine_list
print("\n--- cluster_machine_list ---")
try:
    machine_df = pd.read_csv(os.path.join(data_dir, 'cluster_machine_list'), header=None)
    print(f"Columns: {list(machine_df.columns)}")
    print("Sample:")
    print(machine_df.head(3))
except Exception as e:
    print(f"Could not read as CSV. Error: {e}")

print("\n--- GENERATING EXCEL SCHEMA ---")
# Create the initial schema dictionary structure
schema_columns = ['File', 'Column', 'Type', 'Description', 'Useful For Harbinger?']
schema_data = [
    ['cluster_job_log', 'status', 'string', 'The final state of the job (Pass/Failed/Killed)', ''],
    ['cluster_gpu_util', '0', 'int', 'Likely the machine ID or timestamp', ''],
]

schema_df = pd.DataFrame(schema_data, columns=schema_columns)

# Export to Excel
excel_path = os.path.join(docs_dir, 'philly_schema_dictionary.xlsx')
schema_df.to_excel(excel_path, index=False)

print(f"Deliverable created successfully at: {excel_path}")