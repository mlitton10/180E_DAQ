import os.path

dir_path=os.path.dirname(os.path.realpath(__file__))
version_number="03/01/2018 12:37pm"			# update this when a change has been made

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class PositionControls(QGroupBox):
	def __init__(self):
		super().__init__()
		self.setTitle("Set up DAQ position")

		self.xMax = UserSettingsRow("Max x:")
		self.xMin = UserSettingsRow("Min x:")
		self.yMax = UserSettingsRow("Max y:")
		self.yMin = UserSettingsRow("Min y:")
		self.nx = UserSettingsRow("Nx:")
		self.ny = UserSettingsRow("Ny:")


		self.ConfirmButton = QPushButton("Confirm Input",self)


		controls_layout = QGridLayout()
		controls_layout.addWidget(self.xMaxLabel, 0, 0)
		controls_layout.addWidget(self.xMinLabel, 1, 0)
		controls_layout.addWidget(self.yMaxLabel, 2, 0)
		controls_layout.addWidget(self.yMinLabel, 3, 0)
		controls_layout.addWidget(self.nxLabel, 4, 0)
		controls_layout.addWidget(self.nyLabel, 5, 0)


		controls_layout.addWidget(self.xMaxInput, 0, 1)
		controls_layout.addWidget(self.xMinInput, 1, 1)
		controls_layout.addWidget(self.yMaxInput, 2, 1)
		controls_layout.addWidget(self.yMinInput, 3, 1)
		controls_layout.addWidget(self.nxInput, 4, 1)
		controls_layout.addWidget(self.nyInput, 5, 1)

		controls_layout.addWidget(self.ConfirmButton, 6, 1)

		self.setLayout(controls_layout)
