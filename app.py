import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Dashboard Analitik Jasa Sedot WC MGM",
    page_icon="🚛",
    layout="wide"
)

# 2. Load Data Bersih (dengan cache agar cepat)
@st.cache_data
def load_data():
    df = pd.read_csv("dataset_bersih_mgm.csv")
    df["tanggal_waktu"] = pd.to_datetime(df["tanggal_waktu"])
    df["bulan"] = df["tanggal_waktu"].dt.to_period("M").astype(str)
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("File 'dataset_bersih_mgm.csv' tidak ditemukan di repositori.")
    st.stop()

# 3. Header & Catatan Etika Data Sintetis
st.title("🚛 Dashboard Analitik Kinerja Jasa Sedot WC MGM")
st.caption("Proyek PjBL Big Data & Cloud Computing — Sektor P5 (UMKM)")
st.info(
    "Catatan Etika Data: Dataset yang digunakan merupakan data transaksi sintetis "
    "(simulasi skala Big Data) untuk tujuan pengujian sistem analitik dan bukan data pribadi pelanggan riil."
)

# 4. Sidebar Filter (Waktu, Kategori Layanan, Wilayah)
st.sidebar.header("🔍 Filter Data")

min_tgl = df["tanggal_waktu"].dt.date.min()
max_tgl = df["tanggal_waktu"].dt.date.max()

rentang_tanggal = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    value=(min_tgl, max_tgl),
    min_value=min_tgl,
    max_value=max_tgl
)

semua_wilayah = sorted(df["wilayah_operasional"].unique())
pilih_wilayah = st.sidebar.multiselect(
    "Pilih Wilayah Operasional",
    options=semua_wilayah,
    default=semua_wilayah
)

semua_layanan = sorted(df["jenis_layanan"].unique())
pilih_layanan = st.sidebar.multiselect(
    "Pilih Jenis Layanan",
    options=semua_layanan,
    default=semua_layanan
)

# Penanganan aman saat pengguna baru memilih 1 tanggal
if isinstance(rentang_tanggal, tuple) and len(rentang_tanggal) == 2:
    tgl_awal, tgl_akhir = rentang_tanggal
else:
    st.warning("Silakan pilih tanggal awal dan tanggal akhir pada filter rentang tanggal.")
    st.stop()

# Terapkan Filter
df_filtered = df[
    (df["tanggal_waktu"].dt.date >= tgl_awal) &
    (df["tanggal_waktu"].dt.date <= tgl_akhir) &
    (df["wilayah_operasional"].isin(pilih_wilayah)) &
    (df["jenis_layanan"].isin(pilih_layanan))
]

# Penanganan aman jika hasil filter kosong (agar aplikasi tidak crash)
if df_filtered.empty:
    st.warning("Tidak ada data transaksi yang cocok dengan kombinasi filter Anda. Silakan pilih minimal satu wilayah dan layanan.")
    st.stop()

# 5. Bagian KPI Utama (4 Indikator)
st.subheader("📊 Ringkasan Indikator Kinerja Utama (KPI)")

total_omzet = df_filtered["nilai_transaksi"].sum()
total_pesanan = len(df_filtered)
rata_rating = df_filtered["rating_pelanggan"].mean()
layanan_terlaris = df_filtered["jenis_layanan"].value_counts().idxmax()

col1, col2, col3, col4 = st.columns(4)
col1.metric("KPI 1: Total Omzet", f"Rp {total_omzet:,.0f}".replace(",", "."))
col2.metric("KPI 2: Total Pesanan Sukses", f"{total_pesanan:,}".replace(",", "."))
col3.metric("KPI 3: Rata-Rata Rating", f"{rata_rating:.2f} / 5.00")
col4.metric("KPI 4: Layanan Terlaris", layanan_terlaris)

st.divider()

# 6. Visualisasi Grafik
grafik_kiri, grafik_kanan = st.columns(2)

with grafik_kiri:
    st.subheader("📈 Tren Omzet Bulanan")
    tren_bulanan = df_filtered.groupby("bulan", as_index=False)["nilai_transaksi"].sum()
    fig_tren = px.line(
        tren_bulanan,
        x="bulan",
        y="nilai_transaksi",
        markers=True,
        labels={"bulan": "Bulan", "nilai_transaksi": "Total Omzet (Rp)"}
    )
    st.plotly_chart(fig_tren, use_container_width=True)

with grafik_kanan:
    st.subheader("🗺️ Total Omzet per Wilayah Operasional")
    omzet_wilayah = (
        df_filtered.groupby("wilayah_operasional", as_index=False)["nilai_transaksi"]
        .sum()
        .sort_values(by="nilai_transaksi", ascending=False)
    )
    fig_wilayah = px.bar(
        omzet_wilayah,
        x="wilayah_operasional",
        y="nilai_transaksi",
        color="wilayah_operasional",
        labels={"wilayah_operasional": "Wilayah", "nilai_transaksi": "Total Omzet (Rp)"}
    )
    fig_wilayah.update_layout(showlegend=False)
    st.plotly_chart(fig_wilayah, use_container_width=True)

st.subheader("🛠️ Perbandingan Jumlah Pesanan & Omzet per Jenis Layanan")
ringkasan_layanan = df_filtered.groupby("jenis_layanan", as_index=False).agg(
    Jumlah_Pesanan=("id_pesanan", "count"),
    Total_Omzet=("nilai_transaksi", "sum"),
    Rata_Rata_Rating=("rating_pelanggan", "mean")
)

kol_pie, kol_tabel = st.columns([1, 1.3])
with kol_pie:
    fig_pie = px.pie(
        ringkasan_layanan,
        names="jenis_layanan",
        values="Jumlah_Pesanan",
        hole=0.4
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with kol_tabel:
    ringkasan_tampil = ringkasan_layanan.copy()
    ringkasan_tampil["Total_Omzet"] = ringkasan_tampil["Total_Omzet"].apply(
        lambda x: f"Rp {x:,.0f}".replace(",", ".")
    )
    ringkasan_tampil["Rata_Rata_Rating"] = ringkasan_tampil["Rata_Rata_Rating"].round(2)
    st.dataframe(ringkasan_tampil, use_container_width=True, hide_index=True)

# 7. Sampel Data Transaksi
with st.expander("📄 Lihat Sampel 100 Data Transaksi Terfilter"):
    st.dataframe(df_filtered.head(100), use_container_width=True, hide_index=True)
