# Implementasi Data Mining untuk Klasterisasi Karakteristik Kerusakan Perangkat Elektronik Menggunakan Algoritma K-Means

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Algorithm](https://img.shields.io/badge/Algorithm-K--Means%20Clustering-orange?style=for-the-badge)

## 📌 Pendahuluan

Proyek ini bertujuan untuk menganalisis pola kerusakan perangkat elektronik dan memberikan rekomendasi manajemen stok *sparepart* yang lebih efisien. Menggunakan algoritma **K-Means Clustering**, sistem mengelompokkan *sparepart* berdasarkan frekuensi kerusakan dan harga rata-rata untuk menentukan prioritas stok (High, Medium, Low Priority).

[cite_start]Proyek ini disusun sebagai tugas akhir mata kuliah Data Mining[cite: 1].

## 🎯 Tujuan Penelitian

1.  **Efisiensi Stok:** Mengidentifikasi *sparepart* yang paling sering dibutuhkan (Fast Moving).
2.  **Pola Kerusakan:** Memvisualisasikan tren kerusakan bulanan.
3.  [cite_start]**Segmentasi:** Mengelompokkan barang berdasarkan tingkat urgensi menggunakan *Clustering*[cite: 14, 33].

## 🛠️ Teknologi & Library

Proyek ini dibangun menggunakan Python dengan library berikut:

* **Pandas & NumPy:** Manipulasi dan pembersihan data.
* [cite_start]**Matplotlib & Seaborn:** Visualisasi data (Barplot, Time Series, Scatter Plot)[cite: 13, 31].
* **Scikit-Learn:** Implementasi algoritma K-Means dan StandardScaler.
* **OpenPyXL:** Ekstraksi data dari file Excel `.xlsx`.

## 📂 Struktur Folder

```text
├── Image/                   # Folder penyimpanan hasil visualisasi (Grafik)
│   ├── grafik_1_top10_sparepart.png
│   ├── grafik_2_tren_bulanan.png
│   └── grafik_3_hasil_clustering.png
├── raw/                     # Folder penyimpanan data mentah (CSV hasil ekstrak)
├── 0_extract_excel.py       # Script ekstraksi sheet Excel
├── 1_anonymize_data.py      # Script sensor data sensitif (Anonymization)
├── 2_analisis_clustering.py # Script utama analisis & modeling
├── requirements.txt         # Daftar dependency library
└── README.md                # Dokumentasi proyek

```

## 📊 Hasil Analisis & Visualisasi

Berikut adalah hasil visualisasi data yang telah diolah:

### 1. Top 10 Sparepart Paling Sering Rusak

Grafik ini menunjukkan komponen yang memiliki frekuensi penggantian tertinggi.

### 2. Tren Kerusakan Bulanan (Time Series)

Analisis tren untuk melihat lonjakan permintaan perbaikan pada bulan-bulan tertentu.

### 3. Hasil Clustering (K-Means)

Segmentasi *sparepart* menjadi 3 klaster:

* 🔴 **High Priority:** Sering rusak, stok wajib banyak.
* 🟠 **Medium Priority:** Kerusakan sedang.
* 🟢 **Low Priority:** Jarang rusak.

## 🚀 Cara Menjalankan Project

Ikuti langkah-langkah berikut untuk menjalankan analisis di komputer lokal Anda:

### 1. Clone Repository

```bash
git clone [https://github.com/username-anda/nama-repo.git](https://github.com/username-anda/nama-repo.git)
cd nama-repo

```

### 2. Install Dependencies

Pastikan Python sudah terinstal, lalu jalankan:

```bash
pip install -r requirements.txt

```

### 3. Jalankan Script Secara Berurutan

Proses dibagi menjadi 3 tahap agar data tetap aman dan terstruktur:

**Tahap 1: Ekstraksi Excel**
Memecah file Excel utama menjadi CSV terpisah.

```bash
python 0_extract_excel.py

```

**Tahap 2: Anonymization**
Menyensor data sensitif (No BAP, Kode Toko) demi privasi data.

```bash
python 1_anonymize_data.py

```

**Tahap 3: Analisis & Clustering**
Menjalankan algoritma K-Means dan menghasilkan grafik.

```bash
python 2_analisis_clustering.py

```

## 👥 Anggota Kelompok

| NIM | Nama Mahasiswa | Peran |
| --- | --- | --- |
| XXXXXXXX | Nama Anggota 1 | Project Manager |
| XXXXXXXX | Nama Anggota 2 | Data Analyst |
| XXXXXXXX | Nama Anggota 3 | Programmer |
| XXXXXXXX | Nama Anggota 4 | Technical Writer |

---

*Dibuat untuk memenuhi Tugas UAS Data Mining 2026*

```

### 💡 Poin Penting Agar Gambar Muncul:
1.  Pastikan Anda **membuat folder baru** bernama `Image` di dalam repository Anda.
2.  Setelah Anda menjalankan script `2_analisis_clustering.py`, **pindahkan** 3 file gambar PNG yang dihasilkan (`grafik_1...`, `grafik_2...`, `grafik_3...`) ke dalam folder `Image` tersebut.
3.  Lakukan `git add`, `git commit`, dan `git push` agar folder `Image` dan isinya naik ke GitHub.

```
