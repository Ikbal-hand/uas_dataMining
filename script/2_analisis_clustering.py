import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# ==============================================================================
# 1. LOAD DATA & PERSIAPAN
# ==============================================================================
nama_file = 'data_siap_mining_final.csv'

print("1. Membaca Data Bersih...")
try:
    df = pd.read_csv(nama_file)
    print(f"   - Berhasil membaca {len(df)} baris data transaksi.")
except FileNotFoundError:
    print(f"ERROR: File '{nama_file}' tidak ditemukan. Jalankan script 1 dulu!")
    exit()

# Pastikan tipe data benar
df['Tanggal'] = pd.to_datetime(df['Tanggal'], errors='coerce')
df['Harga'] = pd.to_numeric(df['Harga'], errors='coerce').fillna(0)
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0)

# ==============================================================================
# 2. AGREGASI DATA (Mengubah Data Transaksi -> Data Barang)
# ==============================================================================
# K-Means butuh data per "Item", bukan per "Transaksi".
# Kita hitung total kerusakan & rata-rata harga untuk setiap sparepart.

df_item = df.groupby('Sparepart').agg({
    'BAP_Hash': 'count',    # Frekuensi (Berapa kali muncul di BAP)
    'Quantity': 'sum',      # Total unit yang diganti
    'Harga': 'mean'         # Rata-rata harga
}).reset_index()

# Rename kolom agar lebih jelas
df_item.columns = ['Sparepart', 'Frekuensi_Transaksi', 'Total_Unit', 'Rata_Harga']

# Buang data sampah/typo (Misal sparepart yang cuma muncul 1 kali, opsional)
# df_item = df_item[df_item['Frekuensi_Transaksi'] > 1]

print(f"   - Data telah dikelompokkan menjadi {len(df_item)} jenis sparepart unik.")
print(df_item.head())

# ==============================================================================
# 3. VISUALISASI DESKRIPTIF (Syarat UAS: Minimal 2 Grafik)
# ==============================================================================
print("\n2. Membuat Grafik Dasar...")

# GRAFIK 1: Top 10 Sparepart (Bar Chart)
plt.figure(figsize=(10, 6))
top_10 = df_item.sort_values('Total_Unit', ascending=False).head(10)
sns.barplot(x='Total_Unit', y='Sparepart', data=top_10, palette='viridis')
plt.title('Top 10 Sparepart Paling Sering Diganti')
plt.xlabel('Total Unit Diganti')
plt.ylabel('Nama Sparepart')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('grafik_1_top10_sparepart.png')
print("   - Grafik 1 (Top 10) tersimpan.")

# GRAFIK 2: Tren Kerusakan Bulanan (Time Series)
# Ambil Bulan dan Tahun saja
df['Bulan'] = df['Tanggal'].dt.to_period('M')
tren_bulanan = df.groupby('Bulan')['BAP_Hash'].nunique() # Hitung jumlah BAP unik per bulan

plt.figure(figsize=(10, 6))
tren_bulanan.plot(kind='line', marker='o', color='crimson', linewidth=2)
plt.title('Tren Jumlah Perbaikan (Tiket BAP) Per Bulan')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Tiket BAP')
plt.grid(True)
plt.tight_layout()
plt.savefig('grafik_2_tren_bulanan.png')
print("   - Grafik 2 (Time Series) tersimpan.")

# ==============================================================================
# 4. CLUSTERING K-MEANS
# ==============================================================================
print("\n3. Menjalankan Algoritma K-Means...")

# Kita gunakan 2 Fitur: Frekuensi Kerusakan & Harga
# Tujuannya: Mengelompokkan mana barang "Murah-Sering Rusak" vs "Mahal-Jarang Rusak" dll.
X = df_item[['Total_Unit', 'Rata_Harga']]

# Scaling Data (Wajib untuk K-Means agar angka besar tidak mendominasi)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Jalankan K-Means dengan 3 Cluster (Misal: Low, Med, High Priority)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df_item['Cluster'] = kmeans.fit_predict(X_scaled)

# ==============================================================================
# 5. ANALISIS HASIL CLUSTER & LABELING
# ==============================================================================
# Kita perlu memberi nama cluster (High/Med/Low) secara otomatis
# Logika: Cluster dengan rata-rata 'Total_Unit' tertinggi adalah "High Priority"

# Hitung rata-rata Total_Unit per cluster
cluster_means = df_item.groupby('Cluster')['Total_Unit'].mean().sort_values(ascending=False)

# Mapping nama cluster berdasarkan urutan rata-rata
label_map = {
    cluster_means.index[0]: 'High Priority (Sering Rusak)',
    cluster_means.index[1]: 'Medium Priority',
    cluster_means.index[2]: 'Low Priority (Jarang Rusak)'
}
df_item['Kategori'] = df_item['Cluster'].map(label_map)

# Simpan hasil clustering ke Excel untuk bahan laporan
df_item.to_csv('hasil_clustering_final.csv', index=False)
print("   - File hasil analisis tersimpan: 'hasil_clustering_final.csv'")

# ==============================================================================
# 6. VISUALISASI HASIL CLUSTERING (Scatter Plot)
# ==============================================================================
plt.figure(figsize=(12, 8))

# Scatter plot
sns.scatterplot(
    data=df_item, 
    x='Total_Unit', 
    y='Rata_Harga', 
    hue='Kategori', 
    style='Kategori',
    palette={'High Priority (Sering Rusak)': 'red', 'Medium Priority': 'orange', 'Low Priority (Jarang Rusak)': 'green'},
    s=150, # Ukuran titik
    alpha=0.8
)

# Labeling: Memberi nama pada beberapa titik ekstrem agar grafik informatif
# (Hanya memberi label pada top 5 barang paling sering rusak agar tidak penuh)
top_labels = df_item.nlargest(5, 'Total_Unit')
for i in range(len(top_labels)):
    plt.text(
        top_labels.iloc[i]['Total_Unit'] + 0.2, 
        top_labels.iloc[i]['Rata_Harga'], 
        top_labels.iloc[i]['Sparepart'], 
        fontsize=9, 
        fontweight='bold'
    )

plt.title('Hasil Klasterisasi Karakteristik Sparepart (K-Means)', fontsize=14)
plt.xlabel('Total Unit Diganti (Frekuensi)', fontsize=12)
plt.ylabel('Harga Rata-rata (Rupiah)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(title='Kategori Stok')
plt.tight_layout()
plt.savefig('grafik_3_hasil_clustering.png')
print("   - Grafik 3 (Hasil Clustering) tersimpan.")

print("\n" + "="*50)
print("SELESAI! Silakan cek 3 file gambar PNG yang muncul di folder ini.")
print("Gunakan gambar tersebut untuk Slide PPT Anda.")
print("="*50)