# about_window.py
# -*- coding: utf-8 -*-

# imports
from sys import argv, exit as sys_exit
from typing import Self
from webbrowser import open_new
from zipfile import ZipFile

from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QIcon

from ssv2aboutui import Ui_Dialog


# about window class containing logic
class AboutWindow(QDialog, Ui_Dialog):
    def __init__(self: Self) -> None:

        # setup the window
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("about")
        self.setWindowIcon(QIcon(r"seagull.ico"))
        self.gh_button.clicked.connect(self.github)
        self.extract_button.clicked.connect(self.extract_gull_effects)

    # Opens the online project page
    def github(self: Self) -> None:
        open_new(r"https://github.com/Gabriel-H189/SSV2-Qt5")

    # extracts a zip file containing sound effects to the media dir
    def extract_gull_effects(self: Self) -> None:
        with ZipFile(r"media.zip") as zipfile:
            zipfile.extractall(r"media")


def main() -> None:
    """This function starts the program."""

    app: QApplication = QApplication(argv)
    window: AboutWindow = AboutWindow()
    window.show()

    sys_exit(app.exec_())


if __name__ == "__main__":
    main()
