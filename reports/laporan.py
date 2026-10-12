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

