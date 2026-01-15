import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Job Market Dashboard",
    layout="wide"
)

st.title("Job Market Analysis")
st.markdown("Multi-year job market insights based on structured salary data.")


@st.cache_data
def load_data():
    conn = sqlite3.connect("data/jobs.db")
    df = pd.read_sql("SELECT * FROM jobs", conn)
    conn.close()
    return df

df = load_data()


st.sidebar.header("Filters")

years = sorted(df["year"].unique())
selected_years = st.sidebar.multiselect(
    "Select years",
    years,
    default=years
)

experience_levels = sorted(df["experience_level"].unique())
selected_experience = st.sidebar.multiselect(
    "Experience level",
    experience_levels,
    default=experience_levels
)

filtered_df = df[
    (df["year"].isin(selected_years)) &
    (df["experience_level"].isin(selected_experience))
]

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total job offers",
    f"{len(filtered_df):,}"
)

col2.metric(
    "Average salary (USD)",
    f"{int(filtered_df['salary'].mean()):,}"
)

col3.metric(
    "Median salary (USD)",
    f"{int(filtered_df['salary'].median()):,}"
)

st.divider()

st.subheader("Average salary over time")

salary_trend = (
    filtered_df
    .groupby("year")["salary"]
    .mean()
    .reset_index()
)

fig, ax = plt.subplots()
ax.plot(salary_trend["year"], salary_trend["salary"], marker="o")
ax.set_xlabel("Year")
ax.set_ylabel("Average salary (USD)")
st.pyplot(fig)


st.subheader("Salary by experience level")

salary_exp = (
    filtered_df
    .groupby("experience_level")["salary"]
    .mean()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots()
salary_exp.plot(kind="bar", ax=ax)
ax.set_ylabel("Average salary (USD)")
ax.set_xlabel("Experience level")
st.pyplot(fig)


st.subheader("Salary by company size")

salary_size = (
    filtered_df
    .groupby("company_size")["salary"]
    .mean()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots()
salary_size.plot(kind="bar", ax=ax)
ax.set_ylabel("Average salary (USD)")
ax.set_xlabel("Company size")
st.pyplot(fig)


with st.expander("Show raw data"):
    st.dataframe(filtered_df.head(100))
    
    
def load_sql(query: str) -> pd.DataFrame:
    conn = sqlite3.connect("data/jobs.db")
    df = pd.read_sql(query, conn)
    conn.close()
    return df

st.subheader("Salaries vs Experience Level")

df_exp = load_sql("""
SELECT experience_level,
       COUNT(*) AS job_count,
       ROUND(AVG(salary), 0) AS avg_salary
FROM jobs
GROUP BY experience_level
ORDER BY avg_salary DESC;
""")

st.bar_chart(df_exp.set_index("experience_level")["avg_salary"])
st.dataframe(df_exp)

st.subheader("Salary by Experience Level Over Time")

df_exp_time = load_sql("""
SELECT year,
       experience_level,
       ROUND(AVG(salary), 0) AS avg_salary
FROM jobs
GROUP BY year, experience_level
ORDER BY experience_level, year;
""")

st.line_chart(
    df_exp_time.pivot(
        index="year",
        columns="experience_level",
        values="avg_salary"
    )
)

st.subheader("Salary vs Company Size")

df_size = load_sql("""
SELECT company_size,
       COUNT(*) AS job_count,
       ROUND(AVG(salary), 0) AS avg_salary
FROM jobs
GROUP BY company_size
ORDER BY avg_salary DESC;
""")

st.bar_chart(df_size.set_index("company_size")["avg_salary"])
st.dataframe(df_size)

st.subheader("Top Company Locations by Job Count")

df_locations = load_sql("""
SELECT company_location,
       COUNT(*) AS job_count
FROM jobs
GROUP BY company_location
ORDER BY job_count DESC
LIMIT 10;
""")

st.bar_chart(df_locations.set_index("company_location")["job_count"])
st.dataframe(df_locations)


st.subheader("Salary by Company Location (Min 50 postings)")

df_loc_salary = load_sql("""
SELECT company_location,
       ROUND(AVG(salary), 0) AS avg_salary,
       COUNT(*) AS job_count
FROM jobs
GROUP BY company_location
HAVING COUNT(*) >= 50
ORDER BY avg_salary DESC;
""")

st.bar_chart(df_loc_salary.set_index("company_location")["avg_salary"])
st.dataframe(df_loc_salary)


st.subheader("Remote Work Insight")

df_remote = load_sql("""
SELECT CASE
        WHEN employee_residence = company_location THEN 'Same country'
        ELSE 'Different country'
       END AS work_type,
       COUNT(*) AS job_count,
       ROUND(AVG(salary), 0) AS avg_salary
FROM jobs
GROUP BY work_type;
""")

st.bar_chart(df_remote.set_index("work_type")["avg_salary"])
st.dataframe(df_remote)