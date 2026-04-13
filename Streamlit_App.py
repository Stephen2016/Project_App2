import pandas as pd
import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt


from datetime import date

df = pd.read_csv("TOCHUKWU.csv")

# User profile
st.sidebar.title("User Profile")
st.sidebar.write("Ani Tochukwu Stephen")
st.sidebar.write("Data Analyst")

st.sidebar.divider()

# Filters
st.sidebar.header("Filters")

selected_states = st.sidebar.multiselect(
    "Select State(s)",
    df["State"].unique()
)



# Start date
start_date = st.sidebar.date_input("Start Date", value=date(2026, 1, 1))

# End date
end_date = st.sidebar.date_input("End Date", value=date.today())

# Display selections in main app
#st.write("### Selected Filters")
#st.write(f"**State:** {state}")
#st.write(f"**Start Date:** {start_date}")
#st.write(f"**End Date:** {end_date}")

st.set_page_config(layout="wide")

st.title("Incident Analysis Dashboard")

# Q1
st.subheader("Question 1: Which states recorded the highest number of deaths?")

state_deaths = df.groupby("State")["Number of deaths"].sum().sort_values(ascending=False)

st.subheader("Deaths by State")
st.bar_chart(state_deaths)

st.info("""
Insight:
States with the highest total deaths are the most affected areas.
This may indicate higher conflict intensity, population exposure,
or poor emergency response systems in those regions.
""")
 

#Q2
st.subheader("Question 2: Which incidents caused the most deaths?")

incident_deaths = df.groupby("Incident")["Number of deaths"].sum().sort_values(ascending=False)

st.subheader("Deaths by Incident Type")
st.bar_chart(incident_deaths)

st.info("""
Insight:
Incident types with the highest total deaths represent the most dangerous events.
These incidents contribute the largest share of fatalities and may require stronger
safety measures, policy intervention, and prevention strategies to reduce future losses.
""")

#Q3
st.subheader("Question 3: What is the duration of incidents and how does it relate to deaths?")

df["duration"] = (pd.to_datetime(df["End date"]) - pd.to_datetime(df["Start date"])).dt.days

fig, ax = plt.subplots()
ax.scatter(df["duration"], df["Number of deaths"])

st.subheader("Incident Duration vs Deaths")
st.pyplot(fig)

st.info("""
Insight:
This chart explores whether longer incidents lead to more deaths.
If the points trend upward, it suggests that incidents lasting longer
tend to result in higher fatalities. If the points are scattered with
no clear pattern, incident duration may not strongly influence the
number of deaths.
""")

#Q4
st.subheader("Question 4: Which incidents occur most frequently?")

incident_counts = df["Incident"].value_counts()

# Select top 10 most frequent incidents
top_incidents = incident_counts.nlargest(10)

fig, ax = plt.subplots()
ax.pie(top_incidents, labels=top_incidents.index, autopct='%1.1f%%')

st.subheader("Top 10 Most Frequent Incident Types")
st.pyplot(fig)

st.info("""
Insight:
This chart shows the proportion of each incident type in the dataset.
Incident types with larger percentages occur more frequently and may
represent the most common threats or risks in the affected areas.
Understanding these patterns helps prioritize prevention and response efforts.
""")

#Q5
st.subheader("Question 5: Which incidents last the longest?")

incident_duration = df.groupby("Incident")["duration"].mean()

st.subheader("Average Duration by Incident Type")
st.bar_chart(incident_duration)

st.info("""
Insight:
This chart shows the average duration of different incident types.
Incidents with longer durations may indicate more complex situations,
slower resolution processes, or extended emergency response efforts.
Shorter incidents may reflect quicker containment or less severe events.
""")

#Q6
st.subheader("Question 6: How have deaths changed over time?")

df["Start date"] = pd.to_datetime(df["Start date"])
deaths_over_time = df.groupby(df["Start date"].dt.year)["Number of deaths"].sum()

st.subheader("Deaths Over Time")
st.line_chart(deaths_over_time)

st.info("""
Insight:
This chart shows the yearly trend of deaths over time. An increasing trend
may indicate worsening conditions or rising incident severity, while a
declining trend may suggest improvements in safety, security, or emergency
response efforts.
""")

#Q7
st.subheader("Question 7: Which state has the highest number of incidents?")

state_incidents = df["State"].value_counts()

st.subheader("Number of Incidents by State")
st.bar_chart(state_incidents)

st.info("""
Insight:
This chart shows how incidents are distributed across different states.
States with the highest number of incidents experience more frequent
events, which may indicate higher risk levels or greater exposure to
conflict or hazardous situations.
""")

#Q8
st.subheader("Question 8: What percentage of total deaths occurs in each state?")

# Aggregate deaths by state
state_death_share = df.groupby("State")["Number of deaths"].sum()

# Select top 10 states
top10_state_death_share = state_death_share.nlargest(10)

# Plot pie chart
fig, ax = plt.subplots()
ax.pie(top10_state_death_share, labels=top10_state_death_share.index, autopct='%1.1f%%')

st.subheader("Death Share by Top 10 States")
st.pyplot(fig)

st.info("""
Insight:
This chart shows the proportion of total deaths contributed by the top
10 states. States with larger slices account for a greater share of the
overall fatalities, indicating that deaths are concentrated in a few
regions rather than evenly distributed across all states.
""")

#Q9
st.subheader("Question 9: Which states have the lowest number of deaths?")

lowest_deaths = df.groupby("State")["Number of deaths"].sum().sort_values()

st.subheader("States with Lowest Deaths")
st.bar_chart(lowest_deaths)

st.info("""
Insight:
States with the lowest number of deaths appear to be less affected by
fatal incidents. This may indicate lower incident severity, fewer events,
or better safety and emergency response systems in those regions.
""")

#Q10
st.subheader("Question 10: Which incidents last the longest?")

incident_duration = df.groupby("Incident")["duration"].mean()

st.subheader("Average Duration by Incident Type")
st.bar_chart(incident_duration)

st.info("""
Insight:
This chart shows the average duration of different incident types.
Incident types with longer average durations may involve more complex
situations or prolonged responses, while incidents with shorter durations
are likely resolved more quickly.
""")
