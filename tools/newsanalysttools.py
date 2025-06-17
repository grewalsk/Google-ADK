import requests
from dotenv import load_dotenv
import os
import json
from bs4 import BeautifulSoup

load_dotenv()

INPUT_FILENAME = "selected_market.json"

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

with open (INPUT_FILENAME, 'r', encoding = 'utf-8') as f:
    selected_market = json.load(f)


# Might have to use paignation. 

def get_news_articles():
    """
    Searches for recent news articles related to a specific market question.
    Only use this tool to gather raw, unfiltered news articles.
    """

    market_question = selected_market['question']

    print(f"Tool 'fetch_news_for_market' called with question: '{market_question}'")

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

def scrape_and_assess_news_impact(news_articles_json, market_question):
    """
    Scrapes the full text from article URLs, then analyzes the article content to create a summary
    and assess the likely impact on a specific question about a Polymarket market.

    Use this AFTER fetching news articles with the get_news_articles tool.

    
    Args:
        news_articles_json: The JSON object containing a list of news articles with URLs.
        market_question: The full question text from the Kalshi market for context.
    """

    print(f"Tool 'scrape_and_assess_news_impact' called for question: '{market_question}'")

    article_data = news_articles_json['data']
    if not article_data:
        return "No articles found in the provided JSON. Cannot perform analysis."
    
    context_block = ""

    for i, article in enumerate(article_data):
        url = article["url"]
        if not url:
            continue
        
        print(f"Scraping URL: {url}")

        try: 
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            page_response = requests.get(url, headers=headers, timeout=10)
            page_response.raise_for_status()

            soup = BeautifulSoup(page_response.content, "html.parser")

            article_body = soup.find('article') or soup.find('main')

        except Exception as e: 





    


