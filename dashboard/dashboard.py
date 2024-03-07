import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

all_df = pd.read_csv("https://raw.githubusercontent.com/najwhoas/china-air-quality-analysis/main/dashboard/all_data.csv")
df = pd.read_csv("https://github.com/marceloreis/HTI/raw/master/PRSA_Data_20130301-20170228/PRSA_Data_Gucheng_20130301-20170228.csv")

df.fillna(method='ffill', inplace=True, axis=0)
numeric_df = df.select_dtypes(include='number')
Q1 = numeric_df.quantile(0.25)
Q3 = numeric_df.quantile(0.75)
IQR = Q3 - Q1
maximum = Q3 + (1.5 * IQR)
minimum = Q1 - (1.5 * IQR)
kondisi_lower_than = numeric_df < minimum
kondisi_more_than = numeric_df > maximum
df = df.mask(cond=kondisi_more_than, other=maximum, axis=0)
df = df.mask(cond=kondisi_lower_than, other=minimum, axis=0)

st.title('Gucheng Air Quality 🌨️')
st.write('Analysis of air quality in Gucheng, China&mdash;from 2013 to 2017.')
st.write('*&mdash;by: Najwa Salsabila*')

st.write("__________________")

import streamlit as st

st.markdown(
    """
    <style>
        .container {
            padding: 10px;
            border: 1px solid #d3d3d3;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        .tabs {
            # font-size: 100px !important;
            }
    </style>
    """,
    unsafe_allow_html=True
)

st.header('Recent Condition  &mdash;•')
container = st.container()
columns = st.columns(3)


tile1 = columns[0].container(height=130)
tile1.metric("Average CO Concentration", "82.3%")
tile2 = columns[1].container(height=130)
tile2.metric("Average PM 2.5", "5.03%")
tile3 = columns[2].container(height=130)
tile3.metric("Temperature", "2.2°C")

st.header('')
st.header('')

tab1,tab2,tab3,tab4,tab5,tab6,tab7 = st.tabs(["Data", "Correlation", "Polutant Proportions", "Particulat Consentration", "Polutant Trend", "Ozon Trend","Insight"])


tab1.subheader('DataFrame Overview &mdash;')
df_desc = all_df.describe().transpose()
tab1.write(df_desc)

tab2.subheader('Columns Correlation &mdash;')
fig = px.imshow(all_df.corr(numeric_only=True), color_continuous_scale='YlGnBu')
tab2.plotly_chart(fig)
tab2.write('The most significant pollutant correlated with Particulate 2.5 is Particulate 10, followed by Carbon Monoxide, Nitrogen Dioxide, Sulfur Dioxide, and dew point.')

tab3.subheader('Pollutants Proportions in 2017 &mdash;')
polutant = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO']
mean = df[df['year'] == 2017][['PM2.5', 'PM10', 'SO2', 'NO2', 'CO']].mean()
total = mean.sum()
proportion = mean / total
col1, col2 = st.columns([1, 3])
fig = px.pie(names=polutant, values=proportion.values, labels=proportion.index,
             color_discrete_sequence=px.colors.sequential.YlGnBu_r)
tab3.plotly_chart(fig)
tab3.write('In 2017, of the top 100% of pollutants in Gucheng, 85.3% was dominated by carbon monoxide. This was followed by the proportion of PM 10 at 6%, PM 2.5 at 4.8%, Nitrogen Dioxide at 2.9%, and Sulfur Dioxide at 1%. This indicates that pollutants in the form of exhaust gases from vehicles or other kinds of burning equipment dominate the air pollution in Gucheng.')


tab4.subheader('Average Particulate Concentration in Each Station')
tab4.header("")
partikulats = all_df.groupby('Wilayah')[['Partikulat_2.5', 'Partikulat_10']].mean().reset_index()
tab4.bar_chart(partikulats.set_index('Wilayah'))
tab4.write('For each station, PM 10 pollutant levels are always higher than PM 2.5. The spread of PM 10 pollutants is highest in the Gucheng station. Meanwhile, the spread of PM 2.5 pollutants is highest in Dongsi, although it is actually only at odds with Gucheng by 1.52 ppm. With these figures, it can be said that the station with the highest levels of PM 2.5 and PM 10 pollutants is Gucheng.')


df['waktu'] = all_df['Waktu_Pengamatan']
df['waktu'] = pd.to_datetime(df['waktu'])
df.set_index('waktu', inplace=True)
data = df.resample('M').mean()

tab5.subheader('Trend of Polutant Concentration &mdash;')
tab5.subheader("")
tab5.line_chart(data[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO']], use_container_width=True)
tab5.write('The trend of pollutant distribution per 6 months in Gucheng shows that the distribution of carbon monoxide always increases rapidly at the beginning of the year. While other pollutants tend to stagnate, there is not too significant an increase and decrease.')


tab6.subheader('Trend of Ozon Consentration and Temperature &mdash;')
tab5.subheader("")
tab6.line_chart(data[['O3', 'TEMP']], use_container_width=True)
tab6.write('Compared to carbon monoxide, ozone gas always reaches its highest point in the middle of the year (July). The air temperature also experiences the same up and down movement as ozone gas. With this situation, it can be assumed that if the air temperature is high, it is likely that the O3 gas level is also high. This could be a warning for Gucheng residents to take precautions to protect themselves, such as wearing masks.')

tab7.subheader("Insight &mdash;")
tab7.subheader("")
tab7.write('Based on research, Carbon Monoxide (CO) is one of the precursors of O3 gas resulting from photochemical processes. Based on the available data, the state of CO and O3 experiences a fairly consistent opposite movement. When CO is at a high point, O3 is at a low point.')
tab7.write('Under these circumstances, it can be assumed that the photochemical process of surface ozone (O3) formation occurred for approximately 6 months continuously.')
