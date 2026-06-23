import os.path
from gui_tester.widgets.basic_templates.TextInputBox import UserSettingsRow, make_form_table

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
		self.initialize_boxes()


	def build_layout(self):
		layout = QGridLayout(self)
		layout.setContentsMargins(0,0,0,0)

		layout.setSpacing(0)
		layout.setVerticalSpacing(0)

		layout.setHorizontalSpacing(0)

		positions_box = make_form_table([self.xMax, self.xMin,
									   self.yMax, self.yMin,
									   self.nx, self.ny])
		positions_box.layout().setContentsMargins(0,0,0,0)
		positions_box.layout().setSpacing(0)
		positions_box.layout().setVerticalSpacing(0)

		layout.addWidget(positions_box, 0, 0, 5, 1)

		layout.addWidget(self.ConfirmButton, 5, 0, 1, 1)
		self.setLayout(layout)

	def initialize_boxes(self):
		self.xMax.update_text("0")
		self.xMin.update_text("0")
		self.yMax.update_text("0")
		self.yMin.update_text("0")
		self.nx.update_text("1")
		self.ny.update_text("1")

	def collect_parameters(self):
		parameters = {'xmax': self.xMax.read_text(), 'xmin': self.xMin.read_text(),
					  'ymax': self.yMax.read_text(), 'ymin': self.yMin.read_text(),
					  'nx': self.nx.read_text(), 'ny': self.ny.read_text()}
		return parameters
