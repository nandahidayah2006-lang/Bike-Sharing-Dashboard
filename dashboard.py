import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Konfigurasi Halaman
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    # Membaca file langsung karena berada di satu folder yang sama
    day_df = pd.read_csv("main_data.csv")
    hour_df = pd.read_csv("hour.csv")
    
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    return day_df, hour_df

try:
    day_df, hour_df = load_data()
except Exception as e:
    st.error(f"Gagal memuat data. Error: {e}")
    st.stop()

# --- SIDEBAR ---
st.sidebar.header("Fitur Filtering")

# Filter Rentang Waktu (Asli)
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

start_date, end_date = st.sidebar.date_input(
    label='Rentang Waktu (Untuk RFM)',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# --- TAMBAHAN FILTER MUSIM (Tanpa merubah logika di bawah) ---
list_musim = day_df['season'].unique()
selected_seasons = st.sidebar.multiselect(
    "Pilih Musim untuk Eksplorasi:",
    options=list_musim,
    default=list_musim
)

# --- HEADER ---
st.title("🚲 Bike Sharing Analysis Dashboard")
st.markdown("---")

# --- PENGECEKAN FILTER (Agar muncul Warning jika data kosong) ---
main_day_df = day_df[day_df['season'].isin(selected_seasons)]
main_hour_df = hour_df[hour_df['season'].isin(selected_seasons)]

if main_day_df.empty:
    st.warning("Silakan pilih minimal satu musim di sidebar.")
else:
    # --- GRAFIK 1: PER MUSIM (Codingan Kamu - TIDAK DIUBAH) ---
    st.subheader("Total Penyewaan Sepeda per Musim di Tahun 2012")

    # Menggunakan filter musim yang dipilih tanpa merubah logika tahun 2012
    day_2012_df = main_day_df[main_day_df['dteday'].dt.year == 2012]
    season_total = day_2012_df.groupby("season")["cnt"].sum().reset_index()

    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x="season", 
        y="cnt", 
        data=season_total, 
        palette="viridis", 
        ax=ax1
    )
    ax1.set_title("Total Penyewaan Sepeda per Musim di Tahun 2012", fontsize=15)
    ax1.set_xlabel("Musim", fontsize=12)
    ax1.set_ylabel("Total Penyewaan (Juta)", fontsize=12)
    st.pyplot(fig1)

    st.divider()

   # --- GRAFIK 2: POLA JAM (TAMPIL PERMANEN / TIDAK TERPENGARUH FILTER) ---
    st.subheader("Pola Peminjaman Sepeda Per Jam: Casual vs Registered")

    # Menggunakan 'hour_df' (data asli) agar TIDAK terpengaruh filter sidebar
    # Kita buat salinan agar tidak merusak data asli
    hour_permanent_df = hour_df.copy()
    hour_permanent_df['dteday'] = pd.to_datetime(hour_permanent_df['dteday'])
    
    # Tetap memfilter tahun 2012 dan hari kerja sesuai permintaan awal kamu
    hour_2012_df = hour_permanent_df[(hour_permanent_df['dteday'].dt.year == 2012) & (hour_permanent_df['workingday'] == 1)]
    
    # Grouping rata-rata per jam
    hourly_pattern = hour_2012_df.groupby("hr")[["casual", "registered"]].mean().reset_index()
    hourly_pattern = hourly_pattern.sort_values("hr")

    # Membuat plot
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    
    # Plot garis Casual (Orange)
    ax2.plot(
        hourly_pattern["hr"], 
        hourly_pattern["casual"], 
        marker='o', 
        linestyle='-', 
        linewidth=2, 
        label='Casual', 
        color='orange'
    )
    
    # Plot garis Registered (Blue)
    ax2.plot(
        hourly_pattern["hr"], 
        hourly_pattern["registered"], 
        marker='o', 
        linestyle='-', 
        linewidth=2, 
        label='Registered', 
        color='blue'
    )

    ax2.set_title("Pola Peminjaman Sepeda Per Jam: Casual vs Registered (Hari Kerja 2012 - Statis)", fontsize=15)
    ax2.set_xlabel("Jam (0-23)", fontsize=12)
    ax2.set_ylabel("Rata-rata Penyewaan", fontsize=12)
    
    # Mengatur sumbu Y agar tetap 0-600 dan X tetap 0-23
    ax2.set_ylim(0, 600)
    ax2.set_xticks(range(0, 24))
    
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.5)
    
    # Tampilkan grafik
    st.pyplot(fig2)
    # --- TAMBAHAN GRAFIK 3: RFM ANALYSIS (UNTUK REVISI) ---
    st.subheader("Best Season Based on RFM Parameters")

    # Filter khusus untuk RFM menggunakan gabungan filter tanggal dan musim
    rfm_filtered_df = main_day_df[(main_day_df["dteday"] >= str(start_date)) & (main_day_df["dteday"] <= str(end_date))]

    if not rfm_filtered_df.empty:
        recent_date = day_df['dteday'].max()
        rfm_df = rfm_filtered_df.groupby(by="season", as_index=False).agg({
            "dteday": lambda x: (recent_date - x.max()).days,
            "instant": "count",
            "cnt": "sum"
        })
        rfm_df.columns = ["season", "recency", "frequency", "monetary"]

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Avg Recency (days)", value=round(rfm_df.recency.mean(), 1))
        with col2:
            st.metric("Avg Frequency", value=round(rfm_df.frequency.mean(), 1))
        with col3:
            st.metric("Avg Monetary", value=f"{rfm_df.monetary.mean():,.0f}")

        fig3, ax3 = plt.subplots(nrows=1, ncols=3, figsize=(20, 8))
        sns.barplot(y="recency", x="season", data=rfm_df, palette="viridis", ax=ax3[0])
        ax3[0].set_title("By Recency (days)", fontsize=18)
        sns.barplot(y="frequency", x="season", data=rfm_df, palette="viridis", ax=ax3[1])
        ax3[1].set_title("By Frequency", fontsize=18)
        sns.barplot(y="monetary", x="season", data=rfm_df, palette="viridis", ax=ax3[2])
        ax3[2].set_title("By Monetary", fontsize=18)
        st.pyplot(fig3)

st.divider()
st.caption("Copyright (c) 2024 - Proyek Analisis Data")