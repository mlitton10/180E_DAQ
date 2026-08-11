import os.path

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGroupBox, QPushButton, QGridLayout, QCheckBox
from gui_tester.widgets.basic_templates.TextInputBox import UserTextRow, make_form_table, UserTextColumn

dir_path=os.path.dirname(os.path.realpath(__file__))
version_number="03/01/2018 12:37pm"			# update this when a change has been made


class CurrentRequest(QGroupBox):
    confirm = pyqtSignal()
    plotOnly = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setTitle("Set Magnet PSU Currents")


        self.psuCurrentOne = UserTextColumn('PSU 1')
        self.psuCurrentTwo = UserTextColumn('PSU 2')
        self.psuCurrentThree = UserTextColumn('PSU 3')

        self.ConfirmButton = QPushButton("Confirm Input",self)
        self.CheckBox = QCheckBox("Plot Only: ")

        self.build_layout()
        self.initialize_boxes()
        self.connect_signals()

    def connect_signals(self):
        self.ConfirmButton.clicked.connect(self.confirm)
        self.CheckBox.checkStateChanged.connect(self.plotOnly)
        pass

    def build_layout(self):
        layout = QGridLayout(self)
        layout.setContentsMargins(0,0,0,0)

        layout.setSpacing(0)
        layout.setVerticalSpacing(0)

        layout.setHorizontalSpacing(0)

        layout.addWidget(self.psuCurrentOne, 0, 0)
        layout.addWidget(self.psuCurrentTwo, 0, 1)
        layout.addWidget(self.psuCurrentThree, 0, 2)
        layout.addWidget(self.ConfirmButton, 1,1,2,1)
        layout.addWidget(self.CheckBox, 3,1,1,1)
        self.setLayout(layout)

    def initialize_boxes(self):
        self.xMax.update_text("0")
        self.xMin.update_text("0")
        self.yMax.update_text("0")
        self.yMin.update_text("0")
        self.nx.update_text("1")
        self.ny.update_text("1")

    def collect_parameters(self):
        parameters = {'I_1': float(self.psuCurrentOne.read_text()), 'I_2': float(self.psuCurrentTwo.read_text()),
                      'I_3': float(self.psuCurrentThree.read_text())}
        return parameters
