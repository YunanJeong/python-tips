"""
uv run 예제용 스크립트.

실행:
    uv run hello.py
"""
import sys


def main() -> None:
    print(f"Hello from uv! (python {sys.version_info.major}.{sys.version_info.minor})")


if __name__ == "__main__":
    main()
