# ============================================================
#  PRAKTIKUM ANALISIS DAN VISUALISASI DATA
#  Analisis Performa Penjualan E-Commerce
#  Dataset: data_praktikum_analisis_data.csv
# ============================================================

# ── LANGKAH 1: IMPORT LIBRARY ────────────────────────────────
import datetime as dt
import warnings

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

warnings.filterwarnings('ignore')

# Tema visual konsisten
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    'figure.dpi': 120,
    'axes.titlesize': 13,
    'axes.titleweight': 'bold',
    'axes.labelsize': 11,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
})

print("=" * 60)
print("  PRAKTIKUM ANALISIS DATA E-COMMERCE")
print("=" * 60)


# ── LANGKAH 2: LOAD & INSPEKSI DATA ─────────────────────────
print("\n[1] LOAD DATA")
print("-" * 40)

df = pd.read_csv('data_praktikum_analisis_data.csv')

print(f"Jumlah baris   : {df.shape[0]}")
print(f"Jumlah kolom   : {df.shape[1]}")
print(f"\nInfo dataset:")
print(df.info())
print(f"\nPreview 5 baris pertama:")
print(df.head())


# ── LANGKAH 3: DATA CLEANING ─────────────────────────────────
print("\n[2] DATA CLEANING")
print("-" * 40)

print("Missing values sebelum cleaning:")
print(df.isnull().sum())

mask_null = df['Total_Sales'].isnull()
df.loc[mask_null, 'Total_Sales'] = (
    df.loc[mask_null, 'Quantity'] * df.loc[mask_null, 'Price_Per_Unit']
)
print(f"\n✓ {mask_null.sum()} baris Total_Sales kosong diimputasi (Quantity × Price_Per_Unit)")

df['Order_Date'] = pd.to_datetime(df['Order_Date'])
df['Month']      = df['Order_Date'].dt.to_period('M').astype(str)
df['MonthNum']   = df['Order_Date'].dt.month
df['MonthName']  = df['Order_Date'].dt.strftime('%b')
print("✓ Order_Date dikonversi ke datetime, kolom Month & MonthName ditambahkan")

neg_price = (df['Price_Per_Unit'] <= 0).sum()
neg_ad    = (df['Ad_Budget'] <= 0).sum()
print(f"✓ Harga negatif (Price_Per_Unit): {neg_price} ditemukan")
print(f"✓ Iklan negatif (Ad_Budget)     : {neg_ad} ditemukan")

dup = df['Order_ID'].duplicated().sum()
print(f"✓ Duplikasi Order_ID            : {dup} ditemukan")

print(f"\nMissing values sesudah cleaning:")
print(df.isnull().sum())
print(f"\nDataset siap: {df.shape[0]} baris bersih")


# ── LANGKAH 4: STATISTIK DESKRIPTIF ─────────────────────────
print("\n[3] STATISTIK DESKRIPTIF")
print("-" * 40)

total_sales  = df['Total_Sales'].sum()
total_ad     = df['Ad_Budget'].sum()
avg_order    = df['Total_Sales'].mean()
n_customers  = df['CustomerID'].nunique()

print(f"Total Penjualan      : Rp {total_sales:,.0f}")
print(f"Total Anggaran Iklan : Rp {total_ad:,.0f}")
print(f"Rata-rata per Order  : Rp {avg_order:,.0f}")
print(f"Pelanggan Unik       : {n_customers}")
print(f"\nStatistik numerik:")
print(df[['Quantity','Price_Per_Unit','Ad_Budget','Total_Sales']].describe().apply(
    lambda col: col.map(lambda x: f"Rp {x:,.0f}" if x > 100 else round(x, 2))
))


# ════════════════════════════════════════════════════════════
#  VISUALISASI 1 — TREN PENJUALAN BULANAN
# ════════════════════════════════════════════════════════════
print("\n[4] VISUALISASI 1 — TREN PENJUALAN BULANAN")
print("-" * 40)

monthly = (
    df.groupby(['Month', 'MonthName', 'MonthNum'])['Total_Sales']
    .sum()
    .reset_index()
    .sort_values('MonthNum')
)
monthly['Total_Sales_Jt'] = monthly['Total_Sales'] / 1_000_000

peak = monthly.loc[monthly['Total_Sales_Jt'].idxmax()]
low  = monthly.loc[monthly['Total_Sales_Jt'].idxmin()]

fig, ax = plt.subplots(figsize=(11, 5))

ax.plot(monthly['MonthName'], monthly['Total_Sales_Jt'],
        marker='o', linewidth=2.2, color='#1D9E75',
        markerfacecolor='white', markeredgecolor='#1D9E75', markersize=8)

ax.scatter(peak['MonthName'], peak['Total_Sales_Jt'],
           s=160, color='#1D9E75', zorder=5)
ax.scatter(low['MonthName'], low['Total_Sales_Jt'],
           s=160, color='#E24B4A', zorder=5)

ax.annotate(f"Tertinggi\nRp {peak['Total_Sales_Jt']:.1f} Jt",
            xy=(peak['MonthName'], peak['Total_Sales_Jt']),
            xytext=(0, 14), textcoords='offset points',
            ha='center', fontsize=9, color='#0F6E56', fontweight='bold')
ax.annotate(f"Terendah\nRp {low['Total_Sales_Jt']:.1f} Jt",
            xy=(low['MonthName'], low['Total_Sales_Jt']),
            xytext=(0, -26), textcoords='offset points',
            ha='center', fontsize=9, color='#A32D2D', fontweight='bold')

ax.fill_between(monthly['MonthName'], monthly['Total_Sales_Jt'],
                alpha=0.08, color='#1D9E75')
ax.set_title('Tren Penjualan Bulanan — 2023', pad=12)
ax.set_xlabel('Bulan')
ax.set_ylabel('Total Penjualan (Juta Rp)')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'Rp {x:.0f} Jt'))
plt.tight_layout()
plt.savefig('01_tren_penjualan_bulanan.png', bbox_inches='tight')
plt.show()

print(f"Bulan tertinggi : {peak['MonthName']} — Rp {peak['Total_Sales_Jt']:.2f} Juta")
print(f"Bulan terendah  : {low['MonthName']}  — Rp {low['Total_Sales_Jt']:.2f} Juta")


# ════════════════════════════════════════════════════════════
#  VISUALISASI 2 — SCATTER PLOT UNDERPERFORMER
# ════════════════════════════════════════════════════════════
print("\n[5] TUGAS 1 — IDENTIFIKASI PRODUK UNDERPERFORMER")
print("-" * 40)

avg_price = df['Price_Per_Unit'].mean()
avg_qty   = df['Quantity'].mean()

df['Underperformer'] = (df['Price_Per_Unit'] > avg_price) & (df['Quantity'] < avg_qty)
under_df = df[df['Underperformer']]
normal_df = df[~df['Underperformer']]

print(f"Rata-rata Price_Per_Unit : Rp {avg_price:,.0f}")
print(f"Rata-rata Quantity       : {avg_qty:.2f} unit")
print(f"Jumlah Underperformer    : {len(under_df)} transaksi ({len(under_df)/len(df)*100:.1f}%)")

fig, ax = plt.subplots(figsize=(10, 6))

ax.scatter(normal_df['Price_Per_Unit']/1e6, normal_df['Quantity'],
           alpha=0.55, s=60, color='#1D9E75', label='Normal / Baik', zorder=3)
ax.scatter(under_df['Price_Per_Unit']/1e6, under_df['Quantity'],
           alpha=0.8, s=80, color='#E24B4A', label='Underperformer', zorder=4)

# Garis rata-rata
ax.axvline(avg_price/1e6, color='gray', linestyle='--', linewidth=1, alpha=0.6)
ax.axhline(avg_qty, color='gray', linestyle='--', linewidth=1, alpha=0.6)

ax.text(avg_price/1e6 + 0.03, ax.get_ylim()[1] * 0.97,
        f'avg price\nRp{avg_price/1e6:.2f}Jt', fontsize=8, color='gray', va='top')
ax.text(ax.get_xlim()[0] + 0.02, avg_qty + 0.1,
        f'avg qty {avg_qty:.1f}', fontsize=8, color='gray')

ax.set_title('Identifikasi Produk Underperformer\n(Harga Tinggi, Volume Rendah)', pad=12)
ax.set_xlabel('Price per Unit (Juta Rp)')
ax.set_ylabel('Quantity (unit)')
ax.legend(framealpha=0.9)
plt.tight_layout()
plt.savefig('02_scatter_underperformer.png', bbox_inches='tight')
plt.show()

print("\nBreakdown underperformer per kategori:")
print(under_df.groupby('Product_Category').agg(
    Jumlah_Transaksi=('Order_ID', 'count'),
    Avg_Price=('Price_Per_Unit', 'mean'),
    Avg_Qty=('Quantity', 'mean')
).round(0))


# ════════════════════════════════════════════════════════════
#  VISUALISASI 3 — RFM ANALYSIS
# ════════════════════════════════════════════════════════════
print("\n[6] TUGAS 2 — SEGMENTASI PELANGGAN (RFM ANALYSIS)")
print("-" * 40)

snapshot_date = df['Order_Date'].max() + dt.timedelta(days=1)

rfm = df.groupby('CustomerID').agg(
    Recency   = ('Order_Date',  lambda x: (snapshot_date - x.max()).days),
    Frequency = ('Order_ID',    'count'),
    Monetary  = ('Total_Sales', 'sum')
).reset_index()

# Skor 1–5
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1], duplicates='drop').astype(int)
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5,
                          labels=[1,2,3,4,5], duplicates='drop').astype(int)
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1,2,3,4,5], duplicates='drop').astype(int)
rfm['RFM_Total'] = rfm['R_Score'] + rfm['F_Score'] + rfm['M_Score']

def segment(score):
    if score >= 12:  return 'Champions'
    elif score >= 9: return 'Loyal Customers'
    elif score >= 6: return 'Potential'
    else:            return 'At Risk'

rfm['Segment'] = rfm['RFM_Total'].apply(segment)

seg_count = rfm['Segment'].value_counts()
seg_order = ['Champions', 'Loyal Customers', 'Potential', 'At Risk']
seg_colors = {'Champions':'#1D9E75', 'Loyal Customers':'#378ADD',
              'Potential':'#BA7517', 'At Risk':'#E24B4A'}

print("Distribusi segmen pelanggan:")
for seg in seg_order:
    n = seg_count.get(seg, 0)
    print(f"  {seg:<20}: {n} pelanggan ({n/len(rfm)*100:.1f}%)")

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Bar chart distribusi segmen
bars = [seg_count.get(s, 0) for s in seg_order]
colors_bar = [seg_colors[s] for s in seg_order]
ax = axes[0]
b = ax.bar(seg_order, bars, color=colors_bar, width=0.6, edgecolor='none')
for rect, val in zip(b, bars):
    ax.text(rect.get_x() + rect.get_width()/2, rect.get_height() + 0.2,
            str(val), ha='center', va='bottom', fontsize=10, fontweight='bold')
ax.set_title('Distribusi Segmen RFM')
ax.set_ylabel('Jumlah Pelanggan')
ax.set_xticklabels(seg_order, rotation=15, ha='right')

# Scatter Recency vs Monetary per segmen
ax2 = axes[1]
for seg in seg_order:
    sub = rfm[rfm['Segment'] == seg]
    ax2.scatter(sub['Recency'], sub['Monetary']/1e6,
                label=seg, color=seg_colors[seg], alpha=0.75, s=70)
ax2.set_title('Recency vs Monetary per Segmen')
ax2.set_xlabel('Recency (hari)')
ax2.set_ylabel('Monetary (Juta Rp)')
ax2.legend(fontsize=9)

plt.suptitle('Segmentasi Pelanggan — RFM Analysis', fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('03_rfm_segmentation.png', bbox_inches='tight')
plt.show()

print("\nRata-rata RFM per segmen:")
print(rfm.groupby('Segment')[['Recency','Frequency','Monetary']].mean().round(1))


# ════════════════════════════════════════════════════════════
#  VISUALISASI 4 — EFISIENSI KATEGORI
# ════════════════════════════════════════════════════════════
print("\n[7] TUGAS 3 — ANALISIS EFISIENSI KATEGORI")
print("-" * 40)

cat_df = df.groupby('Product_Category').agg(
    Total_Sales = ('Total_Sales', 'sum'),
    Total_Ad    = ('Ad_Budget',   'sum')
).reset_index()
cat_df['Rasio_Efisiensi'] = cat_df['Total_Sales'] / cat_df['Total_Ad']
cat_df = cat_df.sort_values('Rasio_Efisiensi')

print("Efisiensi per kategori (Sales / Ad Budget):")
for _, row in cat_df.iterrows():
    print(f"  {row['Product_Category']:<15}: {row['Rasio_Efisiensi']:.3f}x  "
          f"(Sales Rp{row['Total_Sales']/1e6:.1f}Jt | Iklan Rp{row['Total_Ad']/1e6:.1f}Jt)")

fig, ax = plt.subplots(figsize=(10, 5))
n = len(cat_df)
palette = ['#E24B4A' if i == 0 else '#1D9E75' if i == n-1 else '#BA7517'
           for i in range(n)]

bars = ax.barh(cat_df['Product_Category'], cat_df['Rasio_Efisiensi'],
               color=palette, height=0.55, edgecolor='none')

for bar, val in zip(bars, cat_df['Rasio_Efisiensi']):
    ax.text(val + 0.01, bar.get_y() + bar.get_height()/2,
            f'{val:.3f}x', va='center', fontsize=10)

ax.set_title('Efisiensi Kategori — Rasio Total Sales / Ad Budget\n(Urutan: Paling Tidak Efisien → Paling Efisien)', pad=10)
ax.set_xlabel('Rasio Efisiensi (kali lipat)')
ax.axvline(1.0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax.text(1.01, -0.6, 'break-even', fontsize=8, color='gray')
plt.tight_layout()
plt.savefig('04_efisiensi_kategori.png', bbox_inches='tight')
plt.show()


# ════════════════════════════════════════════════════════════
#  VISUALISASI 5 — UJI HIPOTESIS
# ════════════════════════════════════════════════════════════
print("\n[8] TUGAS 4 — UJI HIPOTESIS SEDERHANA")
print("-" * 40)

median_ad    = df['Ad_Budget'].median()
grup_tinggi  = df[df['Ad_Budget'] >= median_ad]['Total_Sales']
grup_rendah  = df[df['Ad_Budget'] <  median_ad]['Total_Sales']

avg_tinggi = grup_tinggi.mean()
avg_rendah = grup_rendah.mean()
selisih_pct = (avg_tinggi - avg_rendah) / avg_rendah * 100

print(f"Median Ad_Budget         : Rp {median_ad:,.0f}")
print(f"Rata-rata Sales (Iklan Tinggi) : Rp {avg_tinggi:,.0f}  (n={len(grup_tinggi)})")
print(f"Rata-rata Sales (Iklan Rendah) : Rp {avg_rendah:,.0f}  (n={len(grup_rendah)})")
print(f"Selisih                        : {selisih_pct:+.1f}%")

if selisih_pct > 5:
    print("→ Hipotesis DITERIMA: iklan tinggi menghasilkan penjualan lebih besar secara deskriptif.")
else:
    print("→ Hipotesis LEMAH: perbedaan kecil, faktor lain turut berperan.")

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Bar perbandingan rata-rata
ax1 = axes[0]
labels_h = ['Iklan Rendah\n(< median)', 'Iklan Tinggi\n(≥ median)']
values_h = [avg_rendah/1e6, avg_tinggi/1e6]
colors_h = ['#E24B4A', '#1D9E75']
b = ax1.bar(labels_h, values_h, color=colors_h, width=0.45, edgecolor='none')
for rect, val in zip(b, values_h):
    ax1.text(rect.get_x() + rect.get_width()/2, rect.get_height() + 0.05,
             f'Rp {val:.2f} Jt', ha='center', fontsize=10, fontweight='bold')
ax1.set_title('Rata-rata Penjualan:\nIklan Rendah vs Iklan Tinggi')
ax1.set_ylabel('Rata-rata Total Sales (Juta Rp)')

ax2 = axes[1]
data_box = pd.DataFrame({
    'Total Sales (Jt Rp)': pd.concat([grup_rendah/1e6, grup_tinggi/1e6]),
    'Kelompok': ['Iklan Rendah']*len(grup_rendah) + ['Iklan Tinggi']*len(grup_tinggi)
})
bp = data_box.groupby('Kelompok')['Total Sales (Jt Rp)'].apply(list)
bplot = ax2.boxplot([bp['Iklan Rendah'], bp['Iklan Tinggi']],
                    labels=['Iklan Rendah', 'Iklan Tinggi'],
                    patch_artist=True, widths=0.4,
                    medianprops={'color':'white','linewidth':2})
for patch, color in zip(bplot['boxes'], ['#E24B4Acc', '#1D9E75cc']):
    patch.set_facecolor(color)
ax2.set_title('Distribusi Penjualan per Kelompok Iklan')
ax2.set_ylabel('Total Sales (Juta Rp)')

plt.suptitle('Uji Hipotesis — Pengaruh Anggaran Iklan terhadap Penjualan',
             fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('05_uji_hipotesis.png', bbox_inches='tight')
plt.show()


# ════════════════════════════════════════════════════════════
#  VISUALISASI 6 — KORELASI & HEATMAP
# ════════════════════════════════════════════════════════════
print("\n[9] ANALISIS KORELASI")
print("-" * 40)

corr_cols = ['Quantity', 'Price_Per_Unit', 'Ad_Budget', 'Total_Sales']
corr_matrix = df[corr_cols].corr()

print("Matriks korelasi:")
print(corr_matrix.round(3))
print(f"\nKorelasi Ad_Budget ↔ Total_Sales : {corr_matrix.loc['Ad_Budget','Total_Sales']:.3f}")

fig, ax = plt.subplots(figsize=(7, 5))
mask = np.zeros_like(corr_matrix, dtype=bool)
mask[np.triu_indices_from(mask)] = True
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdYlGn',
            center=0, square=True, linewidths=0.5,
            cbar_kws={'shrink': 0.8}, ax=ax, mask=mask)
ax.set_title('Heatmap Korelasi Antar Variabel', pad=12)
plt.tight_layout()
plt.savefig('06_heatmap_korelasi.png', bbox_inches='tight')
plt.show()


# ════════════════════════════════════════════════════════════
#  VISUALISASI 7 — REGRESI LINEAR
# ════════════════════════════════════════════════════════════
print("\n[10] PENDALAMAN — REGRESI LINEAR SEDERHANA")
print("-" * 40)

X = df[['Ad_Budget']]
y = df['Total_Sales']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
r2     = r2_score(y_test, y_pred)

print(f"Koefisien (slope)  : {model.coef_[0]:.4f}")
print(f"Intercept          : {model.intercept_:,.0f}")
print(f"R² Score (test)    : {r2:.4f}")
print(f"Interpretasi       : Setiap Rp 1 tambahan Ad_Budget → penjualan naik Rp {model.coef_[0]:.2f}")

x_line  = np.linspace(X['Ad_Budget'].min(), X['Ad_Budget'].max(), 200).reshape(-1,1)
y_line  = model.predict(x_line)

fig, ax = plt.subplots(figsize=(9, 5))
ax.scatter(X/1e6, y/1e6, alpha=0.45, s=55, color='#378ADD', label='Data aktual')
ax.plot(x_line/1e6, y_line/1e6, color='#D85A30', linewidth=2.2,
        label=f'Regresi linear (R²={r2:.3f})')
ax.set_title('Regresi Linear: Ad Budget → Total Sales', pad=12)
ax.set_xlabel('Ad Budget (Juta Rp)')
ax.set_ylabel('Total Sales (Juta Rp)')
ax.legend()
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'Rp{x:.0f}Jt'))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'Rp{x:.0f}Jt'))
plt.tight_layout()
plt.savefig('07_regresi_linear.png', bbox_inches='tight')
plt.show()

print("\n" + "=" * 60)
print("  RINGKASAN HASIL PRAKTIKUM")
print("=" * 60)

best_cat  = cat_df.iloc[-1]
worst_cat = cat_df.iloc[0]
champ_n   = (rfm['Segment'] == 'Champions').sum()
risk_n    = (rfm['Segment'] == 'At Risk').sum()

print(f"""
[Data Wrangling]
  • 7 baris Total_Sales kosong → diimputasi Qty × Price
  • Tidak ada harga negatif, tidak ada duplikasi

[Underperformer]
  • {len(under_df)} transaksi ({len(under_df)/len(df)*100:.0f}%) teridentifikasi underperformer
  • Harga > Rp {avg_price:,.0f} & Qty < {avg_qty:.1f} unit

[RFM Segmentation]
  • Champions       : {champ_n} pelanggan
  • At Risk         : {risk_n} pelanggan → perlu win-back campaign

[Efisiensi Kategori]
  • Paling efisien  : {best_cat['Product_Category']} ({best_cat['Rasio_Efisiensi']:.3f}x)
  • Paling boros    : {worst_cat['Product_Category']} ({worst_cat['Rasio_Efisiensi']:.3f}x)

[Uji Hipotesis]
  • Iklan tinggi vs rendah : {selisih_pct:+.1f}% perbedaan rata-rata penjualan
  • R² Regresi Linear      : {r2:.3f}

[Output file]
  01_tren_penjualan_bulanan.png
  02_scatter_underperformer.png
  03_rfm_segmentation.png
  04_efisiensi_kategori.png
  05_uji_hipotesis.png
  06_heatmap_korelasi.png
  07_regresi_linear.png
""")
print("=" * 60)
print("  Praktikum selesai! Semua chart tersimpan sebagai file .png")
print("=" * 60)