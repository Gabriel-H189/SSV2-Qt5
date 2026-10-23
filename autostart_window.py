# autostart_window.py
# -*- coding: utf-8 -*-

from sys import argv, exit as sys_exit
lazy from time import sleep
from typing import Self

from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QDialog, QApplication

from ssv2autostartui import Ui_frm_autostart


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


class AutostartWindow(QDialog, Ui_frm_autostart):
    countdown_finished = pyqtSignal()

    def __init__(self: Self) -> None:
        # setup the window
        QDialog.__init__(self)
        self.setupUi(self)
        
        self.text_cursor = QTextCursor(self.txt_countdown.document())
        self.txt_countdown.setTextCursor(self.text_cursor)
        
        self.countdown_thread: QThread | None = None
        self.countdown_worker: CountdownWorker | None = None

        self.btn_abort.clicked.connect(self.abort)

    # method that starts countdown thread
    def count_down(self: Self, timer: int) -> None:
        self.txt_countdown.insertPlainText("Autostart in...\n")
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

    # updates countdown
    def _show_countdown_tick(self: Self, remaining: int) -> None:
        self.txt_countdown.insertPlainText(f"{remaining}\n")

    def _countdown_thread_finished(self: Self) -> None:
        self.countdown_thread = None
        self.countdown_worker = None

    # method that aborts countdown
    def abort(self: Self) -> None:

        if self.countdown_thread is not None and self.countdown_worker is not None:
            self.countdown_thread.quit()
            self.countdown_thread.wait()
            
            self.countdown_thread = None
            self.countdown_worker = None
            
        self.close()
        exit(0)


# Create an application and show the autostart window
def main() -> None:
    app: QApplication = QApplication(argv)
    auw: AutostartWindow = AutostartWindow()
    auw.show()

    sys_exit(app.exec_())


# Only show the GUI when ran directly
if __name__ == "__main__":
    main()
