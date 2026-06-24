from PyQt5.QtWidgets import QWidget, QLineEdit, QFormLayout, QSpinBox


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

        self.label_edit = QLineEdit()
        self.label_edit.setReadOnly(read_only)
        layout.addRow(label_string, self.label_edit)

    def update_text(self, update_string):
        self.label_edit.setText(update_string)

    def read_text(self):
        return str(self.label_edit.text())

class UserSpinBoxRow(QWidget):
    def __init__(self, label_string, read_only=False):
        super().__init__()

        layout = QFormLayout(self)

        self.label_edit = QSpinBox()
        self.set_range()
        layout.addRow(label_string, self.label_edit)

    def set_range(self, max_range=100):
        self.label_edit.setRange(1, max_range)

    def set_value(self, value):
        self.label_edit.setValue(value)

    def read_value(self):
        return self.label_edit.value()

class UserDoubleSpinBoxRow(QWidget):
    def __init__(self, label_string, read_only=False):
        super().__init__()

        layout = QFormLayout(self)

        self.spin_box = QDoubleSpinBox()
        layout.addRow(label_string, self.spin_box)


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