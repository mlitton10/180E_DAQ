import numpy as np
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject

import pickle


def calculate_magnetic_field(currents):
    with open('../data/section_1_fields.pkl', 'rb') as file:
        # Load the data from the file
        section_1_fields = pickle.load(file)
    with open('../data/section_2_fields.pkl', 'rb') as file:
        # Load the data from the file
        section_2_fields = pickle.load(file)
    with open('../data/section_3_fields.pkl', 'rb') as file:
        # Load the data from the file
        section_3_fields = pickle.load(file)

    fields = [section_1_fields, section_2_fields, section_3_fields]
    total_field_br = np.zeros(section_1_fields['total']['Br'].shape)
    total_field_bz = np.zeros(section_1_fields['total']['Bz'].shape)

    for n,I in enumerate(currents):
        total_field_br += I * fields[n]['total']['Br']
        total_field_bz += I * fields[n]['total']['Bz']

    return total_field_br, total_field_bz

class FieldCalculationWorker(QObject):
    finished = pyqtSignal(object)
    failed = pyqtSignal(str)

    @pyqtSlot(float, float, float)
    def calculate(self, current):
        try:
            total_field_br, total_field_bz = calculate_magnetic_field(current)
            self.finished.emit(result)
        except Exception as exc:
            self.failed.emit(str(exc))