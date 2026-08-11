from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel, QGridLayout,
)
from gui_tester.widgets.magnet_control_widgets.CurrentDisplay import CurrentDisplay
from gui_tester.widgets.magnet_control_widgets.CurrentRequest import CurrentRequest
from gui_tester.widgets.magnet_control_widgets.FieldLine import FieldLine
from gui_tester.widgets.magnet_control_widgets.FieldStrength import FieldStrength


class MagnetWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.currentRequest = CurrentRequest()
        self.fieldLine = FieldLine()
        self.fieldStrength = FieldStrength()
        self.currentDisplay = CurrentDisplay()

        self.build_layout()


    def build_layout(self):
        layout = QGridLayout(self)
        layout.addWidget(self.fieldLine, 0,0)
        layout.addWidget(self.fieldStrength, 1,0)
        layout.addWidget(self.currentDisplay, 0,1)
        layout.addWidget(self.currentRequest, 1,1)

