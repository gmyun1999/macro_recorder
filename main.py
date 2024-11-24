import sys

from PyQt5.QtWidgets import QApplication
from qt_material import apply_stylesheet

from view.macro_gui import MacroGUI
from view_model.macro_viewmodel import MacroViewModel

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    # qt-material 스타일시트 적용햇음
    apply_stylesheet(app, theme="view/theme/custom_theme.xml")  # 테마 파일 경로

    view_model = MacroViewModel()

    window = MacroGUI(view_model)
    window.show()
    sys.exit(app.exec_())
