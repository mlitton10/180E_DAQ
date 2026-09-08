import os.path

from gui_tester.widgets.basic_templates.TextInputBox import UserTextRow, make_form_table
from gui_tester.widgets.basic_templates.basic_application_widget import BasicAppWidget

dir_path=os.path.dirname(os.path.realpath(__file__))
version_number="03/01/2018 12:37pm"			# update this when a change has been made


from PyQt6.QtWidgets import QGridLayout


class ScopeChannel(BasicAppWidget):
	def __init__(self):
		super().__init__()
		self.setTitle("Enter channel descriptions")
		self.c1 = UserTextRow("Channel 1:")
		self.c2 = UserTextRow("Channel 2:")
		self.c3 = UserTextRow("Channel 3:")
		self.c4 = UserTextRow("Channel 4:")

		self._initialize_widget()

	def _build_layout(self):
		sc_layout = QGridLayout(self)

		channel_box = make_form_table([self.c1, self.c2, self.c3, self.c4])

		sc_layout.addWidget(channel_box, 0, 0, 3, 1)

	def _connect_signals(self):
		pass

	def _initialize_widget(self):
		self._build_layout()
		self._connect_signals()

	def get_channel_description(self):
		channel_description = {"C1": self.c1.read_value(),
							   "C2": self.c2.read_value(),
							   "C3": self.c3.read_value(),
							   "C4": self.c4.read_value()}
		return channel_description
