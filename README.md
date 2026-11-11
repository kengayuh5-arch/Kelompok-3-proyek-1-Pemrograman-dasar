# Sistem Pengelolaan Peminjaman Peralatan Laboratorium
**Proyek II — Praktikum Pemrograman Dasar**

## Anggota Kelompok
| Nama | NIM | Akun GitHub |
| :--- | :--- | :--- |
| Bintang Fajar Khoiru Rizal | K3525001 | BitangFajar-blip |
| Ken Gayuh Nusa Islami | K3525031 | kengayuh5-arch |
| Afrizal Affandi Ahmad | K3525046 | afrizal-aff |

## Deskripsi Sistem
Aplikasi berbasis Command Line Interface (CLI) dengan paradigma Object-Oriented Programming (OOP) untuk mengelola peminjaman peralatan laboratorium. 

Pada Proyek 2 ini, sistem telah di-*upgrade* dari penyimpanan sementara (in-memory) menjadi **penyimpanan permanen berbasis text file (`.txt`)**. Aplikasi tidak menggunakan database (MySQL, SQLite, dll) maupun *library* penyimpanan siap pakai (JSON, CSV, pickle, shelve). Seluruh proses baca/tulis file dikelola secara manual menggunakan fungsi `open()`, `split('|')`, dan `join()` di dalam class `FileHandler`.

## Struktur Program
```text
Kelompok-3-proyek-2/
├── main.py                  # Entry point program
├── README.md                # Dokumentasi proyek
├── models/                  # Class model data & FileHandler
│   ├── mahasiswa.py
│   ├── kategori_alat.py
│   ├── alat.py
│   ├── transaksi.py
│   ├── detail_peminjaman.py
│   ├── log_aktivitas.py
│   └── file_handler.py      # Class khusus I/O File
├── services/                # Logika bisnis utama
│   └── sistem_lab.py
├── reports/                 # Pembuatan laporan
│   └── laporan.py
├── ui/                      # Antarmuka pengguna
│   └── menu_app.py
├── data/                    # Folder penyimpanan data permanen
│   ├── mahasiswa.txt
│   ├── kategori.txt
│   ├── alat.txt
│   ├── transaksi.txt
│   ├── detail_transaksi.txt
│   └── log.txt
├── backup/                  # Folder hasil backup data
└── laporan/                 # Folder hasil ekspor laporan
```

## Format Text File
Sistem menggunakan tanda pipa (`|`) sebagai pemisah antar kolom (tanpa spasi). Setiap baris mewakili satu data.

- `mahasiswa.txt` : `NIM|Nama|No_HP`
- `kategori.txt` : `ID_Kategori|Nama_Kategori|Deskripsi`
- `alat.txt` : `Kode|Nama|ID_Kategori|Stok_Baik|Stok_Rusak_Ringan|Stok_Rusak_Berat`
- `transaksi.txt` : `ID_Transaksi|NIM|Tgl_Pinjam|Batas_Kembali|Status`
- `detail_transaksi.txt` : `ID_Transaksi|Kode_Alat|Jumlah|Sudah_Kembali|Kondisi|Tgl_Kembali`
- `log.txt` : `Waktu|Pesan_Aktivitas`


## Cara Menjalankan Aplikasi
1. Buka terminal dan pastikan berada di direktori utama proyek (folder yang sama dengan `main.py`).
2. Jalankan perintah:
   ```bash
   python main.py
   ```
3. Jika file `.txt` belum ada, sistem akan otomatis membuatnya.
4. Data akan tersimpan secara otomatis (*real-time save*) setiap kali ada operasi CRUD, transaksi, atau pengembalian.

## Pembagian Kontribusi
| Anggota | Kontribusi Utama |
| :--- | :--- |
| **Bintang Fajar Khoiru Rizal** | sistem_lab.py, transaksi.py, detail_peminjaman.py, folder data, folder backup |
| **Afrizal Affandi Ahmad** | alat.py, kategori_alat.py, mahasiswa.py, log_aktivitas.py, folder laporan |
| **Ken Gayuh Nusa Islami** | menu_app.py, laporan.py, main.py, README.md, file_handler.py |
```