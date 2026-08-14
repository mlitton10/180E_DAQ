import RPi.GPIO as GPIO
from time import sleep



class PWMPin:
    def __init__(self, pin_number, frequency):
        self.controlPin = pin_number
        self.frequency = frequency

        self.pwm = GPIO.PWM(self.controlPin, self.frequency)

    def _initialize_pin(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(controlPin, GPIO.OUT)
        self.pwm.start(0)
        pass

    def set_duty_cycle(self, duty_cycle):
        self.pwm.ChangeDutyCycle(duty_cycle)
