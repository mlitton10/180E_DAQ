import os
import os.path
import datetime

dir_path=os.path.dirname(os.path.realpath(__file__))
version_number="03/01/2018 12:37pm"			# update this when a change has been made

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class SoftwareVersion(QGroupBox):
	def __init__(self):
		super().__init__()
		self.mod_timestr=(os.path.getmtime(dir_path))
		self.mod_datetime=datetime.datetime.fromtimestamp(self.mod_timestr).strftime('%Y-%b-%d %H:%M:%S %p')
		self.vLabel = QLabel("Last Modified: ")
		self.lastmodified = QLabel(self.mod_datetime)
		self.version = QLabel("Version: "+version_number)

		sv_layout = QGridLayout()
		sv_layout.addWidget(self.vLabel, 0, 0)
		sv_layout.addWidget(self.lastmodified, 1, 0)
		sv_layout.addWidget(self.version, 2, 0)
		self.setLayout(sv_layout)
