#
#
# This graphic user interface allows user to
# (1) set up data point positions, channel description and start data acquisition
#     (by calling Data_Run_2D.py or Data_Run_3D.py)
# (2) control the motor (by calling Motor_Control_2D.py or Motor_Control_3D.py)
# (3) view graphic display of the current probe position and data point positions in the chamber
#
#
# Author: Yuchen Qian
# Oct 2017
#

import sys
import os.path
from widgets.MotorMovement_ui import MotorMovement
from widgets.AcquisitionControls_ui import AcquisitionControls
from widgets.canvas_ui import MyMplCanvas
from widgets.AxisConrols_ui import AxisControls
from widgets.ScopeControls_ui import ScopeChannel
from widgets.SoftwareVersion_ui import SoftwareVersion
from widgets.PositionControls_ui import PositionControls

dir_path=os.path.dirname(os.path.realpath(__file__))
version_number="03/01/2018 12:37pm"			# update this when a change has been made

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

data_running = False
#############################################################################################
#############################################################################################



class Window(QWidget):

	def __init__(self):
		super(Window, self).__init__()

		self.update = None
		self.pc = PositionControls()
		self.canvas = MyMplCanvas()
		self.ac = AcquisitionControls()
		self.axc = AxisControls()
		self.sv = SoftwareVersion()
		self.sc = ScopeChannel()
		self.x_ip = "192.168.0.70"
		self.y_ip = "192.168.0.80"
		self.scope_ip = "192.168.0.60"
		self.port_ip = int(7776)
		self.mm = MotorMovement(x_ip_addr = self.x_ip, y_ip_addr = self.y_ip, motor_port= self.port_ip)
		self.mm.set_input_usage(3)
		self.mm.set_steps_per_rev(20000, 20000)

		self.axc.xupInput.valueChanged.connect(self.axis_change)
		self.axc.yupInput.valueChanged.connect(self.axis_change)
		self.axc.xlowInput.valueChanged.connect(self.axis_change)
		self.axc.ylowInput.valueChanged.connect(self.axis_change)

		self.pc.ConfirmButton.clicked.connect(self.update_geometry)

		self.ac.DataRun.clicked.connect(self.start_data_run)
		self.ac.TestShot.clicked.connect(self.start_test_shot)


		self.ScopeScreen = QLabel(self)
		self.update_screen_dump()


		layout = QGridLayout()
		layout.addWidget(self.canvas, 0, 0, 1, 2)
		layout.addWidget(self.axc, 1, 0, 1, 2)			#axes control
		layout.addWidget(self.mm, 2, 0, 2, 1)					#motor movement
		layout.addWidget(self.pc, 2, 1, 2, 1)					#position control
		layout.addWidget(self.ac, 2, 2)					#acquisition control
		layout.addWidget(self.sc, 2, 3, 1, 1)					#scope channel comments
		layout.addWidget(self.sv, 3, 2)
		layout.addWidget(self.ScopeScreen, 0, 2 , 2, 2)
		self.setLayout(layout)

		self.setWindowTitle("180E Data Acquisition System for XY Probe Drives")
		self.resize(1600, 700)

		self.threadpool = QThreadPool()

		# Set timer to update current probe position and instant motor velocity
		self.timer = QtCore.QTimer(self)
		self.timer.timeout.connect(self.update_current_position)
		self.timer.start(500)


	def axis_change(self):
		xup = self.axc.xupInput.value()
		yup = self.axc.yupInput.value()
		xlow = self.axc.xlowInput.value()
		ylow = self.axc.ylowInput.value()
		self.canvas.update_axis(xup,yup,xlow,ylow)


	def update_current_position(self):
		if not data_running:
			xnow, ynow = self.mm.current_probe_position()
			self.canvas.point.remove()
			self.canvas.update_probe(xnow, ynow)
			self.mm.current_position_display.update_text("(" + str(round(xnow, 2)) + " ," + str(round(ynow, 2)) +")")

		else:
			pass


	def update_current_position_during_data_run(self, xnow, ynow):
		if data_running:
			xnow = xnow
			ynow = ynow
			self.canvas.point.remove()
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
			self.canvas.visited_points.remove()
			self.canvas.update_finished_positions(x_done, y_done)
		else:
			print("Why is this called when data_running == False ?")


	def update_current_speed(self):
			speedx, speedy = self.mm.ask_velocity()
			self.velocityInput.setText("(" + str(speedx) + " ," + str(speedy) +")")

	def update_parameters(self):
		parameters = self.pc.collect_parameters()
		self.update = True
		return parameters

	def update_geometry(self):
		param = self.update_parameters()

		if self.update:
			self.canvas.matrix.remove()
			self.canvas.update_figure(param)
		else:
			pass

	def update_channel_information(self):
		channel_description = self.sc.get_channel_description()
		return channel_description

	def start_data_run(self):
		# start data_run threading
		self.hdf5_filename = None

		pos_param = self.update_parameters()
		pos_param["num_shots"] = self.ac.num_shots.value()
		pos_param["num_run"] = self.ac.num_run.value()

		channel_description = self.update_channel_information()

		ip_addrs = {'x': self.x_ip, 'y': self.y_ip, 'scope': self.scope_ip}

		data_run = DataRunThread(self.hdf5_filename, pos_param, channel_description, ip_addrs)
		self.freeze_all_controls()
		data_run.signals.finished.connect(self.data_run_finished)
		data_run.signals.cancel.connect(self.acquisition_canceled)
		data_run.signals.updated_position.connect(self.update_current_position_during_data_run)
		data_run.signals.finished_position.connect(self.mark_finished_positions)
		data_run.signals.new_screen_dump.connect(self.update_screen_dump)
		self.threadpool.start(data_run)

	def acquisition_canceled(self):
		QMessageBox.about(self, "Acquisition Status", "Data acquisition cancelled.")
		self.enable_all_controls()


	def data_run_finished(self):
		QMessageBox.about(self, "Acquisition Status", "Data acquisition complete.")
		self.enable_all_controls()
		self.canvas.visited_points.remove()
		self.canvas.initialize_visited_points()
		# self.canvas.finished_x = []
		# self.canvas.finished_y = []

	def test_shot_finished(self):
		QMessageBox.about(self, "Take Test Shot", "Test shot is finished.")
		self.enable_all_controls()
		# global data_running
		# data_running = False
		# self.pc.setEnabled(True)
		# self.ac.setEnabled(True)
		# self.sc.setEnabled(True)
		# self.mm.setEnabled(True)

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

	def closeEvent(self, ce):
		self.file_quit()



if __name__ == '__main__':

	app = QApplication(sys.argv)
	window = Window()
	window.show()

	sys.exit(app.exec_())
