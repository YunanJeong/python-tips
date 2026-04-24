# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
#     "rich",
# ]
# ///
"""
PEP 723 인라인 의존성 예제.

실행:
    uv run inline_script.py

uv가 임시 가상환경을 만들어 requests, rich를 설치하고 실행한다.
프로젝트 구조 없이 단일 파일 스크립트로 외부 패키지를 쓸 수 있음.
"""
import requests
from rich import print

resp = requests.get("https://httpbin.org/ip", timeout=5)
print("[bold green]내 IP 정보:[/bold green]", resp.json())
