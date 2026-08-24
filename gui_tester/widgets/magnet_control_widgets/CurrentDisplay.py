import os.path

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QGroupBox, QPushButton, QGridLayout
from gui_tester.widgets.basic_templates.TextInputBox import UserTextRow, make_form_table, UserTextColumn
from gui_tester.widgets.basic_templates.basic_application_widget import BasicAppWidget

dir_path=os.path.dirname(os.path.realpath(__file__))
version_number="03/01/2018 12:37pm"			# update this when a change has been made


class CurrentDisplay(BasicAppWidget):
    def __init__(self):
        super().__init__("Set Magnet PSU Currents")

        self.psuCurrentOne = UserTextColumn('PSU 1',read_only=True)
        self.psuCurrentTwo = UserTextColumn('PSU 2',read_only=True)
        self.psuCurrentThree = UserTextColumn('PSU 3',read_only=True)

        self.initialize_widget()

    def build_layout(self):
        layout = QGridLayout(self)
        layout.setContentsMargins(0,0,0,0)

        layout.setSpacing(0)
        layout.setVerticalSpacing(0)

        layout.setHorizontalSpacing(0)

        layout.addWidget(self.psuCurrentOne, 0, 0)
        layout.addWidget(self.psuCurrentTwo, 0, 1)
        layout.addWidget(self.psuCurrentThree, 0, 2)
        self.setLayout(layout)

    def initialize_boxes(self):
        self.psuCurrentOne.update_text("0")
        self.psuCurrentTwo.update_text("0")
        self.psuCurrentThree.update_text("0")

    def connect_signals(self):
        pass

    def initialize_widget(self):
        self.build_layout()
        self.connect_signals()
        self.initialize_boxes()

    def collect_parameters(self):
        parameters = {'I_1': float(self.psuCurrentOne.read_text()), 'I_2': float(self.psuCurrentTwo.read_text()),
                      'I_3': float(self.psuCurrentThree.read_text())}
        return parameters
