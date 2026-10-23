# announcement_ui.py
# -*- coding: utf-8 -*-

# imports
from sys import argv, exit as sys_exit
from typing import Any, Self
from loguru import logger
lazy from playsound import playsound  # type: ignore
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
lazy from pyttsx3 import init, Engine  # type: ignore

from ssv2announcementui import Ui_frm_announce


class AnnouncementWorker(QObject):
    failed = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self: Self, message: str) -> None:
        super().__init__()
        self.message: str = message

    @pyqtSlot()
    def run(self: Self) -> None:
        try:
            # setup TTS
            engine: Any | Engine = init()
            engine.setProperty("rate", 150)

            # play alarm seagull sound twice
            for _ in range(2):
                playsound(r"media\alarm_seagull.wav")

            # read out message
            engine.say(
                f"This is a Seagull Wars public service announcement. {self.message}"
            )
            engine.runAndWait()

            # play alarm seagull sound twice again
            for _ in range(2):
                playsound(r"media\alarm_seagull.wav")

        except Exception as error:
            self.failed.emit(str(error))

        finally:
            self.finished.emit()


class AnnounceWindow(QDialog, Ui_frm_announce):
    def __init__(self: Self) -> None:

        # setup the window
        QDialog.__init__(self)
        self.setupUi(self)
        
        self.announcement_thread: QThread | None = None
        self.announcement_worker: AnnouncementWorker | None = None

    # method that sends an announcement
    def send_announcement(self: Self, message: str) -> None:
        if self.announcement_thread is not None:
            return

        self.buttons.setEnabled(False)
        thread: QThread = QThread(self)
        
        worker: AnnouncementWorker = AnnouncementWorker(message)
        worker.moveToThread(thread)
        
        thread.started.connect(worker.run)

        worker.failed.connect(self._announcement_failed)
        
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        
        thread.finished.connect(self._announcement_finished)
        thread.finished.connect(thread.deleteLater)

        self.announcement_thread = thread
        self.announcement_worker = worker

        thread.start()

    def _announcement_failed(self: Self, message: str) -> None:
        logger.error(f"Announcement failed: {message}")

    def _announcement_finished(self: Self) -> None:
        self.buttons.setEnabled(True)
        self.announcement_thread = None
        self.announcement_worker = None


# Create an application and show the GUI
def main() -> None:
    app: QApplication = QApplication(argv)
    anw: AnnounceWindow = AnnounceWindow()
    anw.show()

    sys_exit(app.exec_())


# Only show GUI when ran directly
if __name__ == "__main__":
    main()
