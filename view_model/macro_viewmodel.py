from PyQt5.QtCore import QObject, QTimer, pyqtSignal

from model.macro_player import MacroPlayer
from model.macro_recorder import MacroRecorder
from model.server_handler import ServerHandler
from model.server_thread import ServerThread
from view.component.record_btn import RecordBtn, RecordMode


class MacroViewModel(QObject):
    # label 상태 변경
    status_changed = pyqtSignal(str)

    # 녹화 관련
    recording_enabled = pyqtSignal(bool)  # 녹화 버튼 활성화
    recording_countdown_enabled = pyqtSignal(bool, int)  # 카운트 다운 활성화, 카운트 다운 시간
    set_record_mode = pyqtSignal(RecordMode)  # 녹화 버튼 모드 변경

    # 재생 및 저장
    playback_enabled = pyqtSignal(bool)  # 재생 버튼 활성화
    save_record_enabled = pyqtSignal(bool)  # 저장 버튼 활성화

    # client 연결 및 끊김
    connection_disconnected = pyqtSignal(str)
    client_connected = pyqtSignal(str)

    # 모달
    send_message_complete = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.recorder = None
        self.recorded_events = None
        self.server_handler = ServerHandler()
        self.server_thread = ServerThread(self.server_handler)
        self.player = MacroPlayer()
        self.recorder = MacroRecorder()
        self.is_recording = False
        self.is_playing = False

        self.server_handler.register_callback(
            on_connect=self.on_client_connected,
            on_disconnect=self.on_client_disconnected,
        )

        self.player.register_callback(
            on_stop=self.on_playback_stop, on_complete=self.on_playback_complete
        )

    def on_client_connected(self):
        self.client_connected.emit("client connected.")
        self.status_changed.emit("client connected.")
        self.recording_enabled.emit(True)

    def on_client_disconnected(self):
        self.connection_disconnected.emit("client disconnected.")
        self.recording_enabled.emit(False)
        self.playback_enabled.emit(False)
        self.save_record_enabled.emit(False)
        self.status_changed.emit("client disconnected.")

    def start_recording(self):
        self.recorder.start_recording()
        self.is_recording = True
        self.status_changed.emit("recording...")

    def handle_record_button(self, record_button: RecordBtn):
        """녹화 버튼 클릭했을떄 핸들러 - 녹화 시작 또는 중지"""

        if record_button.get_button_mode() == RecordMode.RECORD:
            self.recording_countdown_enabled.emit(True, 5)
            self.set_record_mode.emit(RecordMode.STOP)
        else:  # stop 인경우
            if self.recorder and self.is_recording:
                self.recorder.stop_recording()
                self.recorded_events = self.recorder.get_events()
                self.status_changed.emit("record complete.")
                self.is_recording = False
                # 기타 버튼 활성화
                self.playback_enabled.emit(True)
                self.save_record_enabled.emit(True)
            else:
                self.recording_countdown_enabled.emit(False, 0)

            self.set_record_mode.emit(RecordMode.RECORD)

    def play_macro(self):
        if self.recorded_events:
            self.is_playing = True
            self.recording_enabled.emit(False)
            self.save_record_enabled.emit(False)
            self.status_changed.emit("esc를 연타하면 중지됩니다.")

            # 재생 시작
            # QTimer.singleShot(2000, lambda: self.player.start_playing(self.recorded_events))
            self.player.set_events(self.recorded_events)
            self.player.run()

    def on_playback_stop(self):
        self.is_playing = False
        self.recording_enabled.emit(True)
        self.save_record_enabled.emit(True)
        self.status_changed.emit("playback stopped.")

    def on_playback_complete(self):
        self.is_playing = False
        self.recording_enabled.emit(True)
        self.save_record_enabled.emit(True)
        self.status_changed.emit("playback complete.")

    def save_record(self):
        if self.recorded_events:
            print("record saved.")
            self.server_thread.send_message(self.recorded_events)
            self.status_changed.emit("record saved.")
            self.send_message_complete.emit("sended record. \n go back to web page.")

    def start_server(self):
        """서버를 시작하고 상태를 관리"""
        self.server_thread.start()
