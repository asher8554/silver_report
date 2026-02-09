"""
Gemini API에서 사용 가능한 모델 목록을 조회하는 유틸리티 스크립트입니다.
.env 파일에서 API 키를 로드하여 인증 후 모델 리스트를 출력합니다.
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    # .env 파일 명시적 경로 탐색 시도
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    if os.path.exists(env_path):
        from dotenv import dotenv_values
        config = dotenv_values(env_path)
        api_key = config.get("GEMINI_API_KEY")

if not api_key:
    print("오류: GEMINI_API_KEY를 찾을 수 없습니다.")
    exit(1)

# API 설정
genai.configure(api_key=api_key)

try:
    print("사용 가능한 모델 목록:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"모델 목록 조회 중 오류 발생: {e}")
