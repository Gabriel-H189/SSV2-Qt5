# log_window.py
# -*- coding: utf-8 -*-

# imports
from PyQt5.QtWidgets import QMainWindow
from ssv2logui import Ui_Dialog


class LogWindow(QMainWindow, Ui_Dialog):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("seagull log")

    def add_log(self, log_str):
        self.seagull_log.append(log_str)
