from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QPushButton, QGridLayout, QCheckBox
from gui_tester.widgets.basic_templates.TextInputBox import UserDoubleSpinBoxRow
from gui_tester.widgets.basic_templates.basic_application_widget import BasicAppWidget


class CurrentControlWidget(BasicAppWidget):
    currentPlot = pyqtSignal(list)
    currentSet = pyqtSignal(list)
    def __init__(self, magnet_ip):
        super().__init__()
        self.magnet_ip = magnet_ip
        self.current_input_1 = UserDoubleSpinBoxRow("Current 1:")
        self.current_input_2 = UserDoubleSpinBoxRow("Current 2:")
        self.current_input_3 = UserDoubleSpinBoxRow("Current 3:")

        self.plot_only = QCheckBox("Plot only")
        self.set_button = QPushButton("Set Current")

        self._initialize_widget()

    @pyqtSlot()
    def _request_current(self):
        current_1 = self.current_input_1.read_value()
        current_2 = self.current_input_2.read_value()
        current_3 = self.current_input_3.read_value()
        plot_only = self.plot_only.isChecked()

        if plot_only:
            self.currentPlot.emit([current_1, current_2, current_3])
        else:
            self.currentSet.emit([current_1, current_2, current_3])
            self.currentPlot.emit([current_1, current_2, current_3])

    def _build_layout(self):
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

    def _connect_signals(self):
        self.set_button.clicked.connect(self._request_current)

    def initialize_boxes(self):
        self.current_input_1.set_range(0.0, 100.0)
        self.current_input_1.spin_box.setSuffix(" A")

        self.current_input_2.set_range(0.0, 100.0)
        self.current_input_2.spin_box.setSuffix(" A")

        self.current_input_3.set_range(0.0, 100.0)
        self.current_input_3.spin_box.setSuffix(" A")

    def _initialize_widget(self):
        self._build_layout()
        self._connect_signals()
        self.initialize_boxes()
