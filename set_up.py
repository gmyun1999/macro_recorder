import os
import subprocess

# 포함할 데이터 파일 및 디렉토리 설정
DATA_FILES = [
    ("view", "view"),  # view 디렉토리
    ("view_model", "view_model"),  # view_model 디렉토리
    ("view/theme/custom_theme.xml", "view/theme"),  # 테마 파일
    ("model", "model"),  # model 디렉토리
]

# 추가로 포함해야 할 숨겨진 모듈 설정
HIDDEN_IMPORTS = [
    "fastapi",
    "starlette",
    "pydantic",
    "anyio",
    "pynput.keyboard",
    "pynput.mouse",
    "fastapi.middleware",  # 추가
    "fastapi.middleware.cors",  # 추가
    "uvicorn",  # FastAPI 서버에 필요할 수 있음
]


# PyInstaller 빌드 함수
def build_executable():
    command = [
        "pyinstaller",
        "--onefile",
        "--console",
        "--collect-all",
        "fastapi",  # FastAPI의 모든 의존성 수집
        "--collect-all",
        "starlette",
        "--collect-all",
        "pydantic",
        "--add-data",
        "debug_helper.py;.",
    ]

    # 데이터 파일 추가
    for src, dest in DATA_FILES:
        command += ["--add-data", f"{src};{dest}"]

    # 숨겨진 모듈 추가
    for module in HIDDEN_IMPORTS:
        command += ["--hidden-import", module]

    # 진입점 스크립트 추가
    command.append("main.py")

    print("Building the executable with the following command:")
    print(" ".join(command))

    # PyInstaller 실행
    subprocess.run(command, check=True)


if __name__ == "__main__":
    build_executable()
