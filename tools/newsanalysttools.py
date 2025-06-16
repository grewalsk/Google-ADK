import requests
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

    news_api_url = "https://api.thenewsapi.com/v1/news/top"

    date = selected_market['startDate'].split(".")[0]

    params = {
        "search": market_question,
        "published_after": date,
        "api_token": NEWS_API_KEY,
        "language": "en",
        "sort": "relevance_score",
        "limit": 3,
    }
    
    try:
        response = requests.get(news_api_url, params=params)
        response.raise_for_status()
        filename = "news_articles.json"
        with open(filename, 'w') as outfile:
            json.dump(response.json(), outfile, indent=2, sort_keys=False)
        return response.json()
    
    except requests.exceptions.HTTPError as http_err:
        return {
            "error": "HTTP error occurred",
            "details": str(http_err),
            "response_text": response.text  
        }
    
    except requests.exceptions.RequestException as req_e:
        return {"error": "A request error occurred", "details": str(req_e)}
    except Exception as e:
        return {"error": "An unknown error occurred", "details": str(e)}

news_articles = get_news_articles()

print(news_articles)


    


