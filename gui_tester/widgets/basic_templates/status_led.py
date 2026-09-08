from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QWidget
from enum import Enum


class LEDState(Enum):
    OFF = "off"
    GREEN = "green"
    ORANGE = "orange"
    RED = "red"

class StatusLED(QWidget):
    """Simple circular status indicator."""

    def __init__(self, parent=None, diameter=14):
        super().__init__(parent)

        self._diameter = diameter
        self._state = LEDState.OFF

        self.setFixedSize(diameter, diameter)

    def set_status(self, state: LEDState) -> None:
        self._state = state
        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        colors = {
            LEDState.OFF: QColor("#555555"),
            LEDState.GREEN: QColor("#2ecc71"),
            LEDState.ORANGE: QColor("#f39c12"),
            LEDState.RED: QColor("#e74c3c"),
        }

        painter.setBrush(colors[self._state])
        painter.setPen(Qt.PenStyle.NoPen)

        painter.drawEllipse(
            0,
            0,
            self._diameter,
            self._diameter,
        )