import os
import requests
import pandas as pd
import sqlite3
from datetime import datetime

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

url = "https://api.adzuna.com/v1/api/jobs/in/search/1"

params = {
    "app_id": APP_ID,
    "app_key": APP_KEY,
    "results_per_page": 50,
    "what": "data analyst"
}

response = requests.get(url, params=params)

# ✅ Safety check
if response.status_code != 200:
    print("API Error:", response.text)
    exit()

data = response.json()

# ✅ Check if 'results' exists
if "results" not in data:
    print("API response does not contain job data.")
    print(data)
    exit()

jobs = []

for job in data["results"]:
    jobs.append({
        "job_title": job.get("title"),
        "company": job.get("company", {}).get("display_name"),
        "location": job.get("location", {}).get("display_name"),
        "salary": job.get("salary_max"),
        "skills": "Python, SQL",
        "date": datetime.today().strftime("%Y-%m-%d")
    })

df = pd.DataFrame(jobs)

conn = sqlite3.connect("jobs.db")
df.to_sql("jobs", conn, if_exists="append", index=False)
conn.close()

print("✅ Job data updated successfully")
