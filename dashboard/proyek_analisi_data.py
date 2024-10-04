# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import io
import contextlib

# Set page title
st.title("Proyek Analisis Data: Bike-sharing Dataset")

# Penulis Info
st.subheader("Informasi Penulis")
st.write("**Nama:** Annisa Silvia Chaniago")
st.write("**Email:** M183B4KX0585@bangkit.academy")
st.write("**ID Dicoding:** M183B4KX0585")

st.title("Data Wrangling")
# Gathering Data
st.header("Gathering Data Data")
"""### Mencari isi Informasi masing-masing data"""
day_df = pd.read_csv('https://raw.githubusercontent.com/kyunisoo/Bike-sharing-dataset/refs/heads/main/day.csv')
hour_df = pd.read_csv('https://raw.githubusercontent.com/kyunisoo/Bike-sharing-dataset/refs/heads/main/hour.csv')
st.write("Data Hari (day_df):")
st.write(day_df.head())
st.write("Data Jam (hour_df):")
st.write(hour_df.head())

"""### **Insight:**
- Dataset terdiri dari dua data yaitu data hari (day.csv) dan data jam (hour.csv).
- Masing-masing data memiliki kolom yang sama, namun isi data yang berbeda."""

# Assessing Data
st.header("Assessing Data")

# Mengambil info Day Data
day_info_buffer = io.StringIO()
with contextlib.redirect_stdout(day_info_buffer):
    day_df.info()

st.write("Info Day Data:")
st.text(day_info_buffer.getvalue())

# Mengambil info Hour Data
hour_info_buffer = io.StringIO()
with contextlib.redirect_stdout(hour_info_buffer):
    hour_df.info()

st.write("Info Hour Data:")
st.text(hour_info_buffer.getvalue())

st.write("Jumlah duplikasi Day Data: ", day_df.duplicated().sum())
st.write("Jumlah duplikasi Hour Data: ", hour_df.duplicated().sum())

st.write("Deskripsi Day Data:")
st.write(day_df.describe())

st.write("Deskripsi Hour Data:")
st.write(hour_df.describe())

"""### **Insight:**
- Pada data day.csv maupun hour.csv sudah terlihat bersih dan tidak terjadi duplikasi dari masing-masing data.
- Pada saat melakukan .info() saya menemukan adanya ketidaksesuaian penggunaan type data yaitu pada bagian dteday yang mana
disitu type datanya object, seharusnya diubah menjadi datetime, lalu untuk kolom season, yr, mnth, hr, holiday, weekday, dan weathersit 
dapat diubah menjadi tipe category untuk efisiensi dan analisis lebih baik."""

# Cleaning Data
st.header("Cleaning Data")
dteday_columns = ["dteday"]

# Mengubah tipe data
for column in dteday_columns:
    day_df[column] = pd.to_datetime(day_df[column])
    hour_df[column] = pd.to_datetime(hour_df[column])

# Menentukan kolom kategori
category_columns_day = ['season', 'yr', 'mnth', 'holiday', 'weekday', 'weathersit']
category_columns_hour = ['season', 'yr', 'mnth', 'hr', 'holiday', 'weekday', 'weathersit']

# Mengubah kolom menjadi kategori
day_df[category_columns_day] = day_df[category_columns_day].astype('category')
hour_df[category_columns_hour] = hour_df[category_columns_hour].astype('category')

# Menampilkan info setelah pembersihan
st.write("Info Day Data setelah Cleaning:")
day_info_buffer_cleaned = io.StringIO()
with contextlib.redirect_stdout(day_info_buffer_cleaned):
    day_df.info()
st.text(day_info_buffer_cleaned.getvalue())

st.write("Info Hour Data setelah Cleaning:")
hour_info_buffer_cleaned = io.StringIO()
with contextlib.redirect_stdout(hour_info_buffer_cleaned):
    hour_df.info()
st.text(hour_info_buffer_cleaned.getvalue())

# Menampilkan deskripsi DataFrame
st.write("Deskripsi Day Data setelah Cleaning:")
st.write(day_df.describe())

st.write("Deskripsi Hour Data setelah Cleaning:")
st.write(hour_df.describe())

# Mengklasifikasikan Musim
st.header("Mengklasifikasikan Musim")
def classify_season(month):
    if month in [12, 1, 2]:
        return 1  # Musim Dingin
    elif month in [3, 4, 5]:
        return 2  # Musim Semi
    elif month in [6, 7, 8]:
        return 3  # Musim Panas
    elif month in [9, 10, 11]:
        return 4  # Musim Gugur

day_df['season'] = day_df['mnth'].apply(classify_season)

season_labels = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
day_df['season'] = day_df['season'].replace(season_labels)

# Menghitung total peminjaman sepeda per musim
seasonal_data = day_df.groupby('season')['cnt'].sum().reset_index()
st.write("Data peminjaman sepeda per musim:")
st.write(seasonal_data)
"""### **Insight:**
- Pada kolom dteday berhasil diubah data typenya menjadi datetime sehingga penggunaannya akan jauh lebih baik
- pada kolom season, yr, hr, mnth, holiday, dan weekend juga sudah berhasil diubah menjadi category."""

st.title("Visualisasi data")
# Membuat visualisasi
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=seasonal_data, x='season', y='cnt', ax=ax, palette='viridis', ci=None)
ax.set_title('Total Peminjaman Sepeda per Musim')
ax.set_xlabel('Musim')
ax.set_ylabel('Jumlah Peminjaman')
ax.grid()

# Menambahkan label nilai di atas setiap bar
for i, v in enumerate(seasonal_data['cnt']):
    ax.text(i, v, f'{v:,}', ha='center', va='bottom')

# Mengatur skala y-axis agar dimulai dari 0
ax.set_ylim(0, max(seasonal_data['cnt']) * 1.1)

# Menampilkan visualisasi di Streamlit
st.pyplot(fig)

# Menghitung Rata-rata Permintaan berdasarkan Hari Libur
st.header("Rata-rata Permintaan berdasarkan Hari Libur")
holiday_stats = day_df.groupby('holiday')['cnt'].agg(['mean', 'sum']).reset_index()
holiday_stats.columns = ['holiday', 'average_demand', 'total_demand']
st.write(holiday_stats)

# Visualisasi Rata-rata Permintaan berdasarkan Hari Libur
st.subheader("Visualisasi: Rata-rata Permintaan Sewa Sepeda berdasarkan Hari Libur")
plt.figure(figsize=(8, 5))
sns.barplot(data=holiday_stats, x='holiday', y='average_demand', palette='Set2')
plt.title('Rata-rata Permintaan Sewa Sepeda berdasarkan Hari Libur')
plt.xlabel('Hari Libur (0 = Tidak, 1 = Ya)')
plt.ylabel('Rata-rata Permintaan')
plt.xticks(ticks=[0, 1], labels=['Tidak Libur', 'Libur'], rotation=0)
st.pyplot(plt)

# Menghitung Rata-rata Permintaan berdasarkan Cuaca
st.header("Rata-rata Permintaan berdasarkan Cuaca")
weather_stats = day_df.groupby('weathersit')['cnt'].agg(['mean']).reset_index()
weather_labels = {1: 'Cuaca Cerah', 2: 'Kabut', 3: 'Salju Ringan', 4: 'Hujan'}
weather_stats['weather_label'] = weather_stats['weathersit'].map(weather_labels)
st.write(weather_stats)

# Visualisasi Rata-rata Permintaan berdasarkan Cuaca
st.subheader("Visualisasi: Rata-rata Permintaan Sewa Sepeda berdasarkan Kondisi Cuaca")
plt.figure(figsize=(10, 6))
sns.barplot(data=weather_stats, x='weather_label', y='mean', palette='mako')
plt.title('Rata-rata Permintaan Sewa Sepeda berdasarkan Kondisi Cuaca')
plt.xlabel('Kondisi Cuaca')
plt.ylabel('Rata-rata Permintaan')
st.pyplot(plt)

"""### **Insight:**
- Menggunakan Bar untuk melihat hasil yang ingin dicari.
- Semua pertanyaan terjawab dari bar yang sudah ditampilkan. Seperti Musim"""

# Analisis Lanjutan
st.title("Analisis Lanjutan")
weekday_stats = day_df.groupby('weekday')['cnt'].agg(['mean', 'sum']).reset_index()
weekday_stats.columns = ['weekday', 'average_demand', 'total_demand']

# Visualisasi Rata-rata Permintaan berdasarkan Hari dalam Seminggu
st.subheader("Visualisasi: Rata-rata Permintaan Sewa Sepeda berdasarkan Hari dalam Seminggu")
plt.figure(figsize=(10, 6))
sns.barplot(data=weekday_stats, x='weekday', y='average_demand', palette='magma')
plt.title('Rata-rata Permintaan Sewa Sepeda berdasarkan Hari dalam Seminggu')
plt.xlabel('Hari dalam Seminggu (0 = Minggu, 1 = Senin, ..., 6 = Sabtu)')
plt.ylabel('Rata-rata Permintaan')
plt.xticks(ticks=range(7), labels=['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'], rotation=45)
st.pyplot(plt)

# Menghitung Rata-rata Permintaan berdasarkan Jam
hour_stats = hour_df.groupby('hr')['cnt'].agg(['mean']).reset_index()

# Visualisasi Rata-rata Permintaan berdasarkan Jam
st.subheader("Visualisasi: Rata-rata Permintaan Sewa Sepeda per Jam")
plt.figure(figsize=(12, 6))
sns.lineplot(data=hour_stats, x='hr', y='mean', marker='o')
plt.title('Rata-rata Permintaan Sewa Sepeda per Jam')
plt.xlabel('Jam')
plt.ylabel('Rata-rata Permintaan')
plt.xticks(range(0, 24))
plt.grid()
st.pyplot(plt)

# Segmentasi Pengguna
st.header("Segmentasi Pengguna")
user_stats = day_df.groupby(['casual', 'registered']).agg({'cnt': 'mean'}).reset_index()

# Visualisasi Segmentasi Pengguna
st.subheader("Visualisasi: Rata-rata Permintaan Sewa Sepeda berdasarkan Segmentasi Pengguna")
plt.figure(figsize=(10, 6))
sns.barplot(data=user_stats, x='casual', y='cnt', color='blue', label='Kasual')
sns.barplot(data=user_stats, x='registered', y='cnt', color='orange', label='Terdaftar')
plt.title('Rata-rata Permintaan Sewa Sepeda berdasarkan Segmentasi Pengguna')
plt.xlabel('Segmentasi Pengguna')
plt.ylabel('Rata-rata Permintaan')
plt.legend()
st.pyplot(plt)

# Conclusion
st.header("Kesimpulan")
st.write(""" 
1. Pengaruh Musim terhadap Penyewaan Sepeda
Hasil analisis menunjukkan bahwa musim panas (summer) adalah periode dengan tingkat penyewaan sepeda tertinggi.
Hal ini dapat dijelaskan oleh sejumlah faktor, termasuk cuaca yang lebih hangat dan panjangnya jam siang, yang mendorong lebih 
banyak orang untuk beraktivitas di luar ruangan. Selain itu, selama musim panas, terdapat banyak kegiatan dan acara luar ruangan, 
seperti festival dan liburan, yang juga berkontribusi pada peningkatan permintaan penyewaan sepeda.

2. Pengaruh Hari Libur pada Penyewaan Sepeda
Analisis juga menunjukkan bahwa hari libur cenderung memiliki tingkat penyewaan sepeda yang lebih rendah dibandingkan
dengan hari kerja (weekday). Pada hari libur, banyak orang memilih untuk bersantai di rumah atau melakukan aktivitas yang
tidak melibatkan penyewaan sepeda, sedangkan pada hari kerja, terdapat lebih banyak individu yang melakukan perjalanan untuk bekerja 
atau menjalani aktivitas sehari-hari. Ini menunjukkan bahwa kegiatan luar ruangan lebih umum terjadi pada hari kerja, sehingga 
meningkatkan permintaan penyewaan sepeda.

3. Pengaruh Cuaca terhadap Penyewaan Sepeda
Dari hasil analisis, jelas bahwa cuaca memiliki pengaruh signifikan terhadap penyewaan sepeda. 
Terbukti bahwa permintaan penyewaan meningkat secara drastis pada hari-hari dengan cuaca cerah. Orang-orang cenderung lebih
memilih untuk bersepeda ketika kondisi cuaca mendukung, karena cuaca cerah memberikan pengalaman yang lebih menyenangkan. Oleh karena itu, 
penyewa sepeda sebaiknya memperhatikan ramalan cuaca untuk mengoptimalkan strategi penyewaan mereka, dengan mempersiapkan lebih banyak 
sepeda pada hari-hari cerah.
""")
