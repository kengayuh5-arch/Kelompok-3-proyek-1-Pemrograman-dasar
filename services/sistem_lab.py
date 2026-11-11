from models.mahasiswa import Mahasiswa, MAKS_TRANSAKSI_AKTIF
from models.alat import Alat
from models.kategori_alat import KategoriAlat
from models.transaksi import Transaksi
from models.detail_peminjaman import DetailPeminjaman
from models.log_aktivitas import LogAktivitas
from models.file_handler import FileHandler


class SistemLab:
    def __init__(self):
        self.mahasiswa = {}
        self.alat = {}
        self.kategori = {}
        self.transaksi = {}
        self.log = []
        self.counter_transaksi = 0
        
        # Inisialisasi FileHandler
        self.file_handler = FileHandler()
    
    # ==========================================
    # FUNGSI LOAD & SAVE (FILE I/O)
    # ==========================================
    def muat_data_awal(self):
        
        # 1. Muat Kategori
        for data in self.file_handler.muat_kategori():
            ktg = KategoriAlat.from_string(data)
            if ktg:
                self.kategori[ktg.getId()] = ktg
                
        # 2. Muat Mahasiswa
        for data in self.file_handler.muat_mahasiswa():
            mhs = Mahasiswa.from_string(data)
            if mhs:
                self.mahasiswa[mhs.getNim()] = mhs
                
        # 3. Muat Alat (Butuh referensi Kategori)
        for data in self.file_handler.muat_alat():
            alt = Alat.from_string(data, self.kategori)
            if alt:
                self.alat[alt.getKode()] = alt
                
        # 4. Muat Transaksi (Butuh referensi Mahasiswa)
        for data in self.file_handler.muat_transaksi():
            trx = Transaksi.from_string(data, self.mahasiswa)
            if trx:
                self.transaksi[trx.getIdTransaksi()] = trx
                # Simpan counter tertinggi agar ID selanjutnya tidak bentrok
                angka_id = int(trx.getIdTransaksi().replace("TRX", ""))
                if angka_id > self.counter_transaksi:
                    self.counter_transaksi = angka_id

        # 5. Muat Detail Transaksi (Butuh referensi Alat dan Transaksi)
        for data in self.file_handler.muat_detail():
            # Ambil ID Transaksi dari data string (elemen pertama)
            id_trx = data.split("|")[0]
            if id_trx in self.transaksi:
                detail = DetailPeminjaman.from_string(data, self.alat)
                if detail:
                    self.transaksi[id_trx].daftar_detail.append(detail)
                    
        # 6. Muat Log
        for data in self.file_handler.muat_log():
            log = LogAktivitas.from_string(data)
            if log:
                self.log.append(log)
        # (Log dibaca dari file, meskipun di aplikasi kita hanya menampilkan 20 terakhir)
        # Karena format log di file sedikit beda, kita abaikan load log ke memori 
        # untuk mencegah error parsing, karena log lama sudah ada di txt.

    def simpan_semua_data(self):
        """Menyimpan seluruh state memori ke file txt (biasanya dipanggil saat exit)"""
        # 1. Simpan Kategori
        list_ktg = [k.to_string() for k in self.kategori.values()]
        self.file_handler.simpan_kategori(list_ktg)
        
        # 2. Simpan Mahasiswa
        list_mhs = [m.to_string() for m in self.mahasiswa.values()]
        self.file_handler.simpan_mahasiswa(list_mhs)
        
        # 3. Simpan Alat
        list_alat = [a.to_string() for a in self.alat.values()]
        self.file_handler.simpan_alat(list_alat)
        
        # 4. Simpan Transaksi
        list_trx = [t.to_string() for t in self.transaksi.values()]
        self.file_handler.simpan_transaksi(list_trx)
        
        # 5. Simpan Detail Transaksi
        list_detail = []
        for trx in self.transaksi.values():
            for detail in trx.getDaftarDetail():
                # Format: IDTransaksi|KodeAlat|Jumlah|SudahKembali|Kondisi|Tgl
                str_detail = detail.to_string()
                list_detail.append(f"{trx.getIdTransaksi()}|{str_detail}")
        self.file_handler.simpan_detail(list_detail)

    # ==========================================
    # HELPER / UTILITY
    # ==========================================
    def catatLog(self, pesan):
        log_baru = LogAktivitas(pesan)
        self.log.append(log_baru)
        # Simpan log langsung ke file txt (mode append)
        self.file_handler.tulis_log(log_baru.to_string())

    def generateIdTransaksi(self):
        """Membuat ID Transaksi baru (TRX001, TRX002, dst)"""
        self.counter_transaksi += 1
        angka_str = str(self.counter_transaksi)
        while len(angka_str) < 3:
            angka_str = "0" + angka_str
        return "TRX" + angka_str

    def hitungTransaksiAktif(self, nim):
        """Menghitung jumlah transaksi aktif milik mahasiswa"""
        if nim not in self.mahasiswa:
            return 0
        return self.mahasiswa[nim].jumlahTransaksiAktif()

    def validasiBatasTransaksi(self, nim):
        """Cek apakah mahasiswa masih boleh meminjam (Aturan 2)"""
        if nim not in self.mahasiswa:
            raise ValueError(f"Mahasiswa {nim} tidak ditemukan!")
        if not self.mahasiswa[nim].bisaPinjamLagi():
            raise ValueError(f"Mahasiswa {nim} sudah mencapai batas maksimal {MAKS_TRANSAKSI_AKTIF} transaksi aktif!")
        return True

    # ==========================================
    # CRUD MAHASISWA
    # ==========================================
    def tambahMahasiswa(self, nim, nama, no_hp):
        if nim in self.mahasiswa:
            raise ValueError(f"Mahasiswa dengan NIM {nim} sudah terdaftar")
        mhs = Mahasiswa(nim, nama, no_hp)
        self.mahasiswa[nim] = mhs
        
        self.simpan_semua_data() # Simpan real-time
        self.catatLog(f"Mahasiswa {nim} ({nama}) ditambahkan")
        return mhs
    
    def editMahasiswa(self, nim, nama="", no_hp=""):
        if nim not in self.mahasiswa:
            raise ValueError(f"Mahasiswa dengan NIM {nim} tidak ditemukan")
        self.mahasiswa[nim].ubahData(nama, no_hp)
        
        self.simpan_semua_data()
        self.catatLog(f"Data mahasiswa {nim} diperbarui")
    
    def hapusMahasiswa(self, nim):
        if nim not in self.mahasiswa:
            raise ValueError(f"Mahasiswa dengan NIM {nim} tidak ditemukan")
        mhs = self.mahasiswa[nim]
        if mhs.punyaTransaksiAktif():
            raise ValueError(f"Mahasiswa {mhs.getNama()} masih punya {mhs.jumlahTransaksiAktif()} transaksi aktif!")
        
        del self.mahasiswa[nim]
        self.simpan_semua_data()
        self.catatLog(f"Mahasiswa {nim} ({mhs.getNama()}) dihapus")

    # ==========================================
    # CRUD KATEGORI & ALAT
    # ==========================================
    def tambahKategori(self, id_kategori, nama, deskripsi=""):
        if id_kategori in self.kategori:
            raise ValueError(f"Kategori {id_kategori} sudah ada!")
        ktg = KategoriAlat(id_kategori, nama, deskripsi)
        self.kategori[id_kategori] = ktg
        
        self.simpan_semua_data()
        self.catatLog(f"Kategori {id_kategori} ({nama}) ditambahkan")
        return ktg
    
    def tambahAlat(self, kode, nama, id_kategori, stok=1):
        if kode in self.alat:
            raise ValueError(f"Alat dengan kode {kode} sudah ada!")
        if id_kategori not in self.kategori:
            raise ValueError(f"Kategori {id_kategori} tidak ditemukan!")
        
        ktg = self.kategori[id_kategori]
        alat = Alat(kode, nama, ktg, stok, "baik")
        self.alat[kode] = alat
        
        self.simpan_semua_data()
        self.catatLog(f"Alat {kode} ({nama}) ditambahkan")
        return alat
    
    def editAlat(self, kode, nama="", id_kategori=None, tambah_stok=0, perbaikan_ringan=0, perbaikan_berat=0):
        if kode not in self.alat:
            raise ValueError(f"Alat dengan kode {kode} tidak ditemukan")
        
        ktg = None
        if id_kategori is not None:
            if id_kategori not in self.kategori:
                raise ValueError(f"Kategori {id_kategori} tidak ditemukan")
            ktg = self.kategori[id_kategori]
            
        self.alat[kode].ubahData(nama, ktg, tambah_stok, perbaikan_ringan, perbaikan_berat)
        
        self.simpan_semua_data()
        self.catatLog(f"Data alat {kode} diperbarui")
    
    def hapusAlat(self, kode):
        if kode not in self.alat:
            raise ValueError(f"Alat dengan kode {kode} tidak ditemukan")
        if self.alatDipakaiTrxAktif(kode):
            raise ValueError(f"Alat {kode} masih tercatat di transaksi aktif")
            
        nama = self.alat[kode].getNama()
        del self.alat[kode]
        
        self.simpan_semua_data()
        self.catatLog(f"Alat {kode} ({nama}) dihapus")

    # ==========================================
    # TRANSAKSI
    # ==========================================
    def buatTransaksi(self, nim, daftar_item):
        if nim not in self.mahasiswa:
            raise ValueError(f"Mahasiswa dengan NIM {nim} tidak ditemukan")
        
        self.validasiBatasTransaksi(nim)
        
        if not daftar_item or len(daftar_item) == 0:
            raise ValueError("Transaksi harus punya minimal 1 alat")
        
        # --- GABUNGKAN KODE ALAT YANG SAMA DULU ---
        item_digabung = {}
        for kode, jumlah in daftar_item:
            if kode in item_digabung:
                item_digabung[kode] += jumlah
            else:
                item_digabung[kode] = jumlah
        
        # Validasi Stok berdasarkan total gabungan
        for kode, total_jumlah in item_digabung.items():
            if kode not in self.alat:
                raise ValueError(f"Alat {kode} tidak ditemukan!")
            alat = self.alat[kode]
            if not alat.isTersedia():
                raise ValueError(f"Alat {alat.getNama()} tidak tersedia (Stok Baik habis).")
            if type(total_jumlah) != int or total_jumlah <= 0:
                raise ValueError(f"Jumlah untuk {kode} harus integer > 0")
            if total_jumlah > alat.getStokBaik():
                raise ValueError(f"Stok {alat.getNama()} tidak cukup! Tersedia: {alat.getStokBaik()}, diminta: {total_jumlah}")
        
        # Generate ID dan buat transaksi
        id_trx = self.generateIdTransaksi()
        mhs = self.mahasiswa[nim]
        trx = Transaksi(id_trx, mhs)
        
        # Masukkan data yang sudah digabung ke dalam transaksi
        for kode, total_jumlah in item_digabung.items():
            trx.tambahDetail(self.alat[kode], total_jumlah)
        
        self.transaksi[id_trx] = trx
        
        self.simpan_semua_data() 
        ringkasan = ", ".join([f"{kode} x {jml}" for kode, jml in item_digabung.items()])
        self.catatLog(f"Transaksi {id_trx} dibuat oleh {mhs.getNama()}: {ringkasan}")
        
        return trx
    
    def prosesPengembalian(self, id_trx, kode_alat, kondisi):
        if id_trx not in self.transaksi:
            raise ValueError(f"Transaksi {id_trx} tidak ditemukan")
        trx = self.transaksi[id_trx]
        if not trx.isAktif():
            raise ValueError(f"Transaksi {id_trx} sudah selesai")
        
        trx.kembalikanAlat(kode_alat, kondisi)
        
        self.simpan_semua_data() # Simpan perubahan detail, status transaksi, dan stok Alat
        self.catatLog(f"{trx.getMahasiswa().getNama()} mengembalikan {kode_alat} (kondisi: {kondisi}) di transaksi {id_trx}")

    # ==========================================
    # GETTER / QUERY (Sama seperti Project 1)
    # ==========================================
    def getMahasiswa(self, nim):
        if nim not in self.mahasiswa:
            raise ValueError(f"Mahasiswa {nim} tidak ditemukan")
        return self.mahasiswa[nim]

    def cariMahasiswa(self, keyword):
        keyword_lower = keyword.lower()
        return [m for m in self.mahasiswa.values() if keyword_lower in m.getNim().lower() or keyword_lower in m.getNama().lower()]

    def getKategori(self, id_kategori):
        if id_kategori not in self.kategori:
            raise ValueError(f"Kategori {id_kategori} tidak ditemukan")
        return self.kategori[id_kategori]

    def getAlat(self, kode):
        if kode not in self.alat:
            raise ValueError(f"Alat {kode} tidak ditemukan")
        return self.alat[kode]

    def cariAlat(self, keyword):
        keyword_lower = keyword.lower()
        return [a for a in self.alat.values() if keyword_lower in a.getKode().lower() or keyword_lower in a.getNama().lower() or keyword_lower in a.getKategori().getNama().lower()]

    def getTransaksi(self, id_trx):
        if id_trx not in self.transaksi:
            raise ValueError(f"Transaksi {id_trx} tidak ditemukan")
        return self.transaksi[id_trx]

    def cariTransaksiByMahasiswa(self, nim):
        if nim not in self.mahasiswa:
            raise ValueError(f"Mahasiswa {nim} tidak ditemukan")
        return [t for t in self.transaksi.values() if t.getMahasiswa().getNim() == nim]

    def alatDipakaiTrxAktif(self, kode):
        for trx in self.transaksi.values():
            if not trx.isAktif(): continue
            for detail in trx.getDaftarDetail():
                if detail.getAlat().getKode() == kode and not detail.isKembali():
                    return True
        return False

    def getAlatTersedia(self):
        return [a for a in self.alat.values() if a.isTersedia()]

    def getAlatDipinjam(self):
        hasil = []
        for alat in self.alat.values():
            for trx in self.transaksi.values():
                if trx.isAktif():
                    for detail in trx.getDaftarDetail():
                        if detail.getAlat().getKode() == alat.getKode() and not detail.isKembali():
                            if alat not in hasil:
                                hasil.append(alat)
        return hasil

    def getAlatRusak(self):
        return [a for a in self.alat.values() if a.getStokRusakRingan() > 0 or a.getStokRusakBerat() > 0]