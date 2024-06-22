import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Sample data loading
data = pd.read_csv("J06_No_Irrad.csv")

st.sidebar.write("Mosquito team app")
group = st.sidebar.radio("Select Group:", ("J06_No_Irrad", "J06_Irrad", "WildType_Yaviza"), index=0)

# Calculate summary statistics for "Male" and "Female" groups
summary_male = data[data["J06_No_Irrad"] == "Male"]["WB_Arm1"].describe().reset_index()
summary_male.columns = ["Statistic", "Male"]

summary_female = data[data["J06_No_Irrad"] == "Female"]["WB_Arm1"].describe().reset_index()
summary_female.columns = ["Statistic", "Female"]

# Merge the summaries into a single DataFrame for display
summary_table = pd.merge(summary_male, summary_female, on="Statistic", suffixes=('_Male', '_Female'))

# Display the summary table
#st.sidebar.write(summary_table)

st.write("### J06_No_Irrad Box Plot by Sex")
st.write("WB_Arm1")
fig = go.Figure()

fig.add_trace(go.Box(
    y=data["WB_Arm1"],
    x=data["J06_No_Irrad"],
    name="Whiskers and Outliers",
    boxpoints='outliers', # only outliers
    marker_color='rgb(107,174,214)',
    line_color='rgb(107,174,214)'
))

st.plotly_chart(fig)
st.write(summary_table)