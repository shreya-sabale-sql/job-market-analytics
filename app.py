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

