# Dashboard Analitik Kinerja Jasa Sedot WC MGM

Proyek Project-Based Learning (PjBL) Mata Kuliah Big Data & Cloud Computing — Sektor P5 (UMKM).

**Live Dashboard:** [https://dbjasawcbuntumgm.streamlit.app](https://dbjasawcbuntumgm.streamlit.app)

## Ringkasan Proyek
Aplikasi ini dirancang untuk membantu pengelola layanan sanitasi (studi kasus Jasa Sedot WC MGM) memantau omzet, volume pesanan, persebaran wilayah operasional, serta tingkat kepuasan pelanggan secara interaktif melalui layanan cloud.

**Anggota Kelompok:**
- Fajar Ramadhan
- M. Mubiin Ben Prayoga
- Nurwahyuni Amanda
- Eglon Saranga

## Arsitektur Pipeline End-to-End
1. **Sumber Data:** 150.000 catatan transaksi sintetis layanan sanitasi periode Januari 2025 – Januari 2026.
2. **Ingest & Transform (Google Colab / Python Pandas):** Konversi format stempel waktu, pembersihan nilai anomali, dan pemfilteran status transaksi sehingga menyisakan **127.527 transaksi berstatus Selesai**.
3. **Storage (GitHub):** Penyimpanan data matang (`dataset_bersih_mgm.csv`) sebagai sumber data terpusat.
4. **Konsumsi & Visualisasi (Streamlit Community Cloud):** Penyajian 4 KPI utama, grafik interaktif Plotly, serta filter rentang tanggal, wilayah operasional, dan jenis layanan.

## Skema Data (`dataset_bersih_mgm.csv`)
| Kolom | Tipe Data | Deskripsi |
| :--- | :--- | :--- |
| `id_pesanan` | String | Kode unik transaksi sintetis |
| `tanggal_waktu` | Datetime | Tanggal dan waktu pencatatan pesanan |
| `jenis_layanan` | String | Kategori layanan (`Sedot WC`, `Pelancaran Pipa Mampet`) |
| `wilayah_operasional` | String | Area layanan (Makassar, Gowa, Maros, Takalar, Pangkep, Jeneponto) |
| `status_pekerjaan` | String | Status akhir pesanan setelah ETL (`Selesai`) |
| `nilai_transaksi` | Integer | Nilai nominal transaksi dalam Rupiah |
| `rating_pelanggan` | Float | Skor kepuasan pelanggan (skala 1.0 – 5.0) |

## Indikator Kinerja Utama (KPI)
- **KPI 1 – Total Omzet:** Rp 41.461.550.000 (rata-rata Rp 325.120 / pesanan)
- **KPI 2 – Total Pesanan Sukses:** 127.527 pesanan
- **KPI 3 – Rata-Rata Rating Pelanggan:** 4,50 / 5,00
- **KPI 4 – Layanan Terlaris:** Sedot WC (63.765 pesanan; 61,5% kontribusi omzet)

## Struktur File Proyek Big Data
- `Eksplorasi_Data_SDTWC.ipynb` — Notebook eksplorasi dan pipeline ETL (Google Colab)
- `dataset_bersih_mgm.csv` — Dataset hasil pembersihan (127.527 baris, 0 null, 0 duplikat)
- `app.py` — Kode sumber aplikasi dashboard Streamlit
- `.streamlit/config.toml` — Konfigurasi tema antarmuka dashboard
- `requirements.txt` — Daftar dependensi Python (`streamlit`, `pandas`, `plotly`)

## Cara Menjalankan Secara Lokal
```bash
pip install -r requirements.txt
streamlit run app.py
