from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)
from gui_tester.widgets.magnet_control_widgets.CurrentRequest import CurrentRequest


class MagnetWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Magnet Controls go here"))

        currentRequest = CurrentRequest()
