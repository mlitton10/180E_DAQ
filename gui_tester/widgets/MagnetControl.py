from PyQt6.QtCore import QThread, QThreadPool
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel, QGridLayout, QMessageBox,
)
from gui_tester.widgets.magnet_control_widgets.CurrentDisplay import CurrentDisplay
from gui_tester.widgets.magnet_control_widgets.CurrentControlWidget import CurrentControlWidget
from gui_tester.widgets.magnet_control_widgets.FieldLine import FieldLine
from gui_tester.widgets.magnet_control_widgets.FieldStrength import FieldStrength

import pickle

from gui_tester.widgets.magnet_control_widgets.workers.FieldCalculation import FieldCalculationWorker


class MagnetGeometry:
    def __init__(self, magnet_data_dir):
        self.data_dir = magnet_data_dir
        self.section_1_geometry = self.load("section_1_geometry.pkl")
        self.section_2_geometry = self.load("section_2_geometry.pkl")
        self.section_3_geometry = self.load("section_3_geometry.pkl")

    def load(self, filename):
        with open(self.data_dir + filename, 'rb') as file:
            # Load the data from the file
            loaded_data = pickle.load(file)

        return loaded_data


class MagnetWidget(QWidget):
    def __init__(self, geometry, magnet_ip):
        super().__init__()

        self.current_control = CurrentControlWidget(magnet_ip)
        self.fieldLine = FieldLine(geometry)
        self.fieldStrength = FieldStrength()
        self.currentDisplay = CurrentDisplay()

        self.build_layout()
        self.connect_signals()

        self.thread = None
        self.worker = None

        self.threadpool = QThreadPool()

    def build_layout(self):
        layout = QGridLayout(self)
        layout.addWidget(self.fieldLine, 0, 0, 1, 2)
        layout.addWidget(self.fieldStrength, 1, 0, 2, 1)
        layout.addWidget(self.currentDisplay, 1, 1)
        layout.addWidget(self.current_control, 2, 1)

    def connect_signals(self):
        self.current_control.currentRequested.connect(self.compute_field_async)
        pass

    def run_worker_async(self, worker):
        self.thread = QThread(self)
        self.worker = worker

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_load_finished)
        self.worker.failed.connect(self.on_load_failed)

        self.worker.finished.connect(self.thread.quit)
        self.worker.failed.connect(self.thread.quit)

        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.failed.connect(self.worker.deleteLater)

        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.on_thread_finished)

        self.thread.start()

    def update_current_async(self, currents, plot_only: bool):
        # If a load is already running, ignore new requests for simplicity.
        if self.thread is not None and self.thread.isRunning():
            return

        self.current_control.setEnabled(False)

        self.run_worker_async(FieldCalculationWorker(currents, plot_only))

    def on_load_finished(self, results):
        self.fieldLine.update_field_lines(results)
        self.fieldStrength.update_plot(results)
#		self.status_label.setText(f"Loaded {os.path.basename(filepath)}")

    def on_load_failed(self, message: str):
#		self.status_label.setText("Load failed")
        QMessageBox.critical(self, "Load Error", message)

    def on_thread_finished(self):
        self.current_control.setEnabled(True)
        self.thread = None
        self.worker = None
