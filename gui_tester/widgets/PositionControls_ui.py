import numpy
import sys
import os
import os.path
import time
import datetime
from Motor_Control_2D_xy import MotorControl2d
from LecroyScope import LecroyScope, WAVEDESC_SIZE
from LecroyScope import EXPANDED_TRACE_NAMES
import tkinter
from tkinter import filedialog
import tkinter.messagebox
import h5py as h5py

dir_path=os.path.dirname(os.path.realpath(__file__))
version_number="03/01/2018 12:37pm"			# update this when a change has been made

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as patches


class PositionControls(QGroupBox):
	def __init__(self):
		super().__init__()
		self.setTitle("Set up DAQ position")

		self.xMaxLabel = QLabel("Max x:")
		self.xMinLabel = QLabel("Min x:")
		self.yMaxLabel = QLabel("Max y:")
		self.yMinLabel = QLabel("Min y:")
		self.nxLabel = QLabel("nx:")
		self.nyLabel = QLabel("ny:")

		#valueLabel = QLabel("Current value:")

		self.xMaxInput = QLineEdit()
		self.xMinInput = QLineEdit()
		self.yMaxInput = QLineEdit()
		self.yMinInput = QLineEdit()
		self.nxInput = QLineEdit()
		self.nyInput = QLineEdit()

		self.xMaxInput.setText("0")
		self.xMinInput.setText("0")
		self.yMaxInput.setText("0")
		self.yMinInput.setText("0")
		self.nxInput.setText("1")
		self.nyInput.setText("1")


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
