from datetime import date, timedelta
from models.mahasiswa import Mahasiswa, MAKS_TRANSAKSI_AKTIF
from models.detail_peminjaman import DetailPeminjaman

MAKS_HARI = 7
STATUS_DIPINJAM = "dipinjam"
STATUS_SEBAGIAN = "sebagian dikembalikan"
STATUS_SELESAI = "selesai"


class Transaksi:
    def __init__(self, id_transaksi, mahasiswa, tanggal_pinjam=None):
        if not id_transaksi or type(id_transaksi) != str:
            raise ValueError("ID transaksi tidak boleh kosong!")
        if type(mahasiswa) != Mahasiswa:
            raise ValueError("Mahasiswa harus berupa objek Mahasiswa!")
        if tanggal_pinjam is not None and type(tanggal_pinjam) != date:
            raise ValueError("Tanggal pinjam harus berupa objek date!")
        
        if not mahasiswa.bisaPinjamLagi():
            raise ValueError(
                f"Mahasiswa {mahasiswa.getNama()} sudah punya "
                f"{MAKS_TRANSAKSI_AKTIF} transaksi aktif!"
            )
        
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
    
    def getIdTransaksi(self):
        return self.id_transaksi
    
    def getMahasiswa(self):
        return self.mahasiswa
    
    def getTanggalPinjam(self):
        return self.tanggal_pinjam
    
    def getBatasKembali(self):
        return self.batas_kembali
    
    def getStatus(self):
        return self.status
    
    def getDaftarDetail(self):
        return self.daftar_detail
    
    def tambahDetail(self, alat, jumlah=1):
        detail = DetailPeminjaman(alat, jumlah)
        alat.pinjam(jumlah)
        self.daftar_detail.append(detail)
    
    def kembalikanAlat(self, kode_alat, kondisi, tgl_kembali=None):
        if tgl_kembali is None:
            tgl_kembali = date.today()
        
        for detail in self.daftar_detail:
            if detail.getAlat().getKode() == kode_alat and not detail.isKembali():
                detail.kembalikan(tgl_kembali, kondisi)
                self.perbaruiStatus()
                return
        
        raise ValueError(
            f"Alat dengan kode {kode_alat} tidak ditemukan "
            f"di transaksi ini (atau sudah dikembalikan)."
        )
    
    def perbaruiStatus(self):
        if self.cekSemuaKembali():
            self.status = STATUS_SELESAI
        else:
            jumlah_kembali = 0
            for d in self.daftar_detail:
                if d.isKembali():
                    jumlah_kembali = jumlah_kembali + 1
            
            if jumlah_kembali > 0:
                self.status = STATUS_SEBAGIAN
            else:
                self.status = STATUS_DIPINJAM
    
    def cekSemuaKembali(self):
        if len(self.daftar_detail) == 0:
            return False
        
        for detail in self.daftar_detail:
            if not detail.isKembali():
                return False
        return True
    
    def detailBelumKembali(self):
        belum = []
        for detail in self.daftar_detail:
            if not detail.isKembali():
                belum.append(detail)
        return belum
    
    def isAktif(self):
        return self.status != STATUS_SELESAI
    
    def hitungHariTerlambat(self, tgl_kembali=None):
        if tgl_kembali is None:
            tgl_kembali = date.today()
        
        selisih = (tgl_kembali - self.batas_kembali).days
        if selisih > 0:
            return selisih
        return 0
    
    def validasiLama(self, tgl_kembali=None):
        return self.hitungHariTerlambat(tgl_kembali) > 0
    
    def getDetail(self):
        baris = []
        baris.append(f"Transaksi {self.id_transaksi}")
        baris.append(f"  Peminjam : {self.mahasiswa.getNama()} ({self.mahasiswa.getNim()})")
        baris.append(f"  Tanggal  : {self.tanggal_pinjam:%d-%m-%Y}")
        baris.append(f"  Batas    : {self.batas_kembali:%d-%m-%Y}")
        baris.append(f"  Status   : {self.status}")
        baris.append(f"  Alat     :")
        
        if len(self.daftar_detail) == 0:
            baris.append("    (Belum ada alat)")
        else:
            for d in self.daftar_detail:
                baris.append(f"    - {d.getDetail()}")
        
        return "\n".join(baris)