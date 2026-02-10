import google.generativeai as genai
import os
from .prompts import BULLISH_PROMPT_TEMPLATE, BEARISH_PROMPT_TEMPLATE
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalysisService:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Gemini API Key is required")
        
        genai.configure(api_key=api_key)
        # 사용 가능한 모델 목록 (더 많은 변형 포함)
        self.models = [
            'gemini-1.5-flash', 
            'gemini-1.5-flash-latest',
            'gemini-1.5-pro',
            'gemini-1.5-pro-latest',
            'gemini-2.0-flash-exp'
        ]
        self.current_model_name = self.models[0]
        self.model = genai.GenerativeModel(self.current_model_name)

    async def generate_report(self, market_data: dict, news_data: list, youtube_data: list, report_type: str = "bullish") -> str:
        """
        제공된 데이터와 타입을 기반으로 투자 리포트를 생성합니다.
        여러 모델을 시도하여 성공할 때까지 반복합니다.
        report_type: 'bullish' (낙관적) 또는 'bearish' (비관적)
        """
        prompt_template = ""
        if report_type.lower() == "bullish":
            prompt_template = BULLISH_PROMPT_TEMPLATE
        elif report_type.lower() == "bearish":
            prompt_template = BEARISH_PROMPT_TEMPLATE
        else:
            return "Error: Invalid report type."

        context = prompt_template.format(
            market_data=str(market_data)[:10000], 
            news_data=str(news_data)[:5000],
            youtube_data=str(youtube_data)[:3000]
        )

        errors = []
        for model_name in self.models:
            try:
                logger.info(f"Generating {report_type} report using {model_name}...")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(context)
                return response.text
            except Exception as e:
                logger.warning(f"Failed with {model_name}: {e}")
                errors.append(f"{model_name}: {str(e)}")
                continue
        
        error_msg = " | ".join(errors)
        logger.error(f"All models failed. Errors: {error_msg}")
        return f"Error generating report (All models failed): {error_msg}"

# 싱글톤 인스턴스 플레이스홀더
analysis_service = None

def get_analysis_service():
    global analysis_service
    if analysis_service is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            analysis_service = AnalysisService(api_key)
    return analysis_service
