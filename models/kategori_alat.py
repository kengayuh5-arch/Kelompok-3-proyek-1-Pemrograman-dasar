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
    
    def getDetail(self):
        if self.deskripsi:
            return f"[{self.id_kategori}] {self.nama} — {self.deskripsi}"
        return f"[{self.id_kategori}] {self.nama}"

    def to_string(self):
        return f"{self.id_kategori}|{self.nama}|{self.deskripsi}"

    
    @staticmethod
    def from_string(data):
        parts = data.split("|")
        if len(parts) >= 2:
            deskripsi = parts[2] if len(parts) > 2 else ""
            return KategoriAlat(parts[0], parts[1], deskripsi)
        return None