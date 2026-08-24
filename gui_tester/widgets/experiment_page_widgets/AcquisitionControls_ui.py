import os.path

from gui_tester.widgets.basic_templates.TextInputBox import UserSpinBoxRow, UserTextRow, make_form_table
from gui_tester.widgets.basic_templates.basic_application_widget import BasicAppWidget

dir_path=os.path.dirname(os.path.realpath(__file__))
version_number="03/01/2018 12:37pm"			# update this when a change has been made

from PyQt6 import QtCore
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

class AcquisitionControls(BasicAppWidget):

	def __init__(self):
		super().__init__()
		self.DataRun = QPushButton("Start Data Acquisition", self)
		self.TestShot = QPushButton("Take Single Test Shot", self)

		self.num_run = UserSpinBoxRow("Number of total runs:")
		self.num_shots = UserSpinBoxRow("Shots per position:")

		self.initialize_widget()

	def build_layout(self):
		layout = QGridLayout(self)
		layout.setContentsMargins(0, 0, 0, 0)

		layout.setSpacing(0)
		layout.setVerticalSpacing(0)

		layout.setHorizontalSpacing(0)

		shots_box = make_form_table([self.num_shots, self.num_run])

		shots_box.layout().setContentsMargins(0, 0, 0, 0)
		shots_box.layout().setSpacing(0)
		shots_box.layout().setVerticalSpacing(0)
		layout.addWidget(self.DataRun, 0, 0)
		layout.addWidget(self.TestShot, 0, 1)
		layout.addWidget(shots_box, 1, 0, 2, 2)

	def initialize_values(self):
		self.num_shots.set_range(max_range=200)

		self.num_run.set_value(1)
		self.num_shots.set_value(1)

	def connect_signals(self):
		pass

	def initialize_widget(self):
		self.build_layout()
		self.connect_signals()