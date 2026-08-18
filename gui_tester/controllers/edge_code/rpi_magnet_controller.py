import argparse

import RPi.GPIO as GPIO
from time import sleep
import json
import socket
import threading
import time

FREQ = 1000.0
I1_MAX = 10
I2_MAX = 10
I3_MAX = 100

HOST = "0.0.0.0"
PORT = 5000


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
    def __init__(self, pin_number, max_current: float) -> None:
        super().__init__(pin_number, FREQ)

        self.max_current = max_current

    def _convert_current_to_duty_cycle(self, current: float) -> float:
        return 100 * current/self.max_current

    def set_current(self, current):
        duty_cycle = self._convert_current_to_duty_cycle(current)
        self.set_duty_cycle(duty_cycle)


class Controller:
    def __init__(self):
        self.lock = threading.Lock()


        self.outputs = [0.0, 0.0, 0.0]
        self.running = True

    def set_outputs(self, values):
        if len(values) != 3:
            raise ValueError("Expected three output values")

        values = [float(v) for v in values]

        if not all(0.0 <= v <= 100.0 for v in values):
            raise ValueError("Output values must be between 0 and 100")

        with self.lock:
            self.outputs = values

            # Replace these with your actual PWM calls.
            self.set_pwm(0, values[0])
            self.set_pwm(1, values[1])
            self.set_pwm(2, values[2])

    def set_pwm(self, channel, duty):
        print(f"PWM {channel}: {duty}%")

    def stop(self):
        with self.lock:
            self.outputs = [0.0, 0.0, 0.0]

            for channel in range(3):
                self.set_pwm(channel, 0.0)

    def get_status(self):
        with self.lock:
            return {
                "outputs": self.outputs.copy(),
                "running": self.running,
            }


controller = Controller()


def handle_command(command):
    name = command.get("command")

    if name == "set_outputs":
        controller.set_outputs(command["values"])

        return {
            "status": "ok",
            "outputs": controller.get_status()["outputs"],
        }

    elif name == "get_status":
        return {
            "status": "ok",
            **controller.get_status(),
        }

    elif name == "stop":
        controller.stop()

        return {
            "status": "ok",
            "outputs": controller.get_status()["outputs"],
        }

    else:
        return {
            "status": "error",
            "message": f"Unknown command: {name}",
        }


def handle_client(conn, address):
    print(f"Connected: {address}")

    buffer = ""

    try:
        while True:
            data = conn.recv(4096)

            if not data:
                break

            buffer += data.decode("utf-8")

            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)

                if not line.strip():
                    continue

                try:
                    command = json.loads(line)
                    response = handle_command(command)

                except Exception as exc:
                    response = {
                        "status": "error",
                        "message": str(exc),
                    }

                response_data = (
                    json.dumps(response) + "\n"
                ).encode("utf-8")

                conn.sendall(response_data)

    finally:
        conn.close()
        print(f"Disconnected: {address}")


def main():
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1,
    )

    server.bind((HOST, PORT))
    server.listen(5)

    print(f"Controller listening on {HOST}:{PORT}")

    try:
        while True:
            conn, address = server.accept()

            thread = threading.Thread(
                target=handle_client,
                args=(conn, address),
                daemon=True,
            )

            thread.start()

    except KeyboardInterrupt:
        print("Shutting down")

    finally:
        controller.stop()
        server.close()


if __name__ == "__main__":
    main()







def main():
    pass

if __name__ == "__main__":
    main()