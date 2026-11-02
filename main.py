from services.sistem_lab import SistemLab
from reports.laporan import Laporan
from ui.menu_app import MenuApp
from data.data_awal import data_dami

def main():
    sistem = SistemLab()

    data_dami(sistem)
    laporan = Laporan(sistem)
    ui = MenuApp(sistem, laporan)
    
    ui.jalankan()


if __name__ == "__main__":
    main()
