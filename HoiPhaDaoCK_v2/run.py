import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from main_ui import MainUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainUI()
    main_win.show()

    # update giá cỗ phiếu hiện tại
    timer_update_price = QTimer()
    timer_update_price.timeout.connect(main_win.update_table)
    timer_update_price.setInterval(10000)  # 10000ms = 10s
    timer_update_price.start()

    # update giá cổ phiếu max min
    timer_update_max_min = QTimer()
    timer_update_max_min.timeout.connect(main_win.update_max_min)
    timer_update_max_min.setInterval(600000)  # 600000ms = 10 phút
    timer_update_max_min.start()

    # Change giá trị trong tuần
    timer_chang_in_week = QTimer()
    timer_chang_in_week.timeout.connect(main_win.chang_in_week)
    timer_chang_in_week.setInterval(600000)  # 600000ms = 10 phút
    timer_chang_in_week.start()
    sys.exit(app.exec())
# ddmynguyen
# tuyet