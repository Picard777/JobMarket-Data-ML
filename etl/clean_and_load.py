import pandas as pd
import sqlite3 

CANONICAL_COLUMNS = [
    "job_id",
    "year",
    "title",
    "experience_level",
    "salary",
    "employee_residence"
    "company location",
    "company_size",
    "remote_ratio",
    
]

def normalize_experiance(level: str) -> str:
    if pd.isna(level):
        return "Mid"
    
    level = str(level).strip().upper()
    
    mapping = {
        "EN": "Junior",
        "MI": "Mid",
        "SE": "Senior",
        "EX": "Senior",
    }
    return mapping.get(level, "Mid")

def normalize_title(title) -> str:
    if pd.isna(title):
        return "Unknown"
    return title.strip().title()

def main():
    df = pd.read_csv("data/raw_jobs.csv")
    
    clean_df = pd.DataFrame({
        "job_id": df.index,
        "year": df["work_year"],
        "title": df["job_title"].apply(normalize_title),
        "experience_level": df["experience_level"].apply(normalize_experiance),
        "salary": df["salary_in_usd"].astype(int),
        "employee_residence": df["employee_residence"].fillna("Unknown"),
        "company_location": df["company_location"].fillna("Unknown"),
        "company_size": df["company_size"].fillna("Unknown"),
        "remote_ratio": df["remote_ratio"].astype(int)
    })
    conn = sqlite3.connect("data/jobs.db")
    clean_df.to_sql("jobs", conn, if_exists="replace", index=False)
    conn.close()
    
    
    print(f"Loaded {len(clean_df)} records into SQLite database.")
    
if __name__ == "__main__":
    main()


    