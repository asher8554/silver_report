from tavily import TavilyClient
import os
import json
from datetime import datetime

# Tavily 클라이언트 초기화
# .env 파일에 TAVILY_API_KEY를 설정해야 합니다.
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def collect_news_data(query="Silver price news", days=1):
    """
    Tavily API를 사용하여 뉴스 기사를 수집합니다.
    """
    if not TAVILY_API_KEY:
        print("Error: TAVILY_API_KEY not found in environment variables.")
        return []

    try:
        if not TAVILY_API_KEY:
            raise ValueError("TAVILY_API_KEY is not set")
            
        tavily = TavilyClient(api_key=TAVILY_API_KEY)
        response = tavily.search(query, search_depth="advanced", topic="news", days=days)
        return response.get("results", [])
    except Exception as e:
        print(f"Error collecting news: {e}")
        # 앱이 중단되지 않도록 빈 리스트 반환
        return []

if __name__ == "__main__":
    # Test execution
    if TAVILY_API_KEY:
        news = collect_news_data()
        print(f"Found {len(news)} articles.")
        for article in news[:3]:
            print(f"- {article['title']} ({article['url']})")
    else:
        print("Please set TAVILY_API_KEY to test.")
