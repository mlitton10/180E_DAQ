import sys

from PyQt5.QtWidgets import QMainWindow, QTabWidget, QApplication
from gui_tester.utils.file_util import list_data_files
from gui_tester.widgets.MagnetControl import MagnetWidget
from gui_tester.widgets.experimentcontrol import ExperimentControl


class MainWindow(QMainWindow):
	def __init__(self, machine_config_paths):
		super(MainWindow, self).__init__()

		self.setWindowTitle("DAQ and Controls")

		tabs = QTabWidget()
		tabs.addTab(ExperimentControl(machine_config_paths), "ExperimentControl")
		tabs.addTab(MagnetWidget(), "Magnets")

		self.setCentralWidget(tabs)

def main():
	app = QApplication(sys.argv)

	machine_configuration_dir = "./data/machine_configurations/"
	machine_config_paths = list_data_files(machine_configuration_dir)
	window = MainWindow(machine_config_paths)

	window.show()

	sys.exit(app.exec_())


if __name__ == '__main__':

	main()