import os.path
import sys

dir_path=os.path.dirname(os.path.realpath(__file__))
version_number="03/01/2018 12:37pm"			# update this when a change has been made

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from gui_tester.widgets.basic_templates.TextInputBox import UserSettingsRow, make_form_table

class MotorMovement(QGroupBox):

	def __init__(self, x_ip_addr = None, y_ip_addr = None, motor_port = None):
		super().__init__()
		self.enabled = None
		self.usage_update = None
		self.setTitle("Motor Movement Control")

		self.x_ip_addr = x_ip_addr
		self.y_ip_addr = y_ip_addr
		self.MOTOR_PORT = motor_port

		# Position inputs
		self.x_position_box = UserSettingsRow("Move x motor to:")
		self.y_position_box = UserSettingsRow("Move y motor to:")

		# Velocity inputs
		self.x_velocity_box = UserSettingsRow("Set x velocity to:")
		self.y_velocity_box = UserSettingsRow("Set y velocity to:")

		self.MoveButton = QPushButton("Move Motor")
		self.StopNowButton = QPushButton("Stop Motor")
		self.SetZero = QPushButton("Set Zero")
		self.SetVelocity = QPushButton("Set Velocity")

		self.MoveButton.clicked.connect(self.move_to_position)
		self.StopNowButton.clicked.connect(self.stop_now)
		self.SetZero.clicked.connect(self.zero)
		self.SetVelocity.clicked.connect(self.set_velocity)

		# Position display
		self.current_position_display = UserSettingsRow("Current probe position (cm, cm):", read_only=False)

		self.velocityButton = QPushButton("Get motor speed (rpm):")
		self.velocityInput = QLineEdit()
		self.velocityInput.setReadOnly(True)
		self.velocityButton.clicked.connect(self.update_current_speed)

		self.build_layout()

	def build_layout(self):
		main_layout = QGridLayout(self)

		position_box = make_form_table([self.x_position_box, self.y_position_box])
		velocity_box = make_form_table([self.x_velocity_box, self.y_velocity_box])
		current_position_box = make_form_table([self.current_position_display])

		main_layout.addWidget(position_box, 0, 0, 1, 1)
		main_layout.addWidget(self.MoveButton, 0, 1)

		main_layout.addWidget(velocity_box, 1, 0, 1, 1)
		main_layout.addWidget(self.SetVelocity, 1, 1)

		main_layout.addWidget(self.SetZero, 2, 0)
		main_layout.addWidget(self.StopNowButton, 2, 1)

		main_layout.addWidget(current_position_box, 3, 0, 1, 1)

		main_layout.addWidget(self.velocityButton, 4, 0)
		main_layout.addWidget(self.velocityInput, 4, 1, 1, 1)
#----------------------------------------------------------------------

	def move_to_position(self):
		# Directly move the motor to their absolute position
		try:
			x_pos = float(self.x_position_box.read_text())
			y_pos = float(self.y_position_box.read_text())

			print(x_pos, y_pos)
			
		except ValueError:
			QMessageBox.about(self, "Error", "Position should be valid numbers.")

	def disable(self):
		print('Disabled')
		self.enabled = False

	def stop_now(self):
		# Stop motor movement now
		print('Stopped')


	def zero(self):
		zeroreply=QMessageBox.question(self, "Set Zero",
			"You are about to set the current probe position to (0,0). Are you sure?",
			QMessageBox.Yes, QMessageBox.No)
		if zeroreply == QMessageBox.Yes:
			QMessageBox.about(self, "Set Zero", "Probe position is now (0,0).")
			print('set zero')


	def ask_velocity(self):
		return 1,1


	def set_velocity(self):
		xv = self.xvInput.text()
		yv = self.yvInput.text()
		print("set velocity: ", xv, ", ", yv)


	def current_probe_position(self):
		return 0,0

	def update_current_speed(self):
		speedx, speedy = self.ask_velocity()
		self.velocityInput.setText("(" + str(speedx) + " ," + str(speedy) +")")

	def set_input_usage(self, usage):
		print('Usage update call:', usage)
		self.usage_update = True

	def set_steps_per_rev(self, stepsx, stepsy):
		print("Set speed: ", stepsx, ", ", stepsy)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MotorMovement()
	window.show()