import os.path

from gui_tester.widgets.basic_templates.TextInputBox import UserTextRow, make_form_table

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
		self.c1 = UserTextRow("Channel 1:")
		self.c2 = UserTextRow("Channel 2:")
		self.c3 = UserTextRow("Channel 3:")
		self.c4 = UserTextRow("Channel 4:")

		self.build_layout()

	def build_layout(self):
		sc_layout = QGridLayout(self)

		channel_box = make_form_table([self.c1, self.c2, self.c3, self.c4])

		sc_layout.addWidget(channel_box, 0, 0, 3, 1)

	def get_channel_description(self):
		channel_description = {"C1": self.c1.read_text(),
							   "C2": self.c2.read_text(),
							   "C3": self.c3.read_text(),
							   "C4": self.c4.read_text()}
		return channel_description