import streamlit as st
import pandas as pd
import plotly.express as px

# Judul aplikasi
st.title("Dashboard Deteksi Mahasiswa/Dosen di Fakultas Ilmu Terapan dan Open Library")

# Membaca data dari CSV
fakultas_data_path = 'data/data_fakultas_5_menit.csv'
library_data_path = 'data/data_library_5_menit.csv'

# Membaca file CSV untuk Fakultas Ilmu Terapan dan Open Library
try:
    df_fakultas = pd.read_csv(fakultas_data_path)
    df_library = pd.read_csv(library_data_path)
    
    # Konversi kolom 'Tanggal' ke datetime untuk memudahkan pengolahan data
    df_fakultas['Tanggal'] = pd.to_datetime(df_fakultas['Tanggal'])
    df_library['Tanggal'] = pd.to_datetime(df_library['Tanggal'])

    # Sidebar untuk memilih lokasi
    st.sidebar.header("Pilih Lokasi")
    location = st.sidebar.radio(
        "Pilih lokasi deteksi yang ingin ditampilkan:",
        ('Fakultas Ilmu Terapan', 'Open Library')
    )
    
    # Memilih data berdasarkan lokasi
    if location == 'Fakultas Ilmu Terapan':
        selected_df = df_fakultas
    else:
        selected_df = df_library
    
    # Sidebar untuk memilih range waktu
    st.sidebar.header("Filter Rentang Waktu")
    
    # Mendapatkan rentang tanggal minimum dan maksimum dari data
    min_date = selected_df['Tanggal'].min().date()
    max_date = selected_df['Tanggal'].max().date()

    # Input rentang waktu di sidebar
    start_date = st.sidebar.date_input("Tanggal Mulai", min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.sidebar.date_input("Tanggal Akhir", min_value=min_date, max_value=max_date, value=max_date)

    # Filter data berdasarkan rentang waktu yang dipilih
    filtered_df = selected_df[(selected_df['Tanggal'].dt.date >= start_date) & (selected_df['Tanggal'].dt.date <= end_date)]

    # Membuat layout untuk menampilkan bar chart dan pie chart di atas, tabel di bawah
    st.subheader(f"Grafik Deteksi di {location} dari {start_date} hingga {end_date}")

    # Membuat dua kolom untuk bar chart dan pie chart
    col1, col2 = st.columns(2)

    # Kolom 1: Barplot untuk membandingkan jumlah Dosen dan Mahasiswa
    with col1:
        st.subheader("Perbandingan Dosen dan Mahasiswa")

        # Filter data untuk kategori dosen dan mahasiswa
        df_filtered_categories = filtered_df[filtered_df['Kategori'].isin(['Dosen', 'Mahasiswa'])]
        
        # Membuat barplot untuk membandingkan jumlah dosen dan mahasiswa
        fig_bar = px.bar(df_filtered_categories, x='Kategori', y='Jumlah Orang', color='Kategori',
                         title='Perbandingan Dosen dan Mahasiswa', 
                         labels={'Jumlah Orang': 'Jumlah Orang', 'Kategori': 'Kategori'})
        
        st.plotly_chart(fig_bar, use_container_width=True)

    # Kolom 2: Pie chart untuk proporsi Dosen, Mahasiswa, dan objek lainnya
    with col2:
        st.subheader("Proporsi Dosen, Mahasiswa, dan Objek Lainnya")

        # Menghitung jumlah total berdasarkan kategori objek
        df_pie = filtered_df.groupby('Kategori')['Jumlah Orang'].sum().reset_index()
        
        # Membuat pie chart
        fig_pie = px.pie(df_pie, values='Jumlah Orang', names='Kategori', 
                         title='Proporsi Dosen, Mahasiswa, dan Objek Lainnya',
                         labels={'Jumlah Orang': 'Jumlah Orang', 'Kategori': 'Kategori'})
        
        st.plotly_chart(fig_pie, use_container_width=True)

    # Menampilkan tabel di bawah grafik
    st.subheader(f"Tabel Data Terfilter di {location}")
    st.dataframe(filtered_df, height=300)  # Tabel data terfilter

    # Rangkuman statistik di bawah kolom
    st.subheader(f"Rangkuman Statistik di {location}")
    total_people = filtered_df['Jumlah Orang'].sum()
    st.write(f"Total orang terdeteksi di {location}: {total_people}")

except FileNotFoundError as e:
    st.error(f"File tidak ditemukan: {e}")
