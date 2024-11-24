from PyQt5.QtCore import QPropertyAnimation, Qt, QVariantAnimation
from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtWidgets import QPushButton


class DefaultButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

        # 기본 색상 설정
        self.default_color = QColor("#1D8FFF")  # 기본 배경색
        self.hover_color = QColor("#0068CD")  # 호버 시 배경색
        self.setStyleSheet(
            f"""
        QPushButton {{
            background-color: {self.default_color.name()}; /* 기본 배경색 */
            border: 2px solid {self.default_color.name()}; /* 테두리 색 */
            color: #FFFFFF;            /* 텍스트 색 */
            border-radius: 12px;        /* 모서리를 둥글게 */
            font-size: 14px;           /* 텍스트 크기 */
            font-weight: bold;       /* 텍스트 굵기 */
            padding: 4px 10px; 
        }}
        QPushButton:pressed {{
            background-color: {self.hover_color.name()}; /* 클릭 시 배경색 */
        }}
        QPushButton:disabled {{
            background-color: #1A1A1A; /* 비활성화 상태 배경색 */
            border: 2px solid #333333; /* 비활성화 상태 테두리 색 */
            color: #FFFFFF;            /* 비활성화 상태 텍스트 색 */
        }}
        """
        )

        # 애니메이션 객체 생성
        self.animation = QVariantAnimation(
            self,
            startValue=self.default_color,
            endValue=self.hover_color,
            duration=300,  # 애니메이션 지속 시간 (밀리초)
        )
        self.animation.valueChanged.connect(self.update_color)

    def update_color(self, color):
        """애니메이션 중간값에 따라 색상을 업데이트"""
        self.setStyleSheet(
            f"""
        QPushButton {{
            background-color: {color.name()}; /* 동적으로 변경된 배경색 */
            border: 2px solid {color.name()}; /* 동적으로 변경된 테두리 색 */
            color: #FFFFFF;            /* 텍스트 색 */
            border-radius: 12px;        /* 모서리를 둥글게 */
            font-size: 14px;           /* 텍스트 크기 */
            font-weight: bold;       /* 텍스트 굵기 */
            padding: 4px 10px; 
        }}
        QPushButton:pressed {{
            background-color: {self.hover_color.name()}; /* 클릭 시 배경색 */
        }}
        QPushButton:disabled {{
            background-color: #1A1A1A; /* 비활성화 상태 배경색 */
            border: 2px solid #333333; /* 비활성화 상태 테두리 색 */
            color: #FFFFFF;            /* 비활성화 상태 텍스트 색 */
        }}
        """
        )

    def enterEvent(self, event):
        """마우스가 버튼 위로 올려졌을 때 애니메이션 및 커서 변경"""
        self.setCursor(QCursor(Qt.PointingHandCursor))  # 커서를 손 모양으로 변경
        self.animation.setDirection(QVariantAnimation.Forward)
        self.animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """마우스가 버튼에서 벗어났을 때 애니메이션 복원"""
        self.setCursor(QCursor(Qt.ArrowCursor))  # 커서를 기본 화살표 모양으로 복원
        self.animation.setDirection(QVariantAnimation.Backward)
        self.animation.start()
        super().leaveEvent(event)
