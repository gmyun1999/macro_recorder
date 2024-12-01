import asyncio
import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware


class ServerHandler:
    def __init__(self):
        self.app = FastAPI()
        self.client_websocket = None  # 단일 클라이언트 관리
        self.connection_callbacks = []
        self.disconnection_callbacks = []

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost", "http://127.0.0.1"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await self.handle_connection(websocket)

    def register_callback(self, on_connect=None, on_disconnect=None):
        """ModelView로부터 콜백 등록"""
        if on_connect:
            self.connection_callbacks.append(on_connect)
        if on_disconnect:
            self.disconnection_callbacks.append(on_disconnect)

    def _notify_callbacks(self, callbacks):
        """콜백 호출"""
        for callback in callbacks:
            callback()

    async def handle_connection(self, websocket: WebSocket):
        """WebSocket 클라이언트 연결 처리"""
        notified_disconnection = False  # 중복 방지 플래그

        try:
            # WebSocket 연결 수락
            await websocket.accept()
            self.client_websocket = websocket
            self._notify_callbacks(self.connection_callbacks)
            print("클라이언트 연결됨")

            while True:
                try:
                    # 클라이언트 메시지 수신
                    message = await websocket.receive_text()
                    parsed_message = json.loads(message)

                    if parsed_message.get("type") == "ping":
                        # Pong 메시지 응답
                        response = {"type": "pong", "data": None}
                        await websocket.send_text(json.dumps(response))
                        print("Pong 메시지 전송")

                except asyncio.TimeoutError:
                    print("타임아웃 발생: 클라이언트가 응답하지 않음")
                    await websocket.close()
                    break

        except WebSocketDisconnect:
            print("클라이언트 연결 끊김")
            if not notified_disconnection:
                self._notify_callbacks(self.disconnection_callbacks)
                notified_disconnection = True

        finally:
            if not notified_disconnection:  # finally에서도 확인
                self._notify_callbacks(self.disconnection_callbacks)
            self.client_websocket = None
            print("클라이언트 WebSocket 정리 완료")

    async def send_message(self, message: dict):
        """특정 클라이언트에게 메시지 전송"""
        if self.client_websocket is not None:
            try:
                await self.client_websocket.send_text(json.dumps(message))
                print(f"메시지 전송 완료: {message}")

            except Exception as e:
                print(f"메시지 전송 중 오류 발생: {e}")
        else:
            print("연결된 클라이언트가 없습니다.")
