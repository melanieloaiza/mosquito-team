import streamlit as st
import pandas as pd
import plotly.graph_objects as go 
import plotly.express as px

# Sample data loading
data = pd.read_csv("mosquitoteam/J06_No_Irrad.csv") 


st.set_option('deprecation.showPyplotGlobalUse', False)

st.title(" 🦟 Mosca Project " )
st.write(
    """
    This app visualizes data from three groups: J06_No_Irrad, J06_Irrad, and WildType_Yaviza. It includes boxplots and histograms for the distributions of WB_Arm1 and WB_Arm2, accounting for sex, along with the corresponding statistical tables.
 """
)

group = st.sidebar.radio("Select Group:", ("J06_No_Irrad", "J06_Irrad", "WildType_Yaviza"), index=0)

if group == "J06_No_Irrad":
    # Calculate summary statistics for "Male" and "Female" groups
    summary_male = data[data["J06_No_Irrad"] == "Male"]["WB_Arm1"].describe().reset_index()
    summary_male.columns = ["Statistic", "Male"]

    summary_female = data[data["J06_No_Irrad"] == "Female"]["WB_Arm1"].describe().reset_index()
    summary_female.columns = ["Statistic", "Female"]

    # Merge the summaries into a single DataFrame for display
    # summary_table = pd.merge(summary_male, summary_female, on="Statistic", suffixes=('_Male', '_Female'))

    st.write("### J06_No_Irrad")
    group = st.radio("Select distribution:", ("WB_Arm1", "WB_Arm2"), index=0)
    if group == "WB_Arm1":
        colors = ['rgb(107,174,214)', 'rgb(255, 127, 14)']

        fig = go.Figure()

        for i, col in enumerate(data["J06_No_Irrad"].unique()):
            subset = data[data["J06_No_Irrad"] == col]
            fig.add_trace(go.Box(
                y=subset["WB_Arm1"],
                name=col,
                boxpoints='outliers',
                marker_color=colors[i % len(colors)],
                line_color=colors[i % len(colors)]
            ))

        fig.update_layout(
            title="WB_Arm1 by Sex",
            xaxis_title="Sex",
            yaxis_title="WB_Arm1"
        )
        st.plotly_chart(fig)

        df = pd.DataFrame(data)
        male_data = df[df["J06_No_Irrad"] == "Male"]
        female_data = df[df["J06_No_Irrad"] == "Female"]

        # Plot histogram for Male
        figMale = px.histogram(male_data, x="WB_Arm1", nbins=10, title="WB_Arm1 for Male")
        figMale.update_traces(marker_color='rgb(107,174,214)', marker_line_color='rgb(107,174,214)', marker_line_width=1,
                          opacity=0.6)
        figMale.update_layout(xaxis_title="WB_Arm1", yaxis_title="Frequency")
        st.plotly_chart(figMale)

        # Plot histogram for Female
        figFemale = px.histogram(female_data, x="WB_Arm1", nbins=10, title="WB_Arm1 for Female")
        figFemale.update_traces(marker_color='rgb(255, 127, 14)', marker_line_color='rgb(255, 127, 14)', marker_line_width=1,
                          opacity=0.6)
        fig.update_layout(xaxis_title="WB_Arm1", yaxis_title="Frequency")
        st.plotly_chart(figFemale)

        # Display the tables horizontally
        col1, col2 = st.columns(2)

        with col1:
            st.write("Summary for Males:")
            st.dataframe(summary_male.style.set_properties(**{'text-align': 'center'}))

        with col2:
            st.write("Summary for Females:")
            st.dataframe(summary_female.style.set_properties(**{'text-align': 'center'}))
    else :
        # Calculate summary statistics for "Male" and "Female" groups
        summary_male = data[data["J06_No_Irrad"] == "Male"]["WB_Arm2"].describe().reset_index()
        summary_male.columns = ["Statistic", "Male"]

        summary_female = data[data["J06_No_Irrad"] == "Female"]["WB_Arm2"].describe().reset_index()
        summary_female.columns = ["Statistic", "Female"]

        colors = ['rgb(107,174,214)', 'rgb(255, 127, 14)']
        fig = go.Figure()

        for i, col in enumerate(data["J06_No_Irrad"].unique()):
            subset = data[data["J06_No_Irrad"] == col]
            fig.add_trace(go.Box(
                y=subset["WB_Arm2"],
                name=col,
                boxpoints='outliers',
                marker_color=colors[i % len(colors)],
                line_color=colors[i % len(colors)]
            ))

        fig.update_layout(
            title="WB_Arm2 by Sex",
            xaxis_title="Sex",
            yaxis_title="WB_Arm2"
        )
        st.plotly_chart(fig)

        df = pd.DataFrame(data)
        male_data = df[df["J06_No_Irrad"] == "Male"]
        female_data = df[df["J06_No_Irrad"] == "Female"]

        # Plot histogram for Male
        figMale = px.histogram(male_data, x="WB_Arm2", nbins=10, title="WB_Arm2 for Male")
        figMale.update_traces(marker_color='rgb(107,174,214)', marker_line_color='rgb(107,174,214)',
                              marker_line_width=1,
                              opacity=0.6)
        figMale.update_layout(xaxis_title="WB_Arm2", yaxis_title="Frequency")
        st.plotly_chart(figMale)

        # Plot histogram for Female
        figFemale = px.histogram(female_data, x="WB_Arm2", nbins=10, title="WB_Arm2 for Female")
        figFemale.update_traces(marker_color='rgb(255, 127, 14)', marker_line_color='rgb(255, 127, 14)',
                                marker_line_width=1,
                                opacity=0.6)
        fig.update_layout(xaxis_title="WB_Arm2", yaxis_title="Frequency")
        st.plotly_chart(figFemale)

        # Display the tables horizontally
        col1, col2 = st.columns(2)

        with col1:
            st.write("Summary for Males:")
            st.dataframe(summary_male.style.set_properties(**{'text-align': 'center'}))

        with col2:
            st.write("Summary for Females:")
            st.dataframe(summary_female.style.set_properties(**{'text-align': 'center'})) 
