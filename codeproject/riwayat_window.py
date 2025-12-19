# riwayat_window.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QScrollArea, QFrame
)
from PyQt5.QtCore import Qt
from data_manage import get_riwayat, get_theme


class RiwayatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Riwayat Pemesanan")
        self.setFixedSize(480, 640)
        self.theme = get_theme()
        self.init_ui()

    def init_ui(self):
        t = self.theme
        self.setStyleSheet(f"background:{t['primary']};")

        layout = QVBoxLayout(self)

        # Header
        header = QLabel("RIWAYAT TIKET")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet(
            "font-size:16pt; color:white; font-weight:bold;"
        )
        layout.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QFrame()
        v = QVBoxLayout(container)

        riw = get_riwayat()

        if not riw:
            lbl = QLabel("Belum ada pemesanan.")
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("color:white;")
            v.addWidget(lbl)
        else:
            for i, tkt in enumerate(reversed(riw), start=1):
                struk = QFrame()
                struk.setStyleSheet("""
                    background: white;
                    border-radius: 8px;
                    padding: 6px;
                """)

                s_layout = QVBoxLayout(struk)

                # Judul Struk
                title = QLabel(f"STRUK TIKET #{i}")
                title.setAlignment(Qt.AlignCenter)
                title.setStyleSheet("font-weight:bold;")
                s_layout.addWidget(title)

                s_layout.addWidget(QLabel("=============================="))

                # Isi Struk
                s_layout.addWidget(QLabel(f"Film   : {tkt.get('film') or tkt.get('judul')}"))
                s_layout.addWidget(QLabel(f"Jam    : {tkt.get('jam')}"))
                s_layout.addWidget(
                    QLabel(f"Kursi  : {', '.join(tkt.get('kursi', []))}")
                )
                s_layout.addWidget(
                    QLabel(f"Total  : Rp {tkt.get('total', 0):,}")
                )

                v.addWidget(struk)

        scroll.setWidget(container)
        layout.addWidget(scroll)
