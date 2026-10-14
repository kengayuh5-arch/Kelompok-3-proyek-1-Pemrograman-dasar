from models.mahasiswa import Mahasiswa, MAKS_TRANSAKSI_AKTIF
from models.alat import Alat
from models.kategori_alat import KategoriAlat
from models.transaksi import Transaksi
from models.log_aktivitas import LogAktivitas


class SistemLab:
    def __init__(self):
        self.mahasiswa = {}
        self.alat = {}
        self.kategori = {}
        self.transaksi = {}
        self.log = []
        self.counter_transaksi = 0

    
    def catatLog(self, pesan):
        log_baru = LogAktivitas(pesan)
        self.log.append(log_baru)
    
    def tambahMahasiswa(self, nim, nama, no_hp):
        if nim in self.mahasiswa:
            raise ValueError(f"Mohon maaf mahasiswa dengan NIM {nim} sudah terdaftar")
        mhs = Mahasiswa(nim, nama, no_hp)
        self.mahasiswa[nim] = mhs
        self.catatLog(f"Mahasiswa {nim} ({nama}) ditambahkan")
        return mhs
    
    def editMahasiswa(self, nim, nama="", no_hp=""):
        if nim not in self.mahasiswa:
            raise ValueError(f"Mohon maaf mahasiswa  dengan NIM {nim} tidak ditemukan")
        self.mahasiswa[nim].ubahData(nama, no_hp)
        self.catatLog(f"Data mahasiswa {nim} diperbarui")
    
    def hapusMahasiswa(self, nim):
        if nim not in self.mahasiswa:
            raise ValueError(f"Mohon maaf mahasiswa dengan NIM {nim} tidak ditemukan")
        mhs = self.mahasiswa[nim]
        if mhs.punyaTransaksiAktif():
            raise ValueError(
                f"Mahasiswa {mhs.getNama()} masih punya "
                f"{mhs.jumlahTransaksiAktif()} transaksi aktif!"
            )
        del self.mahasiswa[nim]
        self.catatLog(f"Mahasiswa {nim} ({mhs.getNama()}) dihapus")
    
    def cariMahasiswa(self, keyword):
        hasil = []
        keyword_lower = keyword.lower()
        for mhs in self.mahasiswa.values():
            if (keyword_lower in mhs.getNim().lower() or
                keyword_lower in mhs.getNama().lower()):
                hasil.append(mhs)
        return hasil
    
    def getMahasiswa(self, nim):
        if nim not in self.mahasiswa:
            raise ValueError(f"Mohon maaf mahasiswa dengan NIM {nim} tidak ditemukan")
        return self.mahasiswa[nim]
    

    def tambahKategori(self, id_kategori, nama, deskripsi=""):
        if id_kategori in self.kategori:
            raise ValueError(f"Kategori {id_kategori} sudah ada!")
        ktg = KategoriAlat(id_kategori, nama, deskripsi)
        self.kategori[id_kategori] = ktg
        self.catatLog(f"Kategori {id_kategori} ({nama}) ditambahkan")
        return ktg
    
    def getKategori(self, id_kategori):
        if id_kategori not in self.kategori:
            raise ValueError(f"Kategori {id_kategori} tidak ditemukan!")
        return self.kategori[id_kategori]

    
    def tambahAlat(self, kode, nama, id_kategori, stok=1, kondisi="baik"):
        if kode in self.alat:
            raise ValueError(f"Alat dengan kode {kode} sudah ada!")
        if id_kategori not in self.kategori:
            raise ValueError(f"Kategori {id_kategori} tidak ditemukan!")
        ktg = self.kategori[id_kategori]
        alat = Alat(kode, nama, ktg, stok, kondisi)
        self.alat[kode] = alat
        self.catatLog(f"Alat {kode} ({nama}) ditambahkan")
        return alat
    
    def editAlat(self, kode, nama="", id_kategori=None):
        if kode not in self.alat:
            raise ValueError(f"Alat dengan kode {kode} tidak ditemukan")
        ktg = None
        if id_kategori is not None:
            if id_kategori not in self.kategori:
                raise ValueError(f"Kategori {id_kategori} tidak ditemukan")
            ktg = self.kategori[id_kategori]
        self.alat[kode].ubahData(nama, ktg)
        self.catatLog(f"Data alat {kode} diperbarui")
    
    def hapusAlat(self, kode):
        if kode not in self.alat:
            raise ValueError(f"Alat dengan kode {kode} tidak ditemukan")
        if self.alatDipakaiTrxAktif(kode):
            raise ValueError(f"Alat {kode} masih tercatat di transaksi aktif")
        nama = self.alat[kode].getNama()
        del self.alat[kode]
        self.catatLog(f"Alat {kode} ({nama}) dihapus")
    
    def cariAlat(self, keyword):
        hasil = []
        keyword_lower = keyword.lower()
        for alat in self.alat.values():
            if (keyword_lower in alat.getKode().lower() or
                keyword_lower in alat.getNama().lower() or
                keyword_lower in alat.getKategori().getNama().lower()):
                hasil.append(alat)
        return hasil
    
    def getAlat(self, kode):
        if kode not in self.alat:
            raise ValueError(f"Alat dengan kode {kode} tidak ditemukan")
        return self.alat[kode]
    
    def alatDipakaiTrxAktif(self, kode):
        for trx in self.transaksi.values():
            if not trx.isAktif():
                continue
            for detail in trx.getDaftarDetail():
                if detail.getAlat().getKode() == kode and not detail.isKembali():
                    return True
        return False
    

    def buatTransaksi(self, nim, daftar_item):
        if nim not in self.mahasiswa:
            raise ValueError(f"Mahasiswa dengan NIM {nim} tidak ditemukan")
        mhs = self.mahasiswa[nim]
        
        if not mhs.bisaPinjamLagi():
            raise ValueError(
                f"Mahasiswa {mhs.getNama()} sudah punya "
                f"{MAKS_TRANSAKSI_AKTIF} transaksi aktif"
            )
        
        if not daftar_item or len(daftar_item) == 0:
            raise ValueError("Transaksi harus punya minimal 1 alat")
        
        for kode, jumlah in daftar_item:
            if kode not in self.alat:
                raise ValueError(f"Alat dengan kode {kode} tidak ditemukan!")
            alat = self.alat[kode]
            if not alat.isTersedia():
                raise ValueError(
                    f"Alat {alat.getNama()} tidak tersedia "
                    f"(kondisi: {alat.getKondisi()}, stok: {alat.getStok()})"
                )
            if type(jumlah) != int or jumlah <= 0:
                raise ValueError(f"Jumlah untuk {kode} harus integer > 0")
            if jumlah > alat.getStok():
                raise ValueError(
                    f"Stok {alat.getNama()} tidak cukup "
                    f"Tersedia: {alat.getStok()}, diminta: {jumlah}"
                )
        
        self.counter_transaksi = self.counter_transaksi + 1
        
   
        angka_str = str(self.counter_transaksi)
        while len(angka_str) < 3:
            angka_str = "0" + angka_str
        id_trx = "TRX" + angka_str
        
        trx = Transaksi(id_trx, mhs)
        
        for kode, jumlah in daftar_item:
            trx.tambahDetail(self.alat[kode], jumlah)
        
        self.transaksi[id_trx] = trx
        
        ringkasan = ", ".join([f"{kode} x {jml}" for kode, jml in daftar_item])
        self.catatLog(f"Transaksi {id_trx} dibuat oleh {mhs.getNama()}: {ringkasan}")
        
        return trx
    
    def prosesPengembalian(self, id_trx, kode_alat, kondisi):
        if id_trx not in self.transaksi:
            raise ValueError(f"Transaksi {id_trx} tidak ditemukan")
        trx = self.transaksi[id_trx]
        if not trx.isAktif():
            raise ValueError(f"Transaksi {id_trx} sudah selesai")
        trx.kembalikanAlat(kode_alat, kondisi)
        self.catatLog(
            f"{trx.getMahasiswa().getNama()} mengembalikan {kode_alat} "
            f"(kondisi: {kondisi}) di transaksi {id_trx}"
        )
    
    def getTransaksi(self, id_trx):
        if id_trx not in self.transaksi:
            raise ValueError(f"Transaksi {id_trx} tidak ditemukan")
        return self.transaksi[id_trx]
    
    def cariTransaksiByMahasiswa(self, nim):
        if nim not in self.mahasiswa:
            raise ValueError(f"Mahasiswa dengan NIM {nim} tidak ditemukan")
        hasil = []
        for trx in self.transaksi.values():
            if trx.getMahasiswa().getNim() == nim:
                hasil.append(trx)
        return hasil
    
    def trxAktifMahasiswa(self, nim):
        if nim not in self.mahasiswa:
            raise ValueError(f"Mahasiswa dengan NIM {nim} tidak ditemukan")
        hasil = []
        for trx in self.transaksi.values():
            if trx.getMahasiswa().getNim() == nim and trx.isAktif():
                hasil.append(trx)
        return hasil


    def getAlatTersedia(self):
        hasil = []
        for alat in self.alat.values():
            if alat.isTersedia():
                hasil.append(alat)
        return hasil
    
    def getAlatDipinjam(self):
        hasil = []
        for alat in self.alat.values():
            if not alat.isTersedia() and alat.getKondisi() == "baik":
                hasil.append(alat)
        return hasil
    
    def getAlatRusak(self):
        hasil = []
        for alat in self.alat.values():
            if alat.getKondisi() in ["rusak ringan", "rusak berat"]:
                hasil.append(alat)
        return hasil
    