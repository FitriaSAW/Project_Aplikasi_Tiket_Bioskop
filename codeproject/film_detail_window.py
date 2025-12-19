import os
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QTabWidget, QScrollArea
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from seat_selection_window import SeatSelectionWindow
from data_manage import get_theme


class FilmDetailWindow(QWidget):
    def __init__(self, film, parent=None):
        super().__init__(parent)
        self.film = film
        self.setWindowTitle(film["judul"])
        self.setFixedSize(420, 520)
        self.theme = get_theme()
        self.init_ui()

    def init_ui(self):
        t = self.theme
        self.setStyleSheet(f"background:{t['card']}; color:black;")

        # TAB WIDGET
        tabs = QTabWidget()
        self.tab_info = QWidget()
        self.tab_jadwal = QWidget()
        tabs.addTab(self.tab_info, "Info Film")
        tabs.addTab(self.tab_jadwal, "Jadwal & Tiket")

        # ===== TAB 1: INFO FILM =====
        self.info_layout = QVBoxLayout()
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Poster
        self.poster_label = QLabel()
        self.poster_label.setAlignment(Qt.AlignCenter)
        poster_path = os.path.join(base_dir, self.film.get("poster", ""))
        if os.path.exists(poster_path):
            pixmap = QPixmap(poster_path)
            self.poster_label.setPixmap(
                pixmap.scaled(220, 320, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
        else:
            self.poster_label.setText("Poster tidak tersedia")
            self.poster_label.setStyleSheet("border:1px solid #aaa;")
        self.info_layout.addWidget(self.poster_label)

        # Judul
        self.title_label = QLabel(self.film["judul"])
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size:16pt; font-weight:bold;")
        self.info_layout.addWidget(self.title_label)

        # Deskripsi (scrollable)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(180)
        self.desc_label = QLabel(self.film.get("deskripsi", ""))
        self.desc_label.setWordWrap(True)
        self.desc_label.setAlignment(Qt.AlignTop)
        self.desc_label.setStyleSheet("padding:6px;")
        scroll.setWidget(self.desc_label)
        self.info_layout.addWidget(scroll)

        # Tombol EXIT/TUTUP
        btn_exit = QPushButton("TUTUP")
        btn_exit.setStyleSheet(f"background:{t['primary']}; color:white; padding:6px; border-radius:4px;")
        btn_exit.clicked.connect(self.close)
        self.info_layout.addWidget(btn_exit)

        self.info_layout.addStretch()
        self.tab_info.setLayout(self.info_layout)

        # ===== TAB 2: JADWAL =====
        jadwal_layout = QVBoxLayout()
        lbl = QLabel("Jadwal Tayang (Default demo):")
        jadwal_layout.addWidget(lbl)

        studios = [("Studio 1", "20:00"), ("Studio 2", "18:30"), ("Studio 3", "21:30")]
        for s, j in studios:
            row = QHBoxLayout()
            lbls = QLabel(f"{s} | Jam {j}")
            btn = QPushButton("Pilih Kursi & Beli")
            btn.setStyleSheet(f"background:{t['primary']}; color:white; padding:6px;")
            btn.clicked.connect(lambda checked, s=s, j=j: self.open_seat(s, j))
            row.addWidget(lbls)
            row.addStretch()
            row.addWidget(btn)
            jadwal_layout.addLayout(row)

        jadwal_layout.addStretch()
        self.tab_jadwal.setLayout(jadwal_layout)

        # ===== MAIN LAYOUT =====
        main_layout = QVBoxLayout()
        main_layout.addWidget(tabs)
        self.setLayout(main_layout)

    # Pilih kursi
    def open_seat(self, studio, jam):
        self.seat_win = SeatSelectionWindow(
            self.film["judul"], studio=studio, jam=jam
        )
        self.seat_win.show()

    # Update konten film tanpa buat window baru
    def update_film(self, film):
        self.film = film
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Poster
        poster_path = os.path.join(base_dir, self.film.get("poster", ""))
        if os.path.exists(poster_path):
            pixmap = QPixmap(poster_path)
            self.poster_label.setPixmap(
                pixmap.scaled(220, 320, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
        else:
            self.poster_label.setText("Poster tidak tersedia")

        # Judul
        self.title_label.setText(self.film["judul"])

        # Deskripsi
        self.desc_label.setText(self.film.get("deskripsi", ""))
