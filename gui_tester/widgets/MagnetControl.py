from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel, QGridLayout,
)
from gui_tester.widgets.magnet_control_widgets.CurrentDisplay import CurrentDisplay
from gui_tester.widgets.magnet_control_widgets.CurrentControlWidget import CurrentControlWidget
from gui_tester.widgets.magnet_control_widgets.FieldLine import FieldLine
from gui_tester.widgets.magnet_control_widgets.FieldStrength import FieldStrength

import pickle


class MagnetGeometry:
    def __init__(self, magnet_data_dir):
        self.data_dir = magnet_data_dir
        self.section_1_geometry = self.load("section_1_geometry.pkl")
        self.section_2_geometry = self.load("section_2_geometry.pkl")
        self.section_3_geometry = self.load("section_3_geometry.pkl")

    def load(self, filename):
        with open(self.data_dir + filename, 'rb') as file:
            # Load the data from the file
            loaded_data = pickle.load(file)

        return loaded_data

class MagnetWidget(QWidget):
    def __init__(self, geometry):
        super().__init__()

        self.currentRequest = CurrentControlWidget()
        self.fieldLine = FieldLine(geometry)
        self.fieldStrength = FieldStrength()
        self.currentDisplay = CurrentDisplay()

        self.build_layout()


    def build_layout(self):
        layout = QGridLayout(self)
        layout.addWidget(self.fieldLine, 0,0,1,2)
        layout.addWidget(self.fieldStrength, 1,0,2,1)
        layout.addWidget(self.currentDisplay, 1,1)
        layout.addWidget(self.currentRequest, 2,1)

