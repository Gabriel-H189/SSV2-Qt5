# main_qt5.py
# -*- coding: utf-8 -*-

# imports
from sys import argv, exit as sys_exit
from configparser import ConfigParser

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QIcon

from main_window import MainWindow
from autostart_window import AutostartWindow


def main() -> None:
    """This function starts the program."""

    parser: ConfigParser = ConfigParser()
    parser.read(r"ssv2cfg.ini")

    config: list[str] = parser.sections()
    app: QApplication = QApplication(argv)
    window: MainWindow | None = None

    # Show the end of support message box
    if parser[config[0]]["eos_notify"] == "True":
        eos: QMessageBox = QMessageBox()
        eos.setIcon(QMessageBox.Warning)
        eos.setWindowIcon(QIcon(r"seagull.ico"))
        eos.setWindowTitle("Seagull Scaring V2 (Qt Edition) End of Support")
        eos.setText(
            "Seagull Scaring V2 (Qt Edition) has reached its end of support date.\nThe program will continue to work but no longer receive updates."
        )

        retval: int = eos.exec_()

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
