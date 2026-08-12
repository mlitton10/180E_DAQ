import sys

from PyQt5.QtWidgets import QMainWindow, QTabWidget, QApplication, QDesktopWidget
from gui_tester.utils.file_util import list_data_files
from gui_tester.widgets.MagnetControl import MagnetWidget
from gui_tester.widgets.experimentcontrol import ExperimentControl
from gui_tester.widgets.magnet_control_widgets.workers.MagnetGeometry import MagnetGeometry


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
	app = QApplication(sys.argv)

	machine_configuration_dir = "./data/machine_configurations/"
	magnet_geometry_dir = "./magnet_control_widgets/data/"
	machine_config_paths = list_data_files(machine_configuration_dir)
	window = MainWindow(machine_config_paths, magnet_geometry_dir)

	window.show()

	sys.exit(app.exec_())


if __name__ == '__main__':

	main()