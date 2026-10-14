from models.kategori_alat import KategoriAlat

KONDISI_VALID = ["baik", "rusak ringan", "rusak berat"]


class Alat:
    def __init__(self, kode, nama, kategori, stok=1, kondisi="baik"):
        if not kode or type(kode) != str:
            raise ValueError("Kode alat tidak boleh kosong!")
        if not nama or type(nama) != str:
            raise ValueError("Nama alat tidak boleh kosong!")
        if type(kategori) != KategoriAlat:
            raise ValueError("Kategori harus berupa objek KategoriAlat!")
        if type(stok) != int or stok < 0:
            raise ValueError("Stok harus integer >= 0!")
        if kondisi not in KONDISI_VALID:
            raise ValueError(f"Kondisi '{kondisi}' tidak valid. Pilih: {KONDISI_VALID}")
        
        self.kode = kode
        self.nama = nama
        self.kategori = kategori
        self.__stok = stok
        self.__kondisi = kondisi
    
    def getKode(self):
        return self.kode
    
    def getNama(self):
        return self.nama
    
    def getKategori(self):
        return self.kategori
    
    def getStok(self):
        return self.__stok
    
    def getKondisi(self):
        return self.__kondisi
    
    def isTersedia(self):
        return self.__kondisi == "baik" and self.__stok > 0
    
    def ubahData(self, nama="", kategori=None):
        if nama:
            if not nama:
                raise ValueError("Nama alat tidak boleh kosong!")
            self.nama = nama
        
        if kategori is not None:
            if type(kategori) != KategoriAlat:
                raise ValueError("Kategori harus berupa objek KategoriAlat!")
            self.kategori = kategori
    
    def pinjam(self, jumlah=1):
        if not self.isTersedia():
            raise ValueError(
                f"Alat {self.nama} tidak tersedia. "
                f"Kondisi: {self.__kondisi}, Stok: {self.__stok}"
            )
        if jumlah <= 0:
            raise ValueError("Jumlah pinjam harus lebih dari 0!")
        if jumlah > self.__stok:
            raise ValueError(
                f"Stok {self.nama} tidak cukup! "
                f"Tersedia: {self.__stok}, diminta: {jumlah}"
            )
        self.__stok = self.__stok - jumlah
    
    def kembali(self, kondisi, jumlah=1):
        if kondisi not in KONDISI_VALID:
            raise ValueError(f"Kondisi '{kondisi}' tidak valid. Pilih: {KONDISI_VALID}")
        
        self.__kondisi = kondisi
        
        if kondisi == "baik":
            self.__stok = self.__stok + jumlah
    
    def masukPemeliharaan(self):
        if self.__kondisi != "rusak berat":
            raise ValueError(
                f"Hanya alat rusak berat yang bisa masuk pemeliharaan. "
                f"Kondisi saat ini: {self.__kondisi}"
            )
    
    def selesaiPerbaikan(self):
        self.__kondisi = "baik"
        if self.__stok == 0:
            self.__stok = 1
    
    def getDetail(self):
        status = "Tersedia" if self.isTersedia() else "Tidak Tersedia"
        return (
            f"[{self.kode}] {self.nama} | "
            f"Kategori: {self.kategori.getNama()} | "
            f"Kondisi: {self.__kondisi} | "
            f"Stok: {self.__stok} | "
            f"{status}"
        )