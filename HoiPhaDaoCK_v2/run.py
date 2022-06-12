import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from main_ui import MainUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainUI()
    main_win.show()
    timer = QTimer()
    timer.timeout.connect(main_win.update_table)
    timer.setInterval(10000)  # 10000ms = 10s
    timer.start()
    sys.exit(app.exec())