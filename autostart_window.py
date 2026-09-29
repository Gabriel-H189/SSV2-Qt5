# autostart_window.py
# -*- coding: utf-8 -*-

from sys import argv, exit as sys_exit
from time import sleep
from typing import Self

from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtWidgets import QDialog, QApplication
from ssv2autostartui import Ui_Dialog


class CountdownWorker(QObject):
    tick = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self: Self, timer: int) -> None:
        super().__init__()
        self.timer: int = timer

    @pyqtSlot()
    def run(self: Self) -> None:
        for remaining in range(self.timer, 0, -1):
            self.tick.emit(remaining)
            sleep(1)
        self.finished.emit()


class AutostartWindow(QDialog, Ui_Dialog):
    countdown_finished = pyqtSignal()

    def __init__(self: Self) -> None:
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Autostart")
        self.setWindowIcon(QIcon(r"seagull.ico"))
        self.text_cursor = QTextCursor(self.countdown.document())
        self.countdown.setTextCursor(self.text_cursor)
        self.countdown_thread: QThread | None = None
        self.countdown_worker: CountdownWorker | None = None
        self.abort_button.clicked.connect(self.abort)

    def count_down(self, timer: int) -> None:
        self.countdown.insertPlainText("Autostart in...\n")
        thread: QThread = QThread(self)
        worker: CountdownWorker = CountdownWorker(timer)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.tick.connect(self._show_countdown_tick)
        worker.finished.connect(self.countdown_finished)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(self._countdown_thread_finished)
        thread.finished.connect(thread.deleteLater)

        self.countdown_thread = thread
        self.countdown_worker = worker
        thread.start()

    def _show_countdown_tick(self, remaining: int) -> None:
        self.countdown.insertPlainText(f"{remaining}\n")

    def _countdown_thread_finished(self) -> None:
        self.countdown_thread = None
        self.countdown_worker = None

    def abort(self: Self) -> None:
        if self.countdown_thread is not None and self.countdown_worker is not None:
            self.countdown_thread.quit()
            self.countdown_thread.wait()
            self.countdown_thread = None
            self.countdown_worker = None
        self.close()
        exit(0)


def main() -> None:
    app: QApplication = QApplication(argv)
    auw: AutostartWindow = AutostartWindow()
    auw.show()

    sys_exit(app.exec_())


if __name__ == "__main__":
    main()
