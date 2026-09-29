# announcement_ui.py
# -*- coding: utf-8 -*-

# imports
from sys import argv, exit as sys_exit
from typing import Self
from playsound import playsound  # type: ignore
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot

from ssv2announcementui import Ui_Dialog


class AnnouncementWorker(QObject):
    failed = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self: Self, message: str) -> None:
        super().__init__()
        self.message: str = message

    @pyqtSlot()
    def run(self: Self) -> None:
        try:
            from pyttsx3 import init  # type: ignore

            engine = init()
            engine.setProperty("rate", 150)

            for _ in range(2):
                playsound(r"media\alarm_seagull.wav")

            engine.say(
                f"This is a Seagull Wars public service announcement. {self.message}"
            )
            engine.runAndWait()

            for _ in range(2):
                playsound(r"media\alarm_seagull.wav")
        except Exception as error:
            self.failed.emit(str(error))
        finally:
            self.finished.emit()


class AnnounceWindow(QDialog, Ui_Dialog):
    def __init__(self: Self) -> None:
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Send announcement")
        self.setWindowIcon(QIcon(r"seagull.ico"))
        self.announcement_thread: QThread | None = None
        self.announcement_worker: AnnouncementWorker | None = None

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
        print(f"Announcement failed: {message}")

    def _announcement_finished(self: Self) -> None:
        self.buttons.setEnabled(True)
        self.announcement_thread = None
        self.announcement_worker = None


def main() -> None:
    app: QApplication = QApplication(argv)
    anw: AnnounceWindow = AnnounceWindow()
    anw.show()

    sys_exit(app.exec_())


if __name__ == "__main__":
    main()
