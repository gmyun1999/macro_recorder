from PyQt5.QtCore import QObject, pyqtSignal

from model.macro_player import MacroPlayer
from model.macro_recorder import MacroRecorder
from model.server_handler import ServerHandler
from model.server_thread import ServerThread


class MacroViewModel(QObject):
    status_changed = pyqtSignal(str)

    recording_enabled = pyqtSignal(bool)
    stop_recording_enabled = pyqtSignal(bool)
    playback_enabled = pyqtSignal(bool)
    save_record_enabled = pyqtSignal(bool)

    connection_disconnected = pyqtSignal(str)  # 연결 끊김 시그널
    send_message_complete = pyqtSignal(str)  # 전송 완료 시그널
    client_connected = pyqtSignal(str)  # 클라이언트 연결완료 시그널

    def __init__(self):
        super().__init__()
        self.recorder = None
        self.recorded_events = None  # 메모리에 저장된 이벤트
        self.server_handler = ServerHandler()
        self.server_thread = ServerThread(self.server_handler)

        self.server_handler.register_callback(
            on_connect=self.on_client_connected,
            on_disconnect=self.on_client_disconnected,
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
        self.recorder = MacroRecorder()
        self.recorder.start_recording()
        self.status_changed.emit("recording...")
        self.recording_enabled.emit(False)
        self.stop_recording_enabled.emit(True)

    def stop_recording(self):
        if self.recorder and self.recorder.recording:
            self.recorder.stop_recording()
            self.recorded_events = self.recorder.get_events()  # 메모리에 저장
            self.status_changed.emit("record complete.")
            self.recording_enabled.emit(True)
            self.stop_recording_enabled.emit(False)
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
        self.server_thread.start()
