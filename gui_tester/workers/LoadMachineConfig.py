import csv
import time

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot


class LoadMachineWorker(QObject):
    finished = pyqtSignal(str, float, float)   # filepath, length, radius
    failed = pyqtSignal(str)

    def __init__(self, filepath: str):
        super().__init__()
        self.filepath = filepath

    @pyqtSlot()
    def run(self):
        try:
            length, radius = self.load_csv(self.filepath)

            self.finished.emit(self.filepath, length, radius)
        except Exception as exc:
            self.failed.emit(f"{type(exc).__name__}: {exc}")

    def load_csv(self, filepath: str):

        with open(filepath, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                length = float(row["length"])
                radius = float(row["radius"])

        return length, radius
