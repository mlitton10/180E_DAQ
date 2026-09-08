import os.path
from pathlib import Path

from PyQt6.QtCore import QThreadPool
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QGridLayout, QMessageBox, QFileDialog
from gui_tester.widgets.basic_templates.basic_application_tab import ApplicationTab
from gui_tester.widgets.experiment_page_widgets.DeviceSpecification_ui import DeviceSpecification
from gui_tester.widgets.experiment_page_widgets.status_ui import StatusWidget
from gui_tester.widgets.experiment_page_widgets.workers.DataRunWorker import ExperimentWorker
from gui_tester.widgets.experiment_page_widgets.workers.LoadMachineConfig import LoadMachineWorker
from gui_tester.widgets.experiment_page_widgets.MotorMovement_ui import MotorMovement
from gui_tester.widgets.experiment_page_widgets.AcquisitionControls_ui import AcquisitionControls
from gui_tester.widgets.experiment_page_widgets.canvas_ui import MyMplCanvas, compute_point_grid, \
	compute_point_grid_polar
from gui_tester.widgets.experiment_page_widgets.ScopeControls_ui import ScopeChannel
from gui_tester.widgets.experiment_page_widgets.SoftwareVersion_ui import SoftwareVersion
from gui_tester.widgets.experiment_page_widgets.PositionControls_ui import PositionControls

dir_path=os.path.dirname(os.path.realpath(__file__))
version_number="03/01/2018 12:37pm"			# update this when a change has been made

from PyQt6 import QtCore

data_running = False

class ExperimentControl(ApplicationTab):

	def __init__(self, machine_config_paths, device_ips):
		super(ExperimentControl, self).__init__()

		self.device_ips = device_ips

		self.pc = PositionControls()
		self.canvas = MyMplCanvas()
		self.ac = AcquisitionControls()
		self.status = StatusWidget()
		self.sc = ScopeChannel()
		self.ds = DeviceSpecification(machine_config_paths)

		self.x_ip, self.y_ip, self.scope_ip, self.port_ip = self.set_ip_address()

		self.mm = MotorMovement(x_ip_addr = self.x_ip, y_ip_addr = self.y_ip, motor_port= self.port_ip)
		self.mm.set_input_usage(3)
		self.mm.set_steps_per_rev(20000, 20000)

		self.ScopeScreen = QLabel(self)
		self.update_screen_dump()

		self._initialize_tab()

		self.load_file_async(self.ds.current_file())

		self.threadpool = QThreadPool()

		# Set timer to update current probe position and instant motor velocity
		self.timer = QtCore.QTimer(self)
		self.timer.timeout.connect(self.update_current_position)
		self.timer.start(500)

	def set_ip_address(self):
		x_ip = self.device_ips.device_ip("x_motor")
		y_ip = self.device_ips.device_ip("y_motor")
		scope_ip = self.device_ips.device_ip("scope_1")
		port_ip = int(7776)
		return x_ip, y_ip, scope_ip, port_ip

	def _connect_signals(self):

		self.pc.confirm.connect(self.update_geometry)

		self.ac.DataRun.clicked.connect(self.start_data_run)
		self.ac.TestShot.clicked.connect(self.start_test_shot)

		self.ds.fileSelected.connect(self.load_file_async)

	def _build_layout(self):
		layout = QGridLayout(self)
		layout.addWidget(self.canvas, 0, 0, 1, 2)
		layout.addWidget(self.mm, 2, 0, 2, 1)  # motor movement
		layout.addWidget(self.pc, 2, 1, 2, 1)  # position control
		layout.addWidget(self.ac, 2, 2)  # acquisition control
		layout.addWidget(self.sc, 2, 3, 1, 1)  # scope channel comments
		layout.addWidget(self.status, 3, 2)
		layout.addWidget(self.ds, 3, 3)
		layout.addWidget(self.ScopeScreen, 0, 2, 2, 2)

		self.setWindowTitle("180E Data Acquisition System for XY Probe Drives")
		self.resize(1600, 700)

	def _initialize_tab(self):
		self._build_layout()
		self._connect_signals()

	def load_file_async(self, filepath: str):
		# If a load is already running, ignore new requests for simplicity.
		if self.thread is not None and self.thread.isRunning():
			return

		self.ds.setEnabled(False)

		self.run_worker_async(LoadMachineWorker(filepath), self.on_load_finished, self.on_load_failed, self.ds)

	def on_load_finished(self, filepath: str, length: float, radius: float):
		self.canvas.update_machine_radial_outline(radius)
#		self.status_label.setText(f"Loaded {os.path.basename(filepath)}")

	def on_load_failed(self, message: str):
#		self.status_label.setText("Load failed")
		QMessageBox.critical(self, "Load Error", message)

	def update_current_position(self):
		if not data_running:
			xnow, ynow = self.mm.current_probe_position()
			self.canvas.update_probe(xnow, ynow)
			self.mm.display_current_position()
		else:
			pass

	def update_current_position_during_data_run(self, xnow, ynow):
		if data_running:
			self.canvas.update_probe(xnow, ynow)
			self.mm.current_position_display.update_text("(" + str(round(xnow, 2)) + " ," + str(round(ynow, 2)) +")")
		else:
			print("Why is this called when data_running == False ?")

	def update_screen_dump(self):
		pixmap = QPixmap("scope_screen_dump.png")
		#self.pixmapscaled = self.pixmap.scaledToHeight(800) #Rescale the picture to fit the screen. However this makes the picture from a HD scope blurry.
		self.ScopeScreen.setPixmap(pixmap)

	def mark_finished_positions(self, x, y):
		if data_running:
			x_done = x
			y_done = y
			self.canvas.update_finished_positions(x_done, y_done)
		else:
			print("Why is this called when data_running == False ?")

	def display_current_speed(self) -> None:
		self.mm.display_current_speed()

	def update_parameters(self) -> dict[str, float | int]:
		parameters = self.pc.collect_parameters()
		return parameters

	def retrieve_coordinate_system(self) -> str:
		coordinate_system = self.pc.current_coordinate_system()
		return coordinate_system

	def update_geometry(self):
		param = self.update_parameters()
		coordinate_system = self.retrieve_coordinate_system()
		if coordinate_system == "Cartesian":
			X, Y = compute_point_grid(param)
			self.canvas.update_figure(X, Y)
		elif coordinate_system == "Polar":
			X, Y = compute_point_grid_polar(param)
			self.canvas.update_figure(X, Y)


	def update_channel_information(self):
		channel_description = self.sc.get_channel_description()
		return channel_description

	def start_data_run(self):
		# start data_run threading
		file_path, _ = QFileDialog.getSaveFileName(
			self,
			"Save Experiment Data",
			"",
			"HDF5 Files (*.h5);;All Files (*)",
		)

		# User cancelled the dialog
		if not file_path:
			return

		output_path = Path(file_path)

		pos_param = self.update_parameters()
		pos_param["num_shots"] = self.ac.num_shots.value()
		pos_param["num_run"] = self.ac.num_run.value()

		channel_description = self.update_channel_information()

		ip_addrs = {'x': self.x_ip, 'y': self.y_ip, 'scope': self.scope_ip}
		data_run = ExperimentWorker(output_path, self.mm, pos_param, channel_description, ip_addrs)
		self.run_worker_async(data_run, self.data_run_finished, self.acquisition_canceled,
							  [self.pc,
							   self.ac,
							   self.sc,
							   self.mm])

		data_run.finished.connect(self.data_run_finished)
		data_run.cancel.connect(self.acquisition_canceled)
		data_run.updated_position.connect(self.update_current_position_during_data_run)
		data_run.finished_position.connect(self.mark_finished_positions)
		data_run.new_screen_dump.connect(self.update_screen_dump)
		self.threadpool.start(data_run)

	def acquisition_canceled(self):
		QMessageBox.about(self, "Acquisition Status", "Data acquisition cancelled.")
		self.enable_all_controls()

	def data_run_finished(self):
		QMessageBox.about(self, "Acquisition Status", "Data acquisition complete.")
		self.enable_all_controls()
		self.canvas.clear_visited_probe_position()
		self.canvas.initialize_visited_points()

	def test_shot_finished(self):
		QMessageBox.about(self, "Take Test Shot", "Test shot is finished.")
		self.enable_all_controls()

	def freeze_all_controls(self):
		global data_running
		data_running = True
		self.pc.setEnabled(False)
		self.ac.setEnabled(False)
		self.sc.setEnabled(False)
		self.mm.MoveButton.setEnabled(False)
		self.mm.SetZero.setEnabled(False)
		self.mm.SetVelocity.setEnabled(False)
		self.mm.velocityButton.setEnabled(False)

	def enable_all_controls(self):
		global data_running
		data_running = False
		self.pc.setEnabled(True)
		self.ac.setEnabled(True)
		self.sc.setEnabled(True)
		self.mm.MoveButton.setEnabled(True)
		self.mm.SetZero.setEnabled(True)
		self.mm.SetVelocity.setEnabled(True)
		self.mm.velocityButton.setEnabled(True)


	def start_test_shot(self):
		ip_addrs = {'scope': self.scope_ip}
		test_shot = TestShotThread(ip_addrs)
		test_shot.signals.finished.connect(self.test_shot_finished)
		test_shot.signals.new_screen_dump.connect(self.update_screen_dump)
		self.threadpool.start(test_shot)


	def file_quit(self):
		self.close()
