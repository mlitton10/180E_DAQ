from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QHBoxLayout, QGroupBox, QGridLayout
from gui_tester.widgets.basic_templates.TextInputBox import DropdownRow

class DeviceSpecification(QWidget):
    fileSelected = pyqtSignal(str)

    def __init__(self, file_paths: list[str], parent=None):
        super().__init__(parent)
        self.file_drop_down = DropdownRow("Select Device: ", file_paths, parent)
        self.build_layout()


    def connect_signals(self):
        self.file_drop_down.optionSelected.connect(self.fileSelected)


    def build_layout(self):
        main_layout = QGridLayout(self)

        self.file_drop_down.layout().setContentsMargins(0, 0, 0, 0)
        self.file_drop_down.layout().setSpacing(0)

        main_layout.addWidget(self.file_drop_down, 0, 1)

    def current_file(self) -> str:
        return self.file_drop_down.current_option()
