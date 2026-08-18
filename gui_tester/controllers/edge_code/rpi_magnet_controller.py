import argparse

import RPi.GPIO as GPIO
from time import sleep

FREQ = 1000.0
I1_MAX = 10
I2_MAX = 10
I3_MAX = 100

def arg_parser() -> list[float]:
    parser = argparse.ArgumentParser()
    parser.add_argument("I1", type=float)
    parser.add_argument("I2", type=float)
    parser.add_argument("I3", type=float)

    args = parser.parse_args()

    return [args.I1, args.I2, args.I3]

class PWMPin:
    def __init__(self, pin_number: int, frequency: float) -> None:
        self.controlPin = pin_number
        self.frequency = frequency

        self.pwm = GPIO.PWM(self.controlPin, self.frequency)
        self._initialize_pin()

    def _initialize_pin(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.controlPin, GPIO.OUT)
        self.pwm.start(0)
        pass

    def set_duty_cycle(self, duty_cycle: float | int) -> None:
        self.pwm.ChangeDutyCycle(duty_cycle)


class PSUController(PWMPin):
    def __init__(self, pin_number, current: float, max_current: float) -> None:
        super().__init__(pin_number, FREQ)

        self.current = current

    def convert_current_to_duty_cycle(self, duty_cycle: float) -> float:







def main():
    pass

if __name__ == "__main__":
    main()