# Kelompok-3-proyek-1-Pemrograman-dasar
Sistem Pengelolaan Peminjaman Peralatan Laboratorium


## Anggota Kelompok
| Nama                       | NIM      | Akun GitHub      |
|----------------------------|----------|------------------|
| Bintang Fajar Khoiru Rizal | K3525001 | BitangFajar-blip |
| Ken Gayuh Nusa Islami      | K3525031 | kengayuh5-arch   |
| Afrizal Affandi Ahmad      | K3525046 | afrizal-aff      |

## Deskripsi Sistem
Aplikasi CLI berbasis Python (OOP, tanpa database) untuk mengelola peminjaman
peralatan laboratorium oleh mahasiswa. Data disimpan selama program berjalan
menggunakan `dict` dan `list`.

## Struktur Program
```
sistem_peminjaman_lab/
├── main.py
├── README.md
├── models/      # mahasiswa, kategori_alat, alat, detail_peminjaman, transaksi, log_aktivitas
├── services/    # sistem_lab.py (manager + aturan bisnis)
├── reports/     # laporan.py
└── ui/          # menu_app.py (CLI)
```

## Pembagian Kontribusi
| Anggota                    | Kontribusi                                                |
|----------------------------|-----------------------------------------------------------|
| Bintang Fajar Khoiru Rizal | detail_peminjaman.py, transaksi.py, sistem_lab.py         |
| Afrizal Affandi Ahmad      | alat.py, kategori_alat.py, mahasiswa.py, log_aktivitas.py |
| Ken Gayuh Nusa Islami      | laporan.py, menu_app.py, main.py, README.md               |

