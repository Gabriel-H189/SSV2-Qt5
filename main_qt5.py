# main_qt5.py
# -*- coding: utf-8 -*-

# imports
from sys import argv, exit as sys_exit

from PyQt5.QtWidgets import QApplication

from main_window import MainWindow


def main() -> None:
    """This function starts the program."""

    app: QApplication = QApplication(argv)
    window: MainWindow = MainWindow()
    window.show()

    sys_exit(app.exec_())


if __name__ == "__main__":
    main()
