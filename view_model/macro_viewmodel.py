from PyQt5.QtCore import QObject, pyqtSignal

from model.macro_player import MacroPlayer
from model.macro_recorder import MacroRecorder
from model.server_handler import ServerHandler
from model.server_thread import ServerThread


class MacroViewModel(QObject):
    status_changed = pyqtSignal(str)
    recording_enabled = pyqtSignal(bool)
    playback_enabled = pyqtSignal(bool)
    save_record_enabled = pyqtSignal(bool)
    server_timeout = pyqtSignal(str)  # 서버 타임아웃 시그널
    connection_disconnected = pyqtSignal(str)  # 연결 끊김 시그널
    server_disconnected = pyqtSignal(str)
    send_message_complete = pyqtSignal(str)  # 전송 완료 시그널

    def __init__(self):
        super().__init__()
        self.recorder = None
        self.recorded_events = None  # 메모리에 저장된 이벤트
        self.server_handler = ServerHandler(timeout=10, retry_limit=3)
        self.server_thread = ServerThread(self.server_handler)

    def start_recording(self):
        self.recorder = MacroRecorder()
        self.recorder.start_recording()
        self.status_changed.emit("recording...")
        self.recording_enabled.emit(False)

    def stop_recording(self):
        if self.recorder and self.recorder.recording:
            self.recorder.stop_recording()
            self.recorded_events = self.recorder.get_events()  # 메모리에 저장
            self.status_changed.emit("record complete.")
            self.recording_enabled.emit(True)
            self.playback_enabled.emit(True)
            self.save_record_enabled.emit(True)

    def play_macro(self):
        if self.recorded_events:
            player = MacroPlayer(self.recorded_events)
            player.play_events()
            self.status_changed.emit("reply complete.")

    def save_record(self):
        if self.recorded_events:
            print("record saved.")
            # 서버에 메시지 전송
            self.server_thread.send_message(self.recorded_events)
            self.status_changed.emit("record saved.")
            self.send_message_complete.emit("sended record. \n go back to web page.")

    def start_server(self):
        """서버를 시작하고 상태를 관리"""
        self.server_thread.finished.connect(self.check_server_status)
        self.server_thread.start()

    def check_server_status(self):
        """서버 상태 확인"""
        if self.server_thread.connection_timeout:
            self.server_timeout.emit("client connection timeout.")
        elif self.server_thread.connection_disconnected:
            self.connection_disconnected.emit("client disconnected.")
        else:
            self.status_changed.emit("client connected.")
