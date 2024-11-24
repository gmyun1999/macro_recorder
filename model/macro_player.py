import json
import time

from pynput import keyboard, mouse


class MacroPlayer:
    def __init__(self, events):
        self.events = events
        self.mouse_controller = mouse.Controller()
        self.keyboard_controller = keyboard.Controller()
        self.stop_flag = False

    def play_events(self):
        self.stop_flag = False
        start_time = time.time()

        # 이벤트를 타임스탬프 기준으로 정렬
        all_events = sorted(
            self.events["mouse_events"] + self.events["keyboard_events"],
            key=lambda event: event["timestamp"],
        )

        for event in all_events:
            if self.stop_flag:
                break
            current_time = time.time() - start_time
            wait_time = event["timestamp"] - current_time
            if wait_time > 0:
                time.sleep(wait_time)

            # 이벤트 실행
            if event["type"] == "mouse_click":
                button = mouse.Button[event["button"]]
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
        if hasattr(keyboard.Key, key_str):
            return keyboard.Key[key_str]
        if len(key_str) == 1:
            return key_str
        return None
