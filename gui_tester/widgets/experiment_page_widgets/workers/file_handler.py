import os
import time
import tkinter
from tkinter import filedialog

import h5py


class HDF5FileHandler:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        ofn = self.get_hdf5_filename()  # callback arg to the current function

    def get_hdf5_filename(self) -> str:

        avoid_overwrite = True     # <-- setting this to False will allow overwriting an existing file without a prompt

        fn = self.filename
        if fn is None  or len(fn) == 0  or  (avoid_overwrite  and  os.path.isfile(fn)):
            # if we are not allowing possible overwrites as default, and the file already exists, use file open dialog
            tk = tkinter.Tk()
            tk.withdraw()		# prevent tk GUI from popping up

            fnoptions = {'title': 'Save file as ...', 'defaultextension': '.hdf5',
                         'filetypes': [("Hierarchical Data Format",'*.hdf5'), ("All files",'*.*')]}

            fn = filedialog.asksaveasfilename(**fnoptions)
            if not fn: 		# if user pressed 'cancel', fn = None
                print("\nUser cancelled save file input.")
                # if len(fn) == 0:
                # 	#raise SystemExit(0)
                # 	fn = exit
            tk.destroy()

        self.hdf5_filename = fn    # save it for later
        return fn

    def create_file(self) -> None:
        fn = self.get_hdf5_filename()
        f = h5py.File(fn,
                      'w')  # 'w' - overwrite (we should have determined whether we want to overwrite in get_hdf5_filename())
        # ============================
        # create HDF5 groups similar to those in the legacy format:

        acq_grp = f.create_group('/Acquisition')  # /Acquisition
        acq_grp.attrs['run_time'] = time.ctime()  # not legacy
        scope_grp = acq_grp.create_group('LeCroy_scope')  # /Acquisition/LeCroy_scope
        header_grp = scope_grp.create_group('Headers')  # not legacy

        ctl_grp = f.create_group('/Control')  # /Control
        pos_grp = ctl_grp.create_group('Positions')  # /Control/Positions
