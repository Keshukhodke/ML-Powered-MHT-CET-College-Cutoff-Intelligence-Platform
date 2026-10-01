import pandas as pd
import os

filepath = r"d:\M_Tech_Data_Science\ML\ML_MINI_Project\College_Cap_Data\raw\2022-2023\CAP1\FE_CAP1_2022_Cutoff.csv"

with open(filepath, 'r') as f:
    lines = f.readlines()
    
# Let's see rows 70 to 85, where the sample bad rows were found
print("Raw CSV lines around 70-85:")
for i in range(70, 85):
    print(f"Line {i}: {lines[i].strip()}")
