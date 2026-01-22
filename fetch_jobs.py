import requests
import pandas as pd
import sqlite3
from datetime import datetime

APP_ID = "your_app_id"
APP_KEY = "your_api_key"

url = f"https://api.adzuna.com/v1/api/jobs/in/search/1"
params = {
    "app_id": APP_ID,
    "app_key": APP_KEY,
    "results_per_page": 50,
    "what": "data analyst",
    "content-type": "application/json"
}

response = requests.get(url, params=params)
data = response.json()

jobs = []

for job in data["results"]:
    jobs.append({
        "job_title": job.get("title"),
        "company": job.get("company", {}).get("display_name"),
        "location": job.get("location", {}).get("display_name"),
        "salary": job.get("salary_max"),
        "skills": "Python, SQL",
        "date": datetime.today().date()
    })

df = pd.DataFrame(jobs)

conn = sqlite3.connect("jobs.db")
df.to_sql("jobs", conn, if_exists="append", index=False)
conn.close()

print("Jobs updated successfully!")
