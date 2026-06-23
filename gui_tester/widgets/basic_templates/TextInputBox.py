from PyQt5.QtWidgets import QWidget, QLineEdit, QFormLayout


class UserSettingsRow(QWidget):
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