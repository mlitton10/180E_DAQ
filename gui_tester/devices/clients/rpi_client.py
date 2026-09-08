import socket
import time

from gui_tester.devices.clients.base import DeviceClient


class PiClient(DeviceClient):
    def __init__(self, ip: str, verbose = True):
        self.ip = ip
        self.connected = False
        self.connection = self.connect()

    def connect(self):
        try:
            self.socket = socket.create_connection(
                (self.host, self.port),
                timeout=2.0,
            )
            self.connected.emit()
        except Exception as exc:
            self.failed.emit(str(exc))

    def disconnect(self):
        self.connection.close()
        self.connected = False

    def is_connected(self):
        return self.connected

    def send_command(self, command:str):
        if not self.connected:
            con_res = self.connect()
            if con_res is None:
                raise ConnectionRefusedError("Unable to connect to motor server at", self.ip)

        message = bytearray(command, encoding='ASCII')
        buf = bytearray(2)
        buf[0] = 0
        buf[1] = 7
        for i in range(len(message)):
            buf.append(message[i])
        buf.append(13)

        self.connection.send(buf)

        buf_size = 1024
        data = self.connection.recv(buf_size)
        return_text = data.decode('ASCII')
        return return_text

