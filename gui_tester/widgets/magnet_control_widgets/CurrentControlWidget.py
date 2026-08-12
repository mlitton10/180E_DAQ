import os.path

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QGroupBox, QPushButton, QGridLayout, QCheckBox, QFormLayout, QDoubleSpinBox
from gui_tester.widgets.basic_templates.TextInputBox import UserTextRow, make_form_table, UserTextColumn, \
    UserDoubleSpinBoxRow


class CurrentControlWidget(QGroupBox):
    currentRequested = pyqtSignal(list, bool)
    def __init__(self):
        super().__init__()

        self.current_input_1 = UserDoubleSpinBoxRow("Current 1:")
        self.current_input_2 = UserDoubleSpinBoxRow("Current 2:")
        self.current_input_3 = UserDoubleSpinBoxRow("Current 3:")

        self.plot_only = QCheckBox("Plot only")
        self.set_button = QPushButton("Set Current")

        self.initialize_boxes()
        self.connect_signals()
        self.build_layout()

    @pyqtSlot()
    def _request_current(self):
        current_1 = self.current_input_1.read_value()
        current_2 = self.current_input_2.read_value()
        current_3 = self.current_input_3.read_value()
        plot_only = self.plot_only.isChecked()

        self.currentRequested.emit([current_1, current_2, current_3], plot_only)

    def build_layout(self):
        layout = QGridLayout(self)
        layout.setContentsMargins(0,0,0,0)

        layout.setSpacing(0)
        layout.setVerticalSpacing(0)

        layout.setHorizontalSpacing(0)

        layout.addWidget(self.current_input_1, 0, 0)
        layout.addWidget(self.current_input_2, 0, 1)
        layout.addWidget(self.current_input_3, 0, 2)
        layout.addWidget(self.set_button, 1,1,2,1)
        layout.addWidget(self.plot_only, 3,1,1,1)
        self.setLayout(layout)

    def connect_signals(self):
        self.set_button.clicked.connect(self._request_current)

    def initialize_boxes(self):
        self.current_input_1.set_range(0.0, 100.0)
        self.current_input_1.spin_box.setSuffix(" A")

        self.current_input_2.set_range(0.0, 100.0)
        self.current_input_2.spin_box.setSuffix(" A")

        self.current_input_3.set_range(0.0, 100.0)
        self.current_input_3.spin_box.setSuffix(" A")
