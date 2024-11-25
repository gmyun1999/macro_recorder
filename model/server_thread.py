import asyncio

import uvicorn
from fastapi import WebSocketDisconnect
from PyQt5.QtCore import QThread


class ServerThread(QThread):
    """FastAPI 서버를 별도의 스레드에서 실행"""

    def __init__(self, server_handler):
        super().__init__()
        self.server_handler = server_handler

    def run(self):
        """FastAPI 서버 시작"""
        config = uvicorn.Config(
            self.server_handler.app, host="127.0.0.1", port=8000, log_level="info"
        )
        server = uvicorn.Server(config)
        server.run()

    def send_message(self, message):
        """WebSocket으로 메시지 전송"""
        asyncio.run(self.server_handler.send_message(message))
