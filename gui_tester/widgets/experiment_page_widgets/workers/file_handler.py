import time
from pathlib import Path

import h5py
import numpy as np


class HDF5FileHandler:
    def __init__(self, path: Path) -> None:
        self.path = path

        self._pos_ds = None
        self._file = None
        self._positions = None
        self._data = None
        self._hdr_data = None
        self._time = None
        self._acq_grp = None
        self._scope_grp = None
        self._header_grp = None
        self._ctl_grp = None
        self._pos_grp = None

    def open(self):
        self._file = h5py.File(self.path, "w")

        # This assumes every acquisition has the same
        # waveform shape.
        self._data = None


        self._acq_grp = self._file.create_group('/Acquisition')  # /Acquisition
        self._acq_grp.attrs['run_time'] = time.ctime()  # not legacy
        self._scope_grp = self._acq_grp.create_group('LeCroy_scope')  # /Acquisition/LeCroy_scope
        self._header_grp = self._scope_grp.create_group('Headers')  # not legacy

        self._ctl_grp = self._file.create_group('/Control')  # /Control
        self._pos_grp = self._ctl_grp.create_group('Positions')  # /Control/Positions

        self._positions = self._file.create_dataset(
            "positions",
            shape=(0,3),
            maxshape=(None,3),
            dtype="f8",
        )

        pass

    def write_meta_data(self, positions, num_duplicate_shots, idn_string):
        self._pos_ds = self._pos_grp.create_dataset('positions_requested',
                                                    data=positions)
        self._pos_ds.attrs['shotperpos'] = num_duplicate_shots  # not legacy

        self._scope_grp.attrs['ScopeType'] = idn_string

    def append(self, position: float,
               dataset: dict[str, np.ndarray],
               hdr_data,
               time,
               WAVEDESC_SIZE=364) -> None:
        if self._file is None:
            raise RuntimeError("HDF5 file is not open.")

        if self._data is None:
            self._data = {}
            self._hdr_data = {}
            for name, data in dataset.items():
                data = np.asarray(data)
                self._data[name] = self._scope_grp.create_dataset(
                    name,
                    shape=(0, *data.shape),
                    maxshape=(None, *data.shape),
                    dtype=data.dtype,
                )
                self._hdr_data[name] = self._scope_grp.create_dataset(name,
                                                                      shape=(0,),
                                                                      max_shape=(None,),
                                                                      dtype="V%i" % WAVEDESC_SIZE,
                                                                      fletcher32=True,
                                                                      compression='gzip',
                                                                      compression_opts=9)
                self._time = self._scope_grp.create_dataset('time',
                                                 shape=(len(time),),
                                                 fletcher32=True,
                                                 compression='gzip',
                                                 compression_opts=9)

        index = self._data.shape[0]

        self._positions.resize(index + 1, axis=0)
        self._positions[index] = position
        for name, data in dataset.items():
            self._data[name].resize(index + 1, axis=0)
            self._data[name][index] = data
            self._hdr_data[name][index] = hdr_data[name]


        self._file.flush()


    def close(self) -> None:
        if self._file is not None:
            self._file.close()
            self._file = None

            self._positions = None
            self._data = None