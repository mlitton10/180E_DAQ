import socket
import time

from gui_tester.devices.clients.base import DeviceClient


class MotorClient(DeviceClient):
    MSIPA_CACHE_FN = 'motor_server_ip_address_cache.tmp'
    MOTOR_SERVER_PORT = 7776
    BUF_SIZE = 1024
    # server_ip_addr = '10.10.10.10' # for direct ethernet connection to PC

    # - - - - - - - - - - - - - - - - -
    # To search IP address:
    last_pos = 999
    def __init__(self, ip: str, verbose = True):
        self.ip = ip
        self.connected = False
        self.connection = None
        self._connected = False

    def connect(self):
        retries = 30
        retry_count = 0
        while retry_count < retries:  # Retries added 17-07-11
            try:
                self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ##if timeout is not None:
                ##	#not on windows: socket.settimeout(timeout)
                ##	s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, struct.pack('LL', timeout, 0))
                self.connection.connect((self.ip, self.MOTOR_SERVER_PORT))
                self.connected = True
                return
            except ConnectionRefusedError:
                retry_count += 1
                print('...connection refused, at', time.ctime(), ' Is motor_server process running on remote machine?',
                      '  Retry', retry_count, '/', retries, "on", str(self.ip))
            except TimeoutError:
                retry_count += 1
                print('...connection attempt timed out, at', time.ctime(),
                      '  Retry', retry_count, '/', retries, "on", str(self.ip))

        if retry_count >= retries:
            self.connected = False
            print('Unable to connect to motor at', self.ip)

    def disconnect(self):
        self.connection.close()
        self.connected = False

    def is_connected(self):
        return self.connected

    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, value: bool):
        if not isinstance(value, bool):
            self._connected = False
            return
        self._connected = value

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

