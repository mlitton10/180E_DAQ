import os.path

import numpy as np
from PyQt6.QtWidgets import QSizePolicy

dir_path=os.path.dirname(os.path.realpath(__file__))
version_number="03/01/2018 12:37pm"			# update this when a change has been made

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

rc_dict = {"figure.autolayout": True, "font.family": 'serif', 'font.size': 18.0,
		   'lines.linewidth': 2.5, 'axes.titlepad':8.0,
          'xtick.minor.visible':True,'ytick.minor.visible':True, 'axes.linewidth':2.0, 'xtick.major.width':2.0,
		   'xtick.direction': 'in',
          'ytick.direction':'in','ytick.major.width':2.3,'xtick.minor.width':1.0,'ytick.minor.width':1.0,
		   'xtick.major.size':8.0,'ytick.major.size':8.0,
          'xtick.minor.size':4.0, 'ytick.minor.size': 4.0, 'savefig.pad_inches': 0.05}

plt.rcParams.update(rc_dict)


def compute_point_grid(parameters):

	x_max = parameters['xmax']
	x_min = parameters['xmin']
	y_max = parameters['ymax']
	y_min = parameters['ymin']
	nx = parameters['nx']
	ny = parameters['ny']

	x_pos = np.linspace(x_min, x_max, nx)
	y_pos = np.linspace(y_min, y_max, ny)

	X = np.zeros(nx * ny)
	Y = np.zeros(nx * ny)

	index = 0
	for xx in x_pos:
		for yy in y_pos:
			X[index] = xx
			Y[index] = yy
			index += 1

	return X, Y

def compute_point_grid_polar(parameters):

	r_max = parameters['r_max']
	r_min = parameters['r_min']
	theta_max = parameters['theta_max']
	theta_min = parameters['theta_min']
	n_r = parameters['n_r']
	n_theta = parameters['n_theta']

	r_pos = np.linspace(r_min, r_max, n_r)
	theta_pos = np.linspace(theta_min, theta_max, n_theta) * np.pi / 180

	X = np.zeros(n_r * n_theta)
	Y = np.zeros(n_r * n_theta)

	index = 0
	for r in r_pos:
		for theta in theta_pos:
			X[index] = r * np.cos(theta)
			Y[index] = r * np.sin(theta)
			index += 1

	return X, Y


class MyMplCanvas(FigureCanvas):
	"""Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

	def __init__(self, parent=None, width=6, height=3, dpi=100):
		fig = Figure(figsize=(width, height), dpi=dpi)
		ax = fig.add_subplot(111)
		ax.grid(True, which='minor')
		FigureCanvas.__init__(self, fig)

		FigureCanvas.setSizePolicy(self,
								   QSizePolicy.Policy.Expanding,
								   QSizePolicy.Policy.Expanding)
		FigureCanvas.updateGeometry(self)
		self.probe_position_plotting_params = {
			'color': 'red',
			'marker': '*',
			's': 80
		}

		self.queued_probe_position_plotting_params = {
			'color': 'blue',
			'marker': 'o',
			's': 80
		}

		self.visited_probe_position_plotting_params = {
			'color': 'green',
			'marker': 'o',
			's': 80
		}

		self.setParent(parent)

		self.ax, self.matrix, self.point, self.machine = self.initialize_canvas(ax)
		self.visited_points, self.finished_x, self. finished_y = self.initialize_visited_points()

	def initialize_canvas(self, ax):
		ax.grid(which='both')

		matrix = ax.scatter(0, 0, **self.queued_probe_position_plotting_params,alpha=0)
		point = ax.scatter(0, 0, **self.probe_position_plotting_params)
		ax.set_xlabel("x-axis [cm]")
		ax.set_ylabel("y-axis [cm]")

		machine_radius = 0
		circle = plt.Circle(
			(0.0, 0.0),
			radius=machine_radius,
			facecolor='grey',  # Inner color
			edgecolor='k',  # Border color
			linewidth=1,  # Border thickness
			linestyle='-',  # Optional: border style (e.g., '--', ':', '-')
			alpha=0.5,
		)
		machine = ax.add_patch(circle)

		ax.set_aspect('equal')

		return ax, matrix, point, machine

	def clear_probe_position(self):
		self.point.remove()

	def clear_queued_probe_position(self):
		self.matrix.remove()

	def clear_visited_probe_position(self):
		self.visited_points.remove()

	def clear_all(self):
		self.clear_probe_position()
		self.clear_visited_probe_position()
		self.clear_queued_probe_position()

	def update_figure(self, X, Y):
		self.clear_queued_probe_position()
		self.matrix = self.ax.scatter(X, Y, **self.queued_probe_position_plotting_params)
		self.draw()

	def update_probe(self, x_now, y_now):
		self.clear_probe_position()
		self.point = self.ax.scatter(x_now, y_now, **self.probe_position_plotting_params)
		self.draw()

	def update_axis(self, x1, y1, x2, y2):
		self.ax.set_xlim(x2, x1)
		self.ax.set_ylim(y2, y1)

	def update_finished_positions(self, x, y):
		self.finished_x.append(x)
		self.finished_y.append(y)
		self.clear_visited_probe_position()
		self.ax.scatter(self.finished_x, self.finished_y, **self.visited_probe_position_plotting_params)
		self.draw()

	def initialize_visited_points(self):
		finished_x = []
		finished_y = []
		visited_points = self.ax.scatter(finished_x, finished_y, **self.visited_probe_position_plotting_params)
		return visited_points, finished_x, finished_y

	def clear_machine_drawing(self):
		self.machine.remove()

	def update_machine_radial_outline(self, radius):

		self.clear_machine_drawing()
		machine_patch = plt.Circle(
			(0.0, 0.0),
			radius=radius,
			facecolor='grey',  # Inner color
			edgecolor='k',  # Border color
			linewidth=1,  # Border thickness
			linestyle='-',  # Optional: border style (e.g., '--', ':', '-')
			alpha=0.5,
		)

		self.machine = self.ax.add_patch(machine_patch)
		self.update_axis(-1.1 * radius, -1.1*radius, 1.1*radius, 1.1*radius)
		self.draw()
