import pandas as pd
import os

# ==============================================================================
# KONFIGURASI
# ==============================================================================
nama_file_excel = 'TEKNIK (2).xlsx'  # Pastikan nama file ini sesuai dengan file Anda
folder_output = 'raw'                # Nama folder untuk menyimpan hasil pecahan

def extract_excel_sheets():
    # 1. Cek apakah file Excel ada
    if not os.path.exists(nama_file_excel):
        print(f"ERROR: File '{nama_file_excel}' tidak ditemukan!")
        print("Pastikan file Excel berada di folder yang sama dengan script ini.")
        return

    # 2. Buat folder 'raw' jika belum ada
    if not os.path.exists(folder_output):
        os.makedirs(folder_output)
        print(f"Folder '{folder_output}' berhasil dibuat.")
    else:
        print(f"Menggunakan folder '{folder_output}' yang sudah ada.")

    print("\nSedang membaca file Excel (mungkin butuh beberapa detik)...")
    
    try:
        # Load File Excel
        xls = pd.ExcelFile(nama_file_excel)
        
        # Daftar Sheet yang ingin kita ambil (Sesuai kebutuhan Data Mining)
        # Jika ingin mengambil SEMUA sheet, biarkan kode berjalan otomatis.
        # Di sini kita akan loop semua sheet yang ada.
        print(f"Ditemukan {len(xls.sheet_names)} sheet: {xls.sheet_names}")
        
        for sheet_name in xls.sheet_names:
            print(f" -> Mengekstrak sheet: [{sheet_name}] ...", end=" ")
            
            # Baca sheet
            df = pd.read_excel(xls, sheet_name=sheet_name)
            
            # Buat nama file CSV (bersihkan spasi di nama sheet jika ada)
            clean_name = sheet_name.strip().replace(" ", "_")
            csv_filename = f"{folder_output}/{clean_name}.csv"
            
            # Simpan ke CSV
            df.to_csv(csv_filename, index=False)
            print("OK.")

        print("\n" + "="*50)
        print("SELESAI! Semua sheet telah dipisahkan ke folder 'raw/'.")
        print("Silakan lanjut jalankan script '1_anonymize_data.py'.")
        print("="*50)

    except Exception as e:
        print(f"\nTerjadi Kesalahan: {e}")

if __name__ == "__main__":
    extract_excel_sheets()