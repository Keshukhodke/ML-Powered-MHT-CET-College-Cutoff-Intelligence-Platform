import pandas as pd
import os

print("Row counts in 2024 new files:")
for i, cap in enumerate(['CAP1', 'CAP2', 'CAP3']):
    f = f"d:\\M_Tech_Data_Science\\ML\\ML_MINI_Project\\College_Cap_Data\\raw\\2024-2025\\{cap}\\FE_{cap}_2024_Cutoff_{i+1}.csv"
    if os.path.exists(f):
        df = pd.read_csv(f)
        print(f"{cap}: {len(df)} rows")
    else:
        print(f"{cap}: File missing ({f})")
