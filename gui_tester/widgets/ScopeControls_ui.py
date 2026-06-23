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
		self.setTitle("Enter channel descriptions")
		self.c1 = UserSettingsRow("Channel 1:")
		self.c2 = UserSettingsRow("Channel 2:")
		self.c3 = UserSettingsRow("Channel 3:")
		self.c4 = UserSettingsRow("Channel 4:")

		self.build_layout()

	def build_layout(self):
		sc_layout = QGridLayout(self)

		channel_box = make_form_table([self.c1, self.c2, self.c3, self.c4])

		sc_layout.addWidget(channel_box, 0, 0, 3, 1)
