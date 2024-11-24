from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from view.component.button import DefaultButton
from view.component.label import CustomLabel
from view.component.modal import CustomMessageBox


class MacroGUI(QWidget):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model
        self.init_ui()
        self.bind_viewmodel()
        self.bind_user_events()

        # ViewModel을 통해 서버 시작
        self.view_model.start_server()

    def init_ui(self):
        self.setWindowTitle("macro builder version_1.0.0")
        self.setGeometry(50, 100, 300, 350)

        layout = QVBoxLayout()
        layout.setSpacing(15)  # 위젯 간의 간격 조정
        layout.setContentsMargins(20, 20, 20, 20)  # 레이아웃 여백 설정

        self.status_label = CustomLabel("condition: waiting..")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        self.record_button = DefaultButton("record")
        layout.addWidget(self.record_button)

        self.stop_button = DefaultButton("stop")
        self.stop_button.setEnabled(False)
        layout.addWidget(self.stop_button)

        self.play_button = DefaultButton("Play")
        self.play_button.setEnabled(False)
        layout.addWidget(self.play_button)

        self.save_record_button = DefaultButton("Save")
        self.save_record_button.setEnabled(False)
        layout.addWidget(self.save_record_button)

        self.setLayout(layout)

    def bind_viewmodel(self):
        """ViewModel에서 발생한 상태 변경 이벤트와 View를 바인딩"""
        self.view_model.status_changed.connect(self.update_status)
        self.view_model.server_timeout.connect(self.show_client_disconnect_modal)
        self.view_model.connection_disconnected.connect(
            self.show_client_disconnect_modal
        )
        # 녹화 및 재생 버튼 활성화 여
        self.view_model.recording_enabled.connect(self.toggle_recording_buttons)
        self.view_model.playback_enabled.connect(self.toggle_playback_buttons)
        self.view_model.save_record_enabled.connect(self.toggle_save_record_button)
        self.view_model.send_message_complete.connect(self.show_client_disconnect_modal)

    def bind_user_events(self):
        """사용자 입력 이벤트(View → ViewModel)를 처리하는 메서드"""
        self.record_button.clicked.connect(self.view_model.start_recording)
        self.stop_button.clicked.connect(self.view_model.stop_recording)
        self.play_button.clicked.connect(self.view_model.play_macro)
        self.save_record_button.clicked.connect(self.view_model.save_record)

    def toggle_save_record_button(self, enabled):
        """저장 버튼 상태 업데이트"""
        self.save_record_button.setEnabled(enabled)

    def toggle_recording_buttons(self, enabled):
        """녹화 버튼 상태 업데이트"""
        self.record_button.setEnabled(enabled)
        self.stop_button.setEnabled(not enabled)

    def toggle_playback_buttons(self, enabled):
        self.play_button.setEnabled(enabled)

    def update_status(self, status):
        """상태 업데이트"""
        self.status_label.setText(f"status: {status}")

    def show_client_disconnect_modal(self, message: str | None = None):
        """타임아웃 모달을 띄우고 프로그램 종료"""
        disconnected_message_title = "No Connection"
        if message is None:
            message = "The connection with the client has been lost.\n\nThe program will now exit."

        message_box = CustomMessageBox(self)
        message_box.critical(disconnected_message_title, message)
        self.close()
