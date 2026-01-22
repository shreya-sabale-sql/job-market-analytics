import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Job Market Analytics",
    layout="wide",
)

# ------------------ STYLING ------------------
st.markdown("""
<style>
body {
    background-color: #ffffff;
}
h1, h2, h3 {
    color: #0b1f3a;
}
.metric-box {
    background-color: #f5f7fa;
    padding: 15px;
    border-radius: 8px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ------------------ LOAD DATA ------------------
conn = sqlite3.connect("jobs.db")
data = pd.read_sql("SELECT * FROM jobs", conn)
conn.close()
# ------------------ HANDLE DATE SAFELY ------------------
if "date" in data.columns:
    data["date"] = pd.to_datetime(data["date"])
else:
    # If date column doesn't exist, create it using today's date
    data["date"] = pd.to_datetime("today")

# ------------------ HEADER ------------------
st.title("📊 Job Market Analytics Dashboard")
st.markdown("""
This dashboard analyzes **job market trends**, **salary distribution**,  
and **skill demand** using automated data collection and SQL-based analytics.
""")

# ------------------ SIDEBAR FILTERS ------------------
st.sidebar.header("🔍 Filter Data")

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

# ------------------ KPI METRICS ------------------
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Jobs", len(filtered))
col2.metric("Average Salary", f"₹{int(filtered['salary'].mean()):,}")
col3.metric("Top Skill",
             filtered["skills"]
             .str.split(",")
             .explode()
             .value_counts()
             .idxmax())

# ------------------ JOB TREND ------------------
st.subheader("📈 Job Posting Trend")

trend = filtered.groupby("date").size()
st.line_chart(trend)

# ------------------ SALARY ANALYSIS ------------------
st.subheader("💰 Salary Analysis")

salary_data = filtered["salary"]

col1, col2, col3 = st.columns(3)
col1.metric("Min Salary", f"₹{int(salary_data.min()):,}")
col2.metric("Max Salary", f"₹{int(salary_data.max()):,}")
col3.metric("Average Salary", f"₹{int(salary_data.mean()):,}")

fig, ax = plt.subplots()
ax.hist(salary_data, bins=8, edgecolor="black")
ax.set_xlabel("Salary (INR)")
ax.set_ylabel("Number of Jobs")
ax.set_title("Salary Distribution")

st.pyplot(fig)

# ------------------ SKILL DEMAND ------------------
st.subheader("🧠 Skill Demand Analysis")

skills = filtered["skills"].str.split(",").explode()
skill_counts = skills.value_counts()

st.bar_chart(skill_counts)

# ------------------ LOCATION ANALYSIS ------------------
st.subheader("📍 Location-wise Job Demand")
location_counts = filtered["location"].value_counts()
st.bar_chart(location_counts)

# ------------------ INSIGHTS ------------------
st.subheader("🧠 Key Insights")

st.markdown(f"""
• **Most demanded skill:** {skill_counts.idxmax()}  
• **Highest hiring location:** {location_counts.idxmax()}  
• **Salary range:** ₹{int(salary_data.min()):,} – ₹{int(salary_data.max()):,}  
• **Data updated automatically via GitHub Actions**
""")

# ------------------ FOOTER ------------------
st.markdown("---")
st.caption("Built with Python, SQL, Streamlit & GitHub Actions")

