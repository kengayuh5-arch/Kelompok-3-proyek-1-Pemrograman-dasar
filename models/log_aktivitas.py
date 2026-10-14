from datetime import datetime


class LogAktivitas:
    def __init__(self, pesan, waktu=None):
        if not pesan or type(pesan) != str:
            raise ValueError("Pesan log tidak boleh kosong!")
        if waktu is not None and type(waktu) != datetime:
            raise ValueError("Waktu harus berupa objek datetime!")
        
        self.pesan = pesan
        if waktu is not None:
            self.waktu = waktu
        else:
            self.waktu = datetime.now()
    
    def getWaktu(self):
        return self.waktu
    
    def getPesan(self):
        return self.pesan
    
    def format(self):
        waktu_str = self.waktu.strftime("%Y-%m-%d %H:%M")
        return f"[{waktu_str}] {self.pesan}"