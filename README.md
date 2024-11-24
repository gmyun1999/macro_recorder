
# 실행 가이드: Macro Recorder 프로젝트

이 문서는 **Macro Recorder** 프로젝트를 실행하는 방법을 설명합니다.

---

## 1. 사전 요구 사항
- Python **3.11** 이상이 설치되어 있어야 합니다.
- `pipenv`가 설치되어 있어야 합니다:
  ```bash
  pip install pipenv
  ```

---

## 2. 프로젝트 설정 및 실행

### 1. 프로젝트 클론
먼저, GitHub에서 프로젝트를 클론합니다:
```bash
git clone https://github.com/gmyun1999/macro_recorder.git
cd macro_recorder
```

### 2. 가상환경 생성 및 의존성 설치
`pipenv`를 사용하여 프로젝트의 가상환경을 생성하고 필요한 의존성을 설치합니다:
```bash
pipenv install
```

### 3. 가상환경 활성화
다음 명령어로 `pipenv` 가상환경을 활성화합니다:
```bash
pipenv shell
```

### 4. 프로그램 실행
프로그램을 실행하려면 다음 명령어를 사용합니다:
```bash
python main.py
```

---

## 3. 주요 명령어 요약

| 단계                   | 명령어                                   |
|------------------------|-----------------------------------------|
| 프로젝트 클론          | `git clone https://github.com/gmyun1999/macro_recorder.git` |
| 의존성 설치            | `pipenv install`                        |
| 가상환경 활성화        | `pipenv shell`                          |
| 프로그램 실행          | `python main.py`                        |

---
