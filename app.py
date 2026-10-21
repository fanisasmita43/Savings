import os
import datetime
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Konfigurasi Halaman
st.set_page_config(page_title="Rencana Keuangan Bersama", page_icon="💰", layout="wide")

# File CSV untuk penyimpanan data agar tidak hilang saat di-refresh
FILE_TABUNGAN = "data_tabungan.csv"
FILE_PENGELUARAN = "data_pengeluaran.csv"

# Fungsi load data
def load_data():
    if os.path.exists(FILE_TABUNGAN):
        df_tab = pd.read_csv(FILE_TABUNGAN)
    else:
        df_tab = pd.DataFrame(columns=["Tanggal", "Nama Penyetor", "Jumlah Tabungan", "Keterangan/Tujuan"])
        
    if os.path.exists(FILE_PENGELUARAN):
        df_kel = pd.read_csv(FILE_PENGELUARAN)
    else:
        df_kel = pd.DataFrame(columns=["Tanggal", "Nama Pengeluar", "Kategori", "Jumlah Pengeluaran", "Keterangan"])
        
    return df_tab, df_kel

def save_data(df_tab, df_kel):
    df_tab.to_csv(FILE_TABUNGAN, index=False)
    df_kel.to_csv(FILE_PENGELUARAN, index=False)

df_tabungan, df_pengeluaran = load_data()

st.title("💰 Rencana Keuangan Bersama (Fani & Sahat)")
st.write("Aplikasi pencatatan tabungan dan pengeluaran bersama pasangan secara real-time.")

# Sidebar untuk Input Data Baru
st.sidebar.header("➕ Tambah Transaksi Baru")
menu_form = st.sidebar.selectbox("Pilih Jenis Transaksi", ["Catatan Tabungan", "Catatan Pengeluaran"])

if menu_form == "Catatan Tabungan":
    st.sidebar.subheader("Tambah Tabungan Baru")
    tgl_input = st.sidebar.date_input("Tanggal Tabungan", datetime.date.today())
    tgl_format = tgl_input.strftime("%d - %m - %Y")
    nama_penyetor = st.sidebar.selectbox("Nama Penyetor", ["Fani", "Sahat"])
    jumlah_tab = st.sidebar.number_input("Jumlah Tabungan (Rp)", min_value=0, step=50000)
    ket_tab = st.sidebar.text_input("Keterangan / Tujuan")
    
    if st.sidebar.button("Simpan Tabungan"):
        baru = pd.DataFrame([{
            "Tanggal": tgl_format,
            "Nama Penyetor": nama_penyetor,
            "Jumlah Tabungan": jumlah_tab,
            "Keterangan/Tujuan": ket_tab
        }])
        df_tabungan = pd.concat([df_tabungan, baru], ignore_index=True)
        save_data(df_tabungan, df_pengeluaran)
        st.sidebar.success("Tabungan berhasil disimpan!")
        st.rerun()

else:
    st.sidebar.subheader("Tambah Pengeluaran Baru")
    tgl_input_kel = st.sidebar.date_input("Tanggal Pengeluaran", datetime.date.today())
    tgl_format_kel = tgl_input_kel.strftime("%d - %m - %Y")
    nama_pengeluar = st.sidebar.selectbox("Nama Pengeluar", ["Fani", "Sahat"])
    kategori_kel = st.sidebar.selectbox("Kategori", ["Makanan", "Transportasi", "Tagihan", "Belanja", "Lainnya"])
    jumlah_kel = st.sidebar.number_input("Jumlah Pengeluaran (Rp)", min_value=0, step=10000)
    ket_kel = st.sidebar.text_input("Keterangan Pengeluaran")
    
    if st.sidebar.button("Simpan Pengeluaran"):
        baru_kel = pd.DataFrame([{
            "Tanggal": tgl_format_kel,
            "Nama Pengeluar": nama_pengeluar,
            "Kategori": kategori_kel,
            "Jumlah Pengeluaran": jumlah_kel,
            "Keterangan": ket_kel
        }])
        df_pengeluaran = pd.concat([df_pengeluaran, baru_kel], ignore_index=True)
        save_data(df_tabungan, df_pengeluaran)
        st.sidebar.success("Pengeluaran berhasil disimpan!")
        st.rerun()

# --- DASHBOARD RINGKASAN ---
total_tabungan = df_tabungan["Jumlah Tabungan"].sum() if not df_tabungan.empty else 0
total_pengeluaran = df_pengeluaran["Jumlah Pengeluaran"].sum() if not df_pengeluaran.empty else 0
saldo_akhir = total_tabungan - total_pengeluaran

col1, col2, col3 = st.columns(3)
col1.metric("Total Tabungan", f"Rp {total_tabungan:,.0f}")
col2.metric("Total Pengeluaran", f"Rp {total_pengeluaran:,.0f}")
col3.metric("Saldo Akhir", f"Rp {saldo_akhir:,.0f}")

st.markdown("---")

# --- TABEL DATA & GRAFIK ---
tab1, tab2 = st.tabs(["📋 Tabel Transaksi", "📊 Grafik Perbandingan"])

with tab1:
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.subheader("Catatan Tabungan")
        st.dataframe(df_tabungan, use_container_width=True)
    with col_t2:
        st.subheader("Catatan Pengeluaran")
        st.dataframe(df_pengeluaran, use_container_width=True)

with tab2:
    st.subheader("Grafik Perbandingan Total Tabungan vs Total Pengeluaran")
    fig, ax = plt.subplots(figsize=(6, 4))
    kategori_grafik = ["Total Tabungan", "Total Pengeluaran"]
    nilai_grafik = [total_tabungan, total_pengeluaran]
    warna = ["#2ecc71", "#e74c3c"]
    
    ax.bar(kategori_grafik, nilai_grafik, color=warna, width=0.5)
    ax.set_ylabel("Jumlah (Rp)")
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    
    st.pyplot(fig)
