import httpx
from dotenv import load_dotenv
import os
import json

load_dotenv()

INPUT_FILENAME = "selected_market.json"

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

with open (INPUT_FILENAME, 'r', encoding = 'utf-8') as f:
    selected_market = json.load(f)

def get_news_articles():
    """
    Searches for news articles on the given market. Use this to find any recent information on the topic.
    """

    market_question = selected_market['question']

    news_api_url = "https://newsapi.org/v2/everything"
    params = {
        "q": market_question,
        "from": selected_market['startDate'],
        "sortBy": "popularity",
        "apiKey": NEWS_API_KEY,
    }
    
    search_results = httpx.get(news_api_url, params=params)
    search_results.raise_for_status()

    return search_results.json()

news_articles = get_news_articles()

print(news_articles)


    


