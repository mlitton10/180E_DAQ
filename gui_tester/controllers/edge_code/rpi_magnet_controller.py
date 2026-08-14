import RPi.GPIO as GPIO
from time import sleep

controlPin = 35
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(controlPin, GPIO.OUT)

pi_pwm = GPIO.PWM(controlPin, 1000)
pi_pwm.start(0)

sleep(5)

pi_pwm.ChangeDutyCycle(50)

while True:
    sleep(1)
    continue