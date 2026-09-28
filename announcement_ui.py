# announcement_ui.py
# -*- coding: utf-8 -*-

# imports
from sys import argv, exit as sys_exit
from typing import Self
from pyttsx3 import init  # type: ignore
from playsound import playsound  # type: ignore
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QIcon

from ssv2announcementui import Ui_Dialog


class AnnounceWindow(QDialog, Ui_Dialog):
    def __init__(self: Self) -> None:
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Send announcement")
        self.setWindowIcon(QIcon(r"seagull.ico"))
        self.engine = init()
        self.engine.setProperty("rate", 150)

    def send_announcement(self: Self, message: str) -> None:
        # play the alarm seagull sound twice
        for _ in range(2):
            playsound(r"media\alarm_seagull.wav")

        # say the announcement and wait
        self.engine.say(
            f"This is a Seagull Wars public service announcement. {message}"
        )
        self.engine.runAndWait()

        for _ in range(2):
            playsound(r"media\alarm_seagull.wav")


def main() -> None:
    app: QApplication = QApplication(argv)
    anw: AnnounceWindow = AnnounceWindow()
    anw.show()

    sys_exit(app.exec_())


if __name__ == "__main__":
    main()
