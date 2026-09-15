from __future__ import annotations

import time
from pathlib import Path

import numpy as np
from gui_tester.devices.probe_drive import ProbeDriveXY
from gui_tester.devices.wavesurfer import WaveSurfer
from gui_tester.widgets.basic_templates.generic_worker import Worker

import threading
import traceback
from PyQt6.QtCore import pyqtSignal, pyqtSlot, QObject, QRunnable

from gui_tester.widgets.experiment_page_widgets.schemas.schemas import QuickExperimentRunConfig
from gui_tester.widgets.experiment_page_widgets.workers.file_handler import HDF5FileHandler


class ExperimentWorker(Worker):

    # Human-readable state information
    status_changed = pyqtSignal(str)

    # Overall progress: 0-100
    progress_changed = pyqtSignal(int)

    # More detailed progress information
    position_changed = pyqtSignal(float, float)
    finished_position = pyqtSignal(float, float)

    # Acquisition data for the GUI/plot
    new_screen_dump = pyqtSignal()

    # Experiment lifecycle
    started = pyqtSignal()
    finished = pyqtSignal()
    stopped = pyqtSignal()

    # Fatal error
    error = pyqtSignal(str)

    def __init__(self, config: QuickExperimentRunConfig):
        super().__init__()

        self.config = config

        self.probe_drive = config.probe_drive
        self.scope = WaveSurfer(config.scope_ip)
        self.writer = HDF5FileHandler(config.output_path)

        self._stop_event = threading.Event()

    @pyqtSlot()
    def run(self) -> None:
        """Run the complete experiment."""

        self.started.emit()

        try:
            self._run_experiment()

        except Exception:
            self.error.emit(traceback.format_exc())

        finally:
            self._cleanup()

    def _run_experiment(self) -> None:

        self._validate_configuration()

        self._set_status("Initializing devices...")
        self._connect_devices()

        self._set_status("Opening output file...")
        self.writer.open()

        positions = self.config.positions
        total_positions = len(positions)

        self.writer.write_meta_data(positions,
                                  self.config.num_duplicate_shots,
                                  self.scope.idn_string)

        n_times = self.scope.max_samples()

        traces = self.scope.displayed_traces()

        self._set_status(
            f"Starting experiment: {total_positions} positions"
        )

        nowx, nowy = (-999, -999)  # why not just get the current position
        for index, position in enumerate(positions):

            if self.is_stop_requested():
                self.stopped.emit()
                return

            self._set_status(
                f"Moving motor to position {position}"
            )
            if nowx!=position[0] or nowy!=position[1]:
                # enable motor
                self.probe_drive.enable()

                # move to next position
                self.probe_drive.move_to_position(*position)
                nowx, nowy = (position[0], position[1])
                x_encoder, y_encoder = self.probe_drive.current_probe_position()
                self.position_changed.emit(x_encoder, y_encoder)

                # Disable the motor current output when taking the data
                self.probe_drive.disable()

            if self.is_stop_requested():
                self.stopped.emit()
                return

            self._set_status(
                f"Acquiring data at position {position}"
            )

            dataset, hdr_data = self.scope.acquire_displayed_traces()
            time_ds = self.scope.time_array()[0:n_times]
            for tr in traces:
                dataset[tr]['description'] = self.config.channel_description[tr]  # callback arg to the current function
                dataset[tr]['recorded'] = True
                dataset[tr]['shots per position'] = self.config.num_duplicate_shots
            self.writer.append(position, dataset, hdr_data, time_ds)

            if self.is_stop_requested():
                self.stopped.emit()
                return

            self._set_status("Writing data...")

            # Update position information
            self.finished_position.emit(
                position
            )
            self.scope.screen_dump()
            self.new_screen_dump.emit()

            progress = int(
                100 * (index + 1) / total_positions
            )

            self.progress_changed.emit(progress)

        self._set_status("Experiment complete")

        self.progress_changed.emit(100)

    def _connect_devices(self) -> None:

        self._set_status("Connecting to oscilloscope...")
        self.scope.connect()

    def _validate_configuration(self) -> None:

        if not self.config.positions:
            raise ValueError("No motor positions were provided.")

        if not self.config.motor_ip:
            raise ValueError("Motor IP address is empty.")

        if not self.config.scope_ip:
            raise ValueError("Oscilloscope IP address is empty.")

        if self.config.output_path.suffix.lower() != ".h5":
            raise ValueError(
                "Output file must have an .h5 extension."
            )

    def _cleanup(self) -> None:

        self._set_status("Cleaning up...")

        try:
            self.writer.close()
        finally:
            try:
                self.scope.disconnect()
            except Exception as e:
                print(e)

        self.finished.emit()

    def _set_status(self, message: str) -> None:
        self.status_changed.emit(message)

    def request_stop(self) -> None:
        """
        Thread-safe stop request.

        This intentionally uses threading.Event rather than a Qt
        signal because run() may be inside a blocking hardware call,
        preventing the worker's Qt event loop from processing slots.
        """
        self._stop_event.set()

    def is_stop_requested(self) -> bool:
        return self._stop_event.is_set()

