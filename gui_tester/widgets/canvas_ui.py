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


class MyMplCanvas(FigureCanvas):
	"""Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

	def __init__(self, parent=None, width=6, height=3, dpi=100):
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.ax = fig.add_subplot(111)
		self.ax.set_xlim(-35, 35)
		self.ax.set_ylim(-35, 35)

		FigureCanvas.__init__(self, fig)
		self.setParent(parent)

		FigureCanvas.setSizePolicy(self,
		                           QSizePolicy.Expanding,
		                           QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)

		self.ax.grid(which = 'both')
		self.ax.add_patch(patches.Rectangle((-38, -50), 76, 100, fill = False, edgecolor = 'red'))

		self.matrix = self.ax.scatter(0, 0, 0, color = 'blue', marker = 'o')
		self.point = self.ax.scatter(0, 0, 0, color = 'red', marker = '*')
		self.xlabel = self.ax.set_xlabel("x-axis [cm]")
		self.ylabel = self.ax.set_ylabel("y-axis [cm]")
		self.initialize_visited_points()

	def update_figure(self, param):

		self.parameters = param

		self.xmax = self.parameters['xmax']
		self.xmin = self.parameters['xmin']
		self.ymax = self.parameters['ymax']
		self.ymin = self.parameters['ymin']
		self.nx = self.parameters['nx']
		self.ny = self.parameters['ny']

		self.xpos = numpy.linspace(self.xmin,self.xmax,self.nx)
		self.ypos = numpy.linspace(self.ymin,self.ymax,self.ny)

		self.X = numpy.zeros(self.nx*self.ny)
		self.Y = numpy.zeros(self.nx*self.ny)

		index = 0
		for xx in self.xpos:
			for yy in self.ypos:
				self.X[index] = xx
				self.Y[index] = yy
				index += 1
		self.matrix = self.ax.scatter(self.X, self.Y, color = 'blue', marker = 'o')
		self.draw()
		print(self.parameters)

	def update_probe(self, xnow, ynow):
		self.point = self.ax.scatter(xnow, ynow, color = 'red', marker = '*')
		self.draw()

	def update_axis(self, x1, y1, x2, y2):
		self.ax.set_xlim(x2, x1)
		self.ax.set_ylim(y2, y1)

	def finished_positions(self, x, y):
		self.finished_x.append(x)
		self.finished_y.append(y)
		self.visited_points = self.ax.scatter(self.finished_x, self.finished_y, color = 'green', marker = 'o')
		self.draw()

	def initialize_visited_points(self):
		self.finished_x = []
		self.finished_y = []
		self.visited_points = self.ax.scatter(self.finished_x, self.finished_y, color = 'green', marker = 'o')

