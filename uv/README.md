# uv

Rust 기반 초고속 파이썬 패키지/환경 통합 관리 도구. Astral사(ruff 만든 곳)가 2024년에 공개.

## 왜 쓰냐

- `파이썬 환경 구축시 더 이상 고민하지 않아도 됨. 빠르게 구축하고 개발단계로 진입 가능.`
- 빠름. 진짜 빠름.
- 파편화된 파이썬 환경 관리도구를 일원화
- uv 채택시 특정 마이너한 도구에 의존하는게 아닌가 걱정하지 않아도 됨
  - 현시점(2026)기준 사실상 표준, 대세로 자리잡음 
  - 핵심 설정파일 pyproject.toml은 파이썬 표준이기도 해서 uv가 아니어도 활용가능

## 주요 특징

- 압도적 속도: `pip` 대비 10~100배
- 도구 통합: pyenv, venv, pip, pipx, conda, poetry, ... 를 하나로
- 환경설정 통합
  - requirements.txt, setup.py, ... 등을 하나로
  - 모든 환경선언은 `pyproject.toml`에 하며, 이는 파이썬 표준(PEP621)
  - 최종 확정된 환경은 `uv.lock` 파일로 자동생성되어 공유,재현성 쉬움
- activate 불필요: `uv run` 한 줄로 프로젝트 환경에서 실행
- pip 호환: `uv pip` 서브커맨드로 기존 워크플로 그대로 이전 가능

## 설치

```sh
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 혹은 pipx / brew / pip
pipx install uv
brew install uv
```

설치 후 쉘 재시작하거나 `source ~/.bashrc`.

## 핵심 워크플로

### 1. 신규 프로젝트

#### 1.1. 프로젝트 생성

```sh
uv init myproj
cd myproj
```

`myproj` 디렉토리와 함께 아래 파일들이 생성된다.

```
myproj/
├── pyproject.toml     # 프로젝트 설정/의존성 명세 (가장 중요)
├── .python-version    # 이 프로젝트가 쓸 파이썬 버전
├── main.py            # 샘플 스크립트
├── README.md          # 기본 템플릿
└── .gitignore         # 기본 템플릿
```

#### 1.2. 의존성 추가

```sh
# requests/pytest/ruff는 PyPI 패키지명 (예시). uv add 뒤에 설치할 패키지명을 적음
uv add requests            # 런타임 의존성
uv add --dev pytest ruff   # 개발용 의존성 (배포시 제외, 운영 환경에 섞이지 않게 분리)
```

첫 `uv add` 실행 시 자동으로:

- `.venv/` 가상환경 생성
- 패키지 설치
- `pyproject.toml`에 의존성 기록
- `uv.lock` 생성 (정확한 버전/해시가 박혀서 재현성 보장)

#### 1.3. 실행

```sh
# uv run이 .venv를 알아서 찾아 씀. source .venv/bin/activate 불필요
uv run python main.py
uv run pytest
```

#### 1.4. 의존성 제거

```sh
# .venv에서 패키지 제거 + pyproject.toml, uv.lock에서도 해당 항목 빠짐
uv remove requests
```

#### 1.5. 커밋 규칙 (중요) 📌

- 커밋 O:
  - `pyproject.toml`: 모든 선언적 설정
  - `uv.lock`: 패키지 확정(pin)
  - `.python-version`: 파이썬 버전 확정(pin)
  - 팀원/배포서버가 같은 환경을 재현하려면 필수
- 커밋 X:
  -  `.venv/`: 용량 크고 OS 종속적이라 절대 커밋 금지. uv init 시 gitignore에 기본 등록됨.

### 2. 기존 프로젝트 합류

`pyproject.toml` + `uv.lock`이 있는 저장소를 받았을 때.

```sh
git clone <repo> && cd <repo>
uv sync           # uv.lock에 박힌 버전 그대로 .venv 복원 (로컬/원격이 같은 환경)
uv run <cmd>      # 실행. <cmd>는 python main.py, pytest 같은 실행할 명령어
```

### 3. 파이썬 버전 관리 (pyenv 대체)

파이썬 자체를 uv가 설치/전환해준다. 시스템 파이썬 건드리지 않음.

```sh
# 숫자는 파이썬 버전. 3.12, 3.11, 3.10.14 같이 적음
uv python install 3.12 3.11    # 여러 버전 설치 (공백으로 나열)
uv python list                 # 설치된 버전 목록
uv python pin 3.12             # 현재 프로젝트를 3.12로 고정 (.python-version에 기록, uv run시 그 버전 사용)
```

### 4. 전역 CLI 툴 (pipx 대체)

`ruff`, `mypy` 같이 프로젝트 의존성이 아니라 커맨드로 쓰고 싶은 도구를 시스템 전역에 깔 때 쓴다. 각 도구별로 독립된 환경에 설치돼서 서로 충돌 안 남.

```sh
uv tool install ruff           # 설치 후 어디서든 `ruff` 로 실행 가능
uv tool install mypy
uv tool list                   # 설치된 도구 목록
uv tool upgrade --all          # 전체 업그레이드
```

프로젝트 내부에서만 쓰고 싶으면 `uv tool install`이 아니라 `uv add --dev`를 쓴다. 둘 차이:

- `uv tool install ruff`: 시스템 어디서든 `ruff` 명령 사용 가능. 프로젝트와 무관
- `uv add --dev ruff`: 이 프로젝트 한정. `uv run ruff`로 실행

### 5. 인라인 스크립트 의존성 (PEP 723)

프로젝트 만들기도 귀찮은 단발성 스크립트용. 파일 상단 주석에 의존성을 적어두면 uv가 임시 가상환경을 만들어서 돌린다.

```py
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "rich"]
# ///
import requests
from rich import print
print(requests.get("https://httpbin.org/ip").json())
```

```sh
# # /// script ~ # /// 블록이 PEP 723 표준 포맷
# dependencies에 쓴 패키지를 uv가 격리된 환경에 설치 후 실행 (pyproject.toml 불필요)
uv run script.py
```

예제는 [`inline_script.py`](./inline_script.py) 참고.

## 명령어 치트시트

```sh
# 프로젝트
uv init [name]              # 새 프로젝트
uv add <pkg>                # 의존성 추가
uv add --dev <pkg>          # 개발용 의존성
uv remove <pkg>             # 의존성 제거
uv sync                     # lock 기준으로 환경 맞추기
uv lock                     # lock 갱신
uv run <cmd>                # 프로젝트 환경에서 실행
uv tree                     # 의존성 트리

# 파이썬 버전
uv python install <ver>     # 설치
uv python pin <ver>         # 프로젝트 버전 고정
uv python list              # 설치된 목록

# 전역 툴
uv tool install <pkg>       # 설치
uv tool run <cmd>           # 1회성 실행 (uvx로 별칭)
uv tool list                # 설치된 목록

# pip 호환 (낮은 수준 작업)
uv pip install <pkg>
uv pip list
uv pip freeze

# 내보내기
uv export -o requirements.txt --no-hashes    # requirements.txt 생성
```

## 기존 프로젝트 마이그레이션

### requirements.txt → pyproject.toml

```sh
cd existing_project
uv init --bare                          # pyproject.toml만 만들고 샘플코드 생성X
uv add --requirements requirements.txt  # 기존 의존성 그대로 옮기기
uv lock                                 # uv.lock 생성
```

### poetry → uv

```sh
# poetry export로 requirements 만든 뒤 위와 동일
poetry export -f requirements.txt -o requirements.txt
uv add --requirements requirements.txt
```

## 팀/배포 시 고려사항

- **uv.lock은 커밋**. venv와 .python-version도 .gitignore로 관리
- **배포서버에 uv 못 깔면**: `uv export -o requirements.txt` 후 기존 pip 파이프라인에 태우기
- **Docker**: 공식 이미지 `ghcr.io/astral-sh/uv` 제공. 멀티스테이지로 사이즈 절감 가능
- **CI**: `astral-sh/setup-uv` GitHub Action으로 몇 초만에 세팅

## 단점 / 주의점

- 2024년에 나온 신생 도구. 사내 정책이 엄격하면 도입 장벽 있음
- 이미 poetry/pdm에 팀이 익숙하면 전환 비용 존재
- 배포 타깃 환경에 uv 없으면 `uv export` 한 번 거쳐야 함

## 참고

- 공식 문서: https://docs.astral.sh/uv/
- GitHub: https://github.com/astral-sh/uv
