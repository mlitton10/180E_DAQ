import os
import sys

from PyQt6.QtWidgets import QMainWindow, QTabWidget, QApplication, QStyleFactory
from gui_tester.utils.file_util import list_data_files
from gui_tester.widgets.MagnetControl import MagnetWidget, MagnetGeometry
from gui_tester.widgets.experimentcontrol import ExperimentControl


class MainWindow(QMainWindow):
	def __init__(self, machine_config_paths, magnet_geometry_dir):
		super(MainWindow, self).__init__()

		self.setWindowTitle("DAQ and Controls")
		geometry = MagnetGeometry(magnet_geometry_dir)
		tabs = QTabWidget()
		tabs.addTab(ExperimentControl(machine_config_paths), "ExperimentControl")
		tabs.addTab(MagnetWidget(geometry), "Magnets")

		self.setCentralWidget(tabs)

def main():
	style_path = os.path.join(
		"resources",
		"styles",
		"dark.qss"
	)

	app = QApplication(sys.argv)
	app.setStyle(QStyleFactory.create("Fusion"))

	with open(style_path) as f:
		app.setStyleSheet(f.read())

	machine_configuration_dir = "./data/machine_configurations/"
	magnet_geometry_dir = "./data/magnet_information/"
	machine_config_paths = list_data_files(machine_configuration_dir)
	window = MainWindow(machine_config_paths, magnet_geometry_dir)

	window.show()

	sys.exit(app.exec())


if __name__ == '__main__':

	main()