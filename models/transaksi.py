from datetime import date, timedelta, datetime
from models.mahasiswa import Mahasiswa, MAKS_TRANSAKSI_AKTIF
from models.detail_peminjaman import DetailPeminjaman

MAKS_HARI = 7
STATUS_DIPINJAM = "dipinjam"
STATUS_SELESAI = "selesai"

class Transaksi:
    def __init__(self, id_transaksi, mahasiswa, tanggal_pinjam=None):
        if not id_transaksi or type(id_transaksi) != str:
            raise ValueError("ID transaksi tidak boleh kosong!")
        if type(mahasiswa) != Mahasiswa:
            raise ValueError("Mahasiswa harus objek Mahasiswa!")
        
        self.id_transaksi = id_transaksi
        self.mahasiswa = mahasiswa
        self.daftar_detail = []
        
        if tanggal_pinjam is None:
            self.tanggal_pinjam = date.today()
        else:
            self.tanggal_pinjam = tanggal_pinjam
            
        self.batas_kembali = self.tanggal_pinjam + timedelta(days=MAKS_HARI)
        self.status = STATUS_DIPINJAM
        
        mahasiswa.tambahTransaksi(self)
    
    def getIdTransaksi(self): return self.id_transaksi
    def getMahasiswa(self): return self.mahasiswa
    def getTanggalPinjam(self): return self.tanggal_pinjam
    def getBatasKembali(self): return self.batas_kembali
    def getStatus(self): return self.status
    def getDaftarDetail(self): return self.daftar_detail
    
    def tambahDetail(self, alat, jumlah=1):
        detail = DetailPeminjaman(alat, jumlah)
        alat.pinjam(jumlah)
        self.daftar_detail.append(detail)
    
    def kembalikanAlat(self, kode_alat, kondisi, tgl_kembali=None):
        if tgl_kembali is None: tgl_kembali = date.today()
        
        for detail in self.daftar_detail:
            if detail.getAlat().getKode() == kode_alat and not detail.isKembali():
                detail.kembalikan(tgl_kembali, kondisi)
                self.perbaruiStatus()
                return
        raise ValueError(f"Alat {kode_alat} tidak ditemukan/sudah kembali.")
    
    def perbaruiStatus(self):
        if self.cekSemuaKembali():
            self.status = STATUS_SELESAI
        else:
            self.status = STATUS_DIPINJAM
    
    def cekSemuaKembali(self):
        if not self.daftar_detail: return False
        return all(d.isKembali() for d in self.daftar_detail)
    
    def detailBelumKembali(self):
        return [d for d in self.daftar_detail if not d.isKembali()]
    
    def isAktif(self): return self.status != STATUS_SELESAI
    
    def getDetail(self):
        baris = [f"Transaksi {self.id_transaksi}",
                 f"  Peminjam : {self.mahasiswa.getNama()} ({self.mahasiswa.getNim()})",
                 f"  Tanggal  : {self.tanggal_pinjam:%d-%m-%Y}",
                 f"  Batas    : {self.batas_kembali:%d-%m-%Y}",
                 f"  Status   : {self.status}",
                 f"  Alat     :"]
        if not self.daftar_detail:
            baris.append("    (Belum ada alat)")
        else:
            for d in self.daftar_detail:
                baris.append(f"    - {d.getDetail()}")
        return "\n".join(baris)

    def to_string(self):
        tgl_pinjam = self.tanggal_pinjam.strftime("%Y-%m-%d")
        tgl_batas = self.batas_kembali.strftime("%Y-%m-%d")
        return f"{self.id_transaksi}|{self.mahasiswa.getNim()}|{tgl_pinjam}|{tgl_batas}|{self.status}"
    
    @staticmethod
    def from_string(data, dict_mahasiswa):
        parts = data.split("|")
        if len(parts) == 5:
            id_trx, nim, tgl_pinjam, tgl_batas, status = parts
            if nim in dict_mahasiswa:
                tanggal = datetime.strptime(tgl_pinjam, "%Y-%m-%d").date()
                trx = Transaksi(id_trx, dict_mahasiswa[nim], tanggal)
                trx.batas_kembali = datetime.strptime(tgl_batas, "%Y-%m-%d").date()
                trx.status = status
                return trx
        return None