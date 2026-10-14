from datetime import date
from models.alat import Alat, KONDISI_VALID


class DetailPeminjaman:
    def __init__(self, alat, jumlah=1):
        if type(alat) != Alat:
            raise ValueError("Alat harus berupa objek Alat!")
        if type(jumlah) != int or jumlah <= 0:
            raise ValueError("Jumlah harus integer > 0!")
        
        self.alat = alat
        self.jumlah = jumlah
        self.sudahKembali = False
        self.tanggalKembali = None
        self.kondisiKembali = None
    
    def getAlat(self):
        return self.alat
    
    def getJumlah(self):
        return self.jumlah
    
    def getTanggalKembali(self):
        return self.tanggalKembali
    
    def getKondisiKembali(self):
        return self.kondisiKembali
    
    def kembalikan(self, tgl, kondisi):
        if self.sudahKembali:
            raise ValueError(
                f"Alat {self.alat.getNama()} sudah dikembalikan sebelumnya!"
            )
        if type(tgl) != date:
            raise ValueError("Tanggal pengembalian harus berupa objek date!")
        if kondisi not in KONDISI_VALID:
            raise ValueError(
                f"Kondisi '{kondisi}' tidak valid. Pilih: {KONDISI_VALID}"
            )
        
        self.sudahKembali = True
        self.tanggalKembali = tgl
        self.kondisiKembali = kondisi
        
        self.alat.kembali(kondisi, self.jumlah)
    
    def isKembali(self):
        return self.sudahKembali
    
    def getDetail(self):
        if self.sudahKembali:
            status = (
                f"Kembali pada {self.tanggalKembali:%d-%m-%Y} "
                f"(kondisi: {self.kondisiKembali})"
            )
        else:
            status = "Belum kembali"
        
        return (
            f"{self.alat.getNama()} x {self.jumlah} "
            f"[{self.alat.getKode()}] - {status}"
        )