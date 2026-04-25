# Proyek Analisis Data: Bike Sharing Dataset 🚲

## Deskripsi
Proyek ini bertujuan untuk menganalisis data penyewaan sepeda guna menemukan pola penggunaan berdasarkan musim dan waktu (jam). Hasil analisis disajikan dalam bentuk dashboard interaktif menggunakan Streamlit.

## Pertanyaan Bisnis
1. Bagaimana tren total penyewaan sepeda berdasarkan musim di tahun 2012?
2. Bagaimana pola peminjaman sepeda per jam antara pengguna Casual dan Registered pada hari kerja di tahun 2012?

## Struktur Folder
- `dashboard/`: Berisi file utama `dashboard.py` dan `main_data.csv`.
- `data/`: Berisi dataset mentah (`day.csv` dan `hour.csv`).
- `notebook.ipynb`: File Jupyter Notebook untuk proses analisis data.
- `README.md`: Panduan proyek.
- `requirements.txt`: Daftar pustaka (library) Python yang dibutuhkan.

## Alur Analisis
1. **Data Wrangling**: 
   - Gathering data dari file CSV.
   - Assessing data untuk mengecek missing values atau duplikasi.
   - Cleaning data (mengubah tipe data `dteday` menjadi datetime).
2. **Exploratory Data Analysis (EDA)**:
   - Mengeksplorasi distribusi penyewaan per musim.
   - Menganalisis perilaku pengguna Casual vs Registered berdasarkan jam.
3. **Visualization & Explanatory Analysis**:
   - Membuat visualisasi Bar Chart untuk tren musim.
   - Membuat Line Chart untuk pola penggunaan per jam.

## Setup Environment

### 1. Menggunakan Terminal/Command Prompt
Pastikan kamu sudah menginstal Python di komputermu, lalu ikuti langkah berikut:

```bash
# Masuk ke direktori proyek
cd submission

# Membuat virtual environment (opsional tapi disarankan)
python -m venv venv

# Mengaktifkan virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Instalasi library yang dibutuhkan
pip install -r requirements.txt
