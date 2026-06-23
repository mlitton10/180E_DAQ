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

		self.build_layout()


	def build_layout(self):
		layout = QGridLayout(self)
		layout.setContentsMargins(0,0,0,0)

		layout.setSpacing(0)
		layout.setVerticalSpacing(0)

		layout.setHorizontalSpacing(0)

		positions_box = make_form_table([self.xMax, self.xMin,
									   self.yMax, self.yMin,
									   self.nx, self.ny])

		self.setLayout(controls_layout)
