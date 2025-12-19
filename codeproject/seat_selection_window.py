# seat_selection_window.py
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from data_manage import get_saldo, set_saldo, get_kursi_terisi, add_kursi_terisi, add_riwayat, get_theme
import math

HARGA_TIKET = 35000

class SeatSelectionWindow(QWidget):
    def __init__(self, judul, studio="Studio 1", jam="20:00"):
        super().__init__()
        self.judul = judul
        self.studio = studio
        self.jam = jam
        self.setWindowTitle(f"Pilih Kursi - {judul}")
        self.setFixedSize(720, 720)
        self.theme = get_theme()
        self.selected = set()
        self.init_ui()

    def init_ui(self):
        t = self.theme
        self.setStyleSheet(f"background:{t['primary']}; color:white;")
        v = QVBoxLayout()
        title = QLabel(f"Pilih Kursi - {self.judul} | {self.studio} | {self.jam}")
        title.setStyleSheet("font-size:14pt; font-weight:bold; color:white;")
        v.addWidget(title)

        screen_lbl = QLabel("[ LAYAR ]")
        screen_lbl.setAlignment(Qt.AlignCenter)
        screen_lbl.setStyleSheet("background:#000; color:#ccc; padding:6px;")
        v.addWidget(screen_lbl)

        grid_frame = QWidget()
        grid = QGridLayout()
        grid.setSpacing(8)

        key = f"{self.judul}|{self.studio}|{self.jam}"
        sold = set(get_kursi_terisi(key))
        rows = [chr(i) for i in range(65, 65+8)]  # A..H
        cols = range(1, 9)  # 1..8

        self.btns = {}
        for r_idx, r in enumerate(rows):
            for c_idx, c in enumerate(cols):
                kode = f"{r}{c}"
                btn = QPushButton(kode)
                btn.setFixedSize(64, 48)
                if kode in sold:
                    btn.setStyleSheet(f"background:{t['sold']}; color:white; border-radius:6px;")
                    btn.setEnabled(False)
                else:
                    btn.setStyleSheet(f"background:{t['available']}; color:black; border-radius:6px;")
                    btn.clicked.connect(lambda checked, k=kode: self.toggle_seat(k))
                grid.addWidget(btn, r_idx, c_idx)
                self.btns[kode] = btn

        grid_frame.setLayout(grid)
        v.addWidget(grid_frame)

        # total & button
        h = QHBoxLayout()
        self.total_lbl = QLabel("Total Harga: Rp 0")
        self.total_lbl.setStyleSheet("font-weight:bold; color:white;")
        h.addWidget(self.total_lbl)
        h.addStretch()
        buy_btn = QPushButton("Beli Tiket")
        buy_btn.setFixedSize(140, 40)
        buy_btn.setStyleSheet(f"background:{t['accent']}; color:black; font-weight:bold;")
        buy_btn.clicked.connect(self.buy)
        h.addWidget(buy_btn)
        v.addLayout(h)

        self.setLayout(v)

    def toggle_seat(self, kode):
        t = self.theme
        if kode in self.selected:
            self.selected.remove(kode)
            self.btns[kode].setStyleSheet(f"background:{t['available']}; color:black; border-radius:6px;")
        else:
            self.selected.add(kode)
            self.btns[kode].setStyleSheet(f"background:{t['selected']}; color:black; border-radius:6px;")
        self.total_lbl.setText(f"Total Harga: Rp {len(self.selected) * HARGA_TIKET}")

    def buy(self):
        if len(self.selected) == 0:
            QMessageBox.warning(self, "Info", "Pilih minimal 1 kursi.")
            return
        total = len(self.selected) * HARGA_TIKET
        s = get_saldo()
        if s < total:
            QMessageBox.warning(self, "Saldo", f"Saldo tidak cukup. Total Rp {total}, Saldo Rp {s}")
            return
        # deduct, add riwayat, mark seats sold
        set_saldo(s - total)
        key = f"{self.judul}|{self.studio}|{self.jam}"
        add_kursi_terisi(key, list(self.selected))
        add_riwayat({
            "judul": self.judul,
            "studio": self.studio,
            "jam": self.jam,
            "kursi": sorted(list(self.selected)),
            "total": total,
            "waktu": __import__("datetime").datetime.utcnow().isoformat()
        })
        QMessageBox.information(self, "Sukses", "Tiket berhasil dibeli.")
        # update UI: disable purchased buttons
        for k in list(self.selected):
            self.btns[k].setEnabled(False)
            self.btns[k].setStyleSheet(f"background:{self.theme['sold']}; color:white; border-radius:6px;")
        self.selected.clear()
        self.total_lbl.setText("Total Harga: Rp 0")
