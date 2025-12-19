import os
from functools import partial
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QGridLayout, QFrame, QInputDialog, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QSound

from film_detail_window import FilmDetailWindow
from data_manage import get_films, add_film, get_saldo, set_saldo, get_theme


# ===== Fungsi bantu =====
def short_text(text, max_words=20):
    words = text.split()
    if len(words) > max_words:
        return " ".join(words[:max_words]) + "..."
    return text


class HomeWindow(QWidget):
    def __init__(self, username="guest", role="user"):
        super().__init__()
        self.username = username
        self.role = role
        self.setWindowTitle("Home - Tiket Bioskop")
        self.setFixedSize(920, 720)
        self.theme = get_theme()

        # sound notif
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.sound_path = os.path.join(base_dir, "sounds", "notif.wav")
        self.notif_sound = QSound(self.sound_path)

        # simpan detail window tunggal
        self.detail = None

        self.init_ui()

    def init_ui(self):
        t = self.theme
        self.setStyleSheet(f"background:{t['primary']};")
        main = QVBoxLayout()

        # ===== HEADER =====
        header = QHBoxLayout()
        lbl = QLabel(f"Selamat datang, {self.username}")
        lbl.setStyleSheet("font-size:14pt; font-weight:bold; color:maroon;")
        header.addWidget(lbl)
        header.addStretch()

        self.btn_saldo = QPushButton(f"Saldo: Rp {get_saldo()}")
        self.btn_saldo.clicked.connect(self.isi_saldo)
        self.btn_saldo.setStyleSheet(
            f"background:{t['card']}; color:{t['primary']}; font-weight:bold; padding:8px;"
        )
        header.addWidget(self.btn_saldo)

        btn_riwayat = QPushButton("Riwayat")
        btn_riwayat.clicked.connect(self.open_riwayat)
        btn_riwayat.setStyleSheet(f"background:{t['card']}; color:{t['primary']}; padding:8px;")
        header.addWidget(btn_riwayat)

        if self.role == "admin":
            btn_add = QPushButton("Tambah Film")
            btn_add.clicked.connect(self.add_film_dialog)
            btn_add.setStyleSheet(
                f"background:{t['accent']}; color:black; padding:8px; font-weight:bold;"
            )
            header.addWidget(btn_add)

        main.addLayout(header)
        main.addSpacing(12)

        # ===== GRID FILM =====
        grid_frame = QFrame()
        grid = QGridLayout()
        grid.setSpacing(14)

        films = get_films()
        cols = 2
        base_dir = os.path.dirname(os.path.abspath(__file__))

        for idx, film in enumerate(films):
            r = idx // cols
            c = idx % cols

            card = QFrame()
            card.setFixedSize(420, 300)
            card.setStyleSheet(f"background:{t['card']}; border-radius:10px; color:black;")

            v = QVBoxLayout()
            v.setContentsMargins(12, 12, 12, 12)
            v.setSpacing(6)

            # POSTER
            poster = QLabel()
            poster.setFixedSize(400, 140)
            poster.setAlignment(Qt.AlignCenter)
            poster_rel = film.get("poster", "")
            poster_full = os.path.join(base_dir, poster_rel)
            if poster_rel and os.path.exists(poster_full):
                pix = QPixmap(poster_full)
                poster.setPixmap(
                    pix.scaled(
                        poster.width(),
                        poster.height(),
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                )
            else:
                poster.setText("Poster tidak tersedia")
                poster.setStyleSheet("border:1px solid #aaa;")
            v.addWidget(poster)

            # JUDUL
            title = QLabel(film["judul"])
            title.setStyleSheet("font-weight:bold; font-size:12pt;")
            title.setAlignment(Qt.AlignCenter)
            v.addWidget(title)

            # DESKRIPSI (short)
            full_desc = film.get("deskripsi", "")
            desc = QLabel(short_text(full_desc, 20))
            desc.setWordWrap(True)
            desc.setAlignment(Qt.AlignCenter)
            v.addWidget(desc)

            v.addStretch()

            # BUTTON DETAIL
            btn = QPushButton("DETAIL & JADWAL")
            btn.clicked.connect(lambda checked, f=film: self.open_detail(f))
            btn.setStyleSheet(f"background:{t['primary']}; color:white; padding:8px; border-radius:6px;")
            v.addWidget(btn)

            card.setLayout(v)
            grid.addWidget(card, r, c)

        grid_frame.setLayout(grid)
        main.addWidget(grid_frame)
        main.addStretch()
        self.setLayout(main)

    # ===== FUNCTIONS =====
    def refresh(self):
        self.layout().deleteLater()
        self.init_ui()

    def add_film_dialog(self):
        judul, ok = QInputDialog.getText(self, "Tambah Film", "Judul film:")
        if not ok or not judul.strip():
            return
        des, ok2 = QInputDialog.getMultiLineText(self, "Deskripsi", "Deskripsi singkat:")
        if not ok2:
            des = ""
        add_film(judul.strip(), des.strip())
        QMessageBox.information(self, "OK", "Film berhasil ditambahkan.")
        self.refresh()

    def open_detail(self, film):
        if self.detail and self.detail.isVisible():
            self.detail.update_film(film)
            self.detail.raise_()
            self.detail.activateWindow()
        else:
            self.detail = FilmDetailWindow(film, parent=self)
            self.detail.show()

    def isi_saldo(self):
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Isi Saldo")
        dialog.setLabelText("Masukkan nominal (Rp):")
        dialog.setInputMode(QInputDialog.IntInput)
        dialog.setIntRange(1, 100000000)
        dialog.setIntStep(1000)

        if not dialog.exec_():
            return
        amt = dialog.intValue()
        set_saldo(get_saldo() + amt)
        if os.path.exists(self.sound_path):
            self.notif_sound.play()
        QMessageBox.information(self, "Berhasil", f"Saldo bertambah Rp {amt}")
        self.btn_saldo.setText(f"Saldo: Rp {get_saldo()}")

    def open_riwayat(self):
        from riwayat_window import RiwayatWindow
        self.riw = RiwayatWindow()
        self.riw.show()
