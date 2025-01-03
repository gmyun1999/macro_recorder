import os
import sys

from PyQt5.QtWidgets import QApplication
from qt_material import apply_stylesheet

from debug_helper import global_exception_handler, log_exception, setup_logging
from view.macro_gui import MacroGUI
from view_model.macro_viewmodel import MacroViewModel

if __name__ == "__main__":
    # 로깅 및 예외 처리 설정
    setup_logging()
    sys.excepthook = global_exception_handler

    # QApplication 생성
    app = QApplication(sys.argv)

    # 실행 환경에 따라 동적 경로 처리
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:  # 개발 환경
        base_path = os.path.dirname(os.path.abspath(__file__))

    try:
        # 테마 적용
        theme_path = os.path.join(base_path, "view", "theme", "custom_theme.xml")
        apply_stylesheet(app, theme=theme_path)

        # ViewModel과 GUI 생성
        view_model = MacroViewModel()
        window = MacroGUI(view_model)
        window.show()

        # 예외 발생 시 로깅
        try:
            sys.exit(app.exec_())
        except Exception as e:
            log_exception(e)

    except Exception as e:
        log_exception(e)
        raise
