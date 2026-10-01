import pandas as pd
import os

data = {
    "Standard Column": [
        "academic_year",
        "cap_round",
        "college_code",
        "college_name",
        "location",
        "district",
        "branch_code",
        "branch_name",
        "category",
        "seat_section",
        "merit_rank",
        "percentile",
        "sanctioned_intake",
        "available_seats",
        "vacancies",
        "vacancy_rate"
    ],
    "Meaning": [
        "CAP academic year",
        "CAP1/2/3/4",
        "Official institute code",
        "Institute name",
        "College location",
        "District",
        "Official course code",
        "Branch name",
        "Reservation category",
        "Seat type",
        "Closing merit number",
        "Closing percentile",
        "Sanctioned intake (future)",
        "Available seats (future)",
        "Vacancies (future)",
        "Vacancy rate (future)"
    ],
    "Type": [
        "string",
        "categorical",
        "string",
        "string",
        "string",
        "string",
        "string",
        "string",
        "categorical",
        "categorical",
        "numeric",
        "numeric",
        "numeric",
        "numeric",
        "numeric",
        "numeric"
    ]
}

df = pd.DataFrame(data)
df.to_excel(r"d:\M_Tech_Data_Science\ML\ML_MINI_Project\College_Cap_Data\data_dictionary.xlsx", index=False)
print("data_dictionary.xlsx created successfully.")
