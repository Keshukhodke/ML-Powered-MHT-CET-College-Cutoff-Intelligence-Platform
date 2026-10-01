import os
import shutil
import re

base_dir = r"d:\M_Tech_Data_Science\ML\ML_MINI_Project\College_Cap_Data"
historical_dir = os.path.join(base_dir, "HIstrorical_Cap_Data")
raw_dir = os.path.join(base_dir, "raw")

# Create folders
folders = [
    "raw",
    "processed",
    "final",
    "models",
    "notebooks",
    "reports"
]
for f in folders:
    os.makedirs(os.path.join(base_dir, f), exist_ok=True)

years = ["2022-2023", "2023-2024", "2024-2025", "2025-2026", "2026-2027"]
caps = ["CAP1", "CAP2", "CAP3", "CAP4"]

for y in years:
    for c in caps:
        os.makedirs(os.path.join(raw_dir, y, c), exist_ok=True)

# mapping rules (rough estimation based on filenames)
def get_year_cap(filename):
    # Year logic
    if "2022" in filename: year = "2022-2023"
    elif "2023" in filename: year = "2023-2024"
    elif "2024" in filename: year = "2024-2025"
    elif "2025" in filename: year = "2025-2026"
    elif "2026" in filename: year = "2026-2027"
    else: year = "Unknown"
    
    # Cap logic
    if "CAP1" in filename: cap = "CAP1"
    elif "CAP2" in filename: cap = "CAP2"
    elif "CAP3" in filename: cap = "CAP3"
    elif "CAP4" in filename: cap = "CAP4"
    else: cap = "Unknown"
    
    return year, cap

if os.path.exists(historical_dir):
    for f in os.listdir(historical_dir):
        if not (f.endswith('.csv') or f.endswith('.xlsx')):
            continue
        year, cap = get_year_cap(f)
        if year != "Unknown" and cap != "Unknown":
            src = os.path.join(historical_dir, f)
            dst = os.path.join(raw_dir, year, cap, f)
            shutil.copy2(src, dst)
            print(f"Copied {f} to {year}/{cap}/")
        else:
            print(f"Could not determine year/cap for {f}, placing in raw root")
            src = os.path.join(historical_dir, f)
            dst = os.path.join(raw_dir, f)
            shutil.copy2(src, dst)
