# about_window.py
# -*- coding: utf-8 -*-
from webbrowser import open_new
from zipfile import ZipFile

from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon
from ssv2aboutui import Ui_Dialog


class AboutWindow(QDialog, Ui_Dialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("about")
        self.setWindowIcon(QIcon("seagull.ico"))
        self.gh_button.clicked.connect(self.github)
        self.extract_button.clicked.connect(self.extract_gull_effects)

    def github(self):
        open_new("https://github.com/Gabriel-H189/SSV2-Qt5")

    def extract_gull_effects(self):
        with ZipFile("media.zip") as zipfile:
            zipfile.extractall("media")
