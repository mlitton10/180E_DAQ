from __future__ import annotations

import time
from pathlib import Path

import numpy as np
from gui_tester.devices.probe_drive import ProbeDriveXY
from gui_tester.devices.wavesurfer import WaveSurfer
from gui_tester.widgets.basic_templates.generic_worker import Worker

import threading
import traceback
from PyQt6.QtCore import pyqtSignal, pyqtSlot, QObject
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

        self.motor = ProbeDriveXY(config.motor_ip)
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

        self._set_status(
            f"Starting experiment: {total_positions} positions"
        )

        for index, position in enumerate(positions):

            if self.is_stop_requested():
                self.stopped.emit()
                return

            self._set_status(
                f"Moving motor to position {position}"
            )

            self.motor.move_to_position(*position)

            if self.is_stop_requested():
                self.stopped.emit()
                return

            self._set_status(
                f"Acquiring data at position {position}"
            )

            data = self.scope.acquire_trace()

            if self.is_stop_requested():
                self.stopped.emit()
                return

            self._set_status("Writing data...")

            self.writer.append(position, data)

            # Send acquired data to GUI
            self.data_ready.emit(data)

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
        self.motor.connect()

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
                self.motor.disconnect()

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

    def __init__(self, hdf5_filename: Path, pos_param, channel_description, ip_addrs):
        super(DataRunThread, self).__init__()

        self.hdf5_filename = hdf5_filename
        self.pos_param = pos_param
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



    def get_positions(self) -> ([(),(),(),()], numpy.array, numpy.array, numpy.array):
        """ callback function to return the positions array
            This function is baroque because we need to to match the legacy format:
              in particular, we assign the positions array as an array of tuples
        """

        xmax = self.pos_param["xmax"]
        xmin = self.pos_param["xmin"]
        ymax = self.pos_param["ymax"]
        ymin = self.pos_param["ymin"]
        nx = self.pos_param["nx"]
        ny = self.pos_param["ny"]

        xpos = numpy.linspace(xmin,xmax,nx)
        ypos = numpy.linspace(ymin,ymax,ny)

        num_duplicate_shots = self.pos_param["num_shots"]       # number of duplicate shots recorded at the ith location
        num_run_repeats = self.pos_param["num_run"]           # number of times to repeat sequentially over all locations

        # allocate the positions array, fill it with zeros
        positions = numpy.zeros((nx*ny*num_duplicate_shots*num_run_repeats), dtype=[('Line_number', '>u4'), ('x', '>f4'), ('y', '>f4')])

        #create rectangular shape position array
        index = 0
        for repeat_cnt in range(num_run_repeats):
            for y in ypos:
                for x in xpos:
                    for dup_cnt in range(num_duplicate_shots):
                        positions[index] = (index+1, x, y)
                        index += 1

        # print(positions)       # for debugging

        return positions, xpos, ypos, num_duplicate_shots


    def run(self):

        positions, xpos, ypos, num_duplicate_shots = self.get_positions()

        # Create empty position arrays
        if xpos is None:
            xpos = np.array([])
        if ypos is None:
            ypos = np.array([])

        self.file.write_meta_data(positions, xpos, ypos, num_duplicate_shots, self.scope.idn_string)

        n_times = self.scope.max_samples()

        traces = self.scope.displayed_traces()

            ######### BEGIN MAIN ACQUISITION LOOP #########
        print('starting acquisition loop at', time.ctime())
        acquisition_loop_start_time = time.time()

        nowx, nowy = (-999, -999) # why not just get the current position
        for pos in positions:
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
                print ('Estimated remaining time:%6.2f'%((len(positions) - pos[0]) * (time.time()-acquisition_loop_start_time)/pos[0] / 3600))
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
