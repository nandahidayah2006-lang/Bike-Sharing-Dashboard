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

# --- HEADER ---
st.title("🚲 Bike Sharing Analysis Dashboard")
st.markdown("---")

# --- GRAFIK 1: PER MUSIM (Sama persis dengan Gambar 1) ---
st.subheader("Total Penyewaan Sepeda per Musim di Tahun 2012")

# Filter data untuk tahun 2012 saja sesuai judul di gambar kamu
day_2012_df = day_df[day_df['dteday'].dt.year == 2012]

fig1, ax1 = plt.subplots(figsize=(10, 6))
# 🔥 Hitung TOTAL per musim
season_total = day_2012_df.groupby("season")["cnt"].sum().reset_index()

fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(
    x="season", 
    y="cnt", 
    data=season_total,   # 👈 ganti di sini
    palette="viridis", 
    ax=ax1
)
ax1.set_title("Total Penyewaan Sepeda per Musim di Tahun 2012", fontsize=15)
ax1.set_xlabel("Musim", fontsize=12)
ax1.set_ylabel("Total Penyewaan (Juta)", fontsize=12)
st.pyplot(fig1)

st.divider()

# --- GRAFIK 2: POLA JAM (Sama persis dengan Gambar 2) ---
st.subheader("Pola Peminjaman Sepeda Per Jam: Casual vs Registered")

# Menyiapkan data hourly_pattern (Asumsi Hari Kerja 2012 sesuai gambar)
# Filter tahun 2012 dan hari kerja (workingday == 1)
hour_2012_df = hour_df[(pd.to_datetime(hour_df['dteday']).dt.year == 2012) & (hour_df['workingday'] == 1)]
hourly_pattern = hour_2012_df.groupby("hr")[["casual", "registered"]].mean().reset_index()

fig2, ax2 = plt.subplots(figsize=(12, 6))
ax2.plot(hourly_pattern["hr"], hourly_pattern["casual"], marker='o', label='Casual', color='orange')
ax2.plot(hourly_pattern["hr"], hourly_pattern["registered"], marker='o', label='Registered', color='blue')

ax2.set_title("Pola Peminjaman Sepeda Per Jam: Casual vs Registered (Hari Kerja 2012)", fontsize=15)
ax2.set_xlabel("Jam (0-23)", fontsize=12)
ax2.set_ylabel("Rata-rata Penyewaan", fontsize=12)
ax2.set_xticks(range(0, 24))
ax2.legend()
ax2.grid(True, linestyle='--', alpha=0.5) # Grid sesuai gambar kamu
st.pyplot(fig2)

st.divider()
st.caption("Copyright (c) 2024 - Proyek Analisis Data")