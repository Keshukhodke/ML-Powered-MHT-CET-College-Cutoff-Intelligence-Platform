import pandas as pd
import os

def create_historical_dataset(input_file, output_file):
    print(f"Loading cleaned data from {input_file}...")
    df = pd.read_csv(input_file)
    
    # Create a new column that combines academic year and cap round
    # Example: '2022-2023_CAP1' -> we can just use the start year '2022_CAP1'
    df['year_cap'] = df['academic_year'].str.slice(0, 4) + '_' + df['cap_round']
    
    # We want to pivot 'percentile' values
    print("Pivoting data to create historical dataset...")
    pivot_df = df.pivot_table(
        index=['college_code', 'branch_code', 'category', 'seat_section'],
        columns='year_cap',
        values='percentile',
        aggfunc='first' # Since we already removed duplicates, 'first' is fine
    ).reset_index()
    
    # Flatten the columns
    pivot_df.columns.name = None
    
    # Optionally, we could merge in the college and branch names from the master
    # But the prompt says Example: college_code, branch_code, category, seat_section, 2022_CAP1...
    
    pivot_df.to_csv(output_file, index=False)
    print(f"Historical dataset created successfully at {output_file} with shape {pivot_df.shape}")

if __name__ == "__main__":
    input_filepath = r"d:\M_Tech_Data_Science\ML\ML_MINI_Project\College_Cap_Data\processed\master_cap_cutoff_cleaned.csv"
    output_filepath = r"d:\M_Tech_Data_Science\ML\ML_MINI_Project\College_Cap_Data\processed\historical_cutoff_dataset.csv"
    create_historical_dataset(input_filepath, output_filepath)
