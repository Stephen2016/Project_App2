import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import date

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(layout="wide")

# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_csv("TOCHUKWU.csv")

# Convert date columns
df["Start date"] = pd.to_datetime(df["Start date"])
df["End date"] = pd.to_datetime(df["End date"])

# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.title("User Profile")
st.sidebar.write("Ani Tochukwu Stephen")
st.sidebar.write("Data Analyst")

st.sidebar.divider()
st.sidebar.header("Filters")

# Get correct min/max dates from dataset
min_date = df["Start date"].min().date()
max_date = df["Start date"].max().date()

states = st.sidebar.multiselect(
    "Select State(s)",
    options=sorted(df["State"].dropna().unique())
)

start_date = st.sidebar.date_input("Start Date", value=min_date)
end_date = st.sidebar.date_input("End Date", value=max_date)

# ----------------------------
# FILTER DATA
# ----------------------------
filtered_df = df.copy()

if states:
    filtered_df = filtered_df[filtered_df["State"].isin(states)]

filtered_df = filtered_df[
    (filtered_df["Start date"] >= pd.to_datetime(start_date)) &
    (filtered_df["Start date"] <= pd.to_datetime(end_date))
]

# Stop if no data
if filtered_df.empty:
    st.warning("No data available for selected filters. Adjust your filters.")
    st.stop()

# Create duration column
filtered_df["duration"] = (filtered_df["End date"] - filtered_df["Start date"]).dt.days

# ----------------------------
# TITLE
# ----------------------------
st.title("Incident Analysis Dashboard")

st.write("### Active Filters")
st.write(f"States: {states if states else 'All'}")
st.write(f"Date Range: {start_date} to {end_date}")

# ----------------------------
# Q1
# ----------------------------
st.subheader("Question 1: Which states recorded the highest number of deaths?")

state_deaths = filtered_df.groupby("State")["Number of deaths"].sum().sort_values(ascending=False)
st.bar_chart(state_deaths)

st.info("""
Insight:
States with the highest total deaths are the most affected areas.
This may indicate higher conflict intensity, population exposure,
or poor emergency response systems in those regions.
""")
# ----------------------------
# Q2
# ----------------------------
st.subheader("Question 2: Which incidents caused the most deaths?")

incident_deaths = filtered_df.groupby("Incident")["Number of deaths"].sum().sort_values(ascending=False)
st.bar_chart(incident_deaths)

st.info("""
Insight:
Incident types with the highest total deaths represent the most dangerous events.
These incidents contribute the largest share of fatalities and may require stronger
safety measures, policy intervention, and prevention strategies to reduce future losses.
""")

# ----------------------------
# Q3
# ----------------------------
st.subheader("Question 3: Duration vs Deaths")

fig, ax = plt.subplots()
ax.scatter(filtered_df["duration"], filtered_df["Number of deaths"])
ax.set_xlabel("Duration (days)")
ax.set_ylabel("Number of deaths")

st.pyplot(fig)

st.info("""
Insight:
This chart explores whether longer incidents lead to more deaths.
If the points trend upward, it suggests that incidents lasting longer
tend to result in higher fatalities. If the points are scattered with
no clear pattern, incident duration may not strongly influence the
number of deaths.
""")

# ----------------------------
# Q4
# ----------------------------
st.subheader("Question 4: Most frequent incidents")

incident_counts = filtered_df["Incident"].value_counts().nlargest(10)

fig, ax = plt.subplots()
ax.pie(incident_counts, labels=incident_counts.index, autopct='%1.1f%%')

st.pyplot(fig)

st.info("""
Insight:
This chart shows the proportion of each incident type in the dataset.
Incident types with larger percentages occur more frequently and may
represent the most common threats or risks in the affected areas.
Understanding these patterns helps prioritize prevention and response efforts.
""")

# ----------------------------
# Q5
# ----------------------------
st.subheader("Question 5: Longest incidents")

incident_duration = filtered_df.groupby("Incident")["duration"].mean().sort_values(ascending=False)
st.bar_chart(incident_duration)

st.info("""
Insight:
This chart shows the average duration of different incident types.
Incidents with longer durations may indicate more complex situations,
slower resolution processes, or extended emergency response efforts.
Shorter incidents may reflect quicker containment or less severe events.
""")

# ----------------------------
# Q6
# ----------------------------
st.subheader("Question 6: Deaths over time")

deaths_over_time = filtered_df.groupby(filtered_df["Start date"].dt.year)["Number of deaths"].sum()
st.line_chart(deaths_over_time)

st.info("""
Insight:
This chart shows the yearly trend of deaths over time. An increasing trend
may indicate worsening conditions or rising incident severity, while a
declining trend may suggest improvements in safety, security, or emergency
response efforts.
""")

# ----------------------------
# Q7
# ----------------------------
st.subheader("Question 7: States with most incidents")

state_incidents = filtered_df["State"].value_counts()
st.bar_chart(state_incidents)

st.info("""
Insight:
This chart shows how incidents are distributed across different states.
States with the highest number of incidents experience more frequent
events, which may indicate higher risk levels or greater exposure to
conflict or hazardous situations.
""")

# ----------------------------
# Q8
# ----------------------------
st.subheader("Question 8: Death share by state")

state_death_share = filtered_df.groupby("State")["Number of deaths"].sum().nlargest(10)

fig, ax = plt.subplots()
ax.pie(state_death_share, labels=state_death_share.index, autopct='%1.1f%%')

st.pyplot(fig)

st.info("""
Insight:
This chart shows the proportion of total deaths contributed by the top
10 states. States with larger slices account for a greater share of the
overall fatalities, indicating that deaths are concentrated in a few
regions rather than evenly distributed across all states.
""")

# ----------------------------
# Q9
# ----------------------------
st.subheader("Question 9: Lowest deaths by state")

lowest_deaths = filtered_df.groupby("State")["Number of deaths"].sum().sort_values()
st.bar_chart(lowest_deaths)

st.info("""
Insight:
States with the lowest number of deaths appear to be less affected by
fatal incidents. This may indicate lower incident severity, fewer events,
or better safety and emergency response systems in those regions.
""")

# ----------------------------
# Q10
# ----------------------------
st.subheader("Question 10: Incident duration comparison")

incident_duration = filtered_df.groupby("Incident")["duration"].mean().sort_values(ascending=False)
st.bar_chart(incident_duration)

st.info("""
Insight:
This chart shows the average duration of different incident types.
Incident types with longer average durations may involve more complex
situations or prolonged responses, while incidents with shorter durations
are likely resolved more quickly.
""")
