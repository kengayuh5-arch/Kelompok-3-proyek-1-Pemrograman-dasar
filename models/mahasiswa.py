MAKS_TRANSAKSI_AKTIF = 2


class Mahasiswa:
    def __init__(self, nim, nama, no_hp):
        if not nim or type(nim) != str:
            raise ValueError("NIM tidak boleh kosong!")
        if not nama or type(nama) != str:
            raise ValueError("Nama tidak boleh kosong!")
        if not no_hp or type(no_hp) != str:
            raise ValueError("Nomor HP tidak boleh kosong!")
        
        self.nim = nim
        self.nama = nama
        self.no_hp = no_hp
        self.daftar_transaksi = []
    
    def getNim(self):
        return self.nim
    
    def getNama(self):
        return self.nama
    
    def getNoHp(self):
        return self.no_hp
    
    def getDaftarTransaksi(self):
        return self.daftar_transaksi
    
    def ubahData(self, nama="", no_hp=""):
        if nama:
            if type(nama) != str:
                raise ValueError("Nama tidak boleh kosong!")
            self.nama = nama
        
        if no_hp:
            if type(no_hp) != str:
                raise ValueError("Nomor HP tidak boleh kosong!")
            self.no_hp = no_hp
    
    def tambahTransaksi(self, transaksi):
        self.daftar_transaksi.append(transaksi)
    
    def jumlahTransaksiAktif(self):
        aktif = 0
        for t in self.daftar_transaksi:
            if t.status != "selesai":
                aktif = aktif + 1
        return aktif
    
    def bisaPinjamLagi(self):
        return self.jumlahTransaksiAktif() < MAKS_TRANSAKSI_AKTIF
    
    def punyaTransaksiAktif(self):
        return self.jumlahTransaksiAktif() > 0
    
    def getDetail(self):
        return (
            f"[{self.nim}] {self.nama} | "
            f"HP: {self.no_hp} | "
            f"Transaksi aktif: {self.jumlahTransaksiAktif()}/{MAKS_TRANSAKSI_AKTIF}"
        )