import numpy
import os.path

import numpy as np
from matplotlib.ticker import MultipleLocator, AutoMinorLocator

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

def plot_magnets(section_geometry, ax):
	for magnet, setting in section_geometry.items():
		rect = patches.Rectangle(
			(setting['position'][0] - setting['width'] / 2, setting['position'][1] - setting['depth'] / 2),
			setting['width'], setting['depth'], linewidth=1, edgecolor='r', facecolor='r')

		# Add the patch to the Axes
		ax.add_patch(rect)
	return ax

class FieldLine(FigureCanvas):
	"""Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

	def __init__(self, geometry, parent=None, width=6, height=3, dpi=100):
		self.geometry = geometry
		fig = Figure(figsize=(width, height), dpi=dpi)
		ax = fig.add_subplot(111)

		FigureCanvas.__init__(self, fig)

		FigureCanvas.setSizePolicy(self,
								   QSizePolicy.Expanding,
								   QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)
		self.field_line_plot_params = {
			'color': 'k',
			'ls': '-',
			'lw': 2
		}

		self.cathode_field_line_plot_params = {
			'color': 'red',
			'ls': '-',
			'lw': 2
		}

		self.setParent(parent)

		self.ax = self.initialize_canvas(ax)
		self.field_lines = self.initialize_field_lines()

	def initialize_canvas(self, ax):
		ax.grid(True, which='minor')
		ax.set_title("Field Lines")
		ax.grid(which='both')

		ax.set_xlabel("z [m]")
		ax.set_ylabel("r [m]")

		ax = plot_magnets(self.geometry.section_1_geometry, ax)
		ax = plot_magnets(self.geometry.section_2_geometry, ax)
		ax = plot_magnets(self.geometry.section_3_geometry, ax)

		z_wall = [0, 3.455 - 0.3]
		z_range = np.linspace(0, 3.455 - 0.3, 10, endpoint=True)
		r_range = np.linspace(0, 0.2, 10, endpoint=True)

		ax.plot([z_wall[0]] * 10, r_range, color='k', ls='-', lw=1.5)
		ax.plot([z_wall[1]] * 10, r_range, color='k', ls='-', lw=1.5)
		ax.plot(z_range, [0.2] * 10, color='k', ls='-', lw=1.5)
		rect = patches.Rectangle((3.45 + -158*1e-3 - 0.3, 0),
								 0.04,0.078, linewidth=1, edgecolor='magenta', facecolor='magenta')
		ax.add_patch(rect)
		ax.set_xlim(-0.6, 3.5)
		ax.set_ylim(0,.4)
		return ax

	def initialize_field_lines(self):
		line = self.ax.plot([],[])[0]
		return [line]

	def clear_field_lines(self):
		for line in self.field_lines:
			line.remove()

	def update_field_lines(self, field_data):
		self.clear_field_lines()
		solutions = field_data['solutions']
		solution_cathode = field_data['solution_cathode']

		for solution in solutions:
			line = self.ax.plot(solution[0], solution[1], **self.field_line_plot_params)[0]
			self.field_lines.append(line)
		for solution in solution_cathode:
			line = self.ax.plot(solution[0], solution[1], **self.cathode_field_line_plot_params)[0]
			self.field_lines.append(line)
		self.draw()
