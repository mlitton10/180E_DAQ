import os.path

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QPushButton, QGridLayout
from gui_tester.widgets.basic_templates.TextInputBox import make_form_table, UserDoubleSpinBoxRow, UserSpinBoxRow
from gui_tester.widgets.basic_templates.basic_application_widget import BasicAppWidget

dir_path=os.path.dirname(os.path.realpath(__file__))
version_number="03/01/2018 12:37pm"			# update this when a change has been made


class PositionControls(BasicAppWidget):
	confirm = pyqtSignal()
	def __init__(self):
		super().__init__()
		self.setTitle("Set up DAQ position")

		self.xMax = UserDoubleSpinBoxRow("Max x:")
		self.xMin = UserDoubleSpinBoxRow("Min x:")
		self.yMax = UserDoubleSpinBoxRow("Max y:")
		self.yMin = UserDoubleSpinBoxRow("Min y:")
		self.nx = UserSpinBoxRow("Nx:")
		self.ny = UserSpinBoxRow("Ny:")

		self.ConfirmButton = QPushButton("Confirm Input",self)

		self.initialize_widget()

	def connect_signals(self):
		self.ConfirmButton.clicked.connect(self.confirm)
		pass

	def build_layout(self):
		layout = QGridLayout(self)
		layout.setContentsMargins(0,0,0,0)

		layout.setSpacing(0)
		layout.setVerticalSpacing(0)

		layout.setHorizontalSpacing(0)

		positions_box = make_form_table([self.xMax, self.xMin,
									   self.yMax, self.yMin,
									   self.nx, self.ny])
		positions_box.layout().setContentsMargins(0,0,0,0)
		positions_box.layout().setSpacing(0)
		positions_box.layout().setVerticalSpacing(0)

		layout.addWidget(positions_box, 0, 0, 5, 1)

		layout.addWidget(self.ConfirmButton, 5, 0, 1, 1)
		self.setLayout(layout)

	def initialize_boxes(self):
		self.xMax.update_text("0")
		self.xMin.update_text("0")
		self.yMax.update_text("0")
		self.yMin.update_text("0")
		self.nx.update_text("1")
		self.ny.update_text("1")

	def initialize_widget(self):
		self.build_layout()
		self.connect_signals()

	def collect_parameters(self):
		parameters = {'xmax': float(self.xMax.read_text()), 'xmin': float(self.xMin.read_text()),
					  'ymax': float(self.yMax.read_text()), 'ymin': float(self.yMin.read_text()),
					  'nx': int(self.nx.read_text()), 'ny': int(self.ny.read_text())}
		return parameters
