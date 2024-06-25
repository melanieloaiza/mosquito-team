import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import tempfile
from statsmodels.formula.api import ols
from scipy.stats import f_oneway
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import f
from statsmodels.stats.multicomp import pairwise_tukeyhsd

st.set_page_config(layout="wide")

# J06_No_Irrad DATASET
data = pd.read_csv("mosquitoteam/J06_No_Irrad.csv")
df = pd.DataFrame(data)
male_data = df[df["J06_No_Irrad"] == "Male"]
female_data = df[df["J06_No_Irrad"] == "Female"]

# J06_Irrad DATASET
data1 = pd.read_csv("mosquitoteam/J06_Irrad.csv")
df1 = pd.DataFrame(data1)
male_data1 = df1[df1["J06_Irrad"] == "Male"]
female_data1 = df1[df1["J06_Irrad"] == "Female"]

# WildType_Yaviza DATASET
data2 = pd.read_csv("mosquitoteam/WildType_Yaviza.csv")
df2 = pd.DataFrame(data2)
male_data2 = df2[df2["WildType_Yaviza"] == "Male"]
female_data2 = df2[df2["WildType_Yaviza"] == "Female"]

data3 = pd.read_csv("mosquitoteam/groups.csv")
df3 = pd.read_csv("groups.csv")

st.title(" 🦟 Mosca Project " )
group = st.sidebar.radio("Select Group:", ("J06_No_Irrad", "J06_Irrad", "WildType_Yaviza" , "Conclusion" , "One Way (ANOVA)"), index=0)

if group == "J06_No_Irrad":
    col1, col2, col3 = st.columns(3)
    st.write("### J06_No_Irrad")
    group = st.radio("Select distribution:", ("WB_Arm1", "WB_Arm2"), index=0)
    if group == "WB_Arm1":
        colors = ['rgb(107,174,214)', '#7201a8', 'rgb(255,127,14)']
        fig = go.Figure()
        for i, col in enumerate(data["J06_No_Irrad"].unique()):
            subset = data[data["J06_No_Irrad"] == col]
            fig.add_trace(go.Box(
                y=subset["WB_Arm1"],
                name=col,
                jitter=0.3,
                pointpos=-1.8,
                boxpoints='all',
                marker_color=colors[i % len(colors)],
                line_color=colors[i % len(colors)]
            ))
            fig.update_layout(
                title={
                    'text': "WB_Arm1 by Gender",
                    'x': 0.5,
                    'xanchor': 'center'
                },
                xaxis_title="Gender",
                yaxis_title="WB_Arm1" ,
                annotations=[
                    dict(
                        xref='paper',
                        yref='paper',
                        x=0.5,
                        y=-0.3,
                        showarrow=False,
                        text="Figure 1 shows boxplots of WB_Arm1 by gender for the J06_No_Irrad population, with males (left panel) and females (right panel).",
                    )
                ]
            )
        ## PRINT FIGURE 1
        st.plotly_chart(fig)

        male_distribution_text = """
        <h6 style="text-align: justify;">Distribution for Males:</h6>
        <p style="text-align: justify;">
        The distribution for males is mostly symmetric with a small left tail and three potential outliers: 285, 277, and 169.  
        This suggests that for most males, the majority of WB_Arm1 values are closer to 227.5, with only a few values falling below that threshold.
        </p>
        """
        st.markdown(male_distribution_text, unsafe_allow_html=True)
        col1, col2 = st.columns([2, 2])
        with col1:
            num_bins = st.slider('Number of Bins', min_value=1, max_value=15, value=5, key='num_bins_sliderMale')
        figMale = px.histogram(male_data,
                               x="WB_Arm1",
                               nbins=num_bins,
                               title="WB_Arm1 for Male")
        figMale.update_traces(marker_color='rgb(107,174,214)',
                              marker_line_color='rgb(107,174,214)',
                              marker_line_width=2,
                              marker_line=dict(width=2, color='rgb(8,81,156)'),
                              opacity=0.6)
        figMale.update_layout(xaxis_title="WB_Arm1",
                              yaxis_title="Frequency",
                              title={
                                  'text': "WB_Arm1 for Male",
                                  'x': 0.5,
                                  'xanchor': 'center'
                              },
                              width=600,
                              height=500
                              )
        st.plotly_chart(figMale)
        # DOWNLOAD BUTTON
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            figMale.write_image(tmpfile.name, width=800, height=600, scale=2)
            tmpfile_path = tmpfile.name

        with open(tmpfile_path, "rb") as file:
            st.download_button(
                label="Download figure",
                data=file,
                file_name="plotly_chart.png",
                mime="image/png",
                key='buttom1'
            )

        summary_male = data[data["J06_No_Irrad"] == "Male"]["WB_Arm1"].describe().reset_index()
        summary_male.columns = ["Statistic", "Male"]

        st.write("Summary for Males:")
        st.dataframe(summary_male.style.set_properties(**{'text-align': 'center'}))

        female_distribution_text = """
        <h6 style="text-align: justify;">Distribution for Females:</h6>
        <p style="text-align: justify;">
        The distribution for females is mostly symmetric, with four potential outliers: 276, 166, 163, and 158.  
        For most females, the majority of WB_Arm1 values are closer to 225.
        </p>
        """
        st.markdown(female_distribution_text, unsafe_allow_html=True)

        col1, col2 = st.columns([2, 2])
        with col1:
            num_bins = st.slider('Number of Bins', min_value=1, max_value=15, value=5, key='num_bins_sliderFemale')

        # Plot histogram for Female
        figFemale = px.histogram(female_data1,
                                 x="WB_Arm1",
                                 nbins=num_bins,
                                 title="WB_Arm1 for Female")
        figFemale.update_traces(marker_color='#7201a8',
                                marker_line_color='#7201a8',
                                marker_line_width=2,
                                marker_line=dict(width=2, color='#380340'),
                                opacity=0.6)
        figFemale.update_layout(xaxis_title="WB_Arm1",
                          yaxis_title="Frequency",
                          title={
                              'text': "WB_Arm1 for Female",
                              'x': 0.5,
                              'xanchor': 'center'
                          },
                          width=600,
                          height=500)
        st.plotly_chart(figFemale)
        # DOWNLOAD BUTTON
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            figFemale.write_image(tmpfile.name, width=800, height=600, scale=2)
            tmpfile_path = tmpfile.name

        with open(tmpfile_path, "rb") as file:
            st.download_button(
                label="Download figure",
                data=file,
                file_name="plotly_chart.png",
                mime="image/png",
                key='buttom2'
            )


        summary_female = data[data["J06_No_Irrad"] == "Female"]["WB_Arm1"].describe().reset_index()
        summary_female.columns = ["Statistic", "Female"]

        st.write("Summary for Females:")
        st.dataframe(summary_female.style.set_properties(**{'text-align': 'center'}))

        st.write("### One-Way ANOVA with a significance level of α = 0.05")
        # Convert 'J06_No_Irrad' to a categorical variable
        data['gender'] = pd.Categorical(data['J06_No_Irrad'])

        # Fit the ANOVA model
        model = ols('WB_Arm1 ~ gender', data=data).fit()

        # Display the summary of the model
        anova_table = sm.stats.anova_lm(model, typ=2)
        st.write(anova_table)

        # Interpretation
        st.markdown("""
                    <div style="text-align: justify">
                    
                    - Since the p-value (0.1075) is greater than the common significance level of 0.05, we do not reject the null hypothesis. 
                    
                    - This suggests that there is no statistically significant difference in WB_Arm1 values between genders at the 5% significance level. 
                    
                    - In other words, the variation in WB_Arm1 explained by gender is not significantly greater than the variation within the groups. The differences in WB_Arm1 values between males and females are likely due to random variation rather than a true difference in their means.
                    </div>
                    """, unsafe_allow_html=True)

    else :
        colors = ['rgb(107,174,214)', '#7201a8', 'rgb(255,127,14)']
        fig = go.Figure()
        for i, col in enumerate(data["J06_No_Irrad"].unique()):
            subset = data[data["J06_No_Irrad"] == col]
            fig.add_trace(go.Box(
                y=subset["WB_Arm2"],
                name=col,
                jitter=0.3,
                pointpos=-1.8,
                boxpoints='all',
                marker_color=colors[i % len(colors)],
                line_color=colors[i % len(colors)]
            ))
            fig.update_layout(
                title={
                    'text': "WB_Arm2 by Gender",
                    'x': 0.5,
                    'xanchor': 'center'
                },
                xaxis_title="Gender",
                yaxis_title="WB_Arm2",
                annotations=[
                    dict(
                        xref='paper',
                        yref='paper',
                        x=0.5,
                        y=-0.3,
                        showarrow=False,
                        text="Figure 1 shows boxplots of WB_Arm2 by gender for the J06_No_Irrad population, with males (left panel) and females (right panel).",
                    )
                ]
            )
        ## PRINT FIGURE 1
        st.plotly_chart(fig)

        # DOWNLOAD BUTTON
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            fig.write_image(tmpfile.name, width=800, height=600, scale=2)
            tmpfile_path = tmpfile.name

        with open(tmpfile_path, "rb") as file:
            st.download_button(
                label="Download figure",
                data=file,
                file_name="plotly_chart.png",
                mime="image/png"
            )

        male_distribution_text = """
            <h6 style="text-align: justify;">Distribution for Males:</h6>
            <p style="text-align: justify;">
            The distribution for males is bimodal, with two peaks around 400-500, and is roughly symmetric. The data ranges from 351 to 711, with most values concentrated near the center around 454. The spread of the data appears to be narrow, indicating low variability within the dataset. Additionally, the potential outlier above 700 could be an influential point and should be investigated further to understand its impact. The histogram suggests that there may be two underlying subgroups within the male population.</p>
            """
        st.markdown(male_distribution_text, unsafe_allow_html=True)
        col1, col2 = st.columns([2, 2])
        with col1:
            num_bins = st.slider('Number of Bins', min_value=1, max_value=15, value=5, key='num_bins_sliderMale')
        figMale = px.histogram(male_data,
                               x="WB_Arm2",
                               nbins=num_bins,
                               title="WB_Arm2 for Male")
        figMale.update_traces(marker_color='rgb(107,174,214)',
                              marker_line_color='rgb(107,174,214)',
                              marker_line_width=2,
                              marker_line=dict(width=2, color='rgb(8,81,156)'),
                              opacity=0.6)
        figMale.update_layout(xaxis_title="WB_Arm2",
                              yaxis_title="Frequency",
                              title={
                                  'text': "WB_Arm2 for Male",
                                  'x': 0.5,
                                  'xanchor': 'center'
                              },
                              width=600,
                              height=500
                              )
        st.plotly_chart(figMale)
        # DOWNLOAD BUTTON
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            figMale.write_image(tmpfile.name, width=800, height=600, scale=2)
            tmpfile_path = tmpfile.name

        with open(tmpfile_path, "rb") as file:
            st.download_button(
                label="Download figure",
                data=file,
                file_name="plotly_chart.png",
                mime="image/png",
                key='buttom1'
            )

        summary_male = data[data["J06_No_Irrad"] == "Male"]["WB_Arm2"].describe().reset_index()
        summary_male.columns = ["Statistic", "Male"]

        st.write("Summary for Males:")
        st.dataframe(summary_male.style.set_properties(**{'text-align': 'center'}))

        female_distribution_text = """
            <h6 style="text-align: justify;">Distribution for Females:</h6>
            <p style="text-align: justify;">
            The distribution for females is unimodal and roughly symmetric, with a peak around 440-459. The narrow spread indicates low variability, with the majority of values clustered closely together around 449. The data ranges from 327 to 604, with a few potential outliers to the right, suggesting some variability in the upper range of values. Overall, the distribution appears to be relatively concentrated, with most values falling within a relatively small range.
            </p>
            """
        st.markdown(female_distribution_text, unsafe_allow_html=True)

        col1, col2 = st.columns([2, 2])
        with col1:
            num_bins = st.slider('Number of Bins', min_value=1, max_value=15, value=5, key='num_bins_sliderFemale')

        # Plot histogram for Female
        figFemale = px.histogram(female_data1,
                                 x="WB_Arm2",
                                 nbins=num_bins,
                                 title="WB_Arm2 for Female")
        figFemale.update_traces(marker_color='#7201a8',
                                marker_line_color='#7201a8',
                                marker_line_width=2,
                                marker_line=dict(width=2, color='#380340'),
                                opacity=0.6)
        figFemale.update_layout(xaxis_title="WB_Arm2",
                                yaxis_title="Frequency",
                                title={
                                    'text': "WB_Arm2 for Female",
                                    'x': 0.5,
                                    'xanchor': 'center'
                                },
                                width=600,
                                height=500)
        st.plotly_chart(figFemale)
        # DOWNLOAD BUTTON
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            figFemale.write_image(tmpfile.name, width=800, height=600, scale=2)
            tmpfile_path = tmpfile.name

        with open(tmpfile_path, "rb") as file:
            st.download_button(
                label="Download figure",
                data=file,
                file_name="plotly_chart.png",
                mime="image/png",
                key='buttom2'
            )

        summary_female = data[data["J06_No_Irrad"] == "Female"]["WB_Arm2"].describe().reset_index()
        summary_female.columns = ["Statistic", "Female"]

        st.write("Summary for Females:")
        st.dataframe(summary_female.style.set_properties(**{'text-align': 'center'}))

        st.write("### One-Way ANOVA with a significance level of α = 0.05")
        # Convert 'J06_No_Irrad' to a categorical variable
        data['gender'] = pd.Categorical(data['J06_No_Irrad'])

        # Fit the ANOVA model
        model = ols('WB_Arm2 ~ gender', data=data).fit()

        # Display the summary of the model
        anova_table = sm.stats.anova_lm(model, typ=2)
        st.write(anova_table)

        # Interpretation
        st.write("<h6 style='text-align: justify;'><b>Interpretation</b></h6>", unsafe_allow_html=True)
        st.write(
            "<p style='text-align: justify;'> "
            " - The F-statistic of 5.37 suggests that there is a significant difference in the means of WB_Arm2 based on gender.</p>",
            unsafe_allow_html=True
        )
        st.write(
            "<p style='text-align: justify;'>- The p-value of 0.0213 is less than the typical significance level of 0.05, indicating that there is a statistically significant difference between genders.</p>",
            unsafe_allow_html=True
        )

        # Conclusion
        st.write("<h6 style='text-align: justify;'><b>Conclusion</b></h6>", unsafe_allow_html=True)
        st.write(
            "<p style='text-align: justify;'>Based on these results, we reject the null hypothesis and conclude that there is a significant difference in the means of WB_Arm2 between males and females.</p>",
            unsafe_allow_html=True
        )

elif group == "J06_Irrad" :
    col1, col2, col3 = st.columns(3)
    st.write("### J06_Irrad")
    group = st.radio("Select distribution:", ("WB_Arm1", "WB_Arm2"), index=0)
    if group == "WB_Arm1":
        colors = ['rgb(107,174,214)', '#7201a8', 'rgb(255,127,14)']
        fig = go.Figure()
        for i, col in enumerate(data1["J06_Irrad"].unique()):
            subset = data1[data1["J06_Irrad"] == col]
            fig.add_trace(go.Box(
                y=subset["WB_Arm1"],
                name=col,
                jitter=0.3,
                pointpos=-1.8,
                boxpoints='all',
                marker_color=colors[i % len(colors)],
                line_color=colors[i % len(colors)]
            ))
            fig.update_layout(
                title={
                    'text': "WB_Arm1 by Gender",
                    'x': 0.5,
                    'xanchor': 'center'
                },
                xaxis_title="Gender",
                yaxis_title="WB_Arm1",
                annotations=[
                    dict(
                        xref='paper',
                        yref='paper',
                        x=0.5,
                        y=-0.3,
                        showarrow=False,
                        text="Figure 1 shows boxplots of WB_Arm1 by gender for the J06_Irrad population, with males (left panel) and females (right panel).",
                    )
                ]
            )
        ## PRINT FIGURE 1
        st.plotly_chart(fig)

        # DOWNLOAD BUTTON
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            fig.write_image(tmpfile.name, width=800, height=600, scale=2)
            tmpfile_path = tmpfile.name

        with open(tmpfile_path, "rb") as file:
            st.download_button(
                label="Download figure",
                data=file,
                file_name="plotly_chart.png",
                mime="image/png"
            )

        male_distribution_text = """
        <h6 style="text-align: justify;">Distribution for Males:</h6>
        <p style="text-align: justify;">
        The distribution of males is uniform, with one peak. The wider spread indicates higher variability. Although the distribution is generally uniform, there is a slight left skew, as evidenced by the median of 223.5 being higher than the mean of 217. This indicates that while some males WB_Arm1  are near the center at 223, some are below this threshold, pulling the mean in the left direction. 
        The data ranges from 149 to 269, suggesting a relatively wide range of values. There are no apparent outliers, but further analysis could explore whether any individual data points significantly impact the distribution."""
        st.markdown(male_distribution_text, unsafe_allow_html=True)
        col1, col2 = st.columns([2, 2])
        with col1:
            num_bins = st.slider('Number of Bins', min_value=1, max_value=15, value=5, key='num_bins_sliderMale')
        figMale = px.histogram(male_data1,
                               x="WB_Arm1",
                               nbins=num_bins,
                               title="WB_Arm1 for Male")
        figMale.update_traces(marker_color='rgb(107,174,214)',
                              marker_line_color='rgb(107,174,214)',
                              marker_line_width=2,
                              marker_line=dict(width=2, color='rgb(8,81,156)'),
                              opacity=0.6)
        figMale.update_layout(xaxis_title="WB_Arm1",
                              yaxis_title="Frequency",
                              title={
                                  'text': "WB_Arm1 for Male",
                                  'x': 0.5,
                                  'xanchor': 'center'
                              },
                              width=600,
                              height=500
                              )
        st.plotly_chart(figMale)
        # DOWNLOAD BUTTON
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            figMale.write_image(tmpfile.name, width=800, height=600, scale=2)
            tmpfile_path = tmpfile.name

        with open(tmpfile_path, "rb") as file:
            st.download_button(
                label="Download figure",
                data=file,
                file_name="plotly_chart.png",
                mime="image/png",
                key='buttom1'
            )

        summary_male = data1[data1["J06_Irrad"] == "Male"]["WB_Arm1"].describe().reset_index()
        summary_male.columns = ["Statistic", "Male"]

        st.write("Summary for Males:")
        st.dataframe(summary_male.style.set_properties(**{'text-align': 'center'}))

        female_distribution_text = """
        <h6 style="text-align: justify;">Distribution for Females:</h6>
        <p style="text-align: justify;">
        The distribution of females is approximately symmetric, displaying two peaks, which indicates the presence of underlying subpopulations within the data. The slightly left tail suggests a slight skewness towards lower values. The narrow spread suggests low variability, with most data points clustered around 223.5. The dataset ranges from 177 to 277, indicating a small range. Potential outliers are present and should be further investigated.
        </p>
        """
        st.markdown(female_distribution_text, unsafe_allow_html=True)

        col1, col2 = st.columns([2, 2])
        with col1:
            num_bins = st.slider('Number of Bins', min_value=1, max_value=15, value=5, key='num_bins_sliderFemale')

        # Plot histogram for Female
        figFemale = px.histogram(female_data1,
                                 x="WB_Arm1",
                                 nbins=num_bins,
                                 title="WB_Arm1 for Female")
        figFemale.update_traces(marker_color='#7201a8',
                                marker_line_color='#7201a8',
                                marker_line_width=2,
                                marker_line=dict(width=2, color='#380340'),
                                opacity=0.6)
        figFemale.update_layout(xaxis_title="WB_Arm1",
                                yaxis_title="Frequency",
                                title={
                                    'text': "WB_Arm1 for Female",
                                    'x': 0.5,
                                    'xanchor': 'center'
                                },
                                width=600,
                                height=500)
        st.plotly_chart(figFemale)
        # DOWNLOAD BUTTON
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            figFemale.write_image(tmpfile.name, width=800, height=600, scale=2)
            tmpfile_path = tmpfile.name

        with open(tmpfile_path, "rb") as file:
            st.download_button(
                label="Download figure",
                data=file,
                file_name="plotly_chart.png",
                mime="image/png",
                key='buttom2'
            )

        summary_female = data1[data1["J06_Irrad"] == "Female"]["WB_Arm1"].describe().reset_index()
        summary_female.columns = ["Statistic", "Female"]

        st.write("Summary for Females:")
        st.dataframe(summary_female.style.set_properties(**{'text-align': 'center'}))

        st.write("### One-Way ANOVA with a significance level of α = 0.05")
        # Convert 'J06_Irrad' to a categorical variable
        data1['gender'] = pd.Categorical(data1['J06_Irrad'])

        # Fit the ANOVA model
        model = ols('WB_Arm1 ~ gender', data=data1).fit()

        # Display the summary of the model
        anova_table = sm.stats.anova_lm(model, typ=2)
        st.write(anova_table)

        # Interpretation
        st.markdown("""
                    <div style="text-align: justify">
                    Since the p-value (0.2518) is greater than the common significance level of 0.05, we do not reject the null hypothesis. This suggests that there is no statistically significant difference in WB_Arm1 values between genders at the 5% significance level. In other words,  the differences in WB_Arm1 values between males and females are likely due to random variation rather than a true difference in their means. 

                     </div>
                    """, unsafe_allow_html=True)

    else:
        colors = ['rgb(107,174,214)', '#7201a8', 'rgb(255,127,14)']
        fig = go.Figure()
        for i, col in enumerate(data1["J06_Irrad"].unique()):
            subset = data1[data1["J06_Irrad"] == col]
            fig.add_trace(go.Box(
                y=subset["WB_Arm2"],
                name=col,
                jitter=0.3,
                pointpos=-1.8,
                boxpoints='all',
                marker_color=colors[i % len(colors)],
                line_color=colors[i % len(colors)]
            ))
            fig.update_layout(
                title={
                    'text': "WB_Arm2 by Gender",
                    'x': 0.5,
                    'xanchor': 'center'
                },
                xaxis_title="Gender",
                yaxis_title="WB_Arm2",
                annotations=[
                    dict(
                        xref='paper',
                        yref='paper',
                        x=0.5,
                        y=-0.3,
                        showarrow=False,
                        text="Figure 1 shows boxplots of WB_Arm2 by gender for the J06_Irrad population, with males (left panel) and females (right panel).",
                    )
                ]
            )
        ## PRINT FIGURE 1
        st.plotly_chart(fig)

        # DOWNLOAD BUTTON
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            fig.write_image(tmpfile.name, width=800, height=600, scale=2)
            tmpfile_path = tmpfile.name

        with open(tmpfile_path, "rb") as file:
            st.download_button(
                label="Download figure",
                data=file,
                file_name="plotly_chart.png",
                mime="image/png"
            )

        male_distribution_text = """
            <h6 style="text-align: justify;">Distribution for Males:</h6>
            <p style="text-align: justify;">
            The distribution of J06_Irrad males with WB_Arm2 is symmetric, exhibiting three peaks. The wider spread suggests higher variability within the group. Despite its symmetry, a few low values skew the mean to the left. No potential outliers are observed. This distribution may indicate the presence of multiple subgroups within the population. Further analysis could investigate the relationship between these subgroups and their biological or environmental determinants, including the effects of radiation exposure. """
        st.markdown(male_distribution_text, unsafe_allow_html=True)
        col1, col2 = st.columns([2, 2])
        with col1:
            num_bins = st.slider('Number of Bins', min_value=1, max_value=15, value=5, key='num_bins_sliderMale')
        figMale = px.histogram(male_data1,
                               x="WB_Arm2",
                               nbins=num_bins,
                               title="WB_Arm2 for Male")
        figMale.update_traces(marker_color='rgb(107,174,214)',
                              marker_line_color='rgb(107,174,214)',
                              marker_line_width=2,
                              marker_line=dict(width=2, color='rgb(8,81,156)'),
                              opacity=0.6)
        figMale.update_layout(xaxis_title="WB_Arm2",
                              yaxis_title="Frequency",
                              title={
                                  'text': "WB_Arm2 for Male",
                                  'x': 0.5,
                                  'xanchor': 'center'
                              },
                              width=600,
                              height=500
                              )
        st.plotly_chart(figMale)
        # DOWNLOAD BUTTON
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            figMale.write_image(tmpfile.name, width=800, height=600, scale=2)
            tmpfile_path = tmpfile.name

        with open(tmpfile_path, "rb") as file:
            st.download_button(
                label="Download figure",
                data=file,
                file_name="plotly_chart.png",
                mime="image/png",
                key='buttom1'
            )

        summary_male = data1[data1["J06_Irrad"] == "Male"]["WB_Arm2"].describe().reset_index()
        summary_male.columns = ["Statistic", "Male"]

        st.write("Summary for Males:")
        st.dataframe(summary_male.style.set_properties(**{'text-align': 'center'}))

        female_distribution_text = """
            <h6 style="text-align: justify;">Distribution for Females:</h6>
            <p style="text-align: justify;">
            The distribution of J06_Irrad females with WB_Arm2 is roughly symmetric, with a peak around 440-459. The narrow spread indicates low variability, with the majority of values clustered closely together around 453. A very small tail of low values pulls the mean to the left, suggesting slight skewness. Potential outliers can be seen and should be evaluated. 
            </p>
            """
        st.markdown(female_distribution_text, unsafe_allow_html=True)

        col1, col2 = st.columns([2, 2])
        with col1:
            num_bins = st.slider('Number of Bins', min_value=1, max_value=15, value=5, key='num_bins_sliderFemale')

        # Plot histogram for Female
        figFemale = px.histogram(female_data1,
                                 x="WB_Arm2",
                                 nbins=num_bins,
                                 title="WB_Arm2 for Female")
        figFemale.update_traces(marker_color='#7201a8',
                                marker_line_color='#7201a8',
                                marker_line_width=2,
                                marker_line=dict(width=2, color='#380340'),
                                opacity=0.6)
        figFemale.update_layout(xaxis_title="WB_Arm2",
                                yaxis_title="Frequency",
                                title={
                                    'text': "WB_Arm2 for Female",
                                    'x': 0.5,
                                    'xanchor': 'center'
                                },
                                width=600,
                                height=500)
        st.plotly_chart(figFemale)
        # DOWNLOAD BUTTON
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            figFemale.write_image(tmpfile.name, width=800, height=600, scale=2)
            tmpfile_path = tmpfile.name

        with open(tmpfile_path, "rb") as file:
            st.download_button(
                label="Download figure",
                data=file,
                file_name="plotly_chart.png",
                mime="image/png",
                key='buttom2'
            )

        summary_female = data1[data1["J06_Irrad"] == "Female"]["WB_Arm2"].describe().reset_index()
        summary_female.columns = ["Statistic", "Female"]

        st.write("Summary for Females:")
        st.dataframe(summary_female.style.set_properties(**{'text-align': 'center'}))

        st.write("### One-Way ANOVA with a significance level of α = 0.05")
        # Convert 'J06_Irrad' to a categorical variable
        data1['gender'] = pd.Categorical(data1['J06_Irrad'])

        # Fit the ANOVA model
        model = ols('WB_Arm2 ~ gender', data=data1).fit()

        # Display the summary of the model
        anova_table = sm.stats.anova_lm(model, typ=2)
        st.write(anova_table)

        st.write("Since the p-value (0.3922) is greater than the common significance level of 0.05, we do not reject the null hypothesis. This suggests that there is no statistically significant difference in WB_Arm2 values between genders at the 5% significance level. In other words, the  differences in WB_Arm2 values between males and females are likely due to random variation rather than a true difference in their means.")

elif group == "WildType_Yaviza" :
    col1, col2, col3 = st.columns(3)
    st.write("### WildType_Yaviza")
    group = st.radio("Select distribution:", ("WB_Arm1", "WB_Arm2"), index=0)
    if group == "WB_Arm1":
        colors = ['rgb(107,174,214)', '#7201a8', 'rgb(255,127,14)']
        fig = go.Figure()
        for i, col in enumerate(data2["WildType_Yaviza"].unique()):
            subset = data2[data2["WildType_Yaviza"] == col]
            fig.add_trace(go.Box(
                y=subset["WB_Arm1"],
                name=col,
                jitter=0.3,
                pointpos=-1.8,
                boxpoints='all',
                marker_color=colors[i % len(colors)],
                line_color=colors[i % len(colors)]
            ))
            fig.update_layout(
                title={
                    'text': "WB_Arm1 by Gender",
                    'x': 0.5,
                    'xanchor': 'center'
                },
                xaxis_title="Gender",
                yaxis_title="WB_Arm1",
                annotations=[
                    dict(
                        xref='paper',
                        yref='paper',
                        x=0.5,
                        y=-0.3,
                        showarrow=False,
                        text="Figure 1 shows boxplots of WB_Arm1 by gender for the WildType_Yaviza population, with males (left panel) and females (right panel).",
                    )
                ]
            )
        ## PRINT FIGURE 1
        st.plotly_chart(fig)

        # DOWNLOAD BUTTON
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            fig.write_image(tmpfile.name, width=800, height=600, scale=2)
            tmpfile_path = tmpfile.name

        with open(tmpfile_path, "rb") as file:
            st.download_button(
                label="Download figure",
                data=file,
                file_name="plotly_chart.png",
                mime="image/png"
            )

        male_distribution_text = """
        <h6 style="text-align: justify;">Distribution for Males:</h6>
        <p style="text-align: justify;">
        The distribution of WildType_Yaviza males with WB_Arm1 is roughly symmetrical and unimodal, with one peak between 230 and 239. The small range from 177 to 282 suggests low variability within the population. Some WildType_Yaviza males have WB_Arm1 values below the center, pulling the mean to the left and causing a very slight left skew in the distribution. Most WildType_Yaviza males with WB_Arm1 are centered around 235.
        """
        st.markdown(male_distribution_text, unsafe_allow_html=True)
        col1, col2 = st.columns([2, 2])
        with col1:
            num_bins = st.slider('Number of Bins', min_value=1, max_value=15, value=5, key='num_bins_sliderMale')
        figMale = px.histogram(male_data2,
                               x="WB_Arm1",
                               nbins=num_bins,
                               title="WB_Arm1 for Male")
        figMale.update_traces(marker_color='rgb(107,174,214)',
                              marker_line_color='rgb(107,174,214)',
                              marker_line_width=2,
                              marker_line=dict(width=2, color='rgb(8,81,156)'),
                              opacity=0.6)
        figMale.update_layout(xaxis_title="WB_Arm1",
                              yaxis_title="Frequency",
                              title={
                                  'text': "WB_Arm1 for Male",
                                  'x': 0.5,
                                  'xanchor': 'center'
                              },
                              width=600,
                              height=500
                              )
        st.plotly_chart(figMale)
        # DOWNLOAD BUTTON
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            figMale.write_image(tmpfile.name, width=800, height=600, scale=2)
            tmpfile_path = tmpfile.name

        with open(tmpfile_path, "rb") as file:
            st.download_button(
                label="Download figure",
                data=file,
                file_name="plotly_chart.png",
                mime="image/png",
                key='buttom1'
            )

        summary_male = data2[data2["WildType_Yaviza"] == "Male"]["WB_Arm1"].describe().reset_index()
        summary_male.columns = ["Statistic", "Male"]

        st.write("Summary for Males:")
        st.dataframe(summary_male.style.set_properties(**{'text-align': 'center'}))

        female_distribution_text = """
        <h6 style="text-align: justify;">Distribution for Females:</h6>
        <p style="text-align: justify;">
        The distribution of WildType_Yaviza females with WB_Arm1 is unimodal, with more variability evident in the population as indicated by the wider spread. The data ranges from 170 to a maximum value of 283, with a standard deviation of 20.60 from the mean, which is 226.56. Potential outliers can be observed and warrant further investigation to understand their impact on the overall distribution. 
        </p>
        """
        st.markdown(female_distribution_text, unsafe_allow_html=True)

        col1, col2 = st.columns([2, 2])
        with col1:
            num_bins = st.slider('Number of Bins', min_value=1, max_value=15, value=5, key='num_bins_sliderFemale')

        # Plot histogram for Female
        figFemale = px.histogram(female_data2,
                                 x="WB_Arm1",
                                 nbins=num_bins,
                                 title="WB_Arm1 for Female")
        figFemale.update_traces(marker_color='#7201a8',
                                marker_line_color='#7201a8',
                                marker_line_width=2,
                                marker_line=dict(width=2, color='#380340'),
                                opacity=0.6)
        figFemale.update_layout(xaxis_title="WB_Arm1",
                                yaxis_title="Frequency",
                                title={
                                    'text': "WB_Arm1 for Female",
                                    'x': 0.5,
                                    'xanchor': 'center'
                                },
                                width=600,
                                height=500)
        st.plotly_chart(figFemale)
        # DOWNLOAD BUTTON
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            figFemale.write_image(tmpfile.name, width=800, height=600, scale=2)
            tmpfile_path = tmpfile.name

        with open(tmpfile_path, "rb") as file:
            st.download_button(
                label="Download figure",
                data=file,
                file_name="plotly_chart.png",
                mime="image/png",
                key='buttom2'
            )

        summary_female = data2[data2["WildType_Yaviza"] == "Female"]["WB_Arm1"].describe().reset_index()
        summary_female.columns = ["Statistic", "Female"]

        st.write("Summary for Females:")
        st.dataframe(summary_female.style.set_properties(**{'text-align': 'center'}))

        st.write("### One-Way ANOVA with a significance level of α = 0.05")
        # Convert 'WildType_Yaviza' to a categorical variable
        data2['gender'] = pd.Categorical(data2['WildType_Yaviza'])

        # Fit the ANOVA model
        model = ols('WB_Arm1 ~ gender', data=data2).fit()

        # Display the summary of the model
        anova_table = sm.stats.anova_lm(model, typ=2)
        st.write(anova_table)

        # Interpretation
        st.markdown("""
                    <div style="text-align: justify">
                    Since the p-value (0.0379) is less than the common significance level of 0.05, we reject the null hypothesis. This suggests that there is a statistically significant difference in WB_Arm1 values between genders for WildType_Yaviza distributions at the 5% significance level. In other words, it indicates that gender has a significant impact on WB_Arm1 values.
                     </div>
                    """, unsafe_allow_html=True)

    else:
        colors = ['rgb(107,174,214)', '#7201a8', 'rgb(255,127,14)']
        fig = go.Figure()
        for i, col in enumerate(data2["WildType_Yaviza"].unique()):
            subset = data2[data2["WildType_Yaviza"] == col]
            fig.add_trace(go.Box(
                y=subset["WB_Arm2"],
                name=col,
                jitter=0.3,
                pointpos=-1.8,
                boxpoints='all',
                marker_color=colors[i % len(colors)],
                line_color=colors[i % len(colors)]
            ))
            fig.update_layout(
                title={
                    'text': "WB_Arm2 by Gender",
                    'x': 0.5,
                    'xanchor': 'center'
                },
                xaxis_title="Gender",
                yaxis_title="WB_Arm2",
                annotations=[
                    dict(
                        xref='paper',
                        yref='paper',
                        x=0.5,
                        y=-0.3,
                        showarrow=False,
                        text="Figure 1 shows boxplots of WB_Arm2 by gender for the WildType_Yaviza population, with males (left panel) and females (right panel).",
                    )
                ]
            )
        ## PRINT FIGURE 1
        st.plotly_chart(fig)

        # DOWNLOAD BUTTON
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            fig.write_image(tmpfile.name, width=800, height=600, scale=2)
            tmpfile_path = tmpfile.name

        with open(tmpfile_path, "rb") as file:
            st.download_button(
                label="Download figure",
                data=file,
                file_name="plotly_chart.png",
                mime="image/png"
            )

        male_distribution_text = """
            <h6 style="text-align: justify;">Distribution for Males:</h6>
            <p style="text-align: justify;">
            The distribution of WildType_Yaviza males with WB_Arm2 is unimodal and symmetric, with a very small left tail caused by lower values. Most of the WildType_Yaviza males with WB_Arm2 are centered around 474. The dataset ranges from 363 to 565, indicating a relatively wide range of values. The wider spread suggests higher variability within the population. Very few potential outliers are observed. """
        st.markdown(male_distribution_text, unsafe_allow_html=True)
        col1, col2 = st.columns([2, 2])
        with col1:
            num_bins = st.slider('Number of Bins', min_value=1, max_value=15, value=5, key='num_bins_sliderMale')
        figMale = px.histogram(male_data2,
                               x="WB_Arm2",
                               nbins=num_bins,
                               title="WB_Arm2 for Male")
        figMale.update_traces(marker_color='rgb(107,174,214)',
                              marker_line_color='rgb(107,174,214)',
                              marker_line_width=2,
                              marker_line=dict(width=2, color='rgb(8,81,156)'),
                              opacity=0.6)
        figMale.update_layout(xaxis_title="WB_Arm2",
                              yaxis_title="Frequency",
                              title={
                                  'text': "WB_Arm2 for Male",
                                  'x': 0.5,
                                  'xanchor': 'center'
                              },
                              width=600,
                              height=500
                              )
        st.plotly_chart(figMale)
        # DOWNLOAD BUTTON
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            figMale.write_image(tmpfile.name, width=800, height=600, scale=2)
            tmpfile_path = tmpfile.name

        with open(tmpfile_path, "rb") as file:
            st.download_button(
                label="Download figure",
                data=file,
                file_name="plotly_chart.png",
                mime="image/png",
                key='buttom1'
            )

        summary_male = data2[data2["WildType_Yaviza"] == "Male"]["WB_Arm2"].describe().reset_index()
        summary_male.columns = ["Statistic", "Male"]

        st.write("Summary for Males:")
        st.dataframe(summary_male.style.set_properties(**{'text-align': 'center'}))

        female_distribution_text = """
            <h6 style="text-align: justify;">Distribution for Females:</h6>
            <p style="text-align: justify;">
            The distribution of WildType_Yaviza females with WB_Arm2 is roughly symmetric, with a peak between 460 and 479. The wider range indicates more variability within the distribution, with the majority of values clustered closely together around 462.5. There is a slight left skew caused by some low values. No potential outliers are visualized.
             </p>
            """
        st.markdown(female_distribution_text, unsafe_allow_html=True)

        col1, col2 = st.columns([2, 2])
        with col1:
            num_bins = st.slider('Number of Bins', min_value=1, max_value=15, value=5, key='num_bins_sliderFemale')

        # Plot histogram for Female
        figFemale = px.histogram(female_data2,
                                 x="WB_Arm2",
                                 nbins=num_bins,
                                 title="WB_Arm2 for Female")
        figFemale.update_traces(marker_color='#7201a8',
                                marker_line_color='#7201a8',
                                marker_line_width=2,
                                marker_line=dict(width=2, color='#380340'),
                                opacity=0.6)
        figFemale.update_layout(xaxis_title="WB_Arm2",
                                yaxis_title="Frequency",
                                title={
                                    'text': "WB_Arm2 for Female",
                                    'x': 0.5,
                                    'xanchor': 'center'
                                },
                                width=600,
                                height=500)
        st.plotly_chart(figFemale)
        # DOWNLOAD BUTTON
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            figFemale.write_image(tmpfile.name, width=800, height=600, scale=2)
            tmpfile_path = tmpfile.name

        with open(tmpfile_path, "rb") as file:
            st.download_button(
                label="Download figure",
                data=file,
                file_name="plotly_chart.png",
                mime="image/png",
                key='buttom2'
            )

        summary_female = data2[data2["WildType_Yaviza"] == "Female"]["WB_Arm2"].describe().reset_index()
        summary_female.columns = ["Statistic", "Female"]

        st.write("Summary for Females:")
        st.dataframe(summary_female.style.set_properties(**{'text-align': 'center'}))

        st.write("### One-Way ANOVA with a significance level of α = 0.05")
        # Convert 'WildType_Yaviza' to a categorical variable
        data2['gender'] = pd.Categorical(data2['WildType_Yaviza'])

        # Fit the ANOVA model
        model = ols('WB_Arm2 ~ gender', data=data2).fit()

        # Display the summary of the model
        anova_table = sm.stats.anova_lm(model, typ=2)
        st.write(anova_table)

        st.write(
            "Since the p-value (0.0116) is less than the common significance level of 0.05, we reject the null hypothesis. "
            "This suggests that there is a statistically significant difference in WB_Arm2 values between genders at the 5% significance level. "
            "In other words, it indicates that gender has a significant impact on WB_Arm2 values for WildType_Yaviza distribution.")

elif group == "Conclusion" :
    data = {
        'Population': ['J06_No_Irrad', 'J06_No_Irrad', 'J06_Irrad', 'J06_Irrad', 'WildType_Yaviza',
                                   'WildType_Yaviza'],
        'Variable': ['WB_Arm1', 'WB_Arm2', 'WB_Arm1', 'WB_Arm2', 'WB_Arm1', 'WB_Arm2'],
        'p-value': [0.1075, 0.0213, 0.2518, 0.3922, 0.0379, 0.0116],
        'Result': ['Not Significant', 'Significant', 'Not Significant', 'Not Significant', 'Significant', 'Significant']
    }

    df = pd.DataFrame(data)
    st.table(df)

    st.markdown(
        """
        <div style="text-align: justify">
        
        **Conclusion:**

        The overall results table summarizes the statistical significance of the differences in dependent variable (WB_Arm1 and WB_Arm2) across different experimental population (J06_No_Irrad, J06_Irrad, and WildType_Yaviza).
        1. For the J06_No_Irrad population, WB_Arm1 showed a p-value of 0.1075, indicating that the difference in means between genders was not statistically significant. However, for WB_Arm2 under the same population, the p-value was 0.0213, indicating a statistically significant difference between genders.
        3. For the J06_Irrad population, neither WB_Arm1 (p-value of 0.2518) nor WB_Arm2 (p-value of 0.3922) showed statistically significant differences between genders.
        4. For the WildType_Yaviza population, both WB_Arm1 (p-value of 0.0379) and WB_Arm2 (p-value of 0.0116) showed statistically significant differences between genders.

        Overall, these results suggest that gender has a significant impact on WB_Arm2 values, particularly for the WildType_Yaviza population, but not necessarily for WB_Arm1.
        </div>
        """,
        unsafe_allow_html=True
    )

elif group == "One Way (ANOVA)" :
    anovas = st.radio("Select distribution:", ("WB_Arm1", "WB_Arm2"), index=0)
    if anovas == "WB_Arm1":
        st.sidebar.subheader("Color customization")
        ### COLOR PICKER
        default_colors = {
            'J06_No_Irrad': '#09387D',
            'J06_Irrad': '#08519C',
            'WildType_Yaviza': '#6BAED6'
        }
        color_pickers = {}
        for group_name in default_colors.keys():
            color_pickers[group_name] = st.sidebar.color_picker(f"Pick a color for {group_name}",
                                                                default_colors[group_name])
############# FIGURE 1
        fig = go.Figure()
        for i, col in enumerate(data3["group"].unique()):
            subset = data3[data3["group"] == col]
            fig.add_trace(go.Box(
                y=subset["WB_Arm1"],
                name=col,
                boxpoints='suspectedoutliers',
                marker_color=color_pickers[col],
                line_color=color_pickers[col]
            ))
            fig.update_layout(
                title={
                    'text': "Comparison of WB_Arm1 by Population Group",
                    'x': 0.5,
                    'xanchor': 'center'
                },
                xaxis_title="Group",
                yaxis_title="WB_Arm1",
                width=750,
                height=650,
            )
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.write("")
        with col2:
            st.plotly_chart(fig)
        with col3:
            st.write("")
            # DOWNLOAD BUTTON
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                fig.write_image(tmpfile.name, width=800, height=600, scale=2)
                tmpfile_path = tmpfile.name

            with open(tmpfile_path, "rb") as file:
                st.download_button(
                    label="Download figure",
                    data=file,
                    file_name="plotly_chart.png",
                    mime="image/png",
                    key="b1"
                )

############# FIGURE 2
        fig1 = px.strip(df3, x='group', y='WB_Arm1', color='group', color_discrete_map=color_pickers)
        fig1.update_layout(
            title={
                'text': "Spread of WB_Arm1 Across Population Groups",
                'x': 0.5,
                'xanchor': 'center'
            },
            xaxis_title="Group",
            yaxis_title="WB_Arm1",
            width=600,
            height=500,
        )
        st.divider()
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            st.plotly_chart(fig1)

            # DOWNLOAD BUTTON
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                fig1.write_image(tmpfile.name, width=800, height=600, scale=2)
                tmpfile_path = tmpfile.name

            with open(tmpfile_path, "rb") as file:
                st.download_button(
                    label="Download figure",
                    data=file,
                    file_name="plotly_chart.png",
                    mime="image/png",
                    key="b2"
                )
        with col2:
            st.write("")
        with col3:
            J06NO_distribution_text = """
                                <h6 style="text-align: justify;">J06_NO_Irrad distribution:</h6>
                                <p style="text-align: justify;"> 
                                The distribution of J06_No_Irrad with WB_Arm1 is approximately symmetric and unimodal, ranging between 158 and 285. The low variability suggests that most of the population centers around 226, with some potential outliers at extreme values. This distribution pattern indicates a relatively stable central tendency with notable deviations, which could be explored further to understand factors contributing to these outliers.
                                """
            st.markdown(J06NO_distribution_text, unsafe_allow_html=True)

            J06_distribution_text = """
                                <h6 style="text-align: justify;">J06_Irrad distribution:</h6>
                                <p style="text-align: justify;">
                                The distribution of J06_Irrad with WB_Arm1 is skewed to the left, unimodal, and exhibits a wider spread, with data ranging from 149 to 277. The median value of 223.5 indicates that the majority of J06_Irrad is centered around this point. However, the presence of lower values pulls the mean to the left. Visual inspection identifies potential outlier at 149. 
                                """
            st.markdown(J06_distribution_text, unsafe_allow_html=True)

            WildType_Yaviza_distribution_text = """
                                            <h6 style="text-align: justify;">WildType_Yaviza distribution:</h6>
                                            <p style="text-align: justify;">
                                            The distribution of WildType_Yaviza with WB_Arm1 appears to be approximately symmetric, characterized by a prominent peak between 230-239 and a notable spread, indicating considerable variability. Observations below the median value of 233 skew the mean towards the lower end, resulting in a slight leftward tail. Visual inspection identifies potential outliers above the upper quartile (Q3) and below the lower quartile (Q1).
                                             """
            st.markdown(WildType_Yaviza_distribution_text, unsafe_allow_html=True)

############## FIGURE 3
        num_bins = st.slider('Number of Bins', min_value=1, max_value=15, value=5, key='num_bins_sliderFemale')
        col1, col2, col3 = st.columns([1, 1, 1])
        for i, group_name in enumerate(color_pickers.keys()):
            group_data = data3[data3['group'] == group_name]
            fig2 = px.histogram(group_data, x='WB_Arm1', color='group',
                               color_discrete_map={group_name: color_pickers[group_name]},
                               nbins=num_bins)
            fig2.update_traces(marker_color=color_pickers[group_name],
                              marker_line_color=color_pickers[group_name],
                              marker_line_width=2,
                              opacity=0.6)
            fig2.update_layout(width=450, height=400, showlegend=False,
                              title=f'Distribution of WB_Arm1 for {group_name}', title_x=0.5,
                              title_xanchor='center')

            # Display each figure in its respective column
            if i == 0:
                with col1:
                    st.plotly_chart(fig2)
            elif i == 1:
                with col2:
                    st.plotly_chart(fig2)
            else:
                with col3:
                    st.plotly_chart(fig2)

        # Initialize placeholders for summary tables in each column
        summary_tables_A = []
        summary_tables_B = []
        summary_tables_C = []

        # Loop through each group in data3
        for i, col in enumerate(data3["group"].unique()):
            # Subset data for the current group
            subset = data3[data3["group"] == col]

            # Calculate summary statistics for WB_Arm1
            summary_stats = subset["WB_Arm1"].describe().reset_index()
            summary_stats.columns = ["Statistic", "Value"]

            # Determine which column to append the summary table to
            if i % 3 == 0:
                summary_tables_A.append((col, summary_stats))
            elif i % 3 == 1:
                summary_tables_B.append((col, summary_stats))
            else:
                summary_tables_C.append((col, summary_stats))

        # Display each summary table in its respective column
        col1, col2, col3 = st.columns(3)

        with col1:
            for group_name, summary_table in summary_tables_A:
                st.write(f"Summary for {group_name}:")
                st.dataframe(summary_table.style.set_properties(**{'text-align': 'center'}))

        with col2:
            for group_name, summary_table in summary_tables_B:
                st.write(f"Summary for {group_name}:")
                st.dataframe(summary_table.style.set_properties(**{'text-align': 'center'}))

        with col3:
            for group_name, summary_table in summary_tables_C:
                st.write(f"Summary for {group_name}:")
                st.dataframe(summary_table.style.set_properties(**{'text-align': 'center'}))

        st.divider()
        st.write("### One-Way ANOVA with a significance level of α = 0.05")
        groups = data3.groupby('group')
        group1 = groups.get_group('J06_No_Irrad')['WB_Arm1']
        group2 = groups.get_group('J06_Irrad')['WB_Arm1']
        group3 = groups.get_group('WildType_Yaviza')['WB_Arm1']

        # Performing ANOVA
        f_statistic, p_value = f_oneway(group1, group2, group3)
        df_between = len(data3['group'].unique()) - 1
        df_within = len(data3) - len(data3['group'].unique())
        alpha = 0.05
        critical_value = f.ppf(1 - alpha, df_between, df_within)

        # Fit the model using ordinary least squares
        model = smf.ols('WB_Arm1 ~ C(group)', data=data3).fit()
        anova_table = sm.stats.anova_lm(model, typ=2)

        # Display the ANOVA table in Streamlit
        st.write(anova_table)
        st.write("- **F-statistic:**", f_statistic)
        st.write("- **p-value:**", p_value)
        st.write("- **Critical value at α = 0.05:**", critical_value)

        # Writing the results
        st.write("###### 1. Set up the hypotheses:")
        st.write("- **H0**: μJ06_No_Irrad = μJ06_Irrad = μWildType_Yaviza (All underlying population means are equal)")
        st.write("- **H1**: μi ≠ μj for some i and j (Not all of the underlying population means are equal)")
        st.write("- **α** = 0.05")

        st.write("###### 2. Decision Rule:")
        st.write(
            "With a significance level (probability) of α = 0.05 and degrees of freedom df1 = 2 and df2 = 717, the corresponding critical value is 3.00828.")
        st.write(
            "The decision rule states that we reject the null hypothesis (H0) if the F-statistic is greater than or equal to 3.00828.")
        st.write("Otherwise, we do not reject H0.")

        st.write("###### 3. Conclusion:")
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

        st.divider()
        tukey_results = pairwise_tukeyhsd(data3['WB_Arm1'], data3['group'])

        # Displaying the results as a table
        st.write("""### Tukey's HSD Test """)
        st.write(pd.DataFrame(tukey_results.summary()))

        st.write("""
 
        In this output from the pairwise Tukey's HSD test, each row represents a pairwise comparison between two groups. Here's how to interpret the values:

        - **group1** and **group2**: The two groups being compared.
        - **meandiff**: The difference in means between the two groups.
        - **p-adj**: The adjusted p-value, which is the probability of observing a result as extreme as the one obtained, assuming that the null hypothesis is true. It is adjusted for multiple comparisons.
        - **lower** and **upper**: The lower and upper bounds of the confidence interval for the mean difference.
        - **reject**: Indicates whether the null hypothesis of equal means is rejected. If True, it means that there is a significant difference between the means of the two groups. If False, it means that there is no significant difference.

        ### Interpretation of Each Row

        1. **Comparison between J06_Irrad and J06_No_Irrad**:
           - Mean difference is 4.1458.
           - Adjusted p-value is 0.0801, indicating no significant difference between the means (although it's close to the 0.05 threshold).
           - The 95% confidence interval for the mean difference ranges from -0.376 to 8.6676.
           - Conclusion: Fail to reject the null hypothesis (False), but there might be a trend towards significance.

        2. **Comparison between J06_Irrad and WildType_Yaviza**:
           - Mean difference is 9.8167.
           - Adjusted p-value is very low (0.0), indicating a significant difference between the means.
           - The 95% confidence interval for the mean difference ranges from 5.2949 to 14.3385.
           - Conclusion: Reject the null hypothesis (True), suggesting a significant difference between the means.

        3. **Comparison between J06_No_Irrad and WildType_Yaviza**:
           - Mean difference is 5.6708.
           - Adjusted p-value is 0.0093, indicating a significant difference between the means.
           - The 95% confidence interval for the mean difference ranges from 1.149 to 10.1926.
           - Conclusion: Reject the null hypothesis (True), indicating a significant difference between the means.
        """)
    else:
        st.sidebar.subheader("Color customization")
        ### COLOR PICKER
        default_colors = {
            'J06_No_Irrad': '#09387D',
            'J06_Irrad': '#08519C',
            'WildType_Yaviza': '#6BAED6'
        }
        color_pickers = {}
        for group_name in default_colors.keys():
            color_pickers[group_name] = st.sidebar.color_picker(f"Pick a color for {group_name}",
                                                                default_colors[group_name])
        ############# FIGURE 1
        fig = go.Figure()
        for i, col in enumerate(data3["group"].unique()):
            subset = data3[data3["group"] == col]
            fig.add_trace(go.Box(
                y=subset["WB_Arm2"],
                name=col,
                boxpoints='suspectedoutliers',
                marker_color=color_pickers[col],
                line_color=color_pickers[col]
            ))
            fig.update_layout(
                title={
                    'text': "Comparison of WB_Arm2 by Population Group",
                    'x': 0.5,
                    'xanchor': 'center'
                },
                xaxis_title="Group",
                yaxis_title="WB_Arm2",
                width=750,
                height=650,
            )
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.write("")
        with col2:
            st.plotly_chart(fig)
        with col3:
            st.write("")
            # DOWNLOAD BUTTON
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                fig.write_image(tmpfile.name, width=800, height=600, scale=2)
                tmpfile_path = tmpfile.name

            with open(tmpfile_path, "rb") as file:
                st.download_button(
                    label="Download figure",
                    data=file,
                    file_name="plotly_chart.png",
                    mime="image/png",
                    key="b1"
                )
        ############# FIGURE 2
        fig1 = px.strip(df3, x='group', y='WB_Arm2', color='group', color_discrete_map=color_pickers)
        fig1.update_layout(
            title={
                'text': "Spread of WB_Arm2 Across Population Groups",
                'x': 0.5,
                'xanchor': 'center'
            },
            xaxis_title="Group",
            yaxis_title="WB_Arm2",
            width=600,
            height=500,
        )
        st.divider()
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            st.plotly_chart(fig1)

            # DOWNLOAD BUTTON
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                fig1.write_image(tmpfile.name, width=800, height=600, scale=2)
                tmpfile_path = tmpfile.name

            with open(tmpfile_path, "rb") as file:
                st.download_button(
                    label="Download figure",
                    data=file,
                    file_name="plotly_chart.png",
                    mime="image/png",
                    key="b2"
                )
        with col2:
            st.write("")
        with col3:
            J06NO_distribution_text = """
                                    <h6 style="text-align: justify;">J06_NO_Irrad distribution:</h6>
                                    <p style="text-align: justify;"> 
                                    The distribution of WB_Arm2 for the J06_No_Irrad population is bimodal, with two peaks between 400-449 and 450-499. The wider range suggests high variability, with a standard deviation of 48.746. There is a slight rightward tail, indicating some skewness. The center of the distribution is around 454.43. Multiple potential outliers are visible and should be further studied to understand their impact on the data.
                                    """
            st.markdown(J06NO_distribution_text, unsafe_allow_html=True)

            J06_distribution_text = """
                                    <h6 style="text-align: justify;">J06_Irrad distribution:</h6>
                                    <p style="text-align: justify;">
                                    The distribution of WB_Arm2 for the J06_Irrad population is unimodal and left-skewed. The data ranges from 304 to 555, with a few values at the lower end pulling the mean in that direction. A few potential outliers below the first quartile (Q1) are visualized in the boxplot.
                                    """
            st.markdown(J06_distribution_text, unsafe_allow_html=True)

            WildType_Yaviza_distribution_text = """
                                                <h6 style="text-align: justify;">WildType_Yaviza distribution:</h6>
                                                <p style="text-align: justify;">
                                                The distribution of WB_Arm2 for the WildType_Yaviza population is symmetric and unimodal, with a wider range indicating higher variability. Some values pulling the mean to the left contribute to a slight left tail. Potential outliers are visible in the boxplot.
                                                 """
            st.markdown(WildType_Yaviza_distribution_text, unsafe_allow_html=True)
        ############## FIGURE 3
        num_bins = st.slider('Number of Bins', min_value=1, max_value=15, value=5, key='num_bins_sliderFemale')
        col1, col2, col3 = st.columns([1, 1, 1])
        for i, group_name in enumerate(color_pickers.keys()):
            group_data = data3[data3['group'] == group_name]
            fig2 = px.histogram(group_data, x='WB_Arm2', color='group',
                                color_discrete_map={group_name: color_pickers[group_name]},
                                nbins=num_bins)
            fig2.update_traces(marker_color=color_pickers[group_name],
                               marker_line_color=color_pickers[group_name],
                               marker_line_width=2,
                               opacity=0.6)
            fig2.update_layout(width=450, height=400, showlegend=False,
                               title=f'Distribution of WB_Arm2 for {group_name}', title_x=0.5,
                               title_xanchor='center')

            # Display each figure in its respective column
            if i == 0:
                with col1:
                    st.plotly_chart(fig2)
            elif i == 1:
                with col2:
                    st.plotly_chart(fig2)
            else:
                with col3:
                    st.plotly_chart(fig2)

        # Initialize placeholders for summary tables in each column
        summary_tables_A = []
        summary_tables_B = []
        summary_tables_C = []

        # Loop through each group in data3
        for i, col in enumerate(data3["group"].unique()):
            # Subset data for the current group
            subset = data3[data3["group"] == col]

            # Calculate summary statistics for WB_Arm2
            summary_stats = subset["WB_Arm2"].describe().reset_index()
            summary_stats.columns = ["Statistic", "Value"]

            # Determine which column to append the summary table to
            if i % 3 == 0:
                summary_tables_A.append((col, summary_stats))
            elif i % 3 == 1:
                summary_tables_B.append((col, summary_stats))
            else:
                summary_tables_C.append((col, summary_stats))

        # Display each summary table in its respective column
        col1, col2, col3 = st.columns(3)

        with col1:
            for group_name, summary_table in summary_tables_A:
                st.write(f"Summary for {group_name}:")
                st.dataframe(summary_table.style.set_properties(**{'text-align': 'center'}))

        with col2:
            for group_name, summary_table in summary_tables_B:
                st.write(f"Summary for {group_name}:")
                st.dataframe(summary_table.style.set_properties(**{'text-align': 'center'}))

        with col3:
            for group_name, summary_table in summary_tables_C:
                st.write(f"Summary for {group_name}:")
                st.dataframe(summary_table.style.set_properties(**{'text-align': 'center'}))

        st.divider()
        st.write("### One-Way ANOVA with a significance level of α = 0.05")
        groups = data3.groupby('group')
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
        st.write("- **F-statistic:**", f_statistic)
        st.write("- **p-value:**", p_value)
        st.write("- **Critical value at α = 0.05:**", critical_value)

        # Writing the results
        st.write("###### 1. Set up the hypotheses:")
        st.write("- **H0**: μJ06_No_Irrad = μJ06_Irrad = μWildType_Yaviza (All underlying population means are equal)")
        st.write("- **H1**: μi ≠ μj for some i and j (Not all of the underlying population means are equal)")
        st.write("- **α** = 0.05")

        st.write("###### 2. Decision Rule:")
        st.write(
            "With a significance level (probability) of α = 0.05 and degrees of freedom df1 = 2 and df2 = 717, the corresponding critical value is 3.00828.")
        st.write(
            "The decision rule states that we reject the null hypothesis (H0) if the F-statistic is greater than or equal to 3.00828.")
        st.write("Otherwise, we do not reject H0.")

        st.write("###### 3. Conclusion:")
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


        st.divider()# Performing pairwise Tukey's HSD test
        tukey_results = pairwise_tukeyhsd(data3['WB_Arm2'], data3['group'])

        # Displaying the results as a table
        st.write("""### Tukey's HSD Test """)
        st.write(pd.DataFrame(tukey_results.summary()))

        st.write("""
        
        In this output from the pairwise Tukey's HSD test, each row represents a pairwise comparison between two groups. Here's how to interpret the values:

        - **group1** and **group2**: The two groups being compared.
        - **meandiff**: The difference in means between the two groups.
        - **p-adj**: The adjusted p-value, which is the probability of observing a result as extreme as the one obtained, assuming that the null hypothesis is true. It is adjusted for multiple comparisons.
        - **lower** and **upper**: The lower and upper bounds of the confidence interval for the mean difference.
        - **reject**: Indicates whether the null hypothesis of equal means is rejected. If True, it means that there is a significant difference between the means of the two groups. If False, it means that there is no significant difference.

        ### Interpretation of Each Row

        1. **Comparison between J06_Irrad and J06_No_Irrad**:
           - Mean difference is 7.2083.
           - Adjusted p-value is 0.1825, indicating no significant difference between the means.
           - The 95% confidence interval for the mean difference ranges from -2.3879 to 16.8046.
           - Conclusion: Fail to reject the null hypothesis (False).

        2. **Comparison between J06_Irrad and WildType_Yaviza**:
           - Mean difference is 16.7458.
           - Adjusted p-value is very low (0.0001), indicating a significant difference between the means.
           - The 95% confidence interval for the mean difference ranges from 7.1496 to 26.3421.
           - Conclusion: Reject the null hypothesis (True), suggesting a significant difference between the means.

        3. **Comparison between J06_No_Irrad and WildType_Yaviza**:
           - Mean difference is 9.5375.
           - Adjusted p-value is 0.0518, which is slightly above the significance level of 0.05, indicating a borderline significant difference.
           - The 95% confidence interval for the mean difference ranges from -0.0587 to 19.1337.
           - Conclusion: Borderline fail to reject the null hypothesis (False), suggesting a potential difference but not statistically significant at the 0.05 level.
        """)
