import time

import numpy as np
import pyvisa as visa
from gui_tester.devices.clients.base import DeviceClient
from pyvisa.resources import MessageBasedResource


class WaveSurferClient(DeviceClient):
    def __init__(self, ip: str, verbose=True):
        self.ip = ip
        self.verbose = verbose

        self.connected = False
        self.rm = visa.ResourceManager()
        self.connection = None
        self.connect()   # use resource manager to open 'VICP::'+ipv4_addr+'::INSTR'; assign self.scope to this "instrument"

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
            self.connection = self.rm.open_resource('VICP::' + self.ip + '::INSTR', resource_pyclass=MessageBasedResource)
            try:
                self.idn_string = scope.query('*IDN?')
                if self.verbose: print('<:>', self.idn_string)  # returns scope type, name, version info
                self.connected = True
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
            self.connection.close()
            self.rm.close()
            self.rm = None
            self.connected = False

    def is_connected(self):
        return self.connected

    def rm_list_resources(self):
        """ this is a very slow process --AND-- LeCroy scopes using VISA Passport do not show up in this list, anyway """
        if self.verbose: print('<:> searching for VISA resources')
        t0 = time.time()
        self.rm.list_resources()
        t1 = time.time()
        if self.verbose and (t1-t0 > 1): print('    .............................%6.3g sec' % (t1-t0))
