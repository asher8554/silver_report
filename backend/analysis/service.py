import google.generativeai as genai
import os
from .prompts import BULLISH_PROMPT_TEMPLATE, BEARISH_PROMPT_TEMPLATE
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalysisService:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Gemini API Key is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def generate_report(self, market_data: dict, news_data: list, youtube_data: list, report_type: str = "bullish") -> str:
        """
        Generates an investment report based on the provided data and type.
        report_type: 'bullish' or 'bearish'
        """
        try:
            # Select Prompt Template
            if report_type.lower() == "bullish":
                prompt_template = BULLISH_PROMPT_TEMPLATE
            elif report_type.lower() == "bearish":
                prompt_template = BEARISH_PROMPT_TEMPLATE
            else:
                raise ValueError("Invalid report type. Use 'bullish' or 'bearish'.")

            # Prepare Context
            context = prompt_template.format(
                market_data=str(market_data)[:5000],  # Truncate if too long (rough limit)
                news_data=str(news_data)[:3000],
                youtube_data=str(youtube_data)[:3000]
            )

            # Generate Content
            logger.info(f"Generating {report_type} report...")
            response = self.model.generate_content(context)
            
            return response.text

        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return f"Error generating report: {e}"

# Singleton instance placeholder
analysis_service = None

def get_analysis_service():
    global analysis_service
    if analysis_service is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            analysis_service = AnalysisService(api_key)
    return analysis_service
