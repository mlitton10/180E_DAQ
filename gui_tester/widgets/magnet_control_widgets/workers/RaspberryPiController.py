import json
import socket

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot


class RaspberryPiController(QObject):
    connected = pyqtSignal()
    disconnected = pyqtSignal()
    statusReceived = pyqtSignal(str)
    failed = pyqtSignal(str)
    def __init__(self, host: str, port=5000):
        super().__init__()
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        try:
            self.socket = socket.create_connection(
                (self.host, self.port),
                timeout=2.0,
            )
            self.connected.emit()
        except Exception as exc:
            self.failed.emit(str(exc))

    def _send_command(self, command):
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

    @pyqtSlot(float, float, float)
    def set_outputs(self, output1, output2, output3):
        if self.socket is None:
            self.failed.emit("Not connected to Raspberry Pi")
            return
        try:
            self._send_command({
                "command": "set_outputs",
                "values": [
                    output1,
                    output2,
                    output3,
                ],
            })
        except Exception as exc:
            self.failed.emit(str(exc))
            self._disconnect()

    @pyqtSlot()
    def get_status(self):
        if self.socket is None:
            self.failed.emit("Not connected to Raspberry Pi")
        try:
            response = self._send_command({
                "command": "get_status",
            })
            self.statusReceived.emit(response)
        except Exception as exc:
            self.failed.emit(str(exc))
            self._disconnect()

    @pyqtSlot()
    def stop(self):
        if self.socket is None:
            self.failed.emit("Not connected to Raspberry Pi")
        try:
            self._send_command({
                "command": "stop",
            })
        except Exception as exc:
            self.failed.emit(str(exc))
            self._disconnect()

    def _disconnect(self):
        if self.socket is not None:
            self.socket.close()
            self.socket = None
        self.disconnected.emit()
