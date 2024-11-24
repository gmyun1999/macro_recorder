from PyQt5.QtCore import QThread


class ServerThread(QThread):
    """서버를 별도의 스레드에서 실행"""

    connection_timeout = False  # 타임아웃 상태 플래그
    connection_disconnected = False  # 연결 끊김 플래그

    def __init__(self, server_handler):
        super().__init__()
        self.server_handler = server_handler

    def run(self):
        try:
            self.server_handler.start_server()

        except TimeoutError:
            self.connection_timeout = True

        except ConnectionError:
            self.connection_disconnected = True

    def send_message(self, message):
        """서버 핸들러를 통해 메시지 전송"""
        self.server_handler.send_message(message)
