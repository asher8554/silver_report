# Project Definition: Silver Investment Analyst (Silver Report)

## 1. Project Goal & Core Value

**Goal**: Silver (SLV)를 중심으로 Gold, Bitcoin, AI 기술 트렌드, 거시 경제 지표를 종합 분석하여 투자 방향성을 제시하는 자동화된 웹 서비스 구축.
**Core Value**:

- **다각도 분석**: 단순 시세 확인이 아닌, 상관관계(금/은/비트코인)와 기술 트렌드(AI)를 복합적으로 고려.
- **균형 잡힌 시각**: 확증 편향을 방지하기 위해 **낙관론(Bull)**과 **비관론(Bear)** 리포트를 동시에 생성.
- **자동화 & 접근성**: 매시간 최신 정보를 수집하여 웹에서 즉시 확인 가능 (Time-saving).

## 2. Target User

- **User**: 본인 (개인 투자자).
- **Needs**:
  - 투자 전문가들이 보는 깊이 있는 뉴스 및 유튜브 숏/롱폼 분석 내용을 놓치고 싶지 않음.
  - 아름답고 직관적인 UI로 복잡한 데이터를 한눈에 파악하고 싶음.
  - 언제 어디서든 웹으로 접속해 현재 시장 상황을 **1시간 단위**로 파악하고 싶음.

## 3. Key Features

1.  **자동 데이터 수집 (Hourly)**:
    - **뉴스**: 주요 경제 뉴스, 원자재(은/금) 관련 속보, AI 기술 트렌드.
    - **유튜브**: 투자 전문가 채널의 최신 영상 요약 및 센티먼트 분석.
    - **시세**: SLV, Gold, BTC, 주요 지수 실시간 데이터.
2.  **AI Analyst Reports**:
    - 수집된 데이터를 바탕으로 LLM이 작성한 **낙관적(Bullish) 리포트** vs **비관적(Bearish) 리포트**.
    - 최종 투자 판단을 위한 종합 스코어링 (예: 매수 강도 1~10).
3.  **Interactive Dashboard**:
    - **시각화**: 가격 추이, 자산 간 상관관계 히트맵, 뉴스 키워드 클라우드.
    - **타임라인**: 시간대별 시장 이슈 타임라인.
4.  **Archive**: 과거 리포트 및 적중률 조회.

## 4. Tech Stack & Tools

**"Beautiful UI, Powerful Data Processing"**

- **Frontend (UI/UX)**: **HTML, Javascript, CSS**
  - 선정 이유: 사용자가 쉽게 웹 서비스를 보고 접근할 수 있는 최신 UI를 위한 모던 웹 기술 스택.
- **Backend (Server/Data)**: **Python**
  - 선정 이유: 데이터 수집(Crawling), 데이터 분석(Pandas), AI 연산에 가장 강력한 언어.
- **Database**: **SQLite** (가볍고 관리가 편한 로컬 DB)
- **AI/LLM**: Google Gemini API (Analysis & Summary)

## 5. Recommended MCPs & Data Sources

- **News**: `Tavily API` (Google Search보다 정제된 AI용 검색 결과 제공, 강력 추천)
- **YouTube**: `Youtube-Transcript-Server` (이미 사용 가능, 영상 자막 추출 용도)
- **Market Data**: `Yahoo Finance` (yfinance 라이브러리 사용, 무료 및 안정적)

## 6. Success Metrics

- **Functional**: 1시간마다 새로운 리포트와 데이터가 갱신되어야 함.
- **UX**: 웹 페이지 로딩 속도 < 2초, 모바일/데스크턳에서 그래프가 깨지지 않아야 함.
- **Quality**: 리포트가 단순 나열이 아닌 "인사이트"를 포함해야 함 (낙관/비관 논리 명확성).
