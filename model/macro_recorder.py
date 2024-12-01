import json
import time
from threading import Event

from pynput import keyboard, mouse


class MacroRecorder:
    def __init__(self):
        self.mouse_events = []
        self.keyboard_events = []
        self.recording = False
        self.start_time = None
        self.stop_event = Event()

    def on_mouse_click(self, x, y, button, pressed):
        if not self.recording:
            return
        event = {
            "type": "mouse_click",
            "timestamp": time.time() - self.start_time,
            "x": x,
            "y": y,
            "button": button.name,
            "pressed": pressed,
        }
        self.mouse_events.append(event)

    def on_mouse_move(self, x, y):
        if not self.recording:
            return
        event = {
            "type": "mouse_move",
            "timestamp": time.time() - self.start_time,
            "x": x,
            "y": y,
        }
        self.mouse_events.append(event)

    def on_keyboard_press(self, key):
        if not self.recording:
            return
        try:
            key_name = key.char
        except AttributeError:
            key_name = key.name
        event = {
            "type": "keyboard_press",
            "timestamp": time.time() - self.start_time,
            "key": key_name,
        }
        self.keyboard_events.append(event)

    def start_recording(self):
        self.recording = True
        self.start_time = time.time()

        self.mouse_listener = mouse.Listener(
            on_click=self.on_mouse_click, on_move=self.on_mouse_move
        )
        self.keyboard_listener = keyboard.Listener(on_press=self.on_keyboard_press)

        self.mouse_listener.start()
        self.keyboard_listener.start()

    def stop_recording(self):
        self.recording = False
        self.mouse_listener.stop()
        self.keyboard_listener.stop()
        self.stop_event.set()

    def get_events(self):
        """현재 메모리에 저장된 이벤트 반환."""
        return {
            "mouse_events": self.mouse_events,
            "keyboard_events": self.keyboard_events,
        }

    def flush_events(self):
        """현재 메모리에 저장된 이벤트 삭제."""
        self.mouse_events = []
        self.keyboard_events = []
