# log_window.py
# -*- coding: utf-8 -*-

# imports
from sys import argv, exit as sys_exit
from typing import Self

from PyQt5.QtWidgets import QApplication, QMainWindow
from ssv2logui import Ui_Dialog


# log window class containing logic
class LogWindow(QMainWindow, Ui_Dialog):
    def __init__(self: Self) -> None:

        # setup the window
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("seagull log")

    # add a log to the list
    def add_log(self: Self, log_str: str) -> None:
        self.seagull_log.append(log_str)


def main() -> None:
    """This function starts the program."""

    app: QApplication = QApplication(argv)
    window: LogWindow = LogWindow()
    window.show()

    sys_exit(app.exec_())


if __name__ == "__main__":
    main()
