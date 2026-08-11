from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)





class MagnetWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Magnet Controls go here"))