from services.sistem_lab import SistemLab

class Laporan:
    def __init__(self, sistem):
        if type(sistem) != SistemLab:
            raise ValueError("Sistem harus berupa objek SistemLab")
        self.sistem = sistem
    
    def alatTersedia(self):
        return self.sistem.getAlatTersedia()
    def alatDipinjam(self):
        return self.sistem.getAlatDipinjam()
    def alatRusak(self):
        return self.sistem.getAlatRusak()
    def riwayatMahasiswa(self, nim):
        return self.sistem.cariTransaksiByMahasiswa(nim)
    def cariTransaksiByMahasiswa(self, nim):
        return self.sistem.cariTransaksiByMahasiswa(nim)


    def alatPalingSeringDipinjam(self):
        hitung = {}
        for trx in self.sistem.transaksi.values():
            for detail in trx.getDaftarDetail():
                nama = detail.getAlat().getNama()
                hitung[nama] = hitung.get(nama, 0) + detail.getJumlah()
        return sorted(hitung.items(), key=lambda x: x[1], reverse=True)

    def mahasiswaPalingSeringMeminjam(self):
        hitung = {}
        for trx in self.sistem.transaksi.values():
            nama = trx.getMahasiswa().getNama()
            hitung[nama] = hitung.get(nama, 0) + 1
        return sorted(hitung.items(), key=lambda x: x[1], reverse=True)

    def jumlahTransaksiSelesai(self):
        return sum(1 for trx in self.sistem.transaksi.values() if trx.getStatus() == "selesai")

    def jumlahTransaksiAktif(self):
        return sum(1 for trx in self.sistem.transaksi.values() if trx.getStatus() != "selesai")


    def buat_teks_laporan(self):
        teks = "=====================================\n"
        teks += "   LAPORAN SISTEM PEMINJAMAN ALAT\n"
        teks += "=====================================\n\n"
        
        teks += f"Total Transaksi: {len(self.sistem.transaksi)}\n"
        teks += f"Transaksi Selesai: {self.jumlahTransaksiSelesai()}\n"
        teks += f"Transaksi Aktif: {self.jumlahTransaksiAktif()}\n\n"
        
        teks += "--- 5 Alat Paling Sering Dipinjam ---\n"
        for i, (nama, jml) in enumerate(self.alatPalingSeringDipinjam()[:5], 1):
            teks += f"{i}. {nama} ({jml} unit)\n"
            
        teks += "\n--- 5 Mahasiswa Teraktif ---\n"
        for i, (nama, jml) in enumerate(self.mahasiswaPalingSeringMeminjam()[:5], 1):
            teks += f"{i}. {nama} ({jml} transaksi)\n"
            
        teks += "\n--- Daftar Alat Rusak ---\n"
        rusak = self.alatRusak()
        if not rusak:
            teks += "Tidak ada alat rusak.\n"
        else:
            for a in rusak:
                teks += f"- {a.getNama()} (Baik: {a.getStokBaik()}, R.Ringan: {a.getStokRusakRingan()}, R.Berat: {a.getStokRusakBerat()})\n"
        return teks


    def cetakAlatTersedia(self):
        print("\n===== Alat Tersedia =====")
        daftar = self.alatTersedia()
        if len(daftar) == 0:
            print("(Tidak ada alat tersedia)")
            return
        print(f"{'KODE':<10} | {'NAMA':<15} | {'KATEGORI':<20} | STOK BAIK")
        print("-" * 65)
        for a in daftar:
            print(f"{a.getKode():<10} | {a.getNama():<15} | {a.getKategori().getNama():<20} | {a.getStokBaik()}")
        print(f"Total: {len(daftar)} alat")
    
    def cetakAlatDipinjam(self):
        print("\n===== Alat Sedang Dipinjam =====")
        daftar = self.alatDipinjam()
        if len(daftar) == 0:
            print("(Tidak ada alat sedang dipinjam)")
            return
        print(f"{'KODE':<10} | {'NAMA':<15} | {'KATEGORI':<20} | STOK BAIK")
        print("-" * 65)
        for a in daftar:
            print(f"{a.getKode():<10} | {a.getNama():<15} | {a.getKategori().getNama():<20} | {a.getStokBaik()}")
        print(f"Total: {len(daftar)} alat")
    
    def cetakAlatRusak(self):
        print("\n===== Alat Rusak =====")
        daftar = self.alatRusak()
        if len(daftar) == 0:
            print("(Tidak ada alat rusak)")
            return
        print(f"{'KODE':<10} | {'NAMA':<15} | {'KATEGORI':<20} | RUSAK RINGAN | RUSAK BERAT")
        print("-" * 85)
        for a in daftar:
            print(f"{a.getKode():<10} | {a.getNama():<15} | {a.getKategori().getNama():<20} | {a.getStokRusakRingan():<12} | {a.getStokRusakBerat()}")
        print(f"Total: {len(daftar)} alat")
    
    def cetakRiwayatMahasiswa(self, nim):
        print(f"\n===== Riwayat Peminjaman: {nim} =====")
        try:
            daftar = self.riwayatMahasiswa(nim)
        except ValueError as e:
            print(f"Error: {e}")
            return
        if len(daftar) == 0:
            print("(Belum ada riwayat transaksi)")
            return
        mhs = self.sistem.getMahasiswa(nim)
        print(f"Mahasiswa: {mhs.getNama()}")
        print(f"Total transaksi: {len(daftar)}\n")
        for trx in daftar:
            print(trx.getDetail())
            print()
    
    def cetakStatistik(self):
        print("\n===== Statistik Peminjaman =====")
        print(f"Total transaksi   : {len(self.sistem.transaksi)}")
        print(f"  - Selesai       : {self.jumlahTransaksiSelesai()}")
        print(f"  - Aktif         : {self.jumlahTransaksiAktif()}\n")
        
        print("Alat Terpopuler:")
        for i, (nama, jml) in enumerate(self.alatPalingSeringDipinjam()[:5], 1):
            print(f"  {i}. {nama} - {jml} unit")
        print()
        
        print("Mahasiswa Teraktif:")
        for i, (nama, jml) in enumerate(self.mahasiswaPalingSeringMeminjam()[:5], 1):
            print(f"  {i}. {nama} - {jml} transaksi")

    def ringkasanHariIni(self):
        from datetime import date
        hari_ini = date.today()
        jumlah_trx = 0
        jumlah_alat = 0
        
        for trx in self.sistem.transaksi.values():
            if trx.getTanggalPinjam() == hari_ini:
                jumlah_trx += 1
                for detail in trx.getDaftarDetail():
                    jumlah_alat += detail.getJumlah()
        
        return {
            "tanggal": hari_ini,
            "jumlah_transaksi": jumlah_trx,
            "jumlah_alat_dipinjam": jumlah_alat
        }