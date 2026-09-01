import time

import numpy as np
import pyvisa as visa
from gui_tester.devices.clients.base import DeviceClient

class WaveSurfer(DeviceClient):
    def __init__(self, ip: str, verbose=True):
        self.ip = ip
        self.verbose = verbose

        self.connected = False
        self.rm = visa.ResourceManager()

        self.connection = self.connect()   # use resource manager to open 'VICP::'+ipv4_addr+'::INSTR'; assign self.scope to this "instrument"

    def connect(self):
        """ open the NI-VISA resource manager
            then open the scope resource 'VICP::'+ipv4_addr+'::INSTR'
            once open, attempt to communicate with the scope
            throw an exception if any of the above fails
            eventually we need to call rm_close()
        """

        if self.verbose: print('<:> attempting to open resource VICP::' + self.ip + '::INSTR')

        # attempt to open a connection to the scope
        try:
            scope = self.rm.open_resource('VICP::' + self.ip + '::INSTR', resource_pyclass=MessageBasedResource)
            try:
                self.idn_string = scope.query('*IDN?')
                if self.verbose: print('<:>', self.idn_string)  # returns scope type, name, version info
                self.connected = True
                return scope
            except Exception:
                self.rm.close()
                self.rm = None
                raise ConnectionError('\n**** Scope at "', self.ip, '" did not respond to "*IDN?" query\n')
        except Exception:
            self.rm.close()
            self.rm = None
            raise ConnectionError('**** Scope not found at "', self.ip, '"\n')

        # send a (standard) *IDN? query as a way of testing whether we have a scope:


    def disconnect(self):
        if self.rm is not None:
            self.rm.close()
            self.rm = None
            self.connected = False

    def is_connected(self):
        return self.connected