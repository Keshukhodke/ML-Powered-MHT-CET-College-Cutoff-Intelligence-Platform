import pandas as pd
import os
import hashlib

def generate_record_id(row):
    key_string = f"{row.get('academic_year','')}_{row.get('cap_round','')}_{row.get('college_code','')}_{row.get('branch_code','')}_{row.get('category','')}_{row.get('seat_section','')}_{row.get('merit_rank','')}"
    return hashlib.md5(key_string.encode('utf-8')).hexdigest()[:12]

def clean_data(input_file, intermediate_file, final_file, quarantine_file):
    print(f"Loading raw data from {input_file}...")
    df = pd.read_csv(input_file)
    
    # Add record_id
    df['record_id'] = df.apply(generate_record_id, axis=1)
    
    # 1. Exact Duplicate
    exact_dupes_mask = df.duplicated(subset=[c for c in df.columns if c != 'record_id'], keep='first')
    df['is_exact_duplicate'] = exact_dupes_mask
    
    # 2. Potential duplicate groups (Business Key)
    duplicate_cols = ["academic_year", "cap_round", "college_code", "branch_code", "category", "seat_section"]
    potential_dupes = df.duplicated(subset=duplicate_cols, keep=False)
    df['is_potential_duplicate'] = potential_dupes
    
    # 3. Category Audit & Normalization
    df['category_status'] = 'VALID'
    
    # Standardize missing categories
    df.loc[df['category'].isna(), 'category_status'] = 'MISSING_SOURCE_CHECK'
    
    # Identify invalid text (allowing hyphens for categories like MI-MH, I-Non)
    invalid_text_mask = df['category'].notna() & (~df['category'].astype(str).str.match(r'^[A-Za-z0-9\-]+$') | (df['category'].astype(str).str.len() > 15))
    df.loc[invalid_text_mask, 'category_status'] = 'INVALID_TEXT_SOURCE_CHECK'
    
    # 3b. Source-level Recovery
    # Forward and Backward fill category within valid source groups (college, branch, seat_section)
    print("Attempting source-level category recovery...")
    df['category_clean'] = df['category']
    df.loc[df['category_status'].str.contains('SOURCE_CHECK'), 'category_clean'] = pd.NA
    
    df['category_clean'] = df.groupby(['academic_year', 'cap_round', 'source_file', 'college_code', 'branch_code', 'seat_section'])['category_clean'].ffill()
    df['category_clean'] = df.groupby(['academic_year', 'cap_round', 'source_file', 'college_code', 'branch_code', 'seat_section'])['category_clean'].bfill()
    
    # Update status for recovered ones
    recovered_mask = df['category_clean'].notna() & df['category_status'].str.contains('SOURCE_CHECK')
    df.loc[recovered_mask, 'category_status'] = 'RECOVERED'
    
    # Replace original category with the recovered one
    df['category'] = df['category_clean'].fillna(df['category'])
    df = df.drop(columns=['category_clean'])
    
    # Update status back for unrecovered ones to just be MISSING or INVALID_TEXT for the final report
    df.loc[df['category_status'] == 'MISSING_SOURCE_CHECK', 'category_status'] = 'MISSING'
    df.loc[df['category_status'] == 'INVALID_TEXT_SOURCE_CHECK', 'category_status'] = 'INVALID_TEXT'
    
    # 4. Branch Mapping
    if 'branch_name' in df.columns:
        # Step A: Explicit Standard Suffix Mapping for known missing cases
        branch_suffixes = {
            'Mechanical Engineering': '61210',
            'Computer Science and Engineering': '24210',
            'Mechatronics Engineering': '62410',
            'Artificial Intelligence and Data Science': '99510',
            'Electronics and Computer Engineering': '84410',
            'Electronics and Telecommunication Engg': '37210'
        }
        missing_branch_mask = df['branch_code'].isna() & df['college_code'].notna()
        for branch, suffix in branch_suffixes.items():
            mask = missing_branch_mask & (df['branch_name'] == branch)
            college_strs = df.loc[mask, 'college_code'].astype(str).str.replace(r'\.0$', '', regex=True)
            df.loc[mask, 'branch_code'] = college_strs + suffix
            
        # Step B: Dynamic mapping from existing valid rows
        missing_branch = df['branch_code'].isna() & df['branch_name'].notna()
        if missing_branch.any():
            valid_branches = df.dropna(subset=['branch_code'])
            mapping = valid_branches.groupby(['college_code', 'branch_name'])['branch_code'].first().to_dict()
            
            def map_branch(row):
                if pd.isna(row['branch_code']) and not pd.isna(row['branch_name']):
                    return mapping.get((row['college_code'], row['branch_name']), row['branch_code'])
                return row['branch_code']
                
            df['branch_code'] = df.apply(map_branch, axis=1)
    
    # 5. Rank Validation
    df['merit_rank'] = pd.to_numeric(df['merit_rank'], errors='coerce')
    
    # 6. Add data_quality_status
    def determine_status(row):
        issues = []
        if row['category_status'] not in ['VALID', 'RECOVERED']:
            issues.append('CHECK_CATEGORY')
        if pd.isna(row['branch_code']):
            issues.append('CHECK_BRANCH')
        if pd.isna(row['merit_rank']) or row['merit_rank'] <= 0:
            issues.append('CHECK_RANK')
            
        if len(issues) == 0:
            return 'VALID'
        elif len(issues) == 1:
            return issues[0]
        else:
            return 'MULTIPLE_ISSUES'
            
    df['data_quality_status'] = df.apply(determine_status, axis=1)
    
    # Save intermediate cleaning file
    os.makedirs(os.path.dirname(intermediate_file), exist_ok=True)
    df.to_csv(intermediate_file, index=False)
    print(f"Saved intermediate file to {intermediate_file}")
    
    # 7. Quarantine
    # Remove exact duplicates from final & quarantine datasets
    df_unique = df[~df['is_exact_duplicate']].copy()
    
    final_df = df_unique[df_unique['data_quality_status'] == 'VALID'].copy()
    
    # Save final
    os.makedirs(os.path.dirname(final_file), exist_ok=True)
    final_df.to_csv(final_file, index=False)
    print(f"Saved final data to {final_file} ({len(final_df)} records)")
    
    # Save specific quarantine files
    quarantine_dir = os.path.dirname(quarantine_file)
    os.makedirs(quarantine_dir, exist_ok=True)
    
    invalid_category_df = df_unique[df_unique['category_status'] == 'INVALID_TEXT']
    if not invalid_category_df.empty:
        invalid_category_df.to_csv(os.path.join(quarantine_dir, 'invalid_category.csv'), index=False)
        
    missing_category_df = df_unique[df_unique['category_status'] == 'MISSING']
    if not missing_category_df.empty:
        missing_category_df.to_csv(os.path.join(quarantine_dir, 'missing_category.csv'), index=False)
        
    missing_branch_df = df_unique[df_unique['branch_code'].isna()]
    if not missing_branch_df.empty:
        missing_branch_df.to_csv(os.path.join(quarantine_dir, 'missing_branch.csv'), index=False)
        
    invalid_rank_df = df_unique[pd.to_numeric(df_unique['merit_rank'], errors='coerce') <= 0]
    if not invalid_rank_df.empty:
        invalid_rank_df.to_csv(os.path.join(quarantine_dir, 'invalid_rank.csv'), index=False)
        
    potential_dupes_df = df_unique[df_unique['is_potential_duplicate']]
    if not potential_dupes_df.empty:
        potential_dupes_df.to_csv(os.path.join(quarantine_dir, 'potential_duplicates.csv'), index=False)
        
    quarantine_df = df_unique[df_unique['data_quality_status'] != 'VALID'].copy()
    quarantine_df.to_csv(quarantine_file, index=False)
    print(f"Saved general quarantined data to {quarantine_file} ({len(quarantine_df)} records)")

if __name__ == "__main__":
    base_dir = r"d:\M_Tech_Data_Science\ML\ML_MINI_Project\College_Cap_Data\data"
    input_filepath = os.path.join(base_dir, "raw", "master_cap_cutoff_raw.csv")
    intermediate_filepath = os.path.join(base_dir, "intermediate", "master_cap_cutoff_cleaning.csv")
    final_filepath = os.path.join(base_dir, "final", "master_cap_cutoff_final.csv")
    quarantine_filepath = os.path.join(base_dir, "quarantine", "quarantine_records.csv")
    
    clean_data(input_filepath, intermediate_filepath, final_filepath, quarantine_filepath)
