from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMessageBox

from view.component.button import DefaultButton


class CustomMessageBox(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        font = QFont()
        font.setPointSize(14)
        self.setFont(font)

        # 스타일시트 제거

    def critical(self, title, message):
        """Critical 메시지 박스를 표시"""
        self.setIcon(QMessageBox.Critical)
        self.setWindowTitle(title)
        self.setText(message)

        # 기존 버튼 숨기기
        self.setStandardButtons(QMessageBox.NoButton)

        # DefaultButton 추가
        ok_button = DefaultButton("OK", self)
        ok_button.setFixedSize(100, 40)
        ok_button.clicked.connect(self.accept)

        self.addButton(ok_button, QMessageBox.AcceptRole)
        self.exec_()
