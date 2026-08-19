import json
import socket

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot


class RaspberryPiController:
    def __init__(self, host: str, port=5000):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        self.socket = socket.create_connection(
            (self.host, self.port),
            timeout=2.0,
        )

    def send_command(self, command):
        if self.socket is None:
            raise RuntimeError("Not connected to Raspberry Pi")

        message = json.dumps(command) + "\n"

        self.socket.sendall(message.encode("utf-8"))

        buffer = ""

        while "\n" not in buffer:
            data = self.socket.recv(4096)

            if not data:
                raise ConnectionError(
                    "Raspberry Pi disconnected"
                )

            buffer += data.decode("utf-8")

        line, _ = buffer.split("\n", 1)

        response = json.loads(line)

        if response.get("status") != "ok":
            raise RuntimeError(
                response.get("message", "Unknown error")
            )

        return response

    def set_outputs(self, output1, output2, output3):
        return self.send_command({
            "command": "set_outputs",
            "values": [
                output1,
                output2,
                output3,
            ],
        })

    def get_status(self):
        return self.send_command({
            "command": "get_status",
        })

    def stop(self):
        return self.send_command({
            "command": "stop",
        })

    def close(self):
        if self.socket is not None:
            self.socket.close()
            self.socket = None


class RaspberryPiWorker(QObject):
    connected = pyqtSignal()
    disconnected = pyqtSignal()
    outputsChanged = pyqtSignal(list)
    error = pyqtSignal(str)
    def __init__(self):
        super().__init__()

    @pyqtSlot()
    def send_command(self):
        pass

class RaspberryPiCurrentControlWorker(RaspberryPiWorker):
    def __init__(self, currents: str):
        super().__init__()
        self.command = currents

    @pyqtSlot()
    def send_command(self):
        try:
            client = RaspberryPiController()

            self.finished.emit({'total_field':total_field,
                                'solutions': solutions,
                                'solution_cathode': solution_cathode,
                                'coordinates': coords})
        except Exception as exc:
            self.error.emit(str(exc))