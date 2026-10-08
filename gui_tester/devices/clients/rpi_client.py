import socket
import time

from gui_tester.devices.clients.base import DeviceClient

class MagnetError(Exception):
    pass

class PiClient(DeviceClient):
    def __init__(self, host_ip: str, port=5025, timeout=3.0, stale_after=2.0, verbose = True):
        self.host_ip, self.port, self.timeout, self.stale_after = host_ip, port, timeout, stale_after

        self.hello = None
        self._status = None
        self._socket = None
        self._lock = threading.Lock()
        self._cv = threading.Condition()
        self._alive = None
        self._status_rx = None


        self.connected = False
        self.connection = self.connect()

    def connect(self):
        self._socket = socket.create_connection(
            (self.host_ip, self.port),
            timeout=self.timeout,
        )
        self._socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self._socket.settimeout(None)
        self._alive = True
        threading.Thread(self._reader, daemon=True).start()
        deadline = time.monotonic() + self.timeout
        with self._cv:
            while self.hello is None:
                if not self._cv.wait(deadline - time.monotonic()) or not self._alive:
                    self.close()
                    raise MagnetError("No hello response from server")

    def close(self):
        self._alive = False
        if self._socket:
            try:
                self._socket.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
        self._socket.close()
        self._socket = None

    __enter__ = connect
    def __exit__(self, *exc):
        self.close()

    @property
    def connected(self):
        return self._alive and (time.monotonic() - self._status_rx) < self.stale_after

    def _reader(self):
        try:
            for line in self._socket.makefile('r', encoding='utf-8'):
                msg = json.loads(line)
                with self._cv:
                    kind = msg.get('type')
                    if kind == 'hello':
                        self.hello = msg
                    elif kind == 'status':
                        self._status, self._status_rx = msg, time.monotonic()
                    else:
                        self._reply = msg
                    self._cv.notify_all()
        except (OSError, ValueError):
            pass
        finally:
            with self._cv:
                self._alive = False
                self._cv.notify_all()

    def _command(self, command: dict):
        with self._lock:

            if not self._alive:
                raise MagnetError("No connection")
            with self._cv:
                self._reply = None
            self._socket.sendall((json.dumps(command) + '\n').encode())
            deadline = time.monotonic() + self.timeout
            with self._cv:
                while self._reply is None:
                    if not self._alive:
                        raise MagnetError("Lost connection")
                    if not self._cv.wait(deadline - time.monotonic()):
                        raise MagnetError("Timed out waiting for response")
                reply = self._reply
            if reply.get("type") == 'error':
                raise MagnetError(reply["error"])
            return reply

    def set(self, psu: str, current: float):
        return self._command({'cmd': "set", 'psu': psu, 'current': float(current)})

    def set_many(self, setpoints: dict):
        return self._command({'cmd': "set_many", 'setpoints': {ch: float(current) for ch, current in setpoints.items()}})

