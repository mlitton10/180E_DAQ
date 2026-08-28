import os.path

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QPushButton, QGridLayout
from gui_tester.widgets.basic_templates.TextInputBox import make_form_table, UserDoubleSpinBoxRow, UserSpinBoxRow, \
	DropdownRow
from gui_tester.widgets.basic_templates.basic_application_widget import BasicAppWidget

dir_path=os.path.dirname(os.path.realpath(__file__))
version_number="03/01/2018 12:37pm"			# update this when a change has been made


class PositionControls(BasicAppWidget):
	confirm = pyqtSignal()
	coordinateSystemSelected = pyqtSignal(str)
	def __init__(self):
		super().__init__()
		self.setTitle("Set up DAQ position")

		self.drop_down = DropdownRow("Select Coordinate System: ",
										  ["Cartesian", "Polar"])

		self.xMax = UserDoubleSpinBoxRow("Max x:", suffix=' cm')
		self.xMin = UserDoubleSpinBoxRow("Min x:", suffix=' cm')
		self.yMax = UserDoubleSpinBoxRow("Max y:", suffix=' cm')
		self.yMin = UserDoubleSpinBoxRow("Min y:", suffix=' cm')
		self.nx = UserSpinBoxRow("Nx:")
		self.ny = UserSpinBoxRow("Ny:")

		self.ConfirmButton = QPushButton("Confirm Input",self)

		self.initialize_widget()

	def connect_signals(self):
		self.ConfirmButton.clicked.connect(self.confirm)
		self.drop_down.optionSelected.connect(self.display_coordinates)
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
		layout.addWidget(self.drop_down, 0, 0)
		layout.addWidget(positions_box, 1, 0, 5, 1)

		layout.addWidget(self.ConfirmButton, 6, 0, 1, 1)
		self.setLayout(layout)

	def initialize_widget(self):
		self.build_layout()
		self.connect_signals()

	def collect_parameters(self):
		parameters = {'xmax': float(self.xMax.read_value()), 'xmin': float(self.xMin.read_value()),
					  'ymax': float(self.yMax.read_value()), 'ymin': float(self.yMin.read_value()),
					  'nx': int(self.nx.read_value()), 'ny': int(self.ny.read_value())}
		return parameters

	def current_coordinate_system(self) -> str:
		return self.drop_down.current_option()

	def display_coordinates(self):
		coordinate_system = self.current_coordinate_system()
		if coordinate_system == "Cartesian":
			self.xMax.label.setText("Max x:")
			self.xMin.label.setText("Min x:")
			self.yMax.label.setText("Max y:")
			self.yMin.label.setText(r"Min y:")
			self.nx.label.setText("N_x:")
			self.ny.label.setText("N_y:")

			self.xMax.spin_box.setSuffix(" cm")
			self.xMin.spin_box.setSuffix(" cm")
			self.yMax.spin_box.setSuffix(" cm")
			self.yMin.spin_box.setSuffix(" cm")
		elif coordinate_system == "Polar":
			self.xMax.label.setText("Max r:")
			self.xMin.label.setText("Min r:")
			self.yMax.label.setText("Max theta:")
			self.yMin.label.setText("Min theta:")
			self.nx.label.setText("N_r:")
			self.ny.label.setText("N_theta:")

			self.xMax.spin_box.setSuffix(" cm")
			self.xMin.spin_box.setSuffix(" cm")
			self.yMax.spin_box.setSuffix(" deg.")
			self.yMin.spin_box.setSuffix(" deg.")
		self.coordinateSystemSelected.emit(coordinate_system)