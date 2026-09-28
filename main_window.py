# main_window.py
# -*- coding: utf-8 -*-

# imports
from configparser import ConfigParser
from random import randint
from sys import argv
from sys import exit as sys_exit
from time import sleep
from datetime import datetime
from typing import Self

from playsound import playsound  # type: ignore
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from pyvolume import custom  # type: ignore

from ssv2newgui1 import Ui_Form
from about_window import AboutWindow
from log_window import LogWindow

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


class ScareWorker(QObject):
    log_received = pyqtSignal(str)
    failed = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(
        self: Self, timer: int, min_time: int, max_time: int, sound_name: str
    ) -> None:
        super().__init__()
        self.timer: int = timer
        self.min_time: int = min_time
        self.max_time: int = max_time
        self.sound_name: str = sound_name

    @pyqtSlot()
    def run(self: Self) -> None:
        logs: list[str] = []
        timer: int = self.timer

        try:
            while timer > 0:
                pause: int = randint(a=self.min_time, b=self.max_time)
                playsound(rf"media\{self.sound_name}.wav")

                current_time: datetime = datetime.now()
                log: str = f"A seagull was scared on {current_time:%d.%m.%Y %H:%M:%S}\n"
                self.log_received.emit(log.strip("\n"))
                logs.append(log)

                sleep(pause)
                timer -= pause

            with open(file=r"ssv2_log.txt", mode="a", encoding="utf-8") as file:
                file.writelines(logs)
        except Exception as error:
            self.failed.emit(str(error))
        finally:
            self.finished.emit()


# main window class containing logic
class MainWindow(QMainWindow, Ui_Form):

    # init method
    def __init__(self: Self) -> None:

        # setup the window
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Seagull Scaring V2")
        self.setWindowIcon(QIcon(r"seagull.ico"))
        self.scare_button.clicked.connect(self.start_scaring)
        self.about_button.clicked.connect(self.about_window)
        self.scare_thread: QThread | None = None
        self.scare_worker: ScareWorker | None = None
        self.log_window: LogWindow | None = None

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

    def start_scaring(self: Self) -> None:
        """Runs the scaring loop outside the GUI thread."""
        if self.scare_thread is not None:
            return

        try:
            timer: int = int(self.timer_entry.text())
            min_time: int = int(self.min_time_entry.text())
            max_time: int = int(self.max_time_entry.text())
        except ValueError:
            return

        self.log_window = LogWindow()
        self.log_window.show()
        self.scare_button.setEnabled(False)

        thread: QThread = QThread(self)
        worker: ScareWorker = ScareWorker(
            timer=timer,
            min_time=min_time,
            max_time=max_time,
            sound_name=self.sounds.currentText().replace(" ", "_"),
        )
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.log_received.connect(self.log_window.add_log)
        worker.failed.connect(self._scare_failed)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(self._scare_finished)
        thread.finished.connect(thread.deleteLater)

        self.scare_thread = thread
        self.scare_worker = worker
        thread.start()

    def _scare_failed(self: Self, message: str) -> None:
        print(f"Scaring failed: {message}")

    def _scare_finished(self: Self) -> None:
        self.scare_button.setEnabled(True)
        self.scare_thread = None
        self.scare_worker = None

    def set_volume(self: Self) -> None:
        """Changes volume according to slider."""

        custom(int(self.volume_slider.value()))

    def about_window(self: Self) -> None:
        """Displays the about window."""

        aw: AboutWindow = AboutWindow()
        aw.show()

        aw.exec_()


def main() -> None:
    """This function starts the program."""

    app: QApplication = QApplication(argv)
    window: MainWindow = MainWindow()
    window.show()

    sys_exit(app.exec_())


# Start program
if __name__ == "__main__":
    main()
