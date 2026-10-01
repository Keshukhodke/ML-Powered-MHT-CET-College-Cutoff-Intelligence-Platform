import pandas as pd
import os

def create_college_branch_master(raw_dir, output_file):
    print("Creating College/Branch Master...")
    master_records = []
    
    columns_to_extract = ['College Code', 'College Name', 'Branch Code', 'Branch Name', 'Location']
    
    for root, dirs, files in os.walk(raw_dir):
        for f in files:
            if f.endswith('.csv'):
                filepath = os.path.join(root, f)
                try:
                    df = pd.read_csv(filepath)
                    # Some files might have slightly different names or missing columns, check:
                    missing = [c for c in columns_to_extract if c not in df.columns]
                    if missing:
                        continue
                        
                    subset = df[columns_to_extract].copy()
                    subset = subset.dropna(subset=['College Code', 'Branch Code'])
                    master_records.append(subset)
                except Exception as e:
                    print(f"Error reading {f}: {e}")
                    
    if master_records:
        master_df = pd.concat(master_records, ignore_index=True)
        # Drop duplicates
        master_df = master_df.drop_duplicates(subset=['College Code', 'Branch Code'])
        
        # Rename columns to match requested format
        master_df = master_df.rename(columns={
            'College Code': 'college_code',
            'College Name': 'college_name',
            'Branch Code': 'branch_code',
            'Branch Name': 'branch_name',
            'Location': 'district'
        })
        
        # Save to CSV
        master_df.to_csv(output_file, index=False)
        print(f"Successfully created master table with {len(master_df)} unique college-branch combinations at {output_file}")
    else:
        print("No records found.")

if __name__ == "__main__":
    raw_directory = r"d:\M_Tech_Data_Science\ML\ML_MINI_Project\College_Cap_Data\raw"
    output_filepath = r"d:\M_Tech_Data_Science\ML\ML_MINI_Project\College_Cap_Data\processed\college_branch_master.csv"
    create_college_branch_master(raw_directory, output_filepath)
