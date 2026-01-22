

import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Job Market Analytics",
    layout="wide",
    page_icon="📊"
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
    background-color: #f4f6f9;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    border-left: 6px solid #0b1f3a;
}

.section {
    margin-top: 30px;
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
st.markdown("<h1>📊 Job Market Analytics Dashboard</h1>", unsafe_allow_html=True)
st.write(
    "Analyze job trends, salary patterns, and in-demand skills using real-time job data."
)


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
st.markdown("## 📌 Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="metric-box">
        <h3>Total Jobs</h3>
        <h2>{len(filtered)}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-box">
        <h3>Average Salary</h3>
        <h2>₹{int(filtered['salary'].mean()):,}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    top_skill = (
        filtered["skills"]
        .str.split(",")
        .explode()
        .value_counts()
        .idxmax()
    )

    st.markdown(
        f"""
        <div class="metric-box">
        <h3>Top Skill</h3>
        <h2>{top_skill}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )


# ------------------ JOB TREND ------------------
st.markdown("## 📈 Job Trends Over Time")

trend = filtered.groupby("date").size()

if len(trend) > 1:
    st.line_chart(trend)
else:
    st.info("Not enough data yet to show trend.")


# ------------------ SALARY ANALYSIS ------------------
st.markdown("## 💰 Salary Distribution")

fig, ax = plt.subplots()
ax.hist(filtered["salary"], bins=8, color="#0b1f3a", edgecolor="white")
ax.set_xlabel("Salary (INR)")
ax.set_ylabel("Job Count")

st.pyplot(fig)

# ------------------ SKILL DEMAND ------------------
st.markdown("## 🧠 Skill Demand")

skills = filtered["skills"].str.split(",").explode()
skill_counts = skills.value_counts()

st.bar_chart(skill_counts)


# ------------------ LOCATION ANALYSIS ------------------
st.subheader("📍 Location-wise Job Demand")
location_counts = filtered["location"].value_counts()
st.bar_chart(location_counts)

# ------------------ INSIGHTS ------------------
st.markdown("## 🧠 Key Insights")

st.success(
    f"""
    ✔ Highest demand skill: {skill_counts.idxmax()}  
    ✔ Highest paying location: {filtered['location'].value_counts().idxmax()}  
    ✔ Salary range: ₹{int(filtered['salary'].min()):,} – ₹{int(filtered['salary'].max()):,}
    """
)


# ------------------ FOOTER ------------------
st.markdown("---")
st.caption("Built with Python, SQL, Streamlit & GitHub Actions | Data Analytics Project")



