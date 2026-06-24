import os.path

dir_path=os.path.dirname(os.path.realpath(__file__))
version_number="03/01/2018 12:37pm"			# update this when a change has been made

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class AcquisitionControls(QGroupBox):

	def __init__(self):
		super().__init__()
		self.DataRun = QPushButton("Start Data Acquisition", self)
		self.TestShot = QPushButton("Take Single Test Shot", self)

		self.num_run = UserSpinBoxRow("Number of total runs:")
		self.num_shots = UserSpinBoxRow("Shots per position:")

		self.num_run = QSpinBox()
		self.num_shots = QSpinBox()
		self.num_run_label = QLabel("Number of total runs:")
		self.num_shots_label = QLabel("Shots per position:")

		self.num_run.setRange(1, 100)
		self.num_shots.setRange(1, 200)
		self.num_run.setValue(1)
		self.num_shots.setValue(1)

		ac_layout = QGridLayout()
		ac_layout.addWidget(self.DataRun, 0, 0)
		ac_layout.addWidget(self.TestShot, 0, 1)
		ac_layout.addWidget(self.num_run_label, 1, 0)
		ac_layout.addWidget(self.num_shots_label, 2, 0)
		ac_layout.addWidget(self.num_run, 1, 1)
		ac_layout.addWidget(self.num_shots, 2, 1)

		self.setLayout(ac_layout)

