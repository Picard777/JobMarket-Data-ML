CREATE TABLE jobs (
    job_id INTEGER PRIMARY KEY,
    year INTEGER NOT NULL,
    title TEXT NOT NULL,
    experience_level TEXT,
    salary INTEGER,
    employee_residence TEXT,
    company_location TEXT,
    company_size TEXT,
    remote_ratio INTEGER
);
```
SANITY CHECK
```
SELECT COUNT(*) AS total_records,
    MIN(year) AS min_year,
    MAX(year) AS max_year,
    MIN(salary) AS min_salary,
    MAX(salary) AS max_salary,
    ROUND(AVG(salary), 0) AS avg_salary
FROM jobs;
```
Number of jobs postings over time
```
SELECT year,
    COUNT(*) AS job_count
FROM jobs
GROUP BY year
ORDER BY year;
```
Average salary over time
```
SELECT year,
    ROUND(AVG(salary), 0) AS avg_salary
FROM jobs
GROUP BY year
ORDER BY year;
```
Salaries vs experiance level
```
SELECT experience_level,
    COUNT(*) AS job_count,
    ROUND(AVG(salary), 0) AS avg_salary
FROM jobs
GROUP BY experience_level
ORDER BY avg_salary DESC;
```
Salary according to experiance in time
```
SELECT year,
    experience_level,
    ROUND(AVG(salary), 0) AS avg_salary
FROM jobs
GROUP BY year,
    experience_level
ORDER BY experience_level,
    year;
```
Salary vs company size
```
SELECT company_size,
    COUNT(*) AS job_count,
    ROUND(AVG(salary), 0) AS avg_salary
FROM jobs
GROUP BY company_size
ORDER BY avg_salary DESC;
``` 
Top company locations per postings count
```
SELECT company_location,
    COUNT(*) AS job_count
FROM jobs
GROUP BY company_location
ORDER BY job_count DESC
LIMIT 10;
```
Remote insight (residence =/= company location)
```
SELECT company_location,
    ROUND(AVG(salary), 0) AS avg_salary,
    COUNT(*) AS job_count
FROM jobs
GROUP BY company_location
HAVING COUNT(*) >= 50
ORDER BY avg_salary DESC;
```
Salary trend
```
SELECT CASE
        WHEN employee_residence = company_location THEN 'Same country'
        ELSE 'Different country'
    END AS work_type,
    COUNT(*) AS job_count,
    ROUND(AVG(salary), 0) AS avg_salary
FROM jobs
GROUP BY work_type;
```
Salary by experiance
``` CREATE VIEW vw_salary_trend AS
SELECT year,
    ROUND(AVG(salary), 0) AS avg_salary
FROM jobs
GROUP BY year;
CREATE VIEW vw_salary_by_experience AS
SELECT experience_level,
    ROUND(AVG(salary), 0) AS avg_salary
FROM jobs
GROUP BY experience_level;