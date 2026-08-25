from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QGridLayout
from gui_tester.widgets.basic_templates.TextInputBox import DropdownRow
from gui_tester.widgets.basic_templates.basic_application_widget import BasicAppWidget


class DeviceSpecification(BasicAppWidget):
    fileSelected = pyqtSignal(str)

    def __init__(self, file_paths: list[str], parent=None):
        super().__init__(parent)
        self.file_drop_down = DropdownRow("Select Device: ", file_paths, parent)
        self.initialize_widget()


    def connect_signals(self):
        self.file_drop_down.optionSelected.connect(self.fileSelected)

    def build_layout(self):
        main_layout = QGridLayout(self)

        self.file_drop_down.layout().setContentsMargins(0, 0, 0, 0)
        self.file_drop_down.layout().setSpacing(0)

        main_layout.addWidget(self.file_drop_down, 0, 1)

    def initialize_widget(self):
        self.build_layout()
        self.connect_signals()

    def current_file(self) -> str:
        return self.file_drop_down.current_option()
