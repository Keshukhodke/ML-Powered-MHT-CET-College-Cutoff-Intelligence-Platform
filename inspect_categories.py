import pandas as pd
import os

raw_dir = r"d:\M_Tech_Data_Science\ML\ML_MINI_Project\College_Cap_Data\raw"

def inspect_year_cap(year, cap):
    path = os.path.join(raw_dir, year, cap)
    if not os.path.exists(path):
        print(f"Path does not exist: {path}")
        return
        
    for f in os.listdir(path):
        if f.endswith('.csv'):
            print(f"\n--- Inspecting {year} {cap} -> {f} ---")
            df = pd.read_csv(os.path.join(path, f))
            # Find rows where category seems invalid (long length)
            invalid_cats = df[df['Category'].astype(str).str.len() > 10]['Category'].dropna().unique()
            print(f"Some long categories: {invalid_cats[:10]}")
            
            # Let's show a few rows of these invalid categories
            bad_rows = df[df['Category'].isin(invalid_cats)].head(3)
            print("Sample bad rows:")
            print(bad_rows[['College Code', 'Branch Code', 'Category', 'Merit No.']].to_string())

inspect_year_cap("2022-2023", "CAP1")
inspect_year_cap("2023-2024", "CAP1")
