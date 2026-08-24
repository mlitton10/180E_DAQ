import csv
import time

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from gui_tester.widgets.basic_templates.generic_worker import Worker


class LoadMachineWorker(Worker):
    finished = pyqtSignal(str, float, float)   # filepath, length, radius

    def __init__(self, filepath: str):
        super().__init__()
        self.filepath = filepath

    def do_work(self):
        filepath, length, radius = self.load_csv(self.filepath)
        return filepath, length, radius

    def load_csv(self, filepath: str):
        with open(filepath, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                length = float(row["length"])
                radius = float(row["radius"])

        f.close()
        return filepath, length, radius
