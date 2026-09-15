from dataclasses import dataclass
from pathlib import Path

from gui_tester.devices.probe_drive import ProbeDriveXY


@dataclass
class QuickExperimentRunConfig:
    scope_ip: str
    output_path: str | Path
    positions: list[tuple]
    num_duplicate_shots: int
    channel_description: dict[str, str]
    probe_drive: ProbeDriveXY