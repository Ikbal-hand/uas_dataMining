import pandas as pd
import hashlib
import os

# ==============================================================================
# KONFIGURASI (Update lokasi file ke folder 'raw')
# ==============================================================================
# Script 0 tadi mengubah spasi jadi underscore, jadi 'Detail Bap' -> 'Detail_Bap.csv'
file_detail = 'raw/Detail_Bap.csv' 
file_bap = 'raw/BAP.csv'
output_file = 'data_siap_mining_final.csv'

def hash_data(value):
    """Mengubah data menjadi kode acak (hash) demi privasi"""
    if pd.isna(value) or value == '':
        return 'UNKNOWN'
    return hashlib.sha256(str(value).encode()).hexdigest()[:8]

print("1. Membaca File CSV dari folder 'raw'...")
try:
    # Cek apakah folder raw ada
    if not os.path.exists('raw'):
        print("ERROR: Folder 'raw' tidak ditemukan. Jalankan script 0_extract_excel.py dulu!")
        exit()

    # Membaca data
    df_detail = pd.read_csv(file_detail)
    df_bap = pd.read_csv(file_bap)
    
    # Membersihkan nama kolom (kadang ada spasi berlebih)
    df_detail.columns = df_detail.columns.str.strip()
    df_bap.columns = df_bap.columns.str.strip()
    
    print(f"   - Detail BAP: {len(df_detail)} baris")
    print(f"   - Header BAP: {len(df_bap)} baris")

except FileNotFoundError as e:
    print(f"ERROR: File tidak ditemukan di folder raw.\n{e}")
    print("Pastikan nama sheet di Excel Anda benar 'Detail Bap' dan 'BAP'.")
    exit()

# ==============================================================================
# 2. DATA CLEANING & MERGING
# ==============================================================================
print("2. Menggabungkan Data...")

# Hapus baris kosong
df_detail = df_detail.dropna(subset=['NO BAP', 'SERVICE'])
df_bap = df_bap.dropna(subset=['NO BAP'])

# Samakan format NO BAP
df_detail['NO BAP'] = df_detail['NO BAP'].astype(str).str.replace('.0', '', regex=False)
df_bap['NO BAP'] = df_bap['NO BAP'].astype(str).str.replace('.0', '', regex=False)

# Gabungkan (Left Join)
df_merged = pd.merge(df_detail, df_bap[['NO BAP', 'TANGGAL', 'KODE TOKO']], on='NO BAP', how='left')

print(f"   - Total Data setelah digabung: {len(df_merged)} baris")

# ==============================================================================
# 3. FILTERING (Hanya ambil Barang/Sparepart)
# ==============================================================================
# Membuang data Jasa/Transport agar Clustering fokus ke Sparepart
keyword_jasa = 'JASA|TRANSPORT|BIAYA|SERVICE|PEMASANGAN'
df_merged = df_merged[~df_merged['SERVICE'].str.contains(keyword_jasa, case=False, na=False)]
print(f"   - Total Data Barang (Sparepart) saja: {len(df_merged)} baris")

# ==============================================================================
# 4. ANONYMIZATION
# ==============================================================================
print("3. Melakukan Sensor Data Sensitif...")

kolom_sensitif = ['NO BAP', 'KODE TOKO']
for col in kolom_sensitif:
    if col in df_merged.columns:
        df_merged[col] = df_merged[col].apply(hash_data)

# Rename kolom final
df_merged = df_merged.rename(columns={
    'SERVICE': 'Sparepart',
    'UNIT': 'Quantity',
    'HARGA SATUAN': 'Harga',
    'TANGGAL': 'Tanggal',
    'NO BAP': 'BAP_Hash',
    'KODE TOKO': 'Toko_Hash'
})

kolom_final = ['BAP_Hash', 'Tanggal', 'Toko_Hash', 'Sparepart', 'Quantity', 'Harga']
df_final = df_merged[kolom_final]

# ==============================================================================
# 5. SIMPAN HASIL
# ==============================================================================
df_final.to_csv(output_file, index=False)
print("\n" + "="*50)
print(f"SUKSES! Data bersih tersimpan di: {output_file}")
print("="*50)