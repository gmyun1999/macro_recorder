import time

from pynput import keyboard, mouse
from pynput.mouse import Button
from PyQt5.QtCore import QThread, QTimer


class MacroPlayer(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mouse_controller = mouse.Controller()
        self.keyboard_controller = keyboard.Controller()
        self.stop_flag = False
        self.on_stop_callbacks = []
        self.on_complete_callbacks = []
        self.events = None
        self.timer = QTimer()
        self.start_time = None
        self.current_index = 0

    def set_events(self, events):
        self.events = sorted(
            events["mouse_events"] + events["keyboard_events"],
            key=lambda event: event["timestamp"],
        )

    def run(self):
        """매크로 이벤트 실행"""
        if not self.events:
            return

        self.stop_flag = False
        self.start_time = time.time()
        self.current_index = 0

        # QTimer 설정
        self.timer.timeout.connect(self.process_next_event)
        self.timer.start(0)  # 첫 이벤트 처리 시작
        self.exec_()  # QThread의 이벤트 루프 실행

    def process_next_event(self):
        if self.current_index >= len(self.events) or self.stop_flag:
            self.timer.stop()
            self._notify_callbacks(
                self.on_stop_callbacks if self.stop_flag else self.on_complete_callbacks
            )
            self.quit()  # QThread 종료
            return

        event = self.events[self.current_index]
        current_time = time.time() - self.start_time
        wait_time = event["timestamp"] - current_time

        if wait_time > 0:
            self.timer.start(int(wait_time))  # 밀리초 단위로 대기
            return

        # 이벤트 실행
        self.execute_event(event)
        self.current_index += 1

    def execute_event(self, event):
        # TODO: 마지막 클릭 무시, esc 키 누르면 중지

        """이벤트 실행"""
        if event["type"] == "mouse_click":
            button = Button[event["button"]]
            if event["pressed"]:
                self.mouse_controller.press(button)
            else:
                self.mouse_controller.release(button)
        elif event["type"] == "mouse_move":
            self.mouse_controller.position = (event["x"], event["y"])
        elif event["type"] == "keyboard_press":
            key = self.parse_key(event["key"])
            if key:
                self.keyboard_controller.press(key)
                self.keyboard_controller.release(key)

    def parse_key(self, key_str):
        """키 문자열을 pynput 키 객체로 변환"""
        if hasattr(keyboard.Key, key_str):
            return keyboard.Key[key_str]
        if len(key_str) == 1:
            return key_str

        # 한/영 키와 같은 특수 키 처리
        if key_str.lower() == "han_eng":  # 한/영 전환 키
            print("한/영 키 전환 감지")
            return None  # IME 전환 키는 실행 불가

        print(f"키를 인식하지 못했습니다: {key_str}")
        return None

    def register_callback(self, on_stop=None, on_complete=None):
        """재생 종료 콜백 등록"""
        if on_stop:
            self.on_stop_callbacks.append(on_stop)
        if on_complete:
            self.on_complete_callbacks.append(on_complete)

    def _notify_callbacks(self, callbacks):
        """콜백 호출"""
        for callback in callbacks:
            callback()
