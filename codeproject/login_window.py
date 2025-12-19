import json
import os
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from home_window import HomeWindow

USER_FILE = "users.json"

# ================= Register Window =================
class RegisterWindow(QWidget):
    def __init__(self, parent_login):
        super().__init__()
        self.parent_login = parent_login
        self.setWindowTitle("Register User Baru")
        self.setFixedSize(360, 260)
        self.setStyleSheet("background: #1E90FF; color: white;")  # biru
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)

        lbl = QLabel("REGISTER USER BARU")
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet("font-size:18pt; font-weight:bold;")
        layout.addWidget(lbl)

        self.user_in = QLineEdit()
        self.user_in.setPlaceholderText("Username")
        self.pass_in = QLineEdit()
        self.pass_in.setPlaceholderText("Password")
        self.pass_in.setEchoMode(QLineEdit.Password)

        self.user_in.setStyleSheet("padding:8px; border-radius:6px;")
        self.pass_in.setStyleSheet("padding:8px; border-radius:6px;")

        layout.addWidget(self.user_in)
        layout.addWidget(self.pass_in)

        # Tombol CONFIRM REGISTER
        btn_confirm = QPushButton("CONFIRM REGISTER")
        btn_confirm.setStyleSheet("background:white; color:#1E90FF; font-weight:bold; height:40px;")
        btn_confirm.clicked.connect(self.do_register)
        layout.addWidget(btn_confirm)

        # Tombol kembali login
        btn_back = QPushButton("Back to login")
        btn_back.setStyleSheet("background:white; color:#1E90FF; font-weight:bold; height:40px;")
        btn_back.clicked.connect(self.back_to_login)
        layout.addWidget(btn_back)

        self.setLayout(layout)

    def do_register(self):
        user = self.user_in.text().strip()
        pw = self.pass_in.text().strip()
        if not user or not pw:
            QMessageBox.warning(self, "Gagal", "Username dan password tidak boleh kosong!")
            return
        if user in self.parent_login.users:
            QMessageBox.warning(self, "Gagal", "Username sudah ada!")
            return
        #menyimpan user baru
        self.parent_login.users[user] = pw
        self.parent_login.save_users()
        QMessageBox.information(self, "Berhasil", f"User {user} berhasil dibuat! Silakan login.")
        self.back_to_login()  # kembali ke login window

    def back_to_login(self):
        self.parent_login.show()  
        self.close()


# ================= Login Window =================
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Tiket Bioskop")
        self.setFixedSize(360, 260)
        self.load_users()
        self.init_ui()

    def load_users(self):
        if not os.path.exists(USER_FILE):
            with open(USER_FILE, "w") as f:
                json.dump({"admin": "12345"}, f)
        with open(USER_FILE, "r") as f:
            self.users = json.load(f)

    def save_users(self):
        with open(USER_FILE, "w") as f:
            json.dump(self.users, f)

    def init_ui(self):
        from data_manage import get_theme
        theme = get_theme()
        primary = theme["primary"]

        self.setStyleSheet(f"background:{primary}; color:white;")
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)

        lbl = QLabel("LOGIN APLIKASI BIOSKOP")
        lbl.setStyleSheet("font-size:18pt; font-weight:bold; color:white;")
        lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl)

        self.user_in = QLineEdit()
        self.user_in.setPlaceholderText("Username")
        self.pass_in = QLineEdit()
        self.pass_in.setPlaceholderText("Password")
        self.pass_in.setEchoMode(QLineEdit.Password)

        self.user_in.setStyleSheet("padding:8px; border-radius:6px;")
        self.pass_in.setStyleSheet("padding:8px; border-radius:6px;")

        layout.addWidget(self.user_in)
        layout.addWidget(self.pass_in)

        
        btn_login = QPushButton("LOGIN")
        btn_login.setFixedHeight(40)
        btn_login.clicked.connect(self.do_login)
        layout.addWidget(btn_login)

        
        btn_register = QPushButton("REGISTER")
        btn_register.setFixedHeight(40)
        btn_register.clicked.connect(self.show_register_window)
        layout.addWidget(btn_register)

        self.setLayout(layout)

    def do_login(self):
        user = self.user_in.text().strip()
        pw = self.pass_in.text().strip()
        if user in self.users:
            if self.users[user] == pw:
                self.open_home(user, role="admin" if user=="admin" else "user")
            else:
                QMessageBox.warning(self, "Gagal", "Password salah!")
        else:
            QMessageBox.warning(self, "Gagal", "User tidak ditemukan. Silakan register terlebih dahulu.")

    def show_register_window(self):
        # menyembunyikan login window
        self.hide()
        # membuat register window
        self.register_window = RegisterWindow(self)
        self.register_window.move(self.x(), self.y())
        self.register_window.show()

    def open_home(self, username, role="user"):
        self.hide()
        self.home = HomeWindow(username=username, role=role)
        self.home.show()
