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
        GPIO.setup(self.controlPin, GPIO.OUT)
        self.pwm.start(0)
        pass

    def set_duty_cycle(self, duty_cycle):
        self.pwm.ChangeDutyCycle(duty_cycle)


class PSUController:
    def __init__(self, pin_numbers, frequency):
        self.psu_1 = PWMPin(pin_numbers[0], frequency)
        self.psu_2 = PWMPin(pin_numbers[1], frequency)
        self.psu_3 = PWMPin(pin_numbers[2], frequency)




