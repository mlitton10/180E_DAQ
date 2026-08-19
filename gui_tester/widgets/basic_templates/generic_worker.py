from PyQt6.QtCore import pyqtSignal, pyqtSlot, QObject
from abc import ABC, abstractmethod


class Worker(QObject, ABC):
    finished = pyqtSignal()
    failed = pyqtSignal(str)
    def __init__(self):
        super().__init__()

    @pyqtSlot()
    def run(self):
        try:
            result = self.do_work()
            self.finished.emit(result)
        except Exception as e:
            self.failed.emit(str(e))

    @abstractmethod
    def do_work(self):
        raise NotImplementedError()