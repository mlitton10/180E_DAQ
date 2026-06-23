import os.path

dir_path=os.path.dirname(os.path.realpath(__file__))
version_number="03/01/2018 12:37pm"			# update this when a change has been made

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class MotorMovement(QGroupBox):

	def __init__(self, x_ip_addr = None, y_ip_addr = None, motor_port = None):
		super().__init__()
		self.setTitle("Motor Movement Control")

		self.x_ip_addr = x_ip_addr
		self.y_ip_addr = y_ip_addr
		self.MOTOR_PORT = motor_port

		# (cm) Move probe to absolute position along the shaft counted by motor encoder
		self.xMoveLabel = QLabel("Move x motor to:")
		self.yMoveLabel = QLabel("Move y motor to:")
		self.xMoveInput = QLineEdit()
		self.yMoveInput = QLineEdit()

		# For 3D acquisition, need another feature to move the probe to absolute position.
		# this should be done by calling "move_to_position" function in Motor_Control_3D, with corresponding geometry calculation

		# Set velocity.
		self.xvLabel = QLabel("Set x velocity:")
		self.yvLabel = QLabel("Set y velocity:")
		self.xvInput = QLineEdit()
		self.yvInput = QLineEdit()


		self.MoveButton     = QPushButton("Move Motor", self)
		self.StopNowButton  = QPushButton("BUG don't click", self)
		self.SetZero        = QPushButton("Set Zero", self)
		self.SetVelocity = QPushButton("Set Velocity", self)
		self.MoveButton.clicked.connect(self.move_to_position)
		self.StopNowButton.clicked.connect(self.stop_now)
		self.SetZero.clicked.connect(self.zero)
		self.SetVelocity.clicked.connect(self.set_velocity)

		self.CurposLabel = QLabel("Current probe position (cm, cm):")
		self.CurposInput = QLineEdit(readOnly = True)
		self.velocityButton = QPushButton("Get motor speed (rpm):")
		self.velocityInput = QLineEdit(readOnly = True)
		self.velocityButton.clicked.connect(self.update_current_speed)

		mm_layout = QGridLayout()
		mm_layout.addWidget(self.xMoveLabel, 0, 0)
		mm_layout.addWidget(self.yMoveLabel, 0, 1)
		mm_layout.addWidget(self.xMoveInput, 1, 0)
		mm_layout.addWidget(self.yMoveInput, 1, 1)
		mm_layout.addWidget(self.MoveButton, 1, 2)
		mm_layout.addWidget(self.xvLabel, 2, 0)
		mm_layout.addWidget(self.yvLabel, 2, 1)
		mm_layout.addWidget(self.xvInput, 3, 0)
		mm_layout.addWidget(self.yvInput, 3, 1)
		mm_layout.addWidget(self.SetVelocity, 3, 2)
		mm_layout.addWidget(self.SetZero, 4, 0)
		mm_layout.addWidget(self.StopNowButton, 4, 1)
		mm_layout.addWidget(self.CurposLabel, 5, 0)
		mm_layout.addWidget(self.CurposInput, 5, 1, 1, 2)
		mm_layout.addWidget(self.velocityButton, 6, 0)
		mm_layout.addWidget(self.velocityInput, 6, 1, 1, 2)


		self.setLayout(mm_layout)

#----------------------------------------------------------------------

	def move_to_position(self):
		# Directly move the motor to their absolute position
		try:
			x_pos = float(self.xMoveInput.text())
			y_pos = float(self.yMoveInput.text())
			self.mc.enable()
			self.mc.move_to_position(x_pos, y_pos)
			self.mc.disable()
		except ValueError:
			QMessageBox.about(self, "Error", "Position should be valid numbers.")

	def disable(self):
		self.mc.disable()

	def stop_now(self):
		# Stop motor movement now
		self.mc.stop_now()


	def zero(self):
		zeroreply=QMessageBox.question(self, "Set Zero",
			"You are about to set the current probe position to (0,0). Are you sure?",
			QMessageBox.Yes, QMessageBox.No)
		if zeroreply == QMessageBox.Yes:
			QMessageBox.about(self, "Set Zero", "Probe position is now (0,0).")
			self.mc.set_zero()


	def ask_velocity(self):
		return self.mc.ask_velocity()


	def set_velocity(self):
		xv = self.xvInput.text()
		yv = self.yvInput.text()
		self.mc.set_velocity(xv, yv)


	def current_probe_position(self):
		return self.mc.current_probe_position()

	def update_current_speed(self):
		speedx, speedy = self.ask_velocity()
		self.velocityInput.setText("(" + str(speedx) + " ," + str(speedy) +")")

	def set_input_usage(self, usage):
		self.mc.set_input_usage(usage)

	def set_steps_per_rev(self, stepsx, stepsy):
		self.mc.set_steps_per_rev(stepsx, stepsy)

