from PyQt5.QtWidgets import QWidget, QLineEdit, QFormLayout, QSpinBox, QDoubleSpinBox


def make_form_table(rows):
    widget = QWidget()
    widget_layout = QFormLayout(widget)
    for row in rows:
        widget_layout.addRow(row)

    return widget


class UserTextRow(QWidget):
    def __init__(self, label_string, read_only=False):
        super().__init__()

        layout = QFormLayout(self)

        self.text_box = QLineEdit()
        self.text_box.setReadOnly(read_only)
        layout.addRow(label_string, self.text_box)

    def update_text(self, update_string):
        self.text_box.setText(update_string)

    def read_text(self):
        return str(self.text_box.text())

class UserSpinBoxRow(QWidget):
    def __init__(self, label_string, read_only=False):
        super().__init__()

        layout = QFormLayout(self)

        self.spin_box = QSpinBox()
        self.set_range()
        layout.addRow(label_string, self.spin_box)

    def set_range(self, min_range=1, max_range=100):
        self.spin_box.setRange(min_range, max_range)

    def set_value(self, value):
        self.spin_box.setValue(value)

    def read_value(self):
        return self.spin_box.value()

class UserDoubleSpinBoxRow(QWidget):
    def __init__(self, label_string):
        super().__init__()

        layout = QFormLayout(self)

        self.spin_box = QDoubleSpinBox()
        self.initialize_spin_box_parameters()
        layout.addRow(label_string, self.spin_box)

    def initialize_spin_box_parameters(self):
        self.set_range()
        self.set_value(0)
        self.set_step_size()
        self.set_decimals()

    def set_range(self, min_range=-100, max_range=100):
        self.spin_box.setRange(min_range, max_range)

    def set_step_size(self, step_size=0.01):
        self.spin_box.setSingleStep(step_size)

    def set_decimals(self, decimals=2):
        self.spin_box.setDecimals(decimals)

    def set_value(self, value):
        self.spin_box.setValue(value)

    def read_value(self):
        return self.spin_box.value()