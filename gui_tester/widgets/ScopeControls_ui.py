import os.path

dir_path=os.path.dirname(os.path.realpath(__file__))
version_number="03/01/2018 12:37pm"			# update this when a change has been made

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class ScopeChannel(QGroupBox):
	def __init__(self):
		super().__init__()
		self.titleLabel = QLabel("Enter channel descriptions")
		self.c1 = UserSettingsRow("Channel 1:")
		self.c2 = UserSettingsRow("Channel 2:")
		self.c3 = UserSettingsRow("Channel 3:")
		self.c4 = UserSettingsRow("Channel 4:")

		self.build_layout()

	def build_layout(self):
		sc_layout = QGridLayout()
		sc_layout.addWidget(self.titleLabel, 0, 0, 1, 2)
		sc_layout.addWidget(self.c1Label, 1, 0)
		sc_layout.addWidget(self.c2Label, 2, 0)
		sc_layout.addWidget(self.c3Label, 3, 0)
		sc_layout.addWidget(self.c4Label, 4, 0)
		sc_layout.addWidget(self.c1Input, 1, 1)
		sc_layout.addWidget(self.c2Input, 2, 1)
		sc_layout.addWidget(self.c3Input, 3, 1)
		sc_layout.addWidget(self.c4Input, 4, 1)
		self.setLayout(sc_layout)