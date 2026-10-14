from services.sistem_lab import SistemLab
from reports.laporan import Laporan
from ui.menu_app import MenuApp


def main():
    sistem = SistemLab()
    
    laporan = Laporan(sistem)
    ui = MenuApp(sistem, laporan)
    
    ui.jalankan()


if __name__ == "__main__":
    main()
