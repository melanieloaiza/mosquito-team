import streamlit as st
import pandas as pd
import plotly.graph_objects as go 
import plotly.express as px

# Sample data loading
data = pd.read_csv("mosquitoteam/J06_No_Irrad.csv") 
data1 = pd.read_csv("mosquitoteam/J06_Irrad.csv")
data2 = pd.read_csv("mosquitoteam/WildType_Yaviza.csv")

st.title(" 🪰 Mosca Project " )
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
        st.write(
            "The distribution for males is mostly symmetric with a small left tail and three potential outliers: 285, 277, and 169. This suggests that for most males, "
            "the majority of WB_Arm1 values are closer to 227.5, with only a few values falling below that threshold.")

        st.write(
            "The distribution for females is mostly symmetric, with four potential outliers: 276, 166, 163, and 158. For most females, the majority of WB_Arm1 values are closer to 225.")
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

elif group == "J06_Irrad" :
    summary_male = data1[data1["J06_Irrad"] == "Male"]["WB_Arm1"].describe().reset_index()
    summary_male.columns = ["Statistic", "Male"]

    summary_female = data1[data1["J06_Irrad"] == "Female"]["WB_Arm1"].describe().reset_index()
    summary_female.columns = ["Statistic", "Female"]

    st.write("### J06_Irrad")
    group = st.radio("Select distribution:", ("WB_Arm1", "WB_Arm2"), index=0)
    if group == "WB_Arm1":
        colors = ['rgb(107,174,214)', 'rgb(255, 127, 14)']

        fig = go.Figure()

        for i, col in enumerate(data1["J06_Irrad"].unique()):
            subset = data1[data1["J06_Irrad"] == col]
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

        df = pd.DataFrame(data1)
        male_data = df[df["J06_Irrad"] == "Male"]
        female_data = df[df["J06_Irrad"] == "Female"]

        # Plot histogram for Male
        figMale = px.histogram(male_data, x="WB_Arm1", nbins=10, title="WB_Arm1 for Male")
        figMale.update_traces(marker_color='rgb(107,174,214)', marker_line_color='rgb(107,174,214)',
                              marker_line_width=1,
                              opacity=0.6)
        figMale.update_layout(xaxis_title="WB_Arm1", yaxis_title="Frequency")
        st.plotly_chart(figMale)

        # Plot histogram for Female
        figFemale = px.histogram(female_data, x="WB_Arm1", nbins=10, title="WB_Arm1 for Female")
        figFemale.update_traces(marker_color='rgb(255, 127, 14)', marker_line_color='rgb(255, 127, 14)',
                                marker_line_width=1,
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
    else:
        # Calculate summary statistics for "Male" and "Female" groups
        summary_male = data1[data1["J06_Irrad"] == "Male"]["WB_Arm2"].describe().reset_index()
        summary_male.columns = ["Statistic", "Male"]

        summary_female = data1[data1["J06_Irrad"] == "Female"]["WB_Arm2"].describe().reset_index()
        summary_female.columns = ["Statistic", "Female"]

        colors = ['rgb(107,174,214)', 'rgb(255, 127, 14)']
        fig = go.Figure()

        for i, col in enumerate(data1["J06_Irrad"].unique()):
            subset = data1[data1["J06_Irrad"] == col]
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

        df = pd.DataFrame(data1)
        male_data = df[df["J06_Irrad"] == "Male"]
        female_data = df[df["J06_Irrad"] == "Female"]

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
else :
    summary_male = data2[data2["WildType_Yaviza"] == "Male"]["WB_Arm1"].describe().reset_index()
    summary_male.columns = ["Statistic", "Male"]

    summary_female = data2[data2["WildType_Yaviza"] == "Female"]["WB_Arm1"].describe().reset_index()
    summary_female.columns = ["Statistic", "Female"]

    st.write("### WildType_Yaviza")
    group = st.radio("Select distribution:", ("WB_Arm1", "WB_Arm2"), index=0)
    if group == "WB_Arm1":
        colors = ['rgb(107,174,214)', 'rgb(255, 127, 14)']

        fig = go.Figure()

        for i, col in enumerate(data2["WildType_Yaviza"].unique()):
            subset = data2[data2["WildType_Yaviza"] == col]
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

        df = pd.DataFrame(data2)
        male_data = df[df["WildType_Yaviza"] == "Male"]
        female_data = df[df["WildType_Yaviza"] == "Female"]

        # Plot histogram for Male
        figMale = px.histogram(male_data, x="WB_Arm1", nbins=10, title="WB_Arm1 for Male")
        figMale.update_traces(marker_color='rgb(107,174,214)', marker_line_color='rgb(107,174,214)',
                              marker_line_width=1,
                              opacity=0.6)
        figMale.update_layout(xaxis_title="WB_Arm1", yaxis_title="Frequency")
        st.plotly_chart(figMale)

        # Plot histogram for Female
        figFemale = px.histogram(female_data, x="WB_Arm1", nbins=10, title="WB_Arm1 for Female")
        figFemale.update_traces(marker_color='rgb(255, 127, 14)', marker_line_color='rgb(255, 127, 14)',
                                marker_line_width=1,
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
    else:
        # Calculate summary statistics for "Male" and "Female" groups
        summary_male = data2[data2["WildType_Yaviza"] == "Male"]["WB_Arm2"].describe().reset_index()
        summary_male.columns = ["Statistic", "Male"]

        summary_female = data2[data2["WildType_Yaviza"] == "Female"]["WB_Arm2"].describe().reset_index()
        summary_female.columns = ["Statistic", "Female"]

        colors = ['rgb(107,174,214)', 'rgb(255, 127, 14)']
        fig = go.Figure()

        for i, col in enumerate(data2["WildType_Yaviza"].unique()):
            subset = data2[data2["WildType_Yaviza"] == col]
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

        df = pd.DataFrame(data2)
        male_data = df[df["WildType_Yaviza"] == "Male"]
        female_data = df[df["WildType_Yaviza"] == "Female"]

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
