import os
import pandas as pd

def standardize_data(raw_dir, output_file):
    all_data = []
    
    column_mapping = {
        'College Code': 'college_code',
        'College Name': 'college_name',
        'Branch Code': 'branch_code',
        'Branch Name': 'branch_name',
        'Seat Section': 'seat_section',
        'Category': 'category',
        'Merit No.': 'merit_rank',
        'Percentile': 'percentile'
    }
    
    columns_to_keep = list(column_mapping.keys())
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    for root, dirs, files in os.walk(raw_dir):
        for f in files:
            if f.endswith('.csv'):
                filepath = os.path.join(root, f)
                
                # Extract year and cap from path
                rel_path = os.path.relpath(filepath, raw_dir)
                parts = rel_path.split(os.sep)
                
                if len(parts) >= 3:
                    academic_year = parts[0]
                    cap_round = parts[1]
                else:
                    print(f"Skipping {f} as it's not in year/cap structure")
                    continue
                
                # Check for updated 2024 CAP1 file
                if f == 'FE_CAP1_2024_Cutoff.csv' and 'FE_CAP1_2024_updated_Cutoff.csv' in files:
                    print(f"Skipping {f} because the updated version is present.")
                    continue
                
                try:
                    df = pd.read_csv(filepath)
                    
                    # Ensure expected columns are present
                    missing_cols = [c for c in columns_to_keep if c not in df.columns]
                    if missing_cols:
                        print(f"File {f} is missing columns: {missing_cols}")
                        continue
                    
                    df = df[columns_to_keep]
                    df = df.rename(columns=column_mapping)
                    
                    df['academic_year'] = academic_year
                    df['cap_round'] = cap_round
                    df['source_file'] = f
                    
                    # Reorder columns
                    df = df[['academic_year', 'cap_round', 'source_file', 'college_code', 'college_name', 
                             'branch_code', 'branch_name', 'category', 'seat_section', 
                             'merit_rank', 'percentile']]
                    
                    all_data.append(df)
                    print(f"Processed {academic_year} - {cap_round} - {f}")
                except Exception as e:
                    print(f"Error processing {f}: {e}")
                    
    if all_data:
        master_df = pd.concat(all_data, ignore_index=True)
        master_df.to_csv(output_file, index=False)
        print(f"Successfully created master dataset at {output_file} with {len(master_df)} records.")
    else:
        print("No data processed.")

if __name__ == "__main__":
    raw_directory = r"d:\M_Tech_Data_Science\ML\ML_MINI_Project\College_Cap_Data\raw"
    output_filepath = r"d:\M_Tech_Data_Science\ML\ML_MINI_Project\College_Cap_Data\data\raw\master_cap_cutoff_raw.csv"
    standardize_data(raw_directory, output_filepath)
