"""Magnet supply setpoint server for Raspberry Pi.

Listens on TCP for newline-delimited JSON commands. Each setpoint is realised as a
filtered PWM output whose DC level (volts) is the analog control input of an
electromagnet power supply. While any client is connected the server streams its
current setpoints/outputs at --status-hz.

Protocol (one JSON object per line, both directions)
  client -> server
    {"cmd": "set", "channel": "coil1", "volts": 1.25}
    {"cmd": "set_many", "setpoints": {"coil1": 1.25, "coil2": 0.0}}
    {"cmd": "get"}                       (one-off status reply)
    {"cmd": "ping"}
  server -> client
    {"type": "hello", "channels": {...}, "limits": {...}}      on connect
    {"type": "status", "t": <unix>, "setpoints": {...}, "outputs": {...}}  streamed
    {"type": "ack", "cmd": "set", ...}  /  {"type": "error", "error": "..."}

"setpoints" = what was last commanded (clamped); "outputs" = the slew-limited value
currently being driven, which converges to the setpoint.

Run on the Pi:  sudo pigpiod  (once)  then  python3 magnet_server.py --channel coil1=18
Use --mock to test on any machine without GPIO.
"""


import RPi.GPIO as GPIO
import threading
import argparse
import asyncio
import json
import logging
import signal
import socket
import time

log = logging.getLogger("magnet_server")

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
        """
        Hardware layer class. Controls the actual GPIO Pin and sets the PWM using the expected low level hardware parameters.

        """
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
    """
    This bridges the gap between RPI hardware and the PSU we are actually trying to control. It adds a layer on top of the
    GPIO controller that translates the desired currents to a GPIO setpoint that will achieve them.
    """
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

        self.psu_1 = PSUController(19, I1_MAX)
        self.psu_2 = PSUController(20, I2_MAX)
        self.psu_3 = PSUController(21, I3_MAX)

        self.outputs = [0.0, 0.0, 0.0]
        self.running = True

    def set_outputs(self, values):
        if len(values) != 3:
            raise ValueError("Expected three output values")

        values = [float(v) for v in values]

        # need to adjust this
        if not all(0.0 <= v <= 100.0 for v in values):
            raise ValueError("Output values must be between 0 and 100")

        with self.lock:
            self.outputs = values

            # Replace these with your actual PWM calls.
            self.set_pwm(self.psu_1, values[0])
            self.set_pwm(self.psu_2, values[1])
            self.set_pwm(self.psu_3, values[2])

    def set_pwm(self, psu: PSUController, current: float) -> None:
        psu.set_current(current)

    def stop(self):
        with self.lock:
            self.outputs = [0.0, 0.0, 0.0]

            self.set_pwm(self.psu_1, 0.0)
            self.set_pwm(self.psu_2, 0.0)
            self.set_pwm(self.psu_3, 0.0)

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


class MagnetServer:
    def __init__(self, channels, backend, vref, max_volts, slew, status_hz, on_disconnect):
        self.channels = {c.name: c for c in channels}
        self.backend = backend
        self.vref = vref
        self.max_volts = max_volts
        self.slew = slew
        self.status_dt = 1.0 / status_hz
        self.on_disconnect = on_disconnect
        self.clients = set()
        for c in channels:  # always start from zero
            self.backend.set_duty(c.gpio, 0.0)

    # ---- output side -------------------------------------------------
    async def ramp_loop(self, dt=0.02):
        last = time.monotonic()
        while True:
            await asyncio.sleep(dt)
            now = time.monotonic()
            step = self.slew * (now - last)
            last = now
            for c in self.channels.values():
                err = c.setpoint - c.output
                if err == 0.0:
                    continue
                c.output = c.setpoint if abs(err) <= step else c.output + step * (1 if err > 0 else -1)
                self.backend.set_duty(c.gpio, c.output / self.vref)

    def status(self):
        return {
            "type": "status",
            "t": time.time(),
            "setpoints": {n: c.setpoint for n, c in self.channels.items()},
            "outputs": {n: round(c.output, 5) for n, c in self.channels.items()},
        }

    # ---- command handling -------------------------------------------
    def _apply(self, name, volts):
        if name not in self.channels:
            raise ValueError(f"unknown channel '{name}'")
        volts = float(volts)
        if volts != volts:  # NaN
            raise ValueError("volts is NaN")
        if volts < 0 or volts > self.max_volts:
            raise ValueError(f"{volts} V outside 0..{self.max_volts} V")
        self.channels[name].setpoint = volts

    def handle_command(self, msg):
        cmd = msg.get("cmd")
        if cmd == "set":
            self._apply(msg["channel"], msg["volts"])
            return {"type": "ack", "cmd": "set", "channel": msg["channel"], "volts": float(msg["volts"])}
        if cmd == "set_many":
            sp = msg["setpoints"]
            for n, v in sp.items():  # validate everything first: all-or-nothing
                if n not in self.channels:
                    raise ValueError(f"unknown channel '{n}'")
                if not 0 <= float(v) <= self.max_volts:
                    raise ValueError(f"{v} V outside 0..{self.max_volts} V on '{n}'")
            for n, v in sp.items():
                self._apply(n, v)
            return {"type": "ack", "cmd": "set_many", "setpoints": sp}
        if cmd == "get":
            return self.status()
        if cmd == "ping":
            return {"type": "ack", "cmd": "ping"}
        raise ValueError(f"unknown cmd '{cmd}'")

    # ---- networking --------------------------------------------------
    async def status_loop(self, writer):
        while True:
            writer.write((json.dumps(self.status()) + "\n").encode())
            await writer.drain()
            await asyncio.sleep(self.status_dt)

    async def handle_client(self, reader, writer):
        peer = writer.get_extra_info("peername")
        sock = writer.get_extra_info("socket")
        if sock is not None:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        log.info("client connected: %s", peer)
        self.clients.add(writer)
        hello = {"type": "hello", "channels": {n: c.gpio for n, c in self.channels.items()},
                 "limits": {"max_volts": self.max_volts, "slew_v_per_s": self.slew}}
        writer.write((json.dumps(hello) + "\n").encode())
        reporter = asyncio.create_task(self.status_loop(writer))
        try:
            while line := await reader.readline():
                try:
                    reply = self.handle_command(json.loads(line))
                except Exception as e:  # bad JSON, bad values, missing keys
                    reply = {"type": "error", "error": f"{type(e).__name__}: {e}"}
                    log.warning("%s: %s", peer, reply["error"])
                writer.write((json.dumps(reply) + "\n").encode())
                await writer.drain()
        except (ConnectionError, asyncio.IncompleteReadError):
            pass
        finally:
            reporter.cancel()
            self.clients.discard(writer)
            writer.close()
            log.info("client disconnected: %s", peer)
            if self.on_disconnect == "zero" and not self.clients:
                log.warning("no clients left - ramping all setpoints to 0")
                for c in self.channels.values():
                    c.setpoint = 0.0

    async def run(self, host, port):
        ramp = asyncio.create_task(self.ramp_loop())
        server = await asyncio.start_server(self.handle_client, host, port)
        log.info("listening on %s (channels: %s)", [s.getsockname() for s in server.sockets],
                 {n: c.gpio for n, c in self.channels.items()})
        stop = asyncio.Event()
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, stop.set)
        await stop.wait()
        log.info("shutting down: ramping to zero")
        server.close()
        for c in self.channels.values():
            c.setpoint = 0.0
        t_end = time.monotonic() + self.max_volts / self.slew + 2
        while any(c.output > 0 for c in self.channels.values()) and time.monotonic() < t_end:
            await asyncio.sleep(0.05)
        ramp.cancel()
        self.backend.close()


def parse_channel(s):
    name, _, gpio = s.partition("=")
    if not name or not gpio.isdigit():
        raise argparse.ArgumentTypeError("use NAME=GPIO, e.g. coil1=18")
    return Channel(name, int(gpio))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--host", default="0.0.0.0")
    p.add_argument("--port", type=int, default=5025)
    p.add_argument("--channel", action="append", type=parse_channel, required=True,
                   help="NAME=GPIO (repeatable). Hardware PWM pins: 12, 13, 18, 19")
    p.add_argument("--pwm-freq", type=int, default=50_000, help="PWM carrier Hz (match your RC filter)")
    p.add_argument("--vref", type=float, default=3.3, help="PWM high level in volts (filter output at 100%% duty)")
    p.add_argument("--max-volts", type=float, default=3.3, help="hard clamp on commanded control voltage")
    p.add_argument("--slew", type=float, default=0.5, help="max output change in V/s (protects magnets)")
    p.add_argument("--status-hz", type=float, default=10.0)
    p.add_argument("--on-disconnect", choices=["hold", "zero"], default="hold",
                   help="what to do when the last client leaves (default: hold last setpoint)")
    p.add_argument("--mock", action="store_true", help="no GPIO; log duty cycles instead")
    p.add_argument("-v", "--verbose", action="store_true")
    a = p.parse_args()
    logging.basicConfig(level=logging.DEBUG if a.verbose else logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    if a.max_volts > a.vref:
        p.error("--max-volts cannot exceed --vref")
    backend = MockPWM(a.pwm_freq) if a.mock else PigpioPWM(a.pwm_freq)
    srv = MagnetServer(a.channel, backend, a.vref, a.max_volts, a.slew, a.status_hz, a.on_disconnect)
    asyncio.run(srv.run(a.host, a.port))


if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
