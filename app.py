import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Job Market Analytics",
    page_icon="📊",
    layout="wide"
)

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
body {
    background-color: #ffffff;
}
h1, h2, h3 {
    color: #0b1f3a;
}
.card {
    background-color: #f7f9fc;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
    text-align: center;
}
.section {
    margin-top: 40px;
}
.small-text {
    color: #6c757d;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ LOAD DATA ------------------
conn = sqlite3.connect("jobs.db")
data = pd.read_sql("SELECT * FROM jobs", conn)
conn.close()

if "date" not in data.columns:
    data["date"] = pd.to_datetime("today")
else:
    data["date"] = pd.to_datetime(data["date"])

# ------------------ HEADER ------------------
st.markdown("## 📊 Job Market Analytics Dashboard")
st.markdown(
    "<span class='small-text'>Real-time analysis of job trends, salaries and in-demand skills</span>",
    unsafe_allow_html=True
)

# ------------------ SIDEBAR ------------------
st.sidebar.header("🔍 Filters")

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

# ------------------ KPI CARDS ------------------
st.markdown("### 📌 Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="card">
        <h3>Total Jobs</h3>
        <h2>{len(filtered)}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
        <h3>Average Salary</h3>
        <h2>₹{int(filtered['salary'].mean()):,}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    top_skill = (
        filtered["skills"]
        .str.split(",")
        .explode()
        .value_counts()
        .idxmax()
    )
    st.markdown(f"""
    <div class="card">
        <h3>Top Skill</h3>
        <h2>{top_skill}</h2>
    </div>
    """, unsafe_allow_html=True)

# ------------------ TABS ------------------
tab1, tab2, tab3 = st.tabs(["📈 Trends", "💰 Salaries", "🧠 Skills"])

# -------- TAB 1 --------
with tab1:
    st.subheader("Job Posting Trend")
    trend = filtered.groupby("date").size()

    if len(trend) > 1:
        st.line_chart(trend)
    else:
        st.info("Not enough data to show trends yet.")

# -------- TAB 2 --------
with tab2:
    st.subheader("Salary Distribution")

    fig, ax = plt.subplots()
    ax.hist(filtered["salary"], bins=8, color="#0b1f3a", edgecolor="white")
    ax.set_xlabel("Salary (INR)")
    ax.set_ylabel("Job Count")

    st.pyplot(fig)

# -------- TAB 3 --------
with tab3:
    st.subheader("Skill Demand")

    skills = filtered["skills"].str.split(",").explode()
    st.bar_chart(skills.value_counts())

# ------------------ INSIGHTS ------------------
st.markdown("### 🧠 Insights")

st.success(
    f"""
    ✔ Most demanded skill: **{skills.value_counts().idxmax()}**  
    ✔ Highest hiring location: **{filtered['location'].value_counts().idxmax()}**  
    ✔ Salary range: ₹{int(filtered['salary'].min()):,} – ₹{int(filtered['salary'].max()):,}  
    """
)

# ------------------ FOOTER ------------------
st.markdown("---")
st.caption("Built with Python • SQL • Streamlit • GitHub Actions")
