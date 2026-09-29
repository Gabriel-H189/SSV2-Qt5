# autostart_window.py
# -*- coding: utf-8 -*-

from sys import argv, exit as sys_exit
from time import sleep
from typing import Self

from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtWidgets import QDialog, QApplication
from ssv2autostartui import Ui_Dialog


class AutostartWindow(QDialog, Ui_Dialog):
    def __init__(self: Self) -> None:
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Autostart")
        self.setWindowIcon(QIcon(r"seagull.ico"))
        self.text_cursor = QTextCursor(self.countdown.document())
        self.countdown.setTextCursor(self.text_cursor)

    def count_down(self, timer: int) -> None:
        self.countdown.insertPlainText("Autostart in...\n")
        while timer > 0:
            self.countdown.insertPlainText(f"{timer}\n")
            timer -= 1
            sleep(timer)


def main() -> None:
    app: QApplication = QApplication(argv)
    auw: AutostartWindow = AutostartWindow()
    auw.show()

    sys_exit(app.exec_())


if __name__ == "__main__":
    main()
