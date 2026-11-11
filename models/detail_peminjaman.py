from datetime import date, datetime
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
    
    def getAlat(self): return self.alat
    def getJumlah(self): return self.jumlah
    
    def kembalikan(self, tgl, kondisi):
        if self.sudahKembali:
            raise ValueError(f"Alat {self.alat.getNama()} sudah dikembalikan!")
        if type(tgl) != date:
            raise ValueError("Tanggal harus date!")
        if kondisi not in KONDISI_VALID:
            raise ValueError("Kondisi tidak valid!")
        
        self.sudahKembali = True
        self.tanggalKembali = tgl
        self.kondisiKembali = kondisi
        self.alat.kembali(kondisi, self.jumlah)
    
    def isKembali(self): return self.sudahKembali
    
    def getDetail(self):
        if self.sudahKembali:
            status = f"Kembali {self.tanggalKembali:%d-%m-%Y} (kondisi: {self.kondisiKembali})"
        else:
            status = "Belum kembali"
        return f"{self.alat.getNama()} x {self.jumlah} [{self.alat.getKode()}] - {status}"

    # --- UNTUK FILE I/O ---
    def to_string(self):
        kembali = 1 if self.sudahKembali else 0
        tgl = self.tanggalKembali.strftime("%Y-%m-%d") if self.tanggalKembali else "-"
        kondisi = self.kondisiKembali if self.kondisiKembali else "-"
        return f"{self.alat.getKode()}|{self.jumlah}|{kembali}|{kondisi}|{tgl}"
    
    @staticmethod
    def from_string(data, dict_alat):
        parts = data.split("|")
        if len(parts) == 6: # Harus 6 karena ada ID_TRX
            kode_alat = parts[1]
            jumlah = parts[2]
            kembali = parts[3]
            kondisi = parts[4]
            tgl = parts[5]
            
            if kode_alat in dict_alat:
                detail = DetailPeminjaman(dict_alat[kode_alat], int(jumlah))
                # Terima 1/0
                if kembali == "1":
                    detail.sudahKembali = True
                    detail.kondisiKembali = kondisi if kondisi != "-" else None
                    detail.tanggalKembali = datetime.strptime(tgl, "%Y-%m-%d").date() if tgl != "-" else None
                return detail
        return None