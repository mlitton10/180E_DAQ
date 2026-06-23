from PyQt5.QtWidgets import QGroupBox, QLabel, QLineEdit


class TextLine(QGroupBox):

    def __init__(self, label_string = None, read_only = False):
        super().__init__()

        self.label = QLabel(label_string)
        self.input_line = QLineEdit(read_only)

        pass


