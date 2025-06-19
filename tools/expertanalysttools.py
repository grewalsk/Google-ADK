import requests
from dotenv import load_dotenv
import os
import json
from bs4 import BeautifulSoup

#TO BE UPDATED AND FIXED

load_dotenv()

#want the ai model to craft a question based on the thing to pass to the json. 
with open("selected_market.json", 'r', encoding = 'utf-8') as f:
    selected_market = json.load(f)

def search_expert_sources(keywords: str) -> list[dict]:
    """
    Searches the web for information related to a specific query.
    Only use this tool to gather raw, unfiltered information.
    """

    url = "https://www.googleapis.com/customsearch/v1"

    params = {
        "key": os.getenv("GOOGLE_CUSTOM_SEARCH_API_KEY"),
        "cx": os.getenv("GOOGLE_CX"),
        "q": keywords,
        "dateRestrict": selected_market['startDate'],
        "num": 5,
        "sort": "date"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    with(open("expert_sources.json", 'w') as outfile):
        json.dump(data, outfile, indent=2, sort_keys=False)

    return data 

search_expert_sources("Pacers NBA 2025")


#NEEDS FIXING

def scrape_and_analyze_url(data: json) -> str:

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    with open(data, 'r', encoding = 'utf-8') as f:
        expert_sources = json.load(f)

    try: 
        for item in data['items']:
            title = item.get('title')
            link = item.get('link')
            snippet = item.get('snippet')

            if not link:
                continue

            response = requests.get(link, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            article_body = soup.find('article') or soup.find('main')

            if article_body:
                paragraphs = article_body.find_all('p')
            
            else:
                paragraphs = soup.find_all('p')

            full_text = " ".join([p.get_text() for p in paragraphs])

            article_data = {
                "title": title,
                "url": link,
                "source_snippet": snippet,
                "scraped_content": full_text
            }

            with open("finalscrape", 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=4)

            return article_data.json()
        
    except IOError as e:
        print(f"Error writing to file: {e}")
    except Exception as e:
        print(f"  > Failed to scrape or parse URL {link}: {e}")


scrape_and_analyze_url("expert_sources.json")

    
    