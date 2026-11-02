def data_dami(sistem):
    sistem.tambahKategori("KT01", "Komputasi")
    sistem.tambahKategori("KT02", "Jaringan")
    sistem.tambahKategori("KT03", "Multimedia")

    sistem.tambahAlat("AL01", "Keyboard", "KT01", 5)
    sistem.tambahAlat("AL02", "Mouse", "KT01", 3)
    sistem.tambahAlat("AL03", "Router", "KT02", 5)
    sistem.tambahAlat("AL04", "Switch", "KT02", 5)
    sistem.tambahAlat("AL05", "Access Point", "KT02", 3)
    sistem.tambahAlat("AL06", "Kamera", "KT03", 1)
    sistem.tambahAlat("AL07", "Proyektor", "KT03", 2)