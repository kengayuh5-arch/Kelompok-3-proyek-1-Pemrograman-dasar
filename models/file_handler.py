import os
import shutil
from datetime import datetime

class FileHandler:
    def __init__(self):
        self.folder_data = "data"
        if not os.path.exists(self.folder_data):
            os.makedirs(self.folder_data)
            
        self._pastikan_file_ada()
    
    def _pastikan_file_ada(self):
        files = ["mahasiswa.txt", "kategori.txt", "alat.txt", "transaksi.txt", "detail_transaksi.txt", "log.txt"]
        for file in files:
            path = os.path.join(self.folder_data, file)
            if not os.path.exists(path):
                with open(path, "w") as f:
                    pass


    def muat_mahasiswa(self):
        data = []
        path = os.path.join(self.folder_data, "mahasiswa.txt")
        try:
            with open(path, "r") as file:
                for baris in file:
                    baris = baris.strip()
                    if not baris: continue
                    parts = baris.split("|")
                    if len(parts) == 3:
                        data.append(baris)
        except FileNotFoundError:
            print("Peringatan: File mahasiswa.txt tidak ditemukan. Membuat baru.")
        return data

    def muat_kategori(self):
        data = []
        path = os.path.join(self.folder_data, "kategori.txt")
        try:
            with open(path, "r") as file:
                for baris in file:
                    baris = baris.strip()
                    if not baris: continue
                    parts = baris.split("|")
                    if len(parts) >= 2:
                        data.append(baris)
        except FileNotFoundError:
            print("Peringatan: File kategori.txt tidak ditemukan.")
        return data

    def muat_alat(self):
        data = []
        path = os.path.join(self.folder_data, "alat.txt")
        try:
            with open(path, "r") as file:
                for baris in file:
                    baris = baris.strip()
                    if not baris: continue
                    parts = baris.split("|")
                    if len(parts) == 6:
                        data.append(baris)
        except FileNotFoundError:
            print("Peringatan: File alat.txt tidak ditemukan.")
        return data

    def muat_transaksi(self):
        data = []
        path = os.path.join(self.folder_data, "transaksi.txt")
        try:
            with open(path, "r") as file:
                for baris in file:
                    baris = baris.strip()
                    if not baris: continue
                    parts = baris.split("|")
                    if len(parts) == 5:
                        data.append(baris)
        except FileNotFoundError:
            print("Peringatan: File transaksi.txt tidak ditemukan.")
        return data

    def muat_detail(self):
        data = []
        path = os.path.join(self.folder_data, "detail_transaksi.txt")
        try:
            with open(path, "r") as file:
                for baris in file:
                    baris = baris.strip()
                    if not baris: continue
                    parts = baris.split("|")
                    if len(parts) == 6:
                        data.append(baris)
        except FileNotFoundError:
            print("Peringatan: File detail_transaksi.txt tidak ditemukan.")
        return data

    def muat_log(self):
        data = []
        path = os.path.join(self.folder_data, "log.txt")
        try:
            with open(path, "r") as file:
                for baris in file:
                    baris = baris.strip()
                    if baris:
                        data.append(baris)
        except FileNotFoundError:
            pass
        return data


    def simpan_mahasiswa(self, data):
        path = os.path.join(self.folder_data, "mahasiswa.txt")
        with open(path, "w") as file:
            for baris in data:
                file.write(baris + "\n")

    def simpan_kategori(self, data):
        path = os.path.join(self.folder_data, "kategori.txt")
        with open(path, "w") as file:
            for baris in data:
                file.write(baris + "\n")

    def simpan_alat(self, data):
        path = os.path.join(self.folder_data, "alat.txt")
        with open(path, "w") as file:
            for baris in data:
                file.write(baris + "\n")

    def simpan_transaksi(self, data):
        path = os.path.join(self.folder_data, "transaksi.txt")
        with open(path, "w") as file:
            for baris in data:
                file.write(baris + "\n")

    def simpan_detail(self, data):
        path = os.path.join(self.folder_data, "detail_transaksi.txt")
        with open(path, "w") as file:
            for baris in data:
                file.write(baris + "\n")

    def tulis_log(self, pesan_terformat):
        path = os.path.join(self.folder_data, "log.txt")
        with open(path, "a") as file:
            file.write(pesan_terformat + "\n")


    def backup_data(self):
        folder_backup = "backup"
        if not os.path.exists(folder_backup):
            os.makedirs(folder_backup)
            
        waktu = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nama_folder_backup = os.path.join(folder_backup, f"backup_{waktu}")
        os.makedirs(nama_folder_backup)
        

        files = ["mahasiswa.txt", "kategori.txt", "alat.txt", "transaksi.txt", "detail_transaksi.txt", "log.txt"]
        for file in files:
            sumber = os.path.join(self.folder_data, file)
            tujuan = os.path.join(nama_folder_backup, file)
            if os.path.exists(sumber):
                shutil.copy2(sumber, tujuan)
                
        return f"backup_{waktu}"

    def daftar_backup(self):
        folder_backup = "backup"
        if not os.path.exists(folder_backup):
            return []
        return [f for f in os.listdir(folder_backup) if os.path.isdir(os.path.join(folder_backup, f))]

    def restore_data(self, nama_backup):
        folder_backup = os.path.join("backup", nama_backup)
        if not os.path.exists(folder_backup):
            return False
            
        files = ["mahasiswa.txt", "kategori.txt", "alat.txt", "transaksi.txt", "detail_transaksi.txt", "log.txt"]
        for file in files:
            sumber = os.path.join(folder_backup, file)
            tujuan = os.path.join(self.folder_data, file)
            if os.path.exists(sumber):
                shutil.copy2(sumber, tujuan)
        return True


    def simpan_laporan(self, nama_file, isi_teks):
        folder_laporan = "laporan"
        if not os.path.exists(folder_laporan):
            os.makedirs(folder_laporan)
            
        path = os.path.join(folder_laporan, nama_file)
        with open(path, "w") as file:
            file.write(isi_teks)