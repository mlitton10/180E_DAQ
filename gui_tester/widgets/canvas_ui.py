import numpy
import os.path

dir_path=os.path.dirname(os.path.realpath(__file__))
version_number="03/01/2018 12:37pm"			# update this when a change has been made

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
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
		self.x_label = self.ax.set_xlabel("x-axis [cm]")
		self.y_label = self.ax.set_ylabel("y-axis [cm]")
		self.finished_x, self. finished_y = self.initialize_visited_points()

	def update_figure(self, param):

		parameters = param

		x_max = parameters['xmax']
		x_min = parameters['xmin']
		y_max = parameters['ymax']
		y_min = parameters['ymin']
		nx = parameters['nx']
		ny = parameters['ny']

		x_pos = numpy.linspace(x_min, x_max, nx)
		y_pos = numpy.linspace(y_min, y_max, ny)

		X = numpy.zeros(nx * ny)
		Y = numpy.zeros(nx * ny)

		index = 0
		for xx in x_pos:
			for yy in y_pos:
				X[index] = xx
				Y[index] = yy
				index += 1
		self.matrix = self.ax.scatter(X, Y, color = 'blue', marker = 'o')
		self.draw()
		print(parameters)

	def update_probe(self, x_now, y_now):
		self.point = self.ax.scatter(x_now, y_now, color ='red', marker ='*')
		self.draw()

	def update_axis(self, x1, y1, x2, y2):
		self.ax.set_xlim(x2, x1)
		self.ax.set_ylim(y2, y1)

	def update_finished_positions(self, x, y):
		self.finished_x.append(x)
		self.finished_y.append(y)
		self.ax.scatter(self.finished_x, self.finished_y, color = 'green', marker = 'o')
		self.draw()

	def initialize_visited_points(self):
		finished_x = []
		finished_y = []
		self.ax.scatter(finished_x, finished_y, color = 'green', marker = 'o')
		return finished_x, finished_y
