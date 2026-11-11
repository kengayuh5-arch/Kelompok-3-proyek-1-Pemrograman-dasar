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
        
        self.kode = kode
        self.nama = nama
        self.kategori = kategori
        
        self.__stok_baik = 0
        self.__stok_rusak_ringan = 0
        self.__stok_rusak_berat = 0
        
        if kondisi == "baik":
            self.__stok_baik = stok
        elif kondisi == "rusak ringan":
            self.__stok_rusak_ringan = stok
        elif kondisi == "rusak berat":
            self.__stok_rusak_berat = stok
    
    def getKode(self):
        return self.kode
    def getNama(self):
        return self.nama
    def getKategori(self):
        return self.kategori
    def getStokBaik(self):
        return self.__stok_baik
    def getStokRusakRingan(self):
        return self.__stok_rusak_ringan
    def getStokRusakBerat(self):
        return self.__stok_rusak_berat
        
    def isTersedia(self):
        return self.__stok_baik > 0 
    
    def ubahData(self, nama="", kategori=None, tambah_stok=0, perbaikan_ringan=0, perbaikan_berat=0):
        if nama: 
            self.nama = nama
        if kategori is not None: 
            self.kategori = kategori
            
        if perbaikan_ringan > self.__stok_rusak_ringan:
            raise ValueError(f"Gagal! Jumlah perbaikan ({perbaikan_ringan}) melebihi stok rusak ringan ({self.__stok_rusak_ringan}).")
        if perbaikan_berat > self.__stok_rusak_berat:
            raise ValueError(f"Gagal! Jumlah perbaikan ({perbaikan_berat}) melebihi stok rusak berat ({self.__stok_rusak_berat}).")
            
        if tambah_stok > 0:
            self.__stok_baik += tambah_stok
            
        if perbaikan_ringan > 0:
            self.__stok_rusak_ringan -= perbaikan_ringan
            self.__stok_baik += perbaikan_ringan
            
        if perbaikan_berat > 0:
            self.__stok_rusak_berat -= perbaikan_berat
            self.__stok_baik += perbaikan_berat
    
    def pinjam(self, jumlah=1):
        if not self.isTersedia():
            raise ValueError(f"Alat {self.nama} tidak tersedia (Stok Baik habis).")
        if jumlah <= 0:
            raise ValueError("Jumlah pinjam harus > 0!")
        if jumlah > self.__stok_baik:
            raise ValueError(f"Stok baik {self.nama} tidak cukup! Tersedia: {self.__stok_baik}")
        
        self.__stok_baik -= jumlah
    
    def kembali(self, kondisi, jumlah=1):
        if kondisi not in KONDISI_VALID:
            raise ValueError(f"Kondisi '{kondisi}' tidak valid.")
        
        if kondisi == "baik":
            self.__stok_baik += jumlah
        elif kondisi == "rusak ringan":
            self.__stok_rusak_ringan += jumlah
        elif kondisi == "rusak berat":
            self.__stok_rusak_berat += jumlah
    
    def getDetail(self):
        status = "Tersedia" if self.isTersedia() else "Tidak Tersedia"
        return (
            f"[{self.kode}] {self.nama} | Kategori: {self.kategori.getNama()} | "
            f"Baik: {self.__stok_baik} | R.Ringan: {self.__stok_rusak_ringan} | R.Berat: {self.__stok_rusak_berat} | {status}"
        )


    def to_string(self):
        return f"{self.kode}|{self.nama}|{self.kategori.getId()}|{self.__stok_baik}|{self.__stok_rusak_ringan}|{self.__stok_rusak_berat}"
    
    @staticmethod
    def from_string(data, dict_kategori):
        parts = data.split("|")
        if len(parts) == 6:
            kode, nama, id_ktg = parts[0], parts[1], parts[2]
            if id_ktg in dict_kategori:
                kategori = dict_kategori[id_ktg]
                alat = Alat(kode, nama, kategori, stok=0)
                alat._Alat__stok_baik = int(parts[3])
                alat._Alat__stok_rusak_ringan = int(parts[4])
                alat._Alat__stok_rusak_berat = int(parts[5])
                return alat
        return None