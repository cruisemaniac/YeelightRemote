from PyQt5.QtWidgets import *


class BulbWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        layout = QHBoxLayout(self)
