from services.sistem_lab import 


class Laporan:
    def __init__(self, sistem):
        if type(sistem) != :
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

    
    def statistik(self):
        hitung_alat = {}
        for trx in self.sistem.transaksi.values():
            for detail in trx.getDaftarDetail():
                nama = detail.getAlat().getNama()
                jumlah = detail.getJumlah()
                if nama not in hitung_alat:
                    hitung_alat[nama] = 0
                hitung_alat[nama] = hitung_alat[nama] + jumlah

        alat_terpopuler = sorted(
            hitung_alat.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        hitung_mhs = {}
        for trx in self.sistem.transaksi.values():
            nama = trx.getMahasiswa().getNama()
            if nama not in hitung_mhs:
                hitung_mhs[nama] = 0
            hitung_mhs[nama] = hitung_mhs[nama] + 1
        
        mahasiswa_teraktif = sorted(
            hitung_mhs.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        selesai = 0
        aktif = 0
        for trx in self.sistem.transaksi.values():
            if trx.getStatus() == "selesai":
                selesai = selesai + 1
            else:
                aktif = aktif + 1
        
        return {
            "alat_terpopuler": alat_terpopuler,
            "mahasiswa_teraktif": mahasiswa_teraktif,
            "transaksi_selesai": selesai,
            "transaksi_aktif": aktif,
            "total_transaksi": len(self.sistem.transaksi)
        }


    def ringkasanHariIni(self):
        from datetime import date
        hari_ini = date.today()
        jumlah_trx = 0
        jumlah_alat = 0
        
        for trx in self.sistem.transaksi.values():
            if trx.getTanggalPinjam() == hari_ini:
                jumlah_trx = jumlah_trx + 1
                for detail in trx.getDaftarDetail():
                    jumlah_alat = jumlah_alat + detail.getJumlah()
        
        return {
            "tanggal": hari_ini,
            "jumlah_transaksi": jumlah_trx,
            "jumlah_alat_dipinjam": jumlah_alat
        }
    
    
    def cetakAlatTersedia(self):
        print("\n===== ALAT TERSEDIA =====")
        daftar = self.alatTersedia()
        
        if len(daftar) == 0:
            print("(Tidak ada alat tersedia)")
            return
        
        print(f"{'KODE':<10} | {'NAMA':<15} | {'KATEGORI':<20} | {'STOK':<5}")
        print("-" * 60)
        for a in daftar:
            print(
                f"{a.getKode():<10} | "
                f"{a.getNama():<15} | "
                f"{a.getKategori().getNama():<20} | "
                f"{a.getStok():<5}"
            )
        print(f"Total: {len(daftar)} alat")

    
    def cetakAlatDipinjam(self):
        print("\n===== ALAT SEDANG DIPINJAM =====")
        daftar = self.alatDipinjam()
        
        if len(daftar) == 0:
            print("(Tidak ada alat sedang dipinjam)")
            return
        
        print(f"{'KODE':<10} | {'NAMA':<15} | {'KATEGORI':<20} | {'STOK':<5}")
        print("-" * 60)
        for a in daftar:
            print(
                f"{a.getKode():<10} | "
                f"{a.getNama():<15} | "
                f"{a.getKategori().getNama():<20} | "
                f"{a.getStok():<5}"
            )
        print(f"Total: {len(daftar)} alat")

    
    def cetakAlatRusak(self):
        print("\n===== ALAT RUSAK =====")
        daftar = self.alatRusak()
        
        if len(daftar) == 0:
            print("(Tidak ada alat rusak)")
            return
        
        print(f"{'KODE':<10} | {'NAMA':<15} | {'KATEGORI':<20} | {'KONDISI':<15}")
        print("-" * 65)
        for a in daftar:
            print(
                f"{a.getKode():<10} | "
                f"{a.getNama():<15} | "
                f"{a.getKategori().getNama():<20} | "
                f"{a.getKondisi():<15}"
            )
        print(f"Total: {len(daftar)} alat")

    def cetakRiwayatMahasiswa(self, nim):
        print(f"\n===== RIWAYAT PEMINJAMAN: {nim} =====")
        
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
        print(f"Total transaksi: {len(daftar)}")
        print()
        
        for trx in daftar:
            print(trx.getDetail())
            print()
    
    def cetakStatistik(self):
        print("\n===== STATISTIK PEMINJAMAN =====")
        
        stat = self.statistik()
        
        print(f"Total transaksi   : {stat['total_transaksi']}")
        print(f"  - Selesai       : {stat['transaksi_selesai']}")
        print(f"  - Aktif         : {stat['transaksi_aktif']}")
        print()
        
        print("Alat Terpopuler:")
        if len(stat["alat_terpopuler"]) == 0:
            print("  (Belum ada data)")
        else:
            for i, (nama, jumlah) in enumerate(stat["alat_terpopuler"][:5], start=1):
                print(f"  {i}. {nama} - {jumlah} unit dipinjam")
        print()
        
        print("Mahasiswa Teraktif:")
        if len(stat["mahasiswa_teraktif"]) == 0:
            print("  (Belum ada data)")
        else:
            for i, (nama, jumlah) in enumerate(stat["mahasiswa_teraktif"][:5], start=1):
                print(f"  {i}. {nama} - {jumlah} transaksi")