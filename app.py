import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

st.set_page_config(page_title="Job Market Analytics", layout="wide")

# Connect to DB
conn = sqlite3.connect("jobs.db")
query = "SELECT * FROM jobs"
data = pd.read_sql(query, conn)

st.title("📊 Job Market Analytics Dashboard")

# Filters
st.sidebar.header("Filters")

job_filter = st.sidebar.multiselect(
    "Job Role",
    data["job_title"].unique(),
    default=data["job_title"].unique()
)

location_filter = st.sidebar.multiselect(
    "Location",
    data["location"].unique(),
    default=data["location"].unique()
)

filtered = data[
    (data["job_title"].isin(job_filter)) &
    (data["location"].isin(location_filter))
]

# Display
st.subheader("📄 Job Data")
st.dataframe(filtered)

# Skills
skills = filtered["skills"].str.split(",").explode()
st.subheader("🔥 In-demand Skills")
st.bar_chart(skills.value_counts())

# Salary
st.subheader("💰 Salary Distribution")
plt.figure()
plt.hist(filtered["salary"], bins=5)
st.pyplot(plt)

# Insights
st.subheader("🧠 Insights")
st.write("Top Skill:", skills.value_counts().idxmax())
st.write("Average Salary:", int(filtered["salary"].mean()))

data["date"] = pd.to_datetime(data["date"])
daily_jobs = data.groupby("date").size().reset_index(name="job_count")

#Chart
st.subheader("📈 Job Posting Trend Over Time")
st.line_chart(daily_jobs.set_index("date"))

#salarytrend
salary_trend = data.groupby("date")["salary"].mean().reset_index()
st.subheader("💰 Average Salary Trend")
st.line_chart(salary_trend.set_index("date"))

#skilldemand
skills = data["skills"].str.split(",").explode()
skill_counts = skills.value_counts()
st.subheader("🧠 Most In-Demand Skills")
st.bar_chart(skill_counts)

#locationdemand
location_counts = data["location"].value_counts()
st.subheader("📍 Job Demand by Location")
st.bar_chart(location_counts)

#dashboard
col1, col2, col3 = st.columns(3)

col1.metric("Total Jobs", len(data))
col2.metric("Avg Salary", int(data["salary"].mean()))
col3.metric("Top Skill", skill_counts.idxmax())

