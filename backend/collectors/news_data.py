from tavily import TavilyClient
import os
import json
from datetime import datetime

# Initialize Tavily client
# You should set TAVILY_API_KEY in your .env file
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def collect_news_data(query="Silver price news", days=1):
    """
    Collects news articles using Tavily API.
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
        # Return empty list to avoid crashing the app
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
