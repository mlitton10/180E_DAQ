import os.path

from gui_tester.widgets.basic_templates.TextInputBox import UserSpinBoxRow

dir_path=os.path.dirname(os.path.realpath(__file__))
version_number="03/01/2018 12:37pm"			# update this when a change has been made

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class AxisControls(QGroupBox):
	def __init__(self):
		super().__init__()

		self.range_settings = {'min_range':-60, 'max_range':60}

		self.x_high = UserSpinBoxRow("x-axis range:")
		self.x_low = UserSpinBoxRow("to: ")

		self.y_high = UserSpinBoxRow("x-axis range:")
		self.y_low = UserSpinBoxRow("to: ")

		self.build_layout()
		self.initialize_values()
		pass

	def build_layout(self):
		layout = QGridLayout(self)
		layout.addWidget(self.x_high, 0, 0)
		layout.addWidget(self.x_low, 0, 1)
		layout.addWidget(self.y_high, 0, 2)
		layout.addWidget(self.y_low, 0, 3)
		pass

	def initialize_values(self):
		self.x_high.set_range(**self.range_settings)
		self.x_low.set_range(**self.range_settings)
		self.y_high.set_range(**self.range_settings)
		self.y_low.set_range(**self.range_settings)

		self.x_high.set_value(35)
		self.x_low.set_value(-35)

		self.y_high.set_value(35)
		self.y_low.set_value(-35)

	def read_axis(self):
		x_high = self.x_high.read_value()
		y_high = self.y_high.read_value()
		x_low = self.x_low.read_value()
		y_low = self.y_low.read_value()
		return [x_high,y_high,x_low,y_low]