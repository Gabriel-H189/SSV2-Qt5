# main_window.py
# -*- coding: utf-8 -*-

from configparser import ConfigParser
from random import randint
from threading import Thread
from time import sleep
from datetime import datetime

from playsound import playsound  # type: ignore
from PyQt5.QtWidgets import QMainWindow
from pyvolume import custom  # type: ignore

from ssv2newgui1 import Ui_Form
from about_window import AboutWindow

# Load config file
parser = ConfigParser()
parser.read("ssv2cfg.ini")

config = parser.sections()

seagull_values = [
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


class MainWindow(QMainWindow, Ui_Form):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)  # type: ignore
        self.setWindowTitle("Seagull Scaring V2")
        self.scare_button.clicked.connect(self.scare_thread)  # type: ignore
        self.about_button.clicked.connect(self.about_window)

        for item in seagull_values:
            self.sounds.addItem(item)  # type: ignore

        self.timer_entry.setText(parser[config[0]]["scaring_time"])  # type: ignore
        self.min_time_entry.setText(parser[config[0]]["min_time"])  # type: ignore
        self.max_time_entry.setText(parser[config[0]]["max_time"])  # type: ignore
        self.volume_slider.setValue(int(parser[config[0]]["default_volume"]))  # type: ignore
        self.volume_slider.valueChanged.connect(self.set_volume)  # type: ignore

        self.sounds.setCurrentIndex(0)  # type: ignore

    def scare(self) -> None:
        """Starts seagull scaring."""

        timer: int = int(self.timer_entry.text())  # type: ignore
        seagulls_scared: int = 0
        logs = []

        while timer > 0:
            pause: int = randint(int(self.min_time_entry.text()), int(self.max_time_entry.text()))  # type: ignore
            sound_name = self.sounds.currentText().replace(" ", "_")
            playsound(rf"media\{sound_name}.wav")  # type: ignore

            # TODO: gui log
            log = f"A seagull was scared on {datetime.now():%d.%m.%Y %H:%M:%S}\n"
            print(log.strip("\n"))
            logs.append(log)

            seagulls_scared += 1
            sleep(pause)
            timer -= pause  # type: ignore

        # write log to file
        with open("ssv2_log.txt", "a") as file:
            file.writelines(logs)

        print("Done! Log written to ssv2_log.txt")

    def scare_thread(self) -> None:
        """Starts seagull scaring thread."""

        thread: Thread = Thread(target=self.scare)
        thread.start()

    def set_volume(self) -> None:
        """Changes volume according to slider."""

        custom(int(self.volume_slider.value()))  # type: ignore

    def about_window(self) -> None:
        aw = AboutWindow()
        aw.exec_()
