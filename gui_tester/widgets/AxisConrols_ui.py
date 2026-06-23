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

		axis_layout = QGridLayout()
		axis_layout.addWidget(self.xaxisLabel, 0, 0)
		axis_layout.addWidget(self.xlowInput, 0, 1)
		axis_layout.addWidget(self.toLabel, 0, 2)
		axis_layout.addWidget(self.xupInput, 0, 3)
		axis_layout.addWidget(self.blankLabel, 0, 4)
		axis_layout.addWidget(self.yaxisLabel, 0, 5)
		axis_layout.addWidget(self.ylowInput, 0, 6)
		axis_layout.addWidget(self.toLabel, 0, 7)
		axis_layout.addWidget(self.yupInput, 0, 8)
		self.setLayout(axis_layout)

