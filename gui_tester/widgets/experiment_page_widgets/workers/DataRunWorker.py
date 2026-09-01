from gui_tester.devices.probe_drive import ProbeDriveXY
from gui_tester.devices.wavesurfer import WaveSurfer
from gui_tester.widgets.basic_templates.generic_worker import Worker


class FieldCalculationWorker(Worker):
    def __init__(self,ip_addresses, parent=None):
        super().__init__()

        self.probe_drive = ProbeDriveXY(ip_addresses['x_motor'], ip_addresses['y_motor'])
        self.wavesurfer = WaveSurfer(ip_addresses['scope'])

