import pandas as pd

df = pd.read_csv(r"d:\M_Tech_Data_Science\ML\ML_MINI_Project\College_Cap_Data\data\intermediate\master_cap_cutoff_cleaning.csv")

invalid_df = df[df['category_status'] == 'INVALID_TEXT']
print(f"Total INVALID_TEXT: {len(invalid_df)}")

# Check year breakdown
print("\nYear breakdown for INVALID_TEXT:")
print(invalid_df['academic_year'].value_counts())

# Show a few examples of INVALID_TEXT categories
print("\nExamples of INVALID_TEXT categories:")
print(invalid_df['category'].value_counts().head(10))

# Check if the real category might be hiding in seat_section
print("\nSeat Sections for these rows:")
print(invalid_df['seat_section'].value_counts().head(10))

# Check missing categories breakdown
missing_df = df[df['category_status'] == 'MISSING']
print(f"\nTotal MISSING: {len(missing_df)}")
print("\nYear breakdown for MISSING:")
print(missing_df['academic_year'].value_counts())

# Also check 2024 row count dropped
df_2024 = df[df['academic_year'] == '2024-2025']
print(f"\n2024-2025 total records: {len(df_2024)}")
print("2024-2025 cap rounds:")
print(df_2024['cap_round'].value_counts())
