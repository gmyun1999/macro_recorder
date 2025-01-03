from PyQt5.QtCore import Qt, QVariantAnimation
from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtWidgets import QPushButton


class StatefulDefaultButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)

        # Define colors for enabled and disabled states
        self.state_colors = {
            "disabled": {
                "default": QColor("#1A1A1A"),
                "border": QColor("#333333"),
                "text": QColor("#FFFFFF"),
            },
            "enabled": {
                "default": QColor("#1D8FFF"),
                "hover": QColor("#0068CD"),
                "text": QColor("#FFFFFF"),
            },
        }

        # Create animation object
        self.animation = QVariantAnimation(
            self,
            duration=300,
        )
        self.animation.valueChanged.connect(self.update_color)

        # Connect the enabled state change to update the style
        self.enabledChanged = (
            self.enabledChanged if hasattr(self, "enabledChanged") else None
        )
        self.stateChanged = self.stateChanged if hasattr(self, "stateChanged") else None
        self.toggled = self.toggled if hasattr(self, "toggled") else None
        self.clicked.connect(self.update_style)
        self.update_style()

    def setEnabled(self, enabled: bool):
        """Override setEnabled to update style when enabled state changes."""
        super().setEnabled(enabled)
        self.update_style()

    def update_style(self):
        """Update the button style based on the enabled state."""
        if not self.isEnabled():
            colors = self.state_colors["disabled"]
            stylesheet = f"""
            QPushButton {{
                background-color: {colors['default'].name()};
                border: 2px solid {colors['border'].name()};
                color: {colors['text'].name()};
                border-radius: 12px;
                font-size: 14px;
                font-weight: bold;
                padding: 4px 10px;
            }}
            """
        else:
            colors = self.state_colors["enabled"]
            stylesheet = f"""
            QPushButton {{
                background-color: {colors['default'].name()};
                border: 2px solid {colors['default'].name()};
                color: {colors['text'].name()};
                border-radius: 12px;
                font-size: 14px;
                font-weight: bold;
                padding: 4px 10px;
            }}
            QPushButton:pressed {{
                background-color: {colors['hover'].name()};
            }}
            """
        self.setStyleSheet(stylesheet)

    def update_color(self, color):
        """Update the color during animation based on the enabled state."""
        if not self.isEnabled():
            return  # No animation for disabled state

        colors = self.state_colors["enabled"]
        stylesheet = f"""
        QPushButton {{
            background-color: {color.name()};
            border: 2px solid {color.name()};
            color: {colors['text'].name()};
            border-radius: 12px;
            font-size: 14px;
            font-weight: bold;
            padding: 4px 10px;
        }}
        QPushButton:pressed {{
            background-color: {colors['hover'].name()};
        }}
        """
        self.setStyleSheet(stylesheet)

    def enterEvent(self, event):
        """Animate color on hover and change cursor."""
        if self.isEnabled():
            colors = self.state_colors["enabled"]
            self.setCursor(QCursor(Qt.PointingHandCursor))

            self.animation.stop()
            self.animation.setStartValue(colors["default"])
            self.animation.setEndValue(colors["hover"])
            self.animation.setDirection(QVariantAnimation.Forward)
            self.animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Revert color animation when hover ends and reset cursor."""
        if self.isEnabled():
            colors = self.state_colors["enabled"]
            self.setCursor(QCursor(Qt.ArrowCursor))

            self.animation.stop()
            self.animation.setStartValue(colors["hover"])
            self.animation.setEndValue(colors["default"])
            self.animation.setDirection(QVariantAnimation.Forward)
            self.animation.start()
        super().leaveEvent(event)
