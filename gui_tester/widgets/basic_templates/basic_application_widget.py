from PyQt6.QtWidgets import QWidget, QGroupBox


class BasicAppWidget(QGroupBox):
    def __init__(self, title=None):
        super().__init__()
        if title is not None:
            self.setTitle(title)


    def build_layout(self):
        raise NotImplementedError("Build the layout")

    def connect_signals(self):
        raise NotImplementedError("Connect the signals")

    def initialize_widget(self):
        raise NotImplementedError("Initialize the widget")