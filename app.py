import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. KONFIGURASI HALAMAN
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Dashboard — Jasa Sedot WC MGM",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# 2. CUSTOM CSS (GAYA CLEAN SAAS / UNTITLED UI)
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #101828;
    }

    .stApp {
        background-color: #F9FAFB;
    }

    /* Header transparan agar tombol toggle sidebar tetap bisa diklik */
    header[data-testid="stHeader"] {
        background-color: transparent;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    /* Spacing area utama */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2.5rem;
        padding-left: 2.2rem;
        padding-right: 2.2rem;
        max-width: 1440px;
    }

    /* Sidebar putih bersih dengan garis pemisah tipis */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #EAECF0;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

    /* Ganti pill merah bawaan Streamlit menjadi soft violet pill */
    span[data-baseweb="tag"] {
        background-color: #F4EBFF !important;
        color: #53389E !important;
        border: 1px solid #E9D7FE !important;
        border-radius: 6px !important;
        font-size: 12px !important;
        font-weight: 500 !important;
    }

    span[data-baseweb="tag"] svg {
        fill: #7F56D9 !important;
    }

    /* Input filter bersih */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background-color: #FFFFFF !important;
        border-color: #D0D5DD !important;
        border-radius: 8px !important;
        font-size: 13px !important;
    }

    /* Label widget sidebar */
    section[data-testid="stSidebar"] label p {
        font-size: 13px !important;
        font-weight: 500 !important;
        color: #344054 !important;
    }

    /* Styling container berbingkai untuk kartu grafik */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF;
        border: 1px solid #EAECF0 !important;
        border-radius: 14px !important;
        box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
        padding: 18px 20px 14px 20px !important;
    }

    /* Expander tabel data */
    div[data-testid="stExpander"] {
        background-color: #FFFFFF;
        border: 1px solid #EAECF0 !important;
        border-radius: 14px !important;
        box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
    }

    /* Brand sidebar */
    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 11px;
        padding-bottom: 18px;
        margin-bottom: 18px;
        border-bottom: 1px solid #F2F4F7;
    }
    .brand-mark {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: radial-gradient(circle at 50% 50%, #7F56D9 0%, #B692F6 48%, #F4EBFF 78%, transparent 100%);
        flex-shrink: 0;
    }
    .brand-title {
        font-size: 15px;
        font-weight: 700;
        color: #101828;
        letter-spacing: -0.01em;
        line-height: 1.2;
    }
    .brand-sub {
        font-size: 11.5px;
        color: #667085;
        font-weight: 400;
    }

    .sidebar-section-label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #667085;
        margin-bottom: 10px;
    }

    .sidebar-footer {
        margin-top: 24px;
        padding-top: 16px;
        border-top: 1px solid #F2F4F7;
    }
    .sidebar-profile {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .avatar-circle {
        width: 34px;
        height: 34px;
        border-radius: 50%;
        background-color: #F4EBFF;
        color: #6941C6;
        font-size: 12px;
        font-weight: 600;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid #E9D7FE;
        flex-shrink: 0;
    }
    .profile-name {
        font-size: 13px;
        font-weight: 600;
        color: #101828;
        line-height: 1.25;
    }
    .profile-meta {
        font-size: 11.5px;
        color: #667085;
    }

    /* Header utama */
    .page-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        flex-wrap: wrap;
        gap: 12px;
        margin-bottom: 20px;
    }
    .page-title {
        font-size: 26px;
        font-weight: 700;
        color: #101828;
        letter-spacing: -0.025em;
        margin: 0;
        line-height: 1.2;
    }
    .page-subtitle {
        font-size: 13.5px;
        color: #667085;
        margin-top: 4px;
    }
    .ethics-pill {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        background-color: #FFFFFF;
        border: 1px solid #EAECF0;
        border-radius: 999px;
        padding: 6px 13px;
        font-size: 12px;
        font-weight: 500;
        color: #475467;
        box-shadow: 0 1px 2px rgba(16, 24, 40, 0.03);
    }
    .ethics-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: #7F56D9;
    }

    /* Grid KPI Cards */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 16px;
        margin-bottom: 20px;
    }
    @media (max-width: 1100px) {
        .kpi-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }
    @media (max-width: 640px) {
        .kpi-grid {
            grid-template-columns: 1fr;
        }
    }
    .kpi-card {
        background-color: #FFFFFF;
        border: 1px solid #EAECF0;
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        gap: 12px;
    }
    .kpi-top {
        display: flex;
        align-items: center;
        gap: 11px;
    }
    .kpi-icon {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background-color: #F4EBFF;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    .kpi-label {
        font-size: 13px;
        font-weight: 500;
        color: #475467;
        line-height: 1.3;
    }
    .kpi-value {
        font-size: 21px;
        font-weight: 700;
        color: #101828;
        letter-spacing: -0.025em;
        font-variant-numeric: tabular-nums;
        line-height: 1.2;
    }
    .kpi-sub {
        font-size: 12px;
        color: #667085;
        margin-top: 3px;
    }

    /* Header kartu grafik */
    .card-head {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }
    .card-title {
        font-size: 15px;
        font-weight: 600;
        color: #101828;
        letter-spacing: -0.01em;
    }
    .card-meta {
        font-size: 12px;
        font-weight: 500;
        color: #6941C6;
    }

    /* Daftar stat layanan di samping donut */
    .service-stat-block {
        padding: 10px 0;
        border-bottom: 1px solid #F2F4F7;
    }
    .service-stat-block:last-child {
        border-bottom: none;
    }
    .service-label-row {
        display: flex;
        align-items: center;
        gap: 7px;
        font-size: 12.5px;
        font-weight: 500;
        color: #475467;
        margin-bottom: 4px;
    }
    .legend-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
    }
    .service-big-num {
        font-size: 20px;
        font-weight: 700;
        color: #101828;
        font-variant-numeric: tabular-nums;
        letter-spacing: -0.02em;
    }
    .service-sub-num {
        font-size: 12px;
        color: #667085;
        margin-top: 2px;
    }

    /* List wilayah bergaya Vault / Roadmap */
    .region-row {
        padding: 11px 13px;
        border: 1px solid #F2F4F7;
        border-radius: 10px;
        margin-bottom: 8px;
        background-color: #FCFCFD;
    }
    .region-row:last-child {
        margin-bottom: 0;
    }
    .region-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }
    .region-name {
        font-size: 13px;
        font-weight: 600;
        color: #101828;
    }
    .region-right {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .region-val {
        font-size: 12.5px;
        font-weight: 600;
        color: #344054;
        font-variant-numeric: tabular-nums;
    }
    .pct-badge {
        font-size: 11px;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 999px;
        background-color: #F4EBFF;
        color: #6941C6;
    }
    .pct-badge-muted {
        font-size: 11px;
        font-weight: 500;
        padding: 2px 8px;
        border-radius: 999px;
        background-color: #F2F4F7;
        color: #475467;
    }
    .progress-track {
        width: 100%;
        height: 6px;
        background-color: #EAECF0;
        border-radius: 999px;
        overflow: hidden;
    }
    .progress-fill {
        height: 100%;
        background-color: #7F56D9;
        border-radius: 999px;
    }
    .region-meta {
        font-size: 11.5px;
        color: #667085;
        margin-top: 5px;
    }

    /* Kotak peringatan bersih (Negative test) */
    .notice-box {
        background-color: #FFFAEB;
        border: 1px solid #FEDF89;
        border-radius: 12px;
        padding: 16px 18px;
        color: #B54708;
        font-size: 13.5px;
        display: flex;
        align-items: center;
        gap: 12px;
        margin-top: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 3. FUNGSI HELPER FORMATTER & LOAD DATA
# -----------------------------------------------------------------------------
def fmt_rupiah(val: float) -> str:
    return f"Rp {val:,.0f}".replace(",", ".")

def fmt_int(val: int) -> str:
    return f"{val:,}".replace(",", ".")

@st.cache_data
def load_data():
    df = pd.read_csv("dataset_bersih_mgm.csv")
    df["tanggal_waktu"] = pd.to_datetime(df["tanggal_waktu"])
    df["bulan"] = df["tanggal_waktu"].dt.to_period("M").astype(str)
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.markdown(
        '<div class="notice-box">File <b>dataset_bersih_mgm.csv</b> tidak ditemukan di repositori.</div>',
        unsafe_allow_html=True,
    )
    st.stop()

# -----------------------------------------------------------------------------
# 4. SIDEBAR (BRAND + FILTER + PROFIL PROYEK)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="brand-mark"></div>
            <div>
                <div class="brand-title">Sedot WC MGM</div>
                <div class="brand-sub">Analitik Layanan Sanitasi</div>
            </div>
        </div>
        <div class="sidebar-section-label">Filter Data</div>
        """,
        unsafe_allow_html=True,
    )

    min_tgl = df["tanggal_waktu"].dt.date.min()
    max_tgl = df["tanggal_waktu"].dt.date.max()

    rentang_tanggal = st.date_input(
        "Rentang Tanggal",
        value=(min_tgl, max_tgl),
        min_value=min_tgl,
        max_value=max_tgl,
    )

    semua_wilayah = sorted(df["wilayah_operasional"].unique())
    pilih_wilayah = st.multiselect(
        "Wilayah Operasional",
        options=semua_wilayah,
        default=semua_wilayah,
        placeholder="Pilih wilayah...",
    )

    semua_layanan = sorted(df["jenis_layanan"].unique())
    pilih_layanan = st.multiselect(
        "Jenis Layanan",
        options=semua_layanan,
        default=semua_layanan,
        placeholder="Pilih layanan...",
    )

    st.markdown(
        """
        <div class="sidebar-footer">
            <div class="sidebar-profile">
                <div class="avatar-circle">MG</div>
                <div>
                    <div class="profile-name">Jasa Sedot WC MGM</div>
                    <div class="profile-meta">PjBL Big Data • Sektor P5 UMKM</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------------------------------------------------------
# 5. HEADER HALAMAN UTAMA
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="page-header">
        <div>
            <h1 class="page-title">Dashboard</h1>
            <div class="page-subtitle">Ringkasan kinerja operasional, omzet, dan distribusi layanan Jasa Sedot WC MGM</div>
        </div>
        <div class="ethics-pill">
            <span class="ethics-dot"></span>
            Dataset Sintetis • Simulasi Uji Analitik (Non-Pribadi)
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Validasi rentang tanggal (penanganan aman saat pengguna baru memilih 1 tanggal)
if isinstance(rentang_tanggal, tuple) and len(rentang_tanggal) == 2:
    tgl_awal, tgl_akhir = rentang_tanggal
else:
    st.markdown(
        """
        <div class="notice-box">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#B54708" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            <span>Silakan pilih <b>tanggal awal</b> dan <b>tanggal akhir</b> pada filter rentang tanggal di panel kiri.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# Terapkan filter
df_filtered = df[
    (df["tanggal_waktu"].dt.date >= tgl_awal)
    & (df["tanggal_waktu"].dt.date <= tgl_akhir)
    & (df["wilayah_operasional"].isin(pilih_wilayah))
    & (df["jenis_layanan"].isin(pilih_layanan))
]

# Penanganan aman jika filter dikosongkan (Negative Test)
if df_filtered.empty:
    st.markdown(
        """
        <div class="notice-box">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#B54708" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
            <span>Tidak ada data transaksi yang cocok dengan kombinasi filter saat ini. Pilih minimal satu <b>Wilayah Operasional</b> dan satu <b>Jenis Layanan</b>.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# -----------------------------------------------------------------------------
# 6. PERHITUNGAN 4 KPI UTAMA
# -----------------------------------------------------------------------------
total_omzet = df_filtered["nilai_transaksi"].sum()
total_pesanan = len(df_filtered)
rata_rating = df_filtered["rating_pelanggan"].mean()
rata_nilai = df_filtered["nilai_transaksi"].mean()
layanan_counts = df_filtered["jenis_layanan"].value_counts()
layanan_terlaris = layanan_counts.idxmax()
porsi_terlaris = (layanan_counts.iloc[0] / total_pesanan) * 100

# Ikon SVG minimalis bergaya Untitled UI
ico_wallet = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#7F56D9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/></svg>'
ico_check = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#7F56D9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>'
ico_star = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#7F56D9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'
ico_trend = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#7F56D9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>'

kpi_html = f"""
<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-top">
            <div class="kpi-icon">{ico_wallet}</div>
            <div class="kpi-label">Total Omzet</div>
        </div>
        <div>
            <div class="kpi-value">{fmt_rupiah(total_omzet)}</div>
            <div class="kpi-sub">Rata-rata {fmt_rupiah(rata_nilai)} / pesanan</div>
        </div>
    </div>
    <div class="kpi-card">
        <div class="kpi-top">
            <div class="kpi-icon">{ico_check}</div>
            <div class="kpi-label">Total Pesanan Sukses</div>
        </div>
        <div>
            <div class="kpi-value">{fmt_int(total_pesanan)}</div>
            <div class="kpi-sub">Dari {len(pilih_wilayah)} wilayah operasional aktif</div>
        </div>
    </div>
    <div class="kpi-card">
        <div class="kpi-top">
            <div class="kpi-icon">{ico_star}</div>
            <div class="kpi-label">Rata-Rata Rating</div>
        </div>
        <div>
            <div class="kpi-value">{rata_rating:.2f} / 5.00</div>
            <div class="kpi-sub">Indeks kepuasan pelanggan</div>
        </div>
    </div>
    <div class="kpi-card">
        <div class="kpi-top">
            <div class="kpi-icon">{ico_trend}</div>
            <div class="kpi-label">Layanan Terlaris</div>
        </div>
        <div>
            <div class="kpi-value">{layanan_terlaris}</div>
            <div class="kpi-sub">{porsi_terlaris:.1f}% dari total volume pesanan</div>
        </div>
    </div>
</div>
"""
st.markdown("".join(line.strip() for line in kpi_html.splitlines()), unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 7. BARIS 2: TREN OMZET BULANAN & KOMPOSISI LAYANAN (GAYA DONUT RING)
# -----------------------------------------------------------------------------
col_tren, col_layanan = st.columns([1.45, 1], gap="medium")

with col_tren:
    with st.container(border=True):
        st.markdown(
            f'<div class="card-head"><div class="card-title">Tren Omzet Bulanan</div><div class="card-meta">{tgl_awal.strftime("%d %b %Y")} — {tgl_akhir.strftime("%d %b %Y")}</div></div>',
            unsafe_allow_html=True,
        )
        tren_bulanan = (
            df_filtered.groupby("bulan", as_index=False)["nilai_transaksi"]
            .sum()
            .sort_values("bulan")
        )
        fig_tren = go.Figure()
        fig_tren.add_trace(
            go.Scatter(
                x=tren_bulanan["bulan"],
                y=tren_bulanan["nilai_transaksi"],
                mode="lines+markers",
                line=dict(color="#7F56D9", width=2.6, shape="spline", smoothing=0.6),
                marker=dict(size=6, color="#FFFFFF", line=dict(color="#7F56D9", width=2)),
                fill="tozeroy",
                fillcolor="rgba(127, 86, 217, 0.08)",
                hovertemplate="<b>%{x}</b><br>Omzet: Rp %{y:,.0f}<extra></extra>",
            )
        )
        fig_tren.update_layout(
            height=290,
            margin=dict(l=6, r=10, t=10, b=6),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", size=12, color="#667085"),
            xaxis=dict(showgrid=False, showline=False, zeroline=False, tickangle=0),
            yaxis=dict(
                showgrid=True,
                gridcolor="#F2F4F7",
                showline=False,
                zeroline=False,
                tickprefix="Rp ",
            ),
            hoverlabel=dict(bgcolor="#101828", font_color="#FFFFFF", font_size=12, bordercolor="#101828"),
        )
        st.plotly_chart(fig_tren, use_container_width=True, config={"displayModeBar": False})

with col_layanan:
    with st.container(border=True):
        ringkasan_layanan = (
            df_filtered.groupby("jenis_layanan", as_index=False)
            .agg(
                Jumlah_Pesanan=("id_pesanan", "count"),
                Total_Omzet=("nilai_transaksi", "sum"),
                Rata_Rata_Rating=("rating_pelanggan", "mean"),
            )
            .sort_values("Total_Omzet", ascending=False)
            .reset_index(drop=True)
        )
        st.markdown(
            f'<div class="card-head"><div class="card-title">Komposisi Layanan</div><div class="card-meta">{len(ringkasan_layanan)} Kategori Aktif</div></div>',
            unsafe_allow_html=True,
        )

        sub_stat, sub_ring = st.columns([1.05, 1.1], vertical_alignment="center")
        palette_layanan = ["#7F56D9", "#F79009", "#9E77ED", "#FDB022"]

        with sub_stat:
            blocks_html = []
            for idx, row in ringkasan_layanan.iterrows():
                dot_color = palette_layanan[idx % len(palette_layanan)]
                share_omzet = (row["Total_Omzet"] / total_omzet) * 100
                blocks_html.append(
                    f"""
                    <div class="service-stat-block">
                        <div class="service-label-row">
                            <span class="legend-dot" style="background:{dot_color};"></span>
                            <span>{row["jenis_layanan"]}</span>
                        </div>
                        <div class="service-big-num">{share_omzet:.1f}%</div>
                        <div class="service-sub-num">{fmt_rupiah(row["Total_Omzet"])} &bull; {fmt_int(row["Jumlah_Pesanan"])} order</div>
                    </div>
                    """
                )
            st.markdown("".join(line.strip() for line in "".join(blocks_html).splitlines()), unsafe_allow_html=True)

        with sub_ring:
            top_share = (ringkasan_layanan.iloc[0]["Total_Omzet"] / total_omzet) * 100
            fig_ring = go.Figure(
                data=[
                    go.Pie(
                        labels=ringkasan_layanan["jenis_layanan"],
                        values=ringkasan_layanan["Total_Omzet"],
                        hole=0.72,
                        marker=dict(colors=palette_layanan[: len(ringkasan_layanan)]),
                        textinfo="none",
                        hovertemplate="<b>%{label}</b><br>Omzet: Rp %{value:,.0f}<br>Porsi: %{percent}<extra></extra>",
                        sort=False,
                    )
                ]
            )
            fig_ring.update_layout(
                height=265,
                margin=dict(l=4, r=4, t=10, b=10),
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)",
                annotations=[
                    dict(
                        text=f"<b>{top_share:.0f}%</b><br><span style='font-size:11px;color:#667085'>Porsi Utama</span>",
                        x=0.5,
                        y=0.5,
                        font=dict(size=20, family="Inter, sans-serif", color="#101828"),
                        showarrow=False,
                    )
                ],
                hoverlabel=dict(bgcolor="#101828", font_color="#FFFFFF", font_size=12, bordercolor="#101828"),
            )
            st.plotly_chart(fig_ring, use_container_width=True, config={"displayModeBar": False})

# -----------------------------------------------------------------------------
# 8. BARIS 3: DISTRIBUSI WILAYAH & PERFORMA DETAIL PER WILAYAH
# -----------------------------------------------------------------------------
omzet_wilayah = (
    df_filtered.groupby("wilayah_operasional", as_index=False)
    .agg(
        Total_Omzet=("nilai_transaksi", "sum"),
        Jumlah_Pesanan=("id_pesanan", "count"),
        Rata_Rating=("rating_pelanggan", "mean"),
    )
    .sort_values("Total_Omzet", ascending=False)
    .reset_index(drop=True)
)

col_bar, col_list = st.columns([1.25, 1], gap="medium")

with col_bar:
    with st.container(border=True):
        st.markdown(
            '<div class="card-head"><div class="card-title">Total Omzet per Wilayah Operasional</div><div class="card-meta">Peringkat Kontribusi</div></div>',
            unsafe_allow_html=True,
        )
        bar_colors = [
            "#7F56D9" if i == 0 else "#B692F6" if i == 1 else "#D6BBFB"
            for i in range(len(omzet_wilayah))
        ]
        fig_bar = go.Figure(
            data=[
                go.Bar(
                    x=omzet_wilayah["wilayah_operasional"],
                    y=omzet_wilayah["Total_Omzet"],
                    marker=dict(color=bar_colors, cornerradius=6),
                    hovertemplate="<b>%{x}</b><br>Omzet: Rp %{y:,.0f}<extra></extra>",
                )
            ]
        )
        fig_bar.update_layout(
            height=330,
            margin=dict(l=6, r=10, t=10, b=6),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", size=12, color="#667085"),
            xaxis=dict(showgrid=False, showline=False, zeroline=False),
            yaxis=dict(
                showgrid=True,
                gridcolor="#F2F4F7",
                showline=False,
                zeroline=False,
                tickprefix="Rp ",
            ),
            hoverlabel=dict(bgcolor="#101828", font_color="#FFFFFF", font_size=12, bordercolor="#101828"),
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

with col_list:
    with st.container(border=True):
        st.markdown(
            '<div class="card-head"><div class="card-title">Rincian Performa Wilayah</div><div class="card-meta">Porsi Omzet</div></div>',
            unsafe_allow_html=True,
        )
        rows_html = []
        for idx, row in omzet_wilayah.iterrows():
            pct = (row["Total_Omzet"] / total_omzet) * 100
            badge_cls = "pct-badge" if idx == 0 else "pct-badge-muted"
            rows_html.append(
                f"""
                <div class="region-row">
                    <div class="region-top">
                        <span class="region-name">{row["wilayah_operasional"]}</span>
                        <div class="region-right">
                            <span class="region-val">{fmt_rupiah(row["Total_Omzet"])}</span>
                            <span class="{badge_cls}">{pct:.1f}%</span>
                        </div>
                    </div>
                    <div class="progress-track">
                        <div class="progress-fill" style="width:{min(pct, 100):.1f}%;"></div>
                    </div>
                    <div class="region-meta">{fmt_int(row["Jumlah_Pesanan"])} pesanan sukses &bull; Rating {row["Rata_Rating"]:.2f}</div>
                </div>
                """
            )
        st.markdown("".join(line.strip() for line in "".join(rows_html).splitlines()), unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 9. BARIS 4: SAMPEL TRANSAKSI TERFILTER
# -----------------------------------------------------------------------------
st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
with st.expander("Lihat Sampel 100 Data Transaksi Terfilter"):
    sampel = df_filtered[
        [
            "id_pesanan",
            "tanggal_waktu",
            "wilayah_operasional",
            "jenis_layanan",
            "nilai_transaksi",
            "rating_pelanggan",
        ]
    ].head(100).copy()
    sampel["nilai_transaksi"] = sampel["nilai_transaksi"].apply(fmt_rupiah)
    sampel.columns = [
        "ID Pesanan",
        "Tanggal & Waktu",
        "Wilayah",
        "Jenis Layanan",
        "Nilai Transaksi",
        "Rating",
    ]
    st.dataframe(sampel, use_container_width=True, hide_index=True)
