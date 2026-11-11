from services.sistem_lab import SistemLab
from reports.laporan import Laporan
from ui.menu_app import MenuApp

def main():
    sistem = SistemLab()
    sistem.muat_data_awal()
    
    laporan = Laporan(sistem)
    ui = MenuApp(sistem, laporan)
    
    try:
        ui.jalankan()
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan paksa oleh pengguna.")
    

if __name__ == "__main__":
    main()