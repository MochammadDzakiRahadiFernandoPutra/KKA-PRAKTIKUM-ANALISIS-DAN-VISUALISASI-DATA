# ╔══════════════════════════════════════════════════════════╗
# ║            LAPORAN PRAKTIKUM                            ║
# ║  Copy output di bawah ini langsung ke README.md GitHub  ║
# ╚══════════════════════════════════════════════════════════╝
 
laporan = f"""
# Laporan Praktikum — Analisis Performa Penjualan E-Commerce
 
**Mata Kuliah :** Analisis dan Visualisasi Data
**Dataset     :** data_praktikum_analisis_data.csv
**Periode Data:** Januari – Desember 2023
**Tools       :** Python · Pandas · Matplotlib · Seaborn · Scikit-Learn
 
---
 
## 1. Business Question
 
Praktikum ini menjawab empat pertanyaan bisnis utama dari sebuah perusahaan
e-commerce yang mengalami penurunan efisiensi meskipun anggaran iklan terus meningkat:
 
1. **Underperformer** — Produk mana yang harganya di atas rata-rata namun volume
   penjualannya justru rendah sehingga membebani arus kas?
2. **Segmentasi Pelanggan** — Siapa pelanggan terbaik yang berhak mendapat voucher
   loyalitas, dan siapa yang berisiko churn?
3. **Efisiensi Iklan** — Kategori produk mana yang paling efisien mengonversi
   anggaran iklan menjadi penjualan nyata?
4. **Uji Hipotesis** — Apakah peningkatan anggaran iklan di atas median benar-benar
   menghasilkan peningkatan total penjualan yang signifikan?
 
---
 
## 2. Data Wrangling
 
Dataset awal terdiri dari **150 baris dan 8 kolom**:
`Order_ID`, `CustomerID`, `Order_Date`, `Product_Category`,
`Quantity`, `Price_Per_Unit`, `Ad_Budget`, `Total_Sales`
 
| Langkah | Tindakan | Hasil |
|---------|----------|-------|
| Missing Values | {n_imputed} baris `Total_Sales` kosong diimputasi dengan `Quantity × Price_Per_Unit` | 0 missing values tersisa |
| Tipe Data | `Order_Date` dikonversi dari string ke datetime; diekstrak kolom `Month` dan `MonthName` | Analisis temporal tersedia |
| Harga Negatif | Pengecekan `Price_Per_Unit <= 0` dan `Ad_Budget <= 0` | {n_neg_price} ditemukan — data valid semua |
| Duplikasi | Pengecekan `Order_ID` duplikat | {n_dup} duplikat — data bersih |
 
**Dataset final: 150 baris bersih · {n_customers} pelanggan unik · 5 kategori produk**
(Books, Electronics, Fashion, Gadget, Home Decor)
 
---
 
## 3. Insights
 
### 3.1 Tren Penjualan Bulanan
*Grafik: `01_tren_penjualan_bulanan.png`*
 
Penjualan tertinggi terjadi pada bulan **{peak['MonthName']}** sebesar
**Rp {peak['Total_Sales_Jt']:.2f} Juta**, sedangkan terendah pada bulan
**{low['MonthName']}** sebesar **Rp {low['Total_Sales_Jt']:.2f} Juta**.
Pola fluktuatif dengan kecenderungan meningkat di pertengahan dan akhir tahun
mengindikasikan adanya efek musiman atau kampanye promosi periodik.
 
### 3.2 Identifikasi Produk Underperformer
*Grafik: `02_scatter_underperformer.png`*
 
Dari scatter plot Price_Per_Unit vs Quantity, ditemukan **{len(under_df)} transaksi
({len(under_df)/len(df)*100:.0f}% dari total)** yang masuk kuadran harga tinggi —
volume rendah (harga > Rp {avg_price:,.0f} dan quantity < {avg_qty:.1f} unit).
Produk-produk ini berpotensi membebani arus kas karena nilai satuannya mahal
namun jarang dibeli sehingga kontribusi pendapatannya tidak proporsional.
 
### 3.3 Segmentasi Pelanggan RFM
*Grafik: `03_rfm_segmentation.png`*
 
Dari **{len(rfm)} pelanggan unik**, segmentasi RFM menghasilkan empat kelompok:
 
| Segmen | Jumlah | Keterangan |
|--------|--------|------------|
| Champions | {champ_n} | Belanja paling sering, terbaru, nilai terbesar — aset utama |
| Loyal Customers | {int(seg_count.get('Loyal Customers', 0))} | Konsisten berbelanja dengan frekuensi dan nilai baik |
| Potential | {int(seg_count.get('Potential', 0))} | Perilaku sedang — perlu stimulus naik ke Loyal |
| At Risk | {risk_n} | Lama tidak transaksi — butuh win-back campaign segera |
 
### 3.4 Efisiensi Kategori Produk
*Grafik: `04_efisiensi_kategori.png`*
 
Perbandingan rasio `Total_Sales / Ad_Budget` per kategori:
- **{best_cat['Product_Category']}** → paling efisien, rasio **{best_cat['Rasio_Efisiensi']:.3f}x**
  (setiap Rp 1 iklan menghasilkan Rp {best_cat['Rasio_Efisiensi']:.2f} penjualan)
- **{worst_cat['Product_Category']}** → paling tidak efisien, rasio **{worst_cat['Rasio_Efisiensi']:.3f}x**
  (anggaran iklan tidak tertutupi oleh pendapatan — di bawah break-even 1.0x)
 
### 3.5 Korelasi Antar Variabel
*Grafik: `06_heatmap_korelasi.png`*
 
Heatmap korelasi menunjukkan **Quantity berkorelasi positif kuat dengan Total_Sales**,
yang logis karena volume langsung membentuk pendapatan. Sebaliknya,
**Ad_Budget berkorelasi sangat lemah terhadap Total_Sales (r = {corr_ad_sales:.3f})**,
mengindikasikan bahwa besarnya anggaran iklan bukan faktor penentu utama penjualan —
kategori produk, harga, dan musim berperan lebih dominan.
 
### 3.6 Uji Hipotesis & Regresi Linear
*Grafik: `05_uji_hipotesis.png` & `07_regresi_linear.png`*
 
Perbandingan dua kelompok berdasarkan median Ad_Budget (Rp {median_ad:,.0f}):
 
| Kelompok | n | Rata-rata Total Sales |
|----------|---|----------------------|
| Iklan Tinggi (≥ median) | {len(grup_tinggi)} | Rp {avg_tinggi:,.0f} |
| Iklan Rendah (< median) | {len(grup_rendah)} | Rp {avg_rendah:,.0f} |
 
Selisih: **{selisih_pct:+.1f}%** → Hipotesis **{"DITERIMA" if selisih_pct > 5 else "LEMAH"}** —
{"peningkatan iklan berkorelasi positif dengan penjualan." if selisih_pct > 5
else "perbedaan kecil; faktor lain (kategori, harga, musim) turut berperan besar."}
 
Model regresi linear menghasilkan koefisien **{coef:.4f}** dan R² = **{r2:.3f}**,
artinya Ad_Budget saja hanya menjelaskan sebagian kecil variasi penjualan.
 
---
 
## 4. Recommendation
 
**1. Repricing & Bundling Produk Underperformer**
Sebanyak {len(under_df)} transaksi ({len(under_df)/len(df)*100:.0f}%) masuk kategori underperformer.
Produk dengan harga di atas rata-rata namun volume rendah sebaiknya diuji melalui
strategi flash sale periodik atau dikemas dalam bundling bersama produk laris untuk
menggerakkan stok dan meningkatkan konversi tanpa menurunkan margin secara permanen.
 
**2. Program Loyalitas Berbasis Segmen RFM**
{champ_n} pelanggan Champions dan {int(seg_count.get('Loyal Customers', 0))} Loyal Customers
diprioritaskan untuk mendapat voucher eksklusif, akses early sale, atau cashback bertingkat.
Sementara {risk_n} pelanggan At Risk perlu kampanye re-engagement personal berdasarkan
riwayat pembelian sebelumnya agar tidak benar-benar churn.
 
**3. Realokasi Anggaran Iklan ke Kategori Efisien**
Anggaran iklan sebaiknya dialihkan secara bertahap dari kategori
**{worst_cat['Product_Category']}** (rasio {worst_cat['Rasio_Efisiensi']:.3f}x, di bawah break-even)
ke **{best_cat['Product_Category']}** (rasio {best_cat['Rasio_Efisiensi']:.3f}x).
Lakukan A/B testing pada kreatif iklan kategori tidak efisien terlebih dahulu untuk
mengidentifikasi apakah masalahnya pada targeting atau pesan iklan.
 
**4. Kembangkan Model Prediktif yang Lebih Kuat**
Model regresi linear saat ini memiliki R² = {r2:.3f}, artinya Ad_Budget saja belum cukup
menjelaskan variasi penjualan. Tambahkan variabel kategori produk, musim, harga, dan
frekuensi promosi untuk meningkatkan akurasi prediksi dan mendukung keputusan iklan
berbasis data secara lebih andal.
 
---
 
## 5. Referensi File Output
 
| File | Keterangan |
|------|------------|
| `01_tren_penjualan_bulanan.png` | Line chart tren penjualan Jan–Des 2023 |
| `02_scatter_underperformer.png` | Scatter plot identifikasi produk underperformer |
| `03_rfm_segmentation.png` | Bar chart + scatter segmentasi pelanggan RFM |
| `04_efisiensi_kategori.png` | Horizontal bar chart efisiensi kategori produk |
| `05_uji_hipotesis.png` | Bar chart + box plot uji hipotesis pengaruh iklan |
| `06_heatmap_korelasi.png` | Heatmap korelasi antar variabel numerik |
| `07_regresi_linear.png` | Scatter + garis regresi Ad Budget vs Total Sales |
 
---
 
*Laporan ini dibuat sebagai bagian dari Praktikum Analisis dan Visualisasi Data.*
*Seluruh kode tersedia di file `final_praktikum_ecommerce.py` dalam repository ini.*
"""
 
print(laporan)
 
# ── AUTO-GENERATE README.md ───────────────────────────────────
# Uncomment 3 baris berikut untuk langsung membuat file README.md:
# with open('README.md', 'w', encoding='utf-8') as f:
#     f.write(laporan)
# print("README.md berhasil dibuat di folder yang sama!")
 







