from enum import StrEnum

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QPushButton

from view.component.stateful_button import StatefulDefaultButton


class RecordMode(StrEnum):
    RECORD = "record"
    STOP = "stop"


class RecordBtn(StatefulDefaultButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._button_mode = RecordMode.RECORD
        self.setText = text

    def set_button_mode(self, mode: RecordMode):
        self._button_mode = mode
        super().setText(mode.value)

    def get_button_mode(self) -> RecordMode:
        return self._button_mode
