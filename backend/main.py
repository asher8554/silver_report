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

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SilverReport")

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Silver Report AI")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global storage (In-memory for prototype, replace with SQLite later)
LATEST_REPORT = {
    "timestamp": None,
    "bullish_report": "Not generated yet.",
    "bearish_report": "Not generated yet.",
    "market_data": {},
    "news_data": []
}

def job_generate_report():
    """
    Scheduled job to collect data and generate reports.
    """
    logger.info("Starting scheduled report generation...")
    # 1. Collect Data
    market_data = collect_market_data()
    news_data = collect_news_data(query="Silver price generic news", days=1)
    
    # YouTube (Example URL, in real app needs to search or list)
    # youtube_data = collect_youtube_transcript("...") 
    youtube_data = "YouTube transcript collection pending implementation of search."

    # 2. Analyze (Bullish & Bearish)
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.warning("GEMINI_API_KEY missing. Skipping AI analysis.")
            return

        service = AnalysisService(api_key=api_key)
        
        # We need an async loop here if calling async method from sync job
        # Often easier to use asyncio.run or make job async if scheduler supports it.
        # APScheduler AsyncIOScheduler supports async jobs.
        # But here run_until_complete is simple for background thread.
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        bullish_report = loop.run_until_complete(
            service.generate_report(market_data, news_data, youtube_data, "bullish")
        )
        bearish_report = loop.run_until_complete(
            service.generate_report(market_data, news_data, youtube_data, "bearish")
        )
        loop.close()

        # 3. Update State
        global LATEST_REPORT
        LATEST_REPORT = {
            "timestamp": datetime.now().isoformat(),
            "bullish_report": bullish_report,
            "bearish_report": bearish_report,
            "market_data": market_data,
            "news_data": news_data
        }
        logger.info("Report generation completed.")

    except Exception as e:
        logger.error(f"Job failed: {e}")

# Scheduler Setup
scheduler = BackgroundScheduler()
scheduler.add_job(job_generate_report, 'interval', minutes=60)
scheduler.start()

@app.on_event("startup")
async def startup_event():
    logger.info("Application starting...")
    # Run initial job immediately for testing (optional)
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
    Manually trigger report generation.
    """
    background_tasks.add_task(job_generate_report)
    return {"message": "Report generation triggered in background."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
