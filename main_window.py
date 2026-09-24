# main_window.py
# -*- coding: utf-8 -*-

# imports
from configparser import ConfigParser
from random import randint
from sys import argv
from sys import exit as sys_exit
from threading import Thread
from time import sleep
from datetime import datetime
from typing import Self

from playsound import playsound  # type: ignore
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
from pyvolume import custom  # type: ignore

from ssv2newgui1 import Ui_Form
from about_window import AboutWindow

# Load config file
parser: ConfigParser = ConfigParser()
parser.read(r"ssv2cfg.ini")

config: list[str] = parser.sections()

seagull_values: list[str] = [
    "seagull",
    "sad seagull",
    "angry seagull",
    "confused seagull",
    "disgust seagull",
    "alarm seagull",
    "robot seagull",
    "Seagull 2",
    "sea gull",
]


# main window class containing logic
class MainWindow(QMainWindow, Ui_Form):
    def __init__(self: Self) -> None:

        # setup the window
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Seagull Scaring V2")
        self.setWindowIcon(QIcon(r"seagull.ico"))
        self.scare_button.clicked.connect(self.scare_thread)
        self.about_button.clicked.connect(self.about_window)

        # Add all seagull sound effects to the drop down list
        for item in seagull_values:
            self.sounds.addItem(item)

        # Set default config file values
        self.timer_entry.setText(parser[config[0]]["scaring_time"])
        self.min_time_entry.setText(parser[config[0]]["min_time"])
        self.max_time_entry.setText(parser[config[0]]["max_time"])
        self.volume_slider.setValue(int(parser[config[0]]["default_volume"]))
        self.volume_slider.valueChanged.connect(self.set_volume)

        self.sounds.setCurrentIndex(0)

    def scare(self: Self) -> None:
        """Starts seagull scaring."""

        timer: int = int(self.timer_entry.text())
        seagulls_scared: int = 0
        logs: list[str] = []

        while timer > 0:

            # Play the seagull sound, write a log and wait random number of seconds
            pause: int = randint(
                a=int(self.min_time_entry.text()), b=int(self.max_time_entry.text())
            )
            sound_name: str = self.sounds.currentText().replace(" ", "_")
            playsound(rf"media\{sound_name!s}.wav")

            current_time: datetime = datetime.now()
            log: str = f"A seagull was scared on {current_time:%d.%m.%Y %H:%M:%S}\n"
            print(log.strip("\n"))
            logs.append(log)

            seagulls_scared += 1
            sleep(pause)
            timer -= pause

        # write log to file
        with open(file=r"ssv2_log.txt", mode="a", encoding="utf-8") as file:
            file.writelines(logs)

        print("Done! Log written to ssv2_log.txt")

    def scare_thread(self: Self) -> None:
        """Starts seagull scaring thread to prevent the main window from freezing."""

        thread: Thread = Thread(target=self.scare)
        thread.start()

    def set_volume(self: Self) -> None:
        """Changes volume according to slider."""

        custom(int(self.volume_slider.value()))

    def about_window(self: Self) -> None:
        """Displays the about window."""

        aw: AboutWindow = AboutWindow()
        aw.exec_()


def main() -> None:
    """This function starts the program."""

    app: QApplication = QApplication(argv)
    window: MainWindow = MainWindow()
    window.show()

    sys_exit(app.exec_())


if __name__ == "__main__":
    main()
