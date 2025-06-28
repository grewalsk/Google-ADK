import requests
from dotenv import load_dotenv
import os
import json
from bs4 import BeautifulSoup
import re

load_dotenv()

INPUT_FILENAME = "selected_market.json"

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

with open (INPUT_FILENAME, 'r', encoding = 'utf-8') as f:
    selected_market = json.load(f)


# Might have to use paignation. 

def get_news_articles(keywords: str):
    """
    Searches for recent news articles related to a specific market question.
    Only use this tool to gather raw, unfiltered news articles.
    """

    print(f"Tool 'fetch_news_for_market' called with question: '{keywords}'")

    news_api_url = "https://api.thenewsapi.com/v1/news/top"

    date = selected_market['startDate'].split(".")[0]

    params = {
        "search": keywords,
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

            if article_body:
                paragraphs = article.body.find_all('p')
            
            else:
                paragraphs = soup.find_all('p')

            full_text = " ".join([p.get_text() for p in paragraphs])

            cleaned_text = re.sub(r'\s+', ' ', full_text).strip()

        # Code below can be improved. 
            context_block += f"Article {i+1} (Source: {article.get('source')}):\n"
            context_block += f"Title: {article.get('title')}\n"
            context_block += f"Full Text Summary: {cleaned_text[:1000]}...\n---\n" # TO avoid huge prompts

        except Exception as e:
            print(f"  > Failed to scrape or parse URL {url}: {e}")
            # Add the snippet as a fallback if scraping fails
            context_block += f"Article {i+1} (Source: {article.get('source')}, SCRAPE FAILED):\n"
            context_block += f"Title: {article.get('title')}\n"
            context_block += f"Snippet: {article.get('snippet')}\n---\n"

    if not context_block:
        return "Could not extract content from any of the provided article URLs."
    
    return f"""
    **Analysis of Scraped News Content:**

    **Market Context:** "{market_question}"

    **Full Article Content Provided:**
    {context_block}

    **Assessment Task:**
    Based on the FULL TEXT from the articles above, provide a neutral, one-paragraph summary. Then, state whether the collective news sentiment leans towards a "Yes" or "No" outcome for the market question, and briefly explain why, citing specifics from the text.
    """





    


