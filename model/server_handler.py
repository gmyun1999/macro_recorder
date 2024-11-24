import json
import socket


class ServerHandler:
    def __init__(self, host="127.0.0.1", port=5000, timeout=10, retry_limit=3):
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_socket = None
        self.is_running = False
        self.timeout = timeout  # 타임아웃 설정
        self.retry_limit = retry_limit  # 최대 재시도 횟수

    def start_server(self):
        """서버를 시작하고 클라이언트를 기다립니다."""
        self.is_running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.settimeout(self.timeout)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print(f"서버가 {self.host}:{self.port}에서 시작되었습니다.")

        try:
            # 클라이언트 연결 대기
            self.client_socket, client_address = self.server_socket.accept()
            print(f"클라이언트 연결: {client_address}")
            self.handle_client()
        except socket.timeout:
            print("클라이언트 연결 타임아웃. 서버를 종료합니다.")
            self.stop_server()
            raise TimeoutError("클라이언트 연결 실패: 타임아웃")

    def handle_client(self):
        """클라이언트와 통신을 처리합니다."""
        retries = 0  # 재시도 횟수 초기화

        while self.is_running:
            try:
                # 클라이언트로부터 메시지 수신
                message = self.client_socket.recv(1024).decode("utf-8")
                if not message:
                    raise ConnectionResetError("클라이언트 연결 끊김")

                print(f"클라이언트로부터 수신: {message}")
                # 서버 응답
                response = f"서버 응답: {message}"
                self.client_socket.sendall(response.encode("utf-8"))
                retries = 0  # 정상 통신 시 재시도 횟수 초기화

            except (socket.error, ConnectionResetError):
                retries += 1
                print(f"통신 오류 발생. 재시도 {retries}/{self.retry_limit}...")

                if retries >= self.retry_limit:
                    print("최대 재시도 횟수 초과. 클라이언트와의 연결 종료.")
                    self.stop_server()
                    raise ConnectionError("클라이언트와의 통신 중단")

    def send_message(self, message):
        """클라이언트에게 메시지 전송"""
        if self.client_socket:
            try:
                message_str = json.dumps(message)
                # JSON 문자열을 UTF-8로 인코딩 후 전송
                self.client_socket.sendall(message_str.encode("utf-8"))
                print(f"서버가 클라이언트에게 전송: {message}")
            except socket.error as e:
                print(f"메시지 전송 오류: {e}")
                raise ConnectionError("메시지 전송 실패")
        else:
            print("클라이언트 소켓이 연결되어 있지 않음")
            raise ConnectionError("클라이언트가 연결되어 있지 않음")

    def stop_server(self):
        """서버 종료"""
        self.is_running = False
        if self.client_socket:
            self.client_socket.close()
        print("서버가 종료되었습니다.")
