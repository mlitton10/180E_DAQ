from gui_tester.devices.base import Device


class WaveSurfer(Device):

    def __init__(self, ip: str):
        self.ip = ip
        self.connected = False

    def connect(self):
        # Establish network connection
        ...

    def disconnect(self):
        ...

    def is_connected(self):
        return self.connected