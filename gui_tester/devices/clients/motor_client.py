import socket
import time

from gui_tester.devices.clients.base import DeviceClient


class MotorClient(DeviceClient):
    MSIPA_CACHE_FN = 'motor_server_ip_address_cache.tmp'
    MOTOR_SERVER_PORT = 7776
    BUF_SIZE = 1024

    # - - - - - - - - - - - - - - - - -
    # To search IP address:
    last_pos = 999
    def __init__(self, ip: str, verbose = True):
        self.ip = ip
        self.connected = False
        self.connection: socket.socket | None = None

    def connect(self,
                retries: int = 30):
        if self.connected and self.connection is not None:
            return

        last_exception: Exception | None = None

        for attempt in range(1, retries + 1):
            try:
                connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                connection.connect((self.ip, self.MOTOR_SERVER_PORT))

                self.connection = connection
                self.connected = True

                if self.verbose:
                    print(
                        f"Connected to motor at {self.ip}"
                    )

                return
            except (ConnectionRefusedError, TimeoutError, OSError) as exc:
                last_exception = exc

                if self.verbose:
                    print(
                        f"Motor connection attempt "
                        f"{attempt}/{retries} failed: "
                        f"{exc}"
                    )

                try:
                    connection.close()
                except (UnboundLocalError, OSError):
                    pass

                if attempt < retries:
                    time.sleep(retry_delay)

        self.connected = False
        self.connection = None

        raise ConnectionError(
            f"Unable to connect to motor at "
            f"{self.ip}:{self.MOTOR_SERVER_PORT}"
        ) from last_exception


    def disconnect(self):
        if self.connection is not None:
            try:
                self.connection.close()
            except OSError:
                pass
        self.connection = None
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

