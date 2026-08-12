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
		self.line_plot_params = {
			'color': 'k',
			'ls': '-',
			'lw': 2
		}

		self.setParent(parent)

		self.ax = self.initialize_canvas(ax)
		self.field_lines = self.initialize_field_lines()

	def initialize_canvas(self, ax):
		ax.grid(True, which='minor')
		ax.set_title("On Axis Field Strength")
		ax.grid(which='both')

		ax.set_xlabel("z [m]")
		ax.set_ylabel("B_z [G]")


		ax.set_xlim(-0.6, 3.5)
		ax.set_ylim(0,)
		return ax

	def initialize_plot(self):
		line = self.ax.plot([],[])[0]
		return [line]

	def clear_plot(self):
		for line in self.field_lines:
			line.remove()

	def update_plot(self, field_data):
		self.clear_plot()
		field = field_data['total_field']['Bz']
		z_space = field_data['coordinates'][0]
		line = self.ax.plot(z_space, field[:, 0] * 1e4, label=r'$r={}$'.format(0), color='k')


		self.draw()