# main_qt5.py
# -*- coding: utf-8 -*-

# imports
from sys import argv, exit as sys_exit
from configparser import ConfigParser

from PyQt5.QtWidgets import QApplication

from main_window import MainWindow
from autostart_window import AutostartWindow


def main() -> None:
    """This function starts the program."""

    parser: ConfigParser = ConfigParser()
    parser.read(r"ssv2cfg.ini")

    config: list[str] = parser.sections()
    app: QApplication = QApplication(argv)
    window: MainWindow | None = None

    def start_main_window() -> None:
        nonlocal window
        window = MainWindow()
        window.show()
        window.start_scaring()

    if parser[config[0]]["autostart"] == "True":
        a_window: AutostartWindow = AutostartWindow()
        a_window.show()
        a_window.countdown_finished.connect(start_main_window)
        a_window.count_down(int(parser[config[0]]["autostart_delay"]))

    else:
        window = MainWindow()
        window.show()

    sys_exit(app.exec_())


if __name__ == "__main__":
    main()
