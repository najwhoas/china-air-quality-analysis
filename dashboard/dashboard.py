import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns
# -*- coding: utf-8 -*-


st.header('Proyek Analisis Data: Air Quality Analysis')
"""- **Nama:** Najwa Salsabila
- **Email:** najwasalsabieee@gmail.com
- **ID Dicoding:** najwasalsabila"""


path = os.path.dirname(__file__)
my_file = path+'/dashboard/photo.png'
df = pd.read_csv(file_path)


st.subheader('DataFrame Overview')
df_desc = df.describe().transpose()
st.write(df_desc)


st.set_option('deprecation.showPyplotGlobalUse', False)

st.write(" ")

st.subheader('Polutan apa saja yang berhubungan dengan jumlah penyebaran Partikulat 2.5?')
plt.figure(figsize=(20,7))
sns.heatmap(df.corr(numeric_only=True), vmin=-1, vmax=1, center=0, cmap='YlGnBu', annot=True)
st.pyplot(plt)
st.write('Polutan paling signifikan hubungannya dengan Partikulat 2.5 adalah Partikulat 10, lalu disusul dengan Karbon Monoksida, Nitrogen Dioksida, Sulfur Dioksida, dan titik embun.')

st.subheader('Bagaimana perbandingan rata-rata sebaran Partikulat 2.5 dan Partikulat 10 pada setiap wilayah?')
partikulats = df.groupby('Wilayah')[['Partikulat_2.5','Partikulat_10',]].mean().reset_index()
partikulats

c=np.arange(len(partikulats['Wilayah']))
plt.figure(figsize=(16,7))
plt.xticks(c,partikulats['Wilayah'])
plt.xlabel('Wilayah')
plt.ylabel('Persebaran Partikulat')
plt.bar(c,partikulats['Partikulat_10'],label='Partikulat 10',width=0.4,color='#8CB9BD')
plt.bar(c+0.2,partikulats['Partikulat_2.5'],label='Partikulat 2.5',width=0.4,color='#ECB159')
plt.legend()
plt.title("Rata-rata Penyebaran Partikulat di Tiap Wilayah", fontsize=15)
plt.grid(axis='y')
st.pyplot(plt)

c=np.arange(len(partikulats['Wilayah']))
colorspm25 = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#ECB159", "#D3D3D3","#D3D3D3", "#D3D3D3", "#D3D3D3","#D3D3D3", "#D3D3D3", "#D3D3D3","#D3D3D3"]
colorspm10 = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3","#8CB9BD", "#D3D3D3", "#D3D3D3","#D3D3D3", "#D3D3D3", "#D3D3D3","#D3D3D3"]
plt.figure(figsize=(16,7))
plt.xticks(c,partikulats['Wilayah'])
plt.xlabel('Wilayah')
plt.ylabel('Persebaran Partikulat')
plt.bar(c,partikulats['Partikulat_10'],width=0.4,color=colorspm10)
plt.bar(c+0.2,partikulats['Partikulat_2.5'],width=0.4,color=colorspm25)
plt.title("Rata-rata Penyebaran Partikulat Terbesar", fontsize=15)
plt.grid(axis='y')
st.pyplot(plt)
st.write('Untuk setiap wilayah, kadar polutan PM 10 selalu lebih tinggi dari PM 2.5. Penyebaran polutan PM 10 terbanyak terjadi di wilayah Gucheng. Sementara, untuk penyebaran polutan PM 2.5 paling banyak terjadi di Dongsi, walau sebenarnya hanya berselisih dengan Gucheng sebesar 1.52 ppm. Dengan angka ini, dapat dikatakan bahwa wilayah dengan kadar polutan PM 2.5 dan PM 10 yang penyebarannya tinggi adalah Gucheng.')

st.write(" ")

st.subheader('Bagaimana proporsi polutan Sulfur Dioksida, Nitrogen Dioksida, dan Karbon Monoksida pada Tahun 2017 di Wilayah Gucheng?')

gucheng_df = pd.read_csv("https://github.com/marceloreis/HTI/raw/master/PRSA_Data_20130301-20170228/PRSA_Data_Gucheng_20130301-20170228.csv")

gucheng_df.fillna(method='ffill', inplace=True, axis=0)

numeric_df = gucheng_df.select_dtypes(include='number')

Q1 = numeric_df.quantile(0.25)
Q3 = numeric_df.quantile(0.75)
IQR = Q3 - Q1

maximum = Q3 + (1.5 * IQR)
minimum = Q1 - (1.5 * IQR)

kondisi_lower_than = numeric_df < minimum
kondisi_more_than = numeric_df > maximum
gucheng_df = gucheng_df.mask(cond=kondisi_more_than, other=maximum, axis=0)
gucheng_df = gucheng_df.mask(cond=kondisi_lower_than, other=minimum, axis=0)



gucheng_df.info()

mean = gucheng_df[gucheng_df['year'] == 2017][['PM2.5','PM10','SO2', 'NO2', 'CO']].mean()
total = mean.sum()


fig, ax = plt.subplots()
ax.pie(mean/total, autopct='%0.1f%%', colors=['#F39233','#EEF296','#EF4F4F','#9ADE7B','#2D9596'], startangle=140)
ax.axis('equal')
ax.legend(['PM2.5','PM10','SO2', 'NO2', 'CO'])
ax.set_title('Proporsi Polutan Udara di Wilayah Gucheng Tahun 2017')
st.pyplot(fig)
st.write('Pada tahun 2017, dari 100% besar polutan yang ada di Gucheng, 85.3% didominasi oleh karbon monoksida. Kemudian disusul dengan proporsi PM 10 sebesar 6%, PM 2.5 sebesar 4.8%, Nitrogen Dioksida sebesar 2.9%, dan Sulfur Dioksida 1%. Ini mengindikasikan bahwa polutan berupa gas buang dari kendaraan atau macam-macam alat pembakaran lainnya mendominasi polusi udara di Gucheng.')

st.write(" ")

st.subheader('Bagaimana tren persebaran polutan Partikulat 2.5, Partikulat 10, Sulfur Dioksida, Nitrogen Dioksida, dan Karbon Monoksida per 6 bulan di wilayah Gucheng?')

gucheng_df['waktu'] = df['Waktu_Pengamatan']
gucheng_df['waktu'] = pd.to_datetime(gucheng_df['waktu'])

gucheng_df.set_index('waktu', inplace=True)

data = gucheng_df.resample('M').mean()

plt.figure(figsize=(15, 6))
plt.plot(data['PM2.5'], label='Partikulat 2.5', color='#F39233')
plt.plot(data['PM10'], label='Partikulat 10', color='#EEF296')
plt.plot(data['SO2'], label='Sulfur Dioksida', color='#EF4F4F')
plt.plot(data['NO2'], label='Nitrogen Dioksida', color='#9ADE7B')
plt.plot(data['CO'], label='Karbon Dioksida', color='#2D9596')

plt.title('Tren Persebaran Polutan per 6 Bulan di Wilayah Gucheng')
plt.xlabel('Waktu Pengamatan')
plt.ylabel('Kadar Polutan')
plt.legend()

st.pyplot(plt)
st.write('Tren persebaran polutan per 6 bulan di Gucheng menunjukkan bahwa persebaran karbon monoksida selalu mengalami kenaikan yang pesat pada awal tahun. Sementara polutan lainnya cenderung stagnan, tidak terlalu signifikan kenaikan dan penurunannya.')

st.write(" ")

st.subheader("Bagaimana tren keadaan gas ozon dan temperatur udara per 6 Bulan di wilayah Gucheng?")

data = gucheng_df.resample('M').mean()

plt.figure(figsize=(15, 6))
plt.plot(data['O3'], label='Gas Ozon', color='#F39233')
plt.plot(data['TEMP'], label='Temperatur Udara', color='#2D9596')

plt.xlabel("Waktu Pengamatan")
plt.ylabel("Kadar")

plt.title("Tren Keadaan Gas Ozon dan Temperatur Udara per 6 Bulan di Wilayah Gucheng")

plt.legend()
st.pyplot(plt)
st.write('Berbanding dengan kondisi karbon monoksida, gas ozon selalu mencapai titik tertingginya di pertengahan tahun (Juli). Keadaan temperatur udara juga mengalami pergerakan naik turun yang sama dengan gas ozon. Dengan keadaan ini, dapat diasumsikan bahwa jika temperatur udara sedang tinggi, besar kemungkinan kadar gas O3 juga tinggi. Ini bisa menjadi petunjuk bagi warga Gucheng untuk berantisipasi melindungi diri, seperti menggunakan masker.')


st.header("Insight")
st.write('Berdasarkan penelitian, Karbon Monoksida (CO) merupakan salah satu prekursor pembentuk gas O3 yang dihasilkan dari proses fotokimia. Berdasarkan data yang ada, keadaan CO dan O3 mengalami pergerakan berlawanan yang lumayan konsisten. Saat CO berada di titik tinggi, O3 berada di titik rendah.')
st.write('Dengan keadaan tersebut, dapat diasumsikan bahwa proses fotokimia pembentukan ozon permukaan (O3) terjadi selama kurang lebih 6 bulan secara kontinu.')


st.set_option('deprecation.showPyplotGlobalUse', False)
