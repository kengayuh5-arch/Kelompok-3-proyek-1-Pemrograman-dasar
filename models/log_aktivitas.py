from datetime import datetime

class LogAktivitas:
    def __init__(self, pesan, waktu=None):
        if not pesan or type(pesan) != str:
            raise ValueError("Pesan log tidak boleh kosong!")
        
        self.pesan = pesan
        self.waktu = waktu if waktu else datetime.now()
    
    def format(self):
        waktu_str = self.waktu.strftime("%Y-%m-%d %H:%M")
        return f"[{waktu_str}] {self.pesan}"


    def to_string(self):
        waktu_str = self.waktu.strftime("%Y-%m-%d %H:%M")
        return f"{waktu_str}|{self.pesan}"
    
    @staticmethod
    def from_string(data):
        parts = data.split("|", 1)
        if len(parts) == 2:
            waktu_str, pesan = parts
            waktu = datetime.strptime(waktu_str, "%Y-%m-%d %H:%M")
            return LogAktivitas(pesan, waktu)
        return None