from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from view.component.label import CustomLabel
from view.component.modal import CustomMessageBox
from view.component.record_btn import RecordBtn, RecordMode
from view.component.stateful_button import StatefulDefaultButton


class MacroGUI(QWidget):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.current_countdown = 0

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

        self.status_label = CustomLabel("condition: web client waiting..")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        self.record_button = RecordBtn()
        self.record_button.setEnabled(False)
        self.record_button.set_button_mode(RecordMode.RECORD)
        layout.addWidget(self.record_button)

        self.play_back_button = StatefulDefaultButton("Play")
        self.play_back_button.setEnabled(False)
        layout.addWidget(self.play_back_button)

        self.save_record_button = StatefulDefaultButton("Save")
        self.save_record_button.setEnabled(False)
        layout.addWidget(self.save_record_button)

        self.setLayout(layout)

    def bind_viewmodel(self):
        """ViewModel에서 발생한 상태 변경 이벤트와 View를 바인딩"""
        # status 변경 시 상태 업데이트
        self.view_model.status_changed.connect(self.update_label_status)

        # client 연결 및 끊김 시 모달 표시
        self.view_model.connection_disconnected.connect(
            self.show_client_disconnect_modal
        )
        self.view_model.client_connected.connect(self.show_client_connect_modal)

        # 녹화 및 재생 버튼 활성화 여부
        self.view_model.recording_enabled.connect(
            self.toggle_recording_buttons
        )  # record 버튼 비활성/활성화
        self.view_model.recording_countdown_enabled.connect(
            self.start_recording_countdown
        )  # 카운트다운 시작/취소, 카운트다운 시간
        self.view_model.set_record_mode.connect(
            self.record_button.set_button_mode
        )  # record 버튼 모드 변경

        self.view_model.playback_enabled.connect(
            self.toggle_playback_buttons
        )  # play 버튼 비활성/활성화
        self.view_model.save_record_enabled.connect(
            self.toggle_save_record_button
        )  # save 버튼 비활성/활성화

        self.view_model.send_message_complete.connect(
            self.show_client_send_complete_modal
        )

    def bind_user_events(self):
        """사용자 입력 이벤트(View → ViewModel)를 처리하는 메서드"""
        self.record_button.clicked.connect(
            lambda: self.view_model.handle_record_button(self.record_button)
        )
        self.play_back_button.clicked.connect(self.view_model.play_macro)
        self.save_record_button.clicked.connect(self.view_model.save_record)

    def start_recording_countdown(self, is_enable: bool, cnt: int):
        """5초 카운트다운 시작"""
        if is_enable:
            self.current_countdown = cnt
            self.countdown_timer.start(1000)  # 1초마다 타이머 호출
            self.update_label_status(
                f"Recording starts in {self.current_countdown} seconds"
            )
        else:
            self.countdown_timer.stop()
            self.update_label_status("Recording canceled")

    def update_countdown(self):
        """카운트다운 업데이트"""
        self.current_countdown -= 1

        if self.current_countdown > 0:
            # 카운트다운 중
            self.update_label_status(
                f"Recording starts in {self.current_countdown} seconds"
            )
        else:
            # 카운트다운 종료, 타이머 중지
            self.countdown_timer.stop()
            # 실제 녹화 시작
            self.view_model.start_recording()

    def toggle_recording_buttons(self, enabled):
        """녹화 버튼 상태 업데이트"""
        print("녹화버튼 상태", enabled)
        self.record_button.setEnabled(enabled)

    def toggle_playback_buttons(self, enabled):
        self.play_back_button.setEnabled(enabled)

    def toggle_save_record_button(self, enabled):
        """저장 버튼 상태 업데이트"""
        self.save_record_button.setEnabled(enabled)

    def update_label_status(self, status):
        """상태 업데이트"""
        self.status_label.setText(f"status: {status}")

    def show_client_disconnect_modal(self, message: str | None = None):
        """connection이 끊어졌음을 알림"""
        disconnected_message_title = "No Connection"
        if message is None:
            message = "The connection with the client has been lost.\n\nThe program will now exit."

        message_box = CustomMessageBox(self)
        message_box.critical(disconnected_message_title, message)

    def show_client_send_complete_modal(self, message: str | None = None):
        """client와 연결되었음을 알림"""
        modal_title = "sending success"
        if message is None:
            message = "Go back to Web site \n\n Block will be add."

        message_box = CustomMessageBox(self)
        message_box.information(modal_title, message)
        self.close()

    def show_client_connect_modal(self, message: str | None = None):
        """client와 연결되었음을 알림"""
        modal_title = "Connection success"
        if message is None:
            message = "connect from web client ."

        message_box = CustomMessageBox(self)
        message_box.information(modal_title, message)
