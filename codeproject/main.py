# main.py
import sys
from PyQt5.QtWidgets import QApplication
from login_window import LoginWindow
from data_manage import ensure_file

def main():
    ensure_file()
    app = QApplication(sys.argv)
    win = LoginWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
