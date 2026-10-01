import os
import pandas as pd
import json

base_dir = r"d:\M_Tech_Data_Science\ML\ML_MINI_Project\College_Cap_Data\raw"

columns_summary = {}

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith(".csv"):
            filepath = os.path.join(root, f)
            try:
                # Read just the first few rows to get columns
                df = pd.read_csv(filepath, nrows=5)
                cols = tuple(df.columns.tolist())
                
                rel_path = os.path.relpath(filepath, base_dir)
                
                if cols not in columns_summary:
                    columns_summary[cols] = []
                columns_summary[cols].append(rel_path)
            except Exception as e:
                print(f"Error reading {f}: {e}")

for cols, files in columns_summary.items():
    print(f"Columns: {cols}")
    print(f"Files: {len(files)}")
    for f in files:
        print(f"  - {f}")
    print("-" * 50)
