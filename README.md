## JobMarket – Data, Analytics & ML Project

End-to-end data project analyzing multi-year job market salary data, including
data cleaning, SQL analytics, machine learning, and an interactive dashboard.

The project focuses on clear data modeling, explainable analytics, and simple ML baselines rather than overengineering.

---

## Project Goals

- Clean and normalize a large, multi-year job market dataset
- Store data in a relational database (SQLite)
- Perform SQL-based analytics on salaries and job characteristics
- Train a baseline salary prediction model using PyTorch
- Visualize insights in an interactive Streamlit dashboard
- Keep the system simple, explainable, and reproducible

---

## Project Structure

```text
jobmarket/
├── data/
│   ├── raw_jobs.csv        # Original dataset
│   └── jobs.db             # SQLite database
│
├── etl/
│   └── clean_and_load.py   # Cleaning + loading pipeline
│
├── ml/
│   └── salary_model.py     # PyTorch regression model
│
├── app/
│   └── dashboard.py        # Streamlit dashboard
│
├── analytics/
│   └── queries.sql         # SQL analysis queries
│
├── requirements.txt
└── README.md
```

## Canonical Data Schema
All raw job posting data is normalized into the following canonical format
before being loaded into the database.

## Canonical Data Schema

| Field | Type | Description |
|------|------|-------------|
| job_id | INTEGER | Unique job identifier |
| year | INTEGER | The exact year of the job posting | 
| title | TEXT | Normalized job title |
| experience_level | TEXT | Inferred seniority level (Junior / Mid / Senior) |
| salary | INTEGER | Annual salary (normalized to a single value) |
| employee_residence | TEXT | Country of employee residence |
| company_location | TEXT | Country of company headquarters |
| company_size | TEXT | Company size category |
|remote_ratio | INTEGER | Remote work model |

## Data Pipeline
```
raw_jobs.csv
   ↓ clean_and_load.py
SQLite database (jobs.db)
   ↓
SQL analytics / ML / Dashboard
```

## SQL Analytics 

The project includes reusable SQL analyses such as:
	•	Salary vs experience level
	•	Salary trends over time
	•	Salary by company size
	•	Top company locations by job count
	•	Remote vs non-remote salary comparison
	•	Multi-year salary trends

All queries are stored in analytics/queries.sql.

## Machine Learning PyTorch

A baseline regression model is implemented in PyTorch to predict salaries.

Features:
•	Year (normalized)
•	Experience level (one-hot encoded)
•	Company size (one-hot encoded)

Model:
•	Linear regression implemented using nn.Linear
•	Optimizer: Adam
•	Loss: Mean Squared Error (MSE)
•	Evaluation metric: Mean Absolute Error (MAE)

The goal is model interpretability and pipeline correctness, not maximum accuracy.

## Interactive Dashboard

The Streamlit dashboard provides:
•	KPI overview (job count, average & median salary)
•	Salary trends over time
•	Salary vs experience level
•	Salary vs company size
•	Top company locations
•	Remote work insights
•	Interactive filters (year, experience level)

Run the dashboard
```
streamlit run app/dashboard.py

```

Built as a portfolio project to demonstrate skills in:
Data Engineering, SQL Analytics, Machine Learning, and Data Visualization.

Author Max/Picard777


