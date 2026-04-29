"""
uv run 예제용 스크립트.

pyproject.toml에 선언된 httpx를 실제로 사용 → `uv run main.py` 시
uv가 .venv 생성 + httpx 설치 + 실행까지 한 번에 처리하는 걸 확인할 수 있다.

(httpx는 시스템 파이썬에 없는 패키지라, 프로젝트 없이 그냥 돌리면
 ModuleNotFoundError가 나서 uv의 격리/자동설치 동작이 눈에 띄게 드러난다.)

실행:
    uv run main.py
"""
import sys

import httpx


def main() -> None:
    print(f"Hello from uv! (python {sys.version_info.major}.{sys.version_info.minor})")
    ip = httpx.get("https://httpbin.org/ip", timeout=5).json()
    print(f"my ip: {ip['origin']}")


if __name__ == "__main__":
    main()
