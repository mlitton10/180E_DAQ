import json
from pathlib import Path


class AppConfig:
    def __init__(self, filename: str | Path) -> None:
        with open(filename) as json_file:
            data = json.load(json_file)

        self.devices = data['devices']

    def device_ip(self, name: str) -> str:
        return self.devices[name]