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
from gui_tester.widgets.experiment_page_widgets.workers.file_handler import HDF5FileHandler


class ExperimentWorker(Worker):

    # Human-readable state information
    status_changed = pyqtSignal(str)

    # Overall progress: 0-100
    progress_changed = pyqtSignal(int)

    # More detailed progress information
    position_changed = pyqtSignal(int, int, float)

    # Acquisition data for the GUI/plot
    data_ready = pyqtSignal(object)

    # Experiment lifecycle
    started = pyqtSignal()
    finished = pyqtSignal()
    stopped = pyqtSignal()

    # Fatal error
    error = pyqtSignal(str)

    def __init__(self, config: ExperimentConfig):
        super().__init__()

        self.config = config

        self.probe_drive = ProbeDriveXY(config.motor_ip)
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
            if nowx!=pos[1] or nowy!=pos[2]:
                # enable motor
                self.probe_drive.enable()

                # move to next position
                self.probe_drive.move_to_position(*position)
                self.updated_position.emit(*position)
                nowx, nowy = (position[1], position[2])
                x_encoder, y_encoder = self.probe_drive.current_probe_position()
                self.updated_position.emit(x_encoder, y_encoder)

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
            self.position_changed.emit(
                index + 1,
                total_positions,
                position,
            )

            progress = int(
                100 * (index + 1) / total_positions
            )

            self.progress_changed.emit(progress)

        self._set_status("Experiment complete")

        self.progress_changed.emit(100)

    def _connect_devices(self) -> None:

        self._set_status("Connecting to motor...")
        self.probe_drive.connect()

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
            finally:
                self.probe_drive.disconnect()

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



class DataRunThread(QRunnable):

    def __init__(self, hdf5_filename: Path, position_list,n_shots, channel_description, ip_addrs):
        super(DataRunThread, self).__init__()

        self.hdf5_filename = hdf5_filename
        self.positions = position_list
        self.num_duplicate_shots = n_shots
        self.channel = channel_description
        self.ip_addrs = ip_addrs

        self.probe_drive = ProbeDriveXY(x_ip_addr=self.ip_addrs['x'], y_ip_addr=self.ip_addrs['y'])
        self.file = HDF5FileHandler(hdf5_filename)
        self.scope = WaveSurfer(ip_addrs['scope'])

    def get_channel_description(self, tr) -> str:
        """ callback function to return a string containing a description of the data in each recorded channel """

        #user: assign channel description text here to override the default:
        if tr == 'C1':
            return self.channel["C1"]
        if tr == 'C2':
            return self.channel["C2"]
        if tr == 'C3':
            return self.channel["C3"]
        if tr == 'C4':
            return self.channel["C4"]

        # otherwise, program-generated default description strings follow
        if tr in EXPANDED_TRACE_NAMES.keys():
            return 'no entered description for ' + EXPANDED_TRACE_NAMES[tr]

        return '**** get_channel_description(): unknown trace indicator "'+tr+'". How did we get here?'


    def run(self):

        self.file.write_meta_data(self.positions,
                                  self.num_duplicate_shots,
                                  self.scope.idn_string)

        n_times = self.scope.max_samples()

        traces = self.scope.displayed_traces()

            ######### BEGIN MAIN ACQUISITION LOOP #########
        print('starting acquisition loop at', time.ctime())
        acquisition_loop_start_time = time.time()

        nowx, nowy = (-999, -999) # why not just get the current position
        for pos in self.positions:
            # prevent motor from enabling/disabling when taking data at the same position
            # this stops the motor noise from being picked up by the data in between shots
            if nowx!=pos[1] or nowy!=pos[2]:
                # enable motor
                self.probe_drive.enable()

                # move to next position
                print('position index =', pos[0], '  x =', pos[1], '  y =', pos[2], end='\n')
                self.probe_drive.move_to_position(pos[1], pos[2])
                self.signals.updated_position.emit(pos[1], pos[2])
                nowx, nowy = (pos[1], pos[2])
                x_encoder, y_encoder = self.probe_drive.current_probe_position()
                self.signals.updated_position.emit(x_encoder, y_encoder)

                # Disable the motor current output when taking the data
                self.probe_drive.disable()


            if pos[0] > 1:
                print ('Estimated remaining time:%6.2f'%((len(self.positions) - pos[0]) * (time.time()-acquisition_loop_start_time)/pos[0] / 3600))
            else:
                print ('')

            dataset, hdr_data = self.scope.acquire_displayed_traces()
            time_ds = self.scope.time_array()[0:n_times]
            for tr in traces:
                dataset[tr]['description'] = self.get_channel_description(tr)  # callback arg to the current function
                dataset[tr]['recorded'] = True
                dataset[tr]['shots per position'] = self.pos_param["num_shots"]
            self.file.append(pos, dataset, hdr_data, time_ds)

            # Show plot traces on GUI
            try:
                self.scope.screen_dump()
                self.signals.new_screen_dump.emit()
            except:
                print ('Unable to grab screen due to unknown Error')
                continue

            self.signals.finished_position.emit(x_encoder, y_encoder)
            ######### END MAIN ACQUISITION LOOP #########

        f.close()  # close the HDF5 file

        self.signals.finished.emit()
            #done
