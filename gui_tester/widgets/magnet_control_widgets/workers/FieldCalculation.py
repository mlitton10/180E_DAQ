from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject

import pickle

# Open the file in read-binary mode
with open('data.pkl', 'rb') as file:
    # Load the data from the file
    loaded_data = pickle.load(file)

print(loaded_data)

def calculate_magnetic_field(current):


class FieldCalculationWorker(QObject):
    finished = pyqtSignal(object)
    failed = pyqtSignal(str)

    @pyqtSlot(float)
    def calculate(self, current):
        try:
            result = calculate_magnetic_field(current)
            self.finished.emit(result)
        except Exception as exc:
            self.failed.emit(str(exc))