import os
import json
import asyncio
import logging
from datetime import datetime
from dotenv import load_dotenv

# 백엔드 모듈 임포트 (경로 설정 필요)
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from collectors.market_data import collect_market_data
from collectors.news_data import collect_news_data
from analysis.service import AnalysisService

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("StaticGenerator")

# 환경 변수 로드
load_dotenv()

async def generate_static_data():
    logger.info("정적 데이터 생성 시작...")

    # 1. 데이터 수집
    logger.info("시장 데이터 수집 중...")
    market_data = collect_market_data()
    
    # 데이터 수집 실패 시 샘플 데이터 사용 (배포 환경에서 빈 데이터로 인한 크래시 방지)
    if not market_data or not market_data.get("Silver") or len(market_data["Silver"]) == 0:
        logger.warning("시장 데이터 수집 실패. 샘플 데이터를 사용합니다.")
        current_time = datetime.now()
        market_data = {
            "Silver": [
                {"Datetime": current_time.strftime("%Y-%m-%dT10:00:00"), "Open": 30.5, "High": 30.8, "Low": 30.3, "Close": 30.6, "Volume": 1000},
                {"Datetime": current_time.strftime("%Y-%m-%dT11:00:00"), "Open": 30.6, "High": 30.9, "Low": 30.5, "Close": 30.7, "Volume": 1100},
                {"Datetime": current_time.strftime("%Y-%m-%dT12:00:00"), "Open": 30.7, "High": 31.0, "Low": 30.6, "Close": 30.9, "Volume": 1200}
            ],
            "Gold": [
                {"Datetime": current_time.strftime("%Y-%m-%dT10:00:00"), "Open": 2050.0, "High": 2055.0, "Low": 2048.0, "Close": 2052.0, "Volume": 500}
            ],
            "Bitcoin": [
                {"Datetime": current_time.strftime("%Y-%m-%dT10:00:00"), "Open": 45000.0, "High": 45500.0, "Low": 44800.0, "Close": 45200.0, "Volume": 100}
            ],
            "USD_Index": []
        }
    
    logger.info("뉴스 데이터 수집 중...")
    news_data = collect_news_data(query="Silver price generic news", days=1)
    
    if not news_data:
        logger.warning("뉴스 데이터 수집 실패. 샘플 데이터를 사용합니다.")
        news_data = [
            {
                "title": "데이터 수집 실패: 샘플 뉴스",
                "url": "#",
                "published_date": datetime.now().isoformat()
            }
        ]
    
    youtube_data = "유튜브 스크립트 수집은 검색 기능 구현 후 연동 예정."

    # 2. AI 분석 (낙관적 & 비관적)
    bullish_report = "AI 분석 실패 (API Key 없음)"
    bearish_report = "AI 분석 실패 (API Key 없음)"

    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        try:
            logger.info("AI 분석 시작...")
            service = AnalysisService(api_key=api_key)
            bullish_report = await service.generate_report(market_data, news_data, youtube_data, "bullish")
            bearish_report = await service.generate_report(market_data, news_data, youtube_data, "bearish")
        except Exception as e:
            logger.error(f"AI 분석 중 오류 발생: {e}")
            bullish_report = f"분석 오류: {e}"
            bearish_report = f"분석 오류: {e}"
    else:
        logger.warning("GEMINI_API_KEY가 설정되지 않았습니다.")

    # 3. 데이터 구조화
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "bullish_report": bullish_report,
        "bearish_report": bearish_report,
        "market_data": market_data,
        "news_data": news_data
    }

    # 4. JSON 파일 저장
    # frontend/public/data.json 에 저장
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "public")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "data.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

    logger.info(f"데이터가 저장되었습니다: {output_path}")

if __name__ == "__main__":
    asyncio.run(generate_static_data())
