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
import matplotlib.pyplot as plt

rc_dict = {"figure.autolayout": True, "font.family": 'serif', 'font.size': 18.0,
		   'lines.linewidth': 2.5, 'axes.titlepad':8.0,
          'xtick.minor.visible':True,'ytick.minor.visible':True, 'axes.linewidth':2.0, 'xtick.major.width':2.0,
		   'xtick.direction': 'in',
          'ytick.direction':'in','ytick.major.width':2.3,'xtick.minor.width':1.0,'ytick.minor.width':1.0,
		   'xtick.major.size':8.0,'ytick.major.size':8.0,
          'xtick.minor.size':4.0, 'ytick.minor.size': 4.0, 'savefig.pad_inches': 0.05}

plt.rcParams.update(rc_dict)

class MyMplCanvas(FigureCanvas):
	"""Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

	def __init__(self, parent=None, width=6, height=3, dpi=100):
		fig = Figure(figsize=(width, height), dpi=dpi)
		ax = fig.add_subplot(111)
		ax.set_xlim(-35, 35)
		ax.set_ylim(-35, 35)
		FigureCanvas.__init__(self, fig)

		FigureCanvas.setSizePolicy(self,
								   QSizePolicy.Expanding,
								   QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)
		self.probe_position_plotting_params = {
			'color': 'red',
			'marker': '*'
		}

		self.queued_probe_position_plotting_params = {
			'color': 'blue',
			'marker': 'o'
		}

		self.visited_probe_position_plotting_params = {
			'color': 'green',
			'marker': 'o'
		}

		self.setParent(parent)

		self.ax, self.matrix, self.point = self.initialize_canvas(ax)
		self.finished_x, self. finished_y = self.initialize_visited_points()

	def initialize_canvas(self, ax):
		ax.grid(which='both')
		ax.add_patch(patches.Rectangle((-38, -50), 76, 100, fill=False, edgecolor='red'))

		matrix = ax.scatter(0, 0, 0, **self.queued_probe_position_plotting_params)
		point = ax.scatter(0, 0, 0, **self.probe_position_plotting_params)
		ax.set_xlabel("x-axis [cm]")
		ax.set_ylabel("y-axis [cm]")

		return ax, matrix, point


	def compute_point_grid(self, parameters):

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

		return X, Y

	def update_figure(self, X, Y):
		self.matrix = self.ax.scatter(X, Y, **self.queued_probe_position_plotting_params)
		self.draw()

	def update_probe(self, x_now, y_now):
		self.point = self.ax.scatter(x_now, y_now, **self.probe_position_plotting_params)
		self.draw()

	def update_axis(self, x1, y1, x2, y2):
		self.ax.set_xlim(x2, x1)
		self.ax.set_ylim(y2, y1)

	def update_finished_positions(self, x, y):
		self.finished_x.append(x)
		self.finished_y.append(y)
		self.ax.scatter(self.finished_x, self.finished_y, **self.visited_probe_position_plotting_params)
		self.draw()

	def initialize_visited_points(self):
		finished_x = []
		finished_y = []
		self.ax.scatter(finished_x, finished_y, **self.visited_probe_position_plotting_params)
		return finished_x, finished_y
