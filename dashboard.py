import pandas as pd
import streamlit as st
import plotly.express as px

# Membaca data
bikes_day_df = pd.read_csv("./dashboard/bikes_day_df.csv")
bikes_hour_df = pd.read_csv("./dashboard/bikes_hour_df.csv")

# Mengonversi kolom tanggal menjadi datetime
bikes_day_df["dteday"] = pd.to_datetime(bikes_day_df["dteday"])
bikes_hour_df["dteday"] = pd.to_datetime(bikes_hour_df["dteday"])

# Cek kolom yang ada
st.write("DataFrame Harian:")
st.dataframe(bikes_day_df.head())
st.write("Kolom:", bikes_day_df.columns)

# Mapping untuk situasi cuaca
weather_mapping = {
    1: 'Clear',
    2: 'Mist',
    3: 'Rain',
    4: 'Snow'
}

# Jika kolom 'weathersit' ada, buat 'weather_desc'
if 'weathersit' in bikes_day_df.columns:
    bikes_day_df['weather_desc'] = bikes_day_df['weathersit'].map(weather_mapping)

# Cek nilai unik dalam kolom weathersit
if 'weathersit' in bikes_day_df.columns:
    st.write("Nilai unik dalam 'weathersit':", bikes_day_df['weathersit'].unique())
else:
    st.write("Kolom 'weathersit' tidak ditemukan dalam DataFrame.")

# Menyiapkan data untuk visualisasi
# Rata-rata penyewaan per situasi cuaca
if 'weather_desc' in bikes_day_df.columns:
    avg_rentals_by_weather = bikes_day_df.groupby('weather_desc')['cnt'].mean().reset_index()
else:
    st.write("Kolom 'weather_desc' tidak ditemukan, tidak dapat menghitung rata-rata penyewaan.")
    avg_rentals_by_weather = pd.DataFrame()  # Set DataFrame kosong

# Rata-rata penyewaan per jam berdasarkan musim
bikes_hour_df['season_label'] = bikes_hour_df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
season_hour_group = bikes_hour_df.groupby(['season_label', 'hr'])['cnt'].mean().reset_index()

# Membuat dashboard
st.title("Dashboard Penyewaan Sepeda")

# Dropdown untuk memilih situasi cuaca
if not avg_rentals_by_weather.empty:
    weather_options = avg_rentals_by_weather['weather_desc'].unique()
    selected_weather = st.selectbox('Pilih Situasi Cuaca:', weather_options)

    # Bar plot untuk rata-rata penyewaan berdasarkan situasi cuaca
    fig_weather = px.bar(avg_rentals_by_weather, x='weather_desc', y='cnt',
                          title='Rata-rata Penyewaan Sepeda Berdasarkan Situasi Cuaca',
                          labels={'cnt': 'Rata-rata Penyewaan', 'weather_desc': 'Situasi Cuaca'},
                          color='cnt',  # Warna berdasarkan jumlah penyewaan
                          text='cnt')   # Tampilkan nilai rata-rata di atas bar
    fig_weather.update_traces(texttemplate='%{text:.2f}', textposition='outside')  # Format angka dengan 2 desimal
    fig_weather.update_layout(xaxis_title='Situasi Cuaca', yaxis_title='Rata-rata Penyewaan',
                              yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
                              xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
                              title_x=0.5)  # Pusatkan judul grafik
    st.plotly_chart(fig_weather)
else:
    st.write("Tidak ada data untuk situasi cuaca yang dipilih.")

# Line plot untuk rata-rata penyewaan per jam berdasarkan musim
if not season_hour_group.empty:
    fig_season_hour = px.line(season_hour_group, x='hr', y='cnt', color='season_label',
                               title='Rata-rata Penyewaan Sepeda per Jam Berdasarkan Musim',
                               labels={'cnt': 'Rata-rata Penyewaan', 'hr': 'Jam (0-23)', 'season_label': 'Musim'})
    st.plotly_chart(fig_season_hour)
else:
    st.write("Tidak ada data untuk rata-rata penyewaan per jam berdasarkan musim.")
