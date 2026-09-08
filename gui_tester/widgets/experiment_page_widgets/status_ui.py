from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QGridLayout
from gui_tester.widgets.basic_templates.basic_application_widget import BasicAppWidget
from gui_tester.widgets.basic_templates.status_led import StatusLED


class StatusWidget(BasicAppWidget):
    """Displays experiment status and device states."""

    def __init__(self, parent=None):
        super().__init__(title="Status")

        self._initialize_widget()


    def _build_layout(self):
        self.status_label = QLabel("Idle")
        self.status_label.setWordWrap(True)

        self.motor_led = StatusLED()
        self.scope_led = StatusLED()
        self.acquisition_led = StatusLED()
        self.saving_led = StatusLED()

        layout = QGridLayout()

        layout.addWidget(
            QLabel("Motor"),
            0,
            0,
        )
        layout.addWidget(
            self.motor_led,
            0,
            1,
        )

        layout.addWidget(
            QLabel("Oscilloscope"),
            1,
            0,
        )
        layout.addWidget(
            self.scope_led,
            1,
            1,
        )

        layout.addWidget(
            QLabel("Acquisition"),
            2,
            0,
        )
        layout.addWidget(
            self.acquisition_led,
            2,
            1,
        )

        layout.addWidget(
            QLabel("Saving"),
            3,
            0,
        )
        layout.addWidget(
            self.saving_led,
            3,
            1,
        )

        container = QVBoxLayout()

        container.addWidget(self.status_label)
        container.addLayout(layout)

        self.setLayout(container)

    def _connect_signals(self):
        pass

    def _initialize_widget(self):
        self._build_layout()
        self._connect_signals()

    @pyqtSlot(str)
    def set_status(self, message: str) -> None:
        self.status_label.setText(message)

    @pyqtSlot(bool)
    def set_motor_status(self, connected: bool) -> None:
        self.motor_led.set_status(connected)

    @pyqtSlot(bool)
    def set_scope_status(self, connected: bool) -> None:
        self.scope_led.set_status(connected)

    @pyqtSlot(bool)
    def set_acquisition_status(self, active: bool) -> None:
        self.acquisition_led.set_status(active)

    @pyqtSlot(bool)
    def set_saving_status(self, active: bool) -> None:
        self.saving_led.set_status(active)

    def reset(self) -> None:
        self.set_status("Idle")
        self.set_motor_status(False)
        self.set_scope_status(False)
        self.set_acquisition_status(False)
        self.set_saving_status(False)