import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy.stats import f_oneway
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import f

# Sample data loading
data = pd.read_csv("mosquitoteam/J06_No_Irrad.csv") 
data1 = pd.read_csv("mosquitoteam/J06_Irrad.csv")
data2 = pd.read_csv("mosquitoteam/WildType_Yaviza.csv")
data3 = pd.read_csv("mosquitoteam/groups.csv")

st.title(" 🦟 Mosca Project " )

group = st.sidebar.radio("Select Group:", ("J06_No_Irrad", "J06_Irrad", "WildType_Yaviza" , "Results" , "ANOVA"), index=0)

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

        st.write("ANOVA")
        # Convert 'J06_No_Irrad' to a categorical variable
        data['gender'] = pd.Categorical(data['J06_No_Irrad'])

        # Fit the ANOVA model
        model = ols('WB_Arm1 ~ gender', data=data).fit()

        # Display the summary of the model
        anova_table = sm.stats.anova_lm(model, typ=2)
        st.write(anova_table)

        st.write(
            """
            **Conclusion:**

            - Since the p-value (0.1075) is greater than the common significance level of 0.05, we do not reject the null hypothesis.
            - This suggests that there is no statistically significant difference in WB_Arm1 values between genders at the 5% significance level.
            - In other words, the variation in WB_Arm1 explained by gender is not significantly greater than the variation within the groups. The differences in WB_Arm1 values between males and females are likely due to random variation rather than a true difference in their means."""
        )

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

        st.write("ANOVA")
        # Convert 'J06_No_Irrad' to a categorical variable
        data['gender'] = pd.Categorical(data['J06_No_Irrad'])

        # Fit the ANOVA model
        model = ols('WB_Arm2 ~ gender', data=data).fit()

        # Display the summary of the model
        anova_table = sm.stats.anova_lm(model, typ=2)
        st.write(anova_table)

        st.write(
            """
            **Conclusion:**

            - Since the p-value (0.0213) is less than the common significance level of 0.05, we reject the null hypothesis.
            - This suggests that there is a statistically significant difference in WB_Arm2 values between genders at the 5% significance level.
            - In other words, the variation in WB_Arm2 explained by gender is significantly greater than the variation within the groups. This indicates that gender has a significant impact on WB_Arm2 values.""")

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

        st.write("#### ANOVA")
        data1['gender'] = pd.Categorical(data1['J06_Irrad'])
        # Fit the ANOVA model
        model = ols('WB_Arm1 ~ gender', data=data1).fit()
        # Display the summary of the model
        anova_table = sm.stats.anova_lm(model, typ=2)
        st.write(anova_table)

        st.write(
            """
            **Conclusion:**

            - Since the p-value (0.2518) is greater than the common significance level of 0.05, we do not reject the null hypothesis.
            - This suggests that there is no statistically significant difference in WB_Arm1 values between genders at the 5% significance level.
            - In other words, the variation in WB_Arm1 explained by gender is not significantly greater than the variation within the groups. The differences in WB_Arm1 values between males and females are likely due to random variation rather than a true difference in their means.""")

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

        st.write("#### ANOVA")
        data1['gender'] = pd.Categorical(data1['J06_Irrad'])
        # Fit the ANOVA model
        model = ols('WB_Arm2 ~ gender', data=data1).fit()
        # Display the summary of the model
        anova_table = sm.stats.anova_lm(model, typ=2)
        st.write(anova_table)

        st.write(
            """
            **Conclusion:**

            - Since the p-value (0.3922) is greater than the common significance level of 0.05, we do not reject the null hypothesis.
            - This suggests that there is no statistically significant difference in WB_Arm2 values between genders at the 5% significance level.
            - In other words, the variation in WB_Arm2 explained by gender is not significantly greater than the variation within the groups. The differences in WB_Arm2 values between males and females are likely due to random variation rather than a true difference in their means.""")

elif group == "WildType_Yaviza" :
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

        st.write("#### ANOVA")
        data2['gender'] = pd.Categorical(data2['WildType_Yaviza'])
        # Fit the ANOVA model
        model = ols('WB_Arm1 ~ gender', data=data2).fit()
        # Display the summary of the model
        anova_table = sm.stats.anova_lm(model, typ=2)
        st.write(anova_table)

        st.write(
            """
            **Conclusion:**

            - Since the p-value (0.0379) is less than the common significance level of 0.05, we reject the null hypothesis.
            - This suggests that there is a statistically significant difference in WB_Arm1 values between genders at the 5% significance level.
            - In other words, the variation in WB_Arm1 explained by gender is significantly greater than the variation within the groups. This indicates that gender has a significant impact on WB_Arm1 values.""")

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

        st.write("#### ANOVA")
        data2['gender'] = pd.Categorical(data2['WildType_Yaviza'])
        # Fit the ANOVA model
        model = ols('WB_Arm2 ~ gender', data=data2).fit()
        # Display the summary of the model
        anova_table = sm.stats.anova_lm(model, typ=2)
        st.write(anova_table)

        st.write(
            """
            **Conclusion:**

            - Since the p-value (0.0116) is less than the common significance level of 0.05, we reject the null hypothesis.
            - This suggests that there is a statistically significant difference in WB_Arm2 values between genders at the 5% significance level.
            - In other words, the variation in WB_Arm2 explained by gender is significantly greater than the variation within the groups. This indicates that gender has a significant impact on WB_Arm2 values.""")

elif group == "Results" :
    st.write("**Conclusion:**")
    # Create a dictionary with the ANOVA results
    data = {
        'Experimental Condition': ['J06_No_Irrad', 'J06_No_Irrad', 'J06_Irrad', 'J06_Irrad', 'WildType_Yaviza',
                                   'WildType_Yaviza'],
        'Dependent Variable': ['WB_Arm1', 'WB_Arm2', 'WB_Arm1', 'WB_Arm2', 'WB_Arm1', 'WB_Arm2'],
        'p-value': [0.1075, 0.0213, 0.2518, 0.3922, 0.0379, 0.0116],
        'Result': ['Not Significant', 'Significant', 'Not Significant', 'Not Significant', 'Significant', 'Significant']
    }

    # Create a DataFrame from the dictionary
    df = pd.DataFrame(data)

    # Display the DataFrame as a table
    st.table(df)

    st.write(
        """
        **Conclusion:**

        - These findings indicate that the impact of gender on WB_Arm1 and WB_Arm2 values varies across different 
        experimental conditions. Gender has a significant effect on WB_Arm1 and WB_Arm2 values in the WildType_Yaviza condition, 
        but not in the J06_No_Irrad or J06_Irrad conditions. Further research is needed to understand the underlying mechanisms driving these differences.""")
elif group == "ANOVA" :
    anovas = st.radio("Select distribution:", ("WB_Arm1", "WB_Arm2"), index=0)
    if anovas == "WB_Arm1":
        st.write("### One-Way ANOVA with a significance level of α = 0.05")
        groups = data3.groupby('group')

        # Extracting the data for each group
        group1 = groups.get_group('J06_No_Irrad')['WB_Arm1']
        group2 = groups.get_group('J06_Irrad')['WB_Arm1']
        group3 = groups.get_group('WildType_Yaviza')['WB_Arm1']

        # Performing ANOVA
        f_statistic, p_value = f_oneway(group1, group2, group3)
        df_between = len(data3['group'].unique()) - 1
        df_within = len(data3) - len(data3['group'].unique())

        # Set the significance level
        alpha = 0.05

        # Find the critical value
        critical_value = f.ppf(1 - alpha, df_between, df_within)

        # Fit the model using ordinary least squares
        model = smf.ols('WB_Arm1 ~ C(group)', data=data3).fit()
        # Perform ANOVA
        anova_table = sm.stats.anova_lm(model, typ=2)

        # Display the ANOVA table in Streamlit
        st.write(anova_table)
        st.write("F-statistic:", f_statistic)
        st.write("p-value:", p_value)
        st.write("Critical value at α = 0.05:", critical_value)

        # Writing the results
        st.write("#### Set up the hypotheses:")
        st.write("- **H0**: μJ06_No_Irrad = μJ06_Irrad = μWildType_Yaviza (All underlying population means are equal)")
        st.write("- **H1**: μi ≠ μj for some i and j (Not all of the underlying population means are equal)")
        st.write("- **α** = 0.05")

        st.write("#### Decision Rule:")
        st.write(
            "With a significance level (probability) of α = 0.05 and degrees of freedom df1 = 2 and df2 = 717, the corresponding critical value is 3.00828.")
        st.write(
            "The decision rule states that we reject the null hypothesis (H0) if the F-statistic is greater than or equal to 3.00828.")
        st.write("Otherwise, we do not reject H0.")

        st.write("#### Conclusion:")
        if f_statistic >= critical_value:
            st.write(
                f"We reject the null hypothesis (H0) since the calculated F-statistic ({f_statistic:.5f}) is greater than the critical F-value (3.00828) at α = 0.05.")
            st.write(
                "Therefore, we have evidence to conclude that there is a significant difference in WB_Arm1 between the groups.")
        else:
            st.write(
                f"We do not reject the null hypothesis (H0) since the calculated F-statistic ({f_statistic:.5f}) is less than the critical F-value (3.00828) at α = 0.05.")
            st.write(
                "Therefore, we do not have sufficient evidence to conclude that there is a significant difference in WB_Arm1 between the groups.")
        st.write(
            "The overall model results are significant, suggesting that appropriate pairwise comparisons should be performed.")
    else:
        st.write("### One-Way ANOVA with a significance level of α = 0.05")
        groups = data3.groupby('group')

        # Extracting the data for each group
        group1 = groups.get_group('J06_No_Irrad')['WB_Arm2']
        group2 = groups.get_group('J06_Irrad')['WB_Arm2']
        group3 = groups.get_group('WildType_Yaviza')['WB_Arm2']

        # Performing ANOVA
        f_statistic, p_value = f_oneway(group1, group2, group3)
        df_between = len(data3['group'].unique()) - 1
        df_within = len(data3) - len(data3['group'].unique())

        # Set the significance level
        alpha = 0.05

        # Find the critical value
        critical_value = f.ppf(1 - alpha, df_between, df_within)

        # Fit the model using ordinary least squares
        model = smf.ols('WB_Arm2 ~ C(group)', data=data3).fit()
        # Perform ANOVA
        anova_table = sm.stats.anova_lm(model, typ=2)

        # Display the ANOVA table in Streamlit
        st.write(anova_table)
        st.write("F-statistic:", f_statistic)
        st.write("p-value:", p_value)
        st.write("Critical value at α = 0.05:", critical_value)

        # Writing the results
        st.write("#### Set up the hypotheses:")
        st.write("- **H0**: μJ06_No_Irrad = μJ06_Irrad = μWildType_Yaviza (All underlying population means are equal)")
        st.write("- **H1**: μi ≠ μj for some i and j (Not all of the underlying population means are equal)")
        st.write("- **α** = 0.05")

        st.write("#### Decision Rule:")
        st.write(
            "With a significance level (probability) of α = 0.05 and degrees of freedom df1 = 2 and df2 = 717, the corresponding critical value is 3.00828.")
        st.write(
            "The decision rule states that we reject the null hypothesis (H0) if the F-statistic is greater than or equal to 3.00828.")
        st.write("Otherwise, we do not reject H0.")

        st.write("#### Conclusion:")
        if f_statistic >= critical_value:
            st.write(
                f"We reject the null hypothesis (H0) since the calculated F-statistic ({f_statistic:.5f}) is greater than the critical F-value (3.00828) at α = 0.05.")
            st.write(
                "Therefore, we have evidence to conclude that there is a significant difference in WB_Arm2 between the groups.")
        else:
            st.write(
                f"We do not reject the null hypothesis (H0) since the calculated F-statistic ({f_statistic:.5f}) is less than the critical F-value (3.00828) at α = 0.05.")
            st.write(
                "Therefore, we do not have sufficient evidence to conclude that there is a significant difference in WB_Arm2 between the groups.")
        st.write("The overall model results are significant, suggesting that appropriate pairwise comparisons should be performed.")
