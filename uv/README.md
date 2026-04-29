# uv

Rust 기반 초고속 파이썬 패키지/환경 통합 관리 도구. Astral사(ruff 만든 곳)가 2024년에 공개.

**`uv run` 한 방 실행** — `pyproject.toml` 하나 두고 `uv run main.py` 치면 venv 생성·의존성 설치·실행까지 끝난다. activate도 `pip install`도 없음.

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

# 설치 후 쉘 재시작하거나 PATH 반영
source ~/.bashrc
```

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
# httpx/pytest/ruff는 PyPI 패키지명 (예시). uv add 뒤에 설치할 패키지명을 적음
uv add httpx               # 런타임 의존성
uv add --dev pytest ruff   # 개발용 의존성 (배포시 제외, 운영 환경에 섞이지 않게 분리)
```

첫 `uv add` 실행 시 자동으로:

- `.venv/` 가상환경 생성
- 패키지 설치
- `pyproject.toml`에 의존성 기록
- `uv.lock` 생성 (정확한 버전/해시가 박혀서 재현성 보장)

#### 1.3. 실행

```sh
# .venv가 없으면 자동 생성하고, 있으면 알아서 찾아 씀. activate 불필요
uv run main.py           # .py 확장자면 python 생략 가능
uv run python main.py    # 명시적으로 쓰고 싶거나 python -m / -u 플래그 붙일 때
uv run pytest            # venv 내 실행파일은 그냥 이름만
```

#### 1.4. 의존성 제거

```sh
# .venv에서 패키지 제거 + pyproject.toml, uv.lock에서도 해당 항목 빠짐
uv remove httpx
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
uv run <cmd>      # 끝. 파이썬 설치 + .venv 생성 + lock 동기화까지 알아서 하고 실행
```

> `uv sync`는 IDE 인터프리터 연결 등 실행 없이 환경만 미리 깔 때만 쓰면 됨.

### 3. 파이썬 버전 관리 (pyenv 대체)

파이썬 자체를 uv가 설치/전환해준다. 시스템 파이썬 건드리지 않음.

```sh
# 숫자는 파이썬 버전. 3.12, 3.11, 3.10.14 같이 적음
uv python install 3.12 3.11    # 여러 버전 설치 (공백으로 나열)
uv python list                 # 설치된 버전 목록
uv python pin 3.12             # 현재 프로젝트를 3.12로 고정 (.python-version에 기록, uv run시 그 버전 사용)
```

### 4. 전역 CLI 툴 (pipx 대체)

```sh
# ruff, mypy 같이 프로젝트 의존성이 아니라 커맨드로 쓰고 싶은 도구용
# 각 도구마다 ~/.local/share/uv/tools/ 에 독립된 venv가 생기고, ~/.local/bin/ 에 심링크가 꽂힘
# → sudo 없이도 PATH에 잡혀서 아무 쉘에서나 호출 가능, 도구끼리 의존성 충돌도 없음
uv tool install ruff           # 설치 후 어느 디렉토리에서든 `ruff`로 실행 가능
uv tool install mypy
uv tool list                   # 설치된 도구 목록
uv tool upgrade --all          # 전체 업그레이드

# 설치 없이 1회성으로 쓰고 싶으면 uvx (= uv tool run의 축약형)
uvx ruff check .               # 캐시에만 받아 즉시 실행
uvx cowsay "hello uv"
```

프로젝트 내부에서만 쓰고 싶으면 `uv tool install`이 아니라 `uv add --dev`를 쓴다.

- `uv tool install <pkg>`: 사용자 환경 어디서든 호출 가능. 프로젝트와 무관
- `uv add --dev <pkg>`: 이 프로젝트 한정. `uv run <pkg>`로 실행

### 5. 인라인 스크립트 의존성 (PEP 723)

프로젝트 만들기도 귀찮은 단발성 스크립트용. 파일 상단 주석에 의존성을 적어두면 uv가 임시 가상환경을 만들어서 돌린다.

```py
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "rich"]
# ///
import httpx
from rich import print
print(httpx.get("https://httpbin.org/ip").json())
```

```sh
# # /// script ~ # /// 블록이 PEP 723 표준 포맷
# dependencies에 쓴 패키지를 uv가 격리된 환경에 설치 후 실행 (pyproject.toml 불필요)
uv run inline_script.py
```

> 프로젝트의 `.venv`와는 **별도로 격리된 임시 환경**에서 돈다. 같은 폴더의 `pyproject.toml`이 있어도 영향 안 주고, 스크립트 종료 후 캐시만 남음.

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

- **`uv.lock`과 `.python-version`은 커밋**. `.venv`는 `.gitignore`로 관리
- **배포서버에 uv 못 깔면**: `uv export -o requirements.txt` 후 기존 pip 파이프라인에 태우기
- **Docker**: 공식 이미지 `ghcr.io/astral-sh/uv` 제공. 멀티스테이지로 사이즈 절감 가능
- **CI**: `astral-sh/setup-uv` GitHub Action으로 몇 초만에 세팅

## 참고

- 공식 문서: https://docs.astral.sh/uv/
- GitHub: https://github.com/astral-sh/uv
