class KategoriAlat:
    def __init__(self, id_kategori, nama, deskripsi=""):
        if not id_kategori or type(id_kategori) != str:
            raise ValueError("ID kategori tidak boleh kosong!")
        if not nama or type(nama) != str:
            raise ValueError("Nama kategori tidak boleh kosong!")
        if type(deskripsi) != str:
            raise ValueError("Deskripsi harus berupa string!")
        
        self.id_kategori = id_kategori
        self.nama = nama
        self.deskripsi = deskripsi
    
    def getId(self):
        return self.id_kategori
    
    def getNama(self):
        return self.nama
    
    def getDeskripsi(self):
        return self.deskripsi
    
    def ubahNama(self, nama_baru):
        if not nama_baru or type(nama_baru) != str:
            raise ValueError("Nama kategori tidak boleh kosong!")
        self.nama = nama_baru
    
    def ubahDeskripsi(self, deskripsi_baru):
        if type(deskripsi_baru) != str:
            raise ValueError("Deskripsi harus berupa string!")
        self.deskripsi = deskripsi_baru
    
    def getDetail(self):
        if self.deskripsi:
            return f"[{self.id_kategori}] {self.nama} — {self.deskripsi}"
        return f"[{self.id_kategori}] {self.nama}"