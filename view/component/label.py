from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel


class CustomLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

        # 스타일시트 적용
        self.setStyleSheet(
            """
        QLabel {
            background-color: #333333;  /* 배경색 */
            color: #FFFFFF;            /* 텍스트 색 */
            border-radius: 12px;        /* 모서리를 둥글게 */
            font-size: 14px;           /* 텍스트 크기 */
            font-weight: bold;       /* 텍스트 굵기 */
            padding: 4px 10px; 
        }
        """
        )

        # 텍스트 가운데 정렬
        self.setAlignment(Qt.AlignCenter)
