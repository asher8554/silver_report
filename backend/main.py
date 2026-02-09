from fastapi import FastAPI, BackgroundTasks
from apscheduler.schedulers.background import BackgroundScheduler
import uvicorn
import logging
from datetime import datetime
import asyncio
from dotenv import load_dotenv
import os

from backend.collectors.market_data import collect_market_data
from backend.collectors.news_data import collect_news_data
from backend.collectors.youtube_data import collect_youtube_transcript
from backend.analysis.service import AnalysisService, get_analysis_service

# 환경 변수 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SilverReport")

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Silver Report AI")

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 전역 저장소 (프로토타입용 인메모리 저장소, 추후 SQLite로 교체 예정)
LATEST_REPORT = {
    "timestamp": None,
    "bullish_report": "아직 생성되지 않음.",
    "bearish_report": "아직 생성되지 않음.",
    "market_data": {},
    "news_data": []
}

def job_generate_report():
    """
    주기적으로 데이터를 수집하고 리포트를 생성하는 작업입니다.
    """
    logger.info("정기 리포트 생성 시작...")
    # 1. 데이터 수집
    market_data = collect_market_data()
    news_data = collect_news_data(query="Silver price generic news", days=1)
    
    # 유튜브 데이터 수집 (예시 URL, 실제 앱에서는 검색 또는 리스트 필요)
    # youtube_data = collect_youtube_transcript("...") 
    youtube_data = "유튜브 스크립트 수집은 검색 기능 구현 후 연동 예정."

    # 2. 분석 (낙관적 & 비관적)
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.warning("GEMINI_API_KEY가 없습니다. AI 분석을 건너뜁니다.")
            return

        service = AnalysisService(api_key=api_key)
        
        # 동기 작업에서 비동기 메서드를 호출하기 위해 이벤트 루프 사용
        # APScheduler의 AsyncIOScheduler를 사용하면 더 간단할 수 있음.
        # 여기서는 백그라운드 스레드에서 실행하기 위해 run_until_complete 사용.
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        bullish_report = loop.run_until_complete(
            service.generate_report(market_data, news_data, youtube_data, "bullish")
        )
        bearish_report = loop.run_until_complete(
            service.generate_report(market_data, news_data, youtube_data, "bearish")
        )
        loop.close()

        # 3. 상태 업데이트
        global LATEST_REPORT
        LATEST_REPORT = {
            "timestamp": datetime.now().isoformat(),
            "bullish_report": bullish_report,
            "bearish_report": bearish_report,
            "market_data": market_data,
            "news_data": news_data
        }
        logger.info("리포트 생성 완료.")

    except Exception as e:
        logger.error(f"작업 실패: {e}")

# 스케줄러 설정
scheduler = BackgroundScheduler()
scheduler.add_job(job_generate_report, 'interval', minutes=60)
scheduler.start()

@app.on_event("startup")
async def startup_event():
    logger.info("애플리케이션 시작 중...")
    # 테스트를 위해 초기 작업 즉시 실행 (선택 사항)
    # job_generate_report()

@app.get("/")
def read_root():
    return {"message": "Silver Report AI Service Running"}

@app.get("/report/latest")
def get_latest_report():
    return LATEST_REPORT

@app.get("/data/market")
def get_market_data():
    return LATEST_REPORT.get("market_data", {})

@app.post("/trigger-report")
async def trigger_report(background_tasks: BackgroundTasks):
    """
    리포트 생성을 수동으로 트리거합니다.
    """
    background_tasks.add_task(job_generate_report)
    return {"message": "백그라운드에서 리포트 생성이 시작되었습니다."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
