# Silver Report AI

은(Silver), 금(Gold), 비트코인(Bitcoin)의 시장 데이터를 수집하고 AI를 통해 투자 리포트를 생성하는 프로젝트입니다.

## 프로젝트 구조

- **backend/**: FastAPI 기반의 백엔드 서버. 데이터 수집 및 Gemini AI 연동 담당.
- **frontend/**: Next.js 기반의 프론트엔드. 리포트 및 차트 시각화 담당.

## 시작하기 (Getting Started)

### 사전 요구사항

- Python 3.8+
- Node.js 18+
- Gemini API Key
- Tavily API Key

### 백엔드 실행

1. `backend` 디렉토리로 이동합니다.
2. 가상 환경을 생성하고 활성화합니다.
3. 의존성을 설치합니다: `pip install -r requirements.txt` (루트 또는 backend 내)
4. `.env` 파일을 설정합니다.
5. 서버 실행:
   ```bash
   python backend/main.py
   ```

### 프론트엔드 실행

1. `frontend` 디렉토리로 이동합니다.
2. 의존성을 설치합니다: `npm install`
3. 개발 서버 실행:
   ```bash
   npm run dev
   ```

## 기능

- **데이터 수집**: Yahoo Finance, Tavily News, YouTube(예정)
- **AI 분석**: Google Gemini 모델을 사용한 낙관적/비관적 리포트 생성
- **시각화**: Recharts를 이용한 가격 차트 및 리포트 대시보드

## 라이선스

MIT License
