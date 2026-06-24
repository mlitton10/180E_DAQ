import os.path

dir_path=os.path.dirname(os.path.realpath(__file__))
version_number="03/01/2018 12:37pm"			# update this when a change has been made

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class AxisControls(QGroupBox):
	def __init__(self):
		super().__init__()
		self.xupInput = QSpinBox()
		self.yupInput = QSpinBox()
		self.xlowInput = QSpinBox()
		self.ylowInput = QSpinBox()

		self.xupInput.setRange(-60, 60)
		self.yupInput.setRange(-60, 60)
		self.xlowInput.setRange(-60, 60)
		self.ylowInput.setRange(-60, 60)

		self.xupInput.setValue(35)
		self.yupInput.setValue(35)
		self.xlowInput.setValue(-35)
		self.ylowInput.setValue(-35)

		self.xaxisLabel = QLabel("x axis range:")
		self.yaxisLabel = QLabel("y axis range:")
		self.toLabel = QLabel("to")
		self.blankLabel = QLabel("  ")

		self.x_high = UserSpinBoxRow("x-axis range:")
		self.x_low = UserSpinBoxRow("to: ")

		self.y_high = UserSpinBoxRow("x-axis range:")
		self.y_low = UserSpinBoxRow("to: ")

		self.build_layout()
		pass

	def build_layout(self):
		layout = QGridLayout(self)
		layout.addWidget(self.x_high, 0, 0)
		layout.addWidget(self.x_low, 0, 1)
		layout.addWidget(self.y_high, 0, 2)
		layout.addWidget(self.y_low, 0, 3)
		pass
