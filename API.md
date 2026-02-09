# API 문서 (Silver Report AI)

## 개요
FastAPI를 사용하여 제공되는 REST API 명세입니다.

Base URL: `http://localhost:8000`

## 엔드포인트

### 1. 헬스 체크

- **URL**: `/`
- **Method**: `GET`
- **Description**: 서버 상태를 확인합니다.
- **Response**:
  ```json
  {
    "message": "Silver Report AI Service Running"
  }
  ```

### 2. 최신 리포트 조회

- **URL**: `/report/latest`
- **Method**: `GET`
- **Description**: 생성된 최신 리포트와 분석 데이터를 반환합니다.
- **Response**:
  - `timestamp`: 리포트 생성 시간
  - `bullish_report`: 낙관적 분석 내용
  - `bearish_report`: 비관적 분석 내용
  - `market_data`: 수집된 시장 데이터
  - `news_data`: 수집된 뉴스 데이터

### 3. 시장 데이터 조회

- **URL**: `/data/market`
- **Method**: `GET`
- **Description**: 수집된 최신 시장 데이터만 반환합니다.

### 4. 리포트 생성 트리거

- **URL**: `/trigger-report`
- **Method**: `POST`
- **Description**: 리포트 생성 작업을 백그라운드에서 즉시 시작합니다.
- **Response**:
  ```json
  {
    "message": "백그라운드에서 리포트 생성이 시작되었습니다."
  }
  ```
