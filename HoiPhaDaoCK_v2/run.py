import sys
from PyQt5.QtWidgets import QApplication
from main_ui import MainUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainUI()
    main_win.show()
    sys.exit(app.exec())