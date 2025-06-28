import requests
from dotenv import load_dotenv
import os
import json
from bs4 import BeautifulSoup
from datetime import datetime

#TO BE UPDATED AND FIXED

load_dotenv()

#want the ai model to craft a question based on the thing to pass to the json. 
with open("selected_market.json", 'r', encoding = 'utf-8') as f:
    selected_market = json.load(f)

def search_expert_sources(keywords: str) -> list[dict]:
    """
    Searches the web for information related to a specific query.
    Only use this tool to gather raw, unfiltered information.

    Args: 
        keywords (str): a single string of keywords to search for.

    Returns: 
        list[dict]: A JSON object, each containing information about a search result.
    """

    api_key = os.getenv("GOOGLE_CUSTOM_SEARCH_API_KEY")
    search_engine_id = os.getenv("GOOGLE_CX")

    if not api_key or not search_engine_id:
        print("Error: GOOGLE_CUSTOM_SEARCH_API_KEY or GOOGLE_CX is not set. Check your .env file.")
        return None

    url = "https://www.googleapis.com/customsearch/v1"

    params = {
        "key": api_key,
        "cx": search_engine_id,
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


def scrape_url(url: str) -> str:
    """
    Scrapes all visible text from a single URL. This function has a single responsibility.

    Args:
        url (str): The URL of the web page to scrape.

    Returns:
        str: The extracted text content, or an error message string if scraping fails.
    """
    print(f"  > Scraping URL: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        return soup.get_text(separator=' ', strip=True)
    except requests.exceptions.RequestException as e:
        error_message = f"Failed to scrape URL {url}: {e}"
        print(f"  > {error_message}")
        return error_message

def process_and_save_scraped_data(search_results: dict):
    """
    Processes the search results dictionary, scrapes each link, and saves the final data.
    """
    print("\n--- Step 2: Scraping content from each source ---")
    if not isinstance(search_results, dict) or 'items' not in search_results:
        print("Error: Invalid search result data provided. Cannot find 'items'.")
        return

    all_scraped_articles = []
    for item in search_results['items']:
        link = item.get('link')
        if not link:
            continue

        scraped_text = scrape_url(link)
        
        article_data = {
            "title": item.get('title'),
            "url": link,
            "source_snippet": item.get('snippet'),
            "scraped_content": scraped_text
        }
        all_scraped_articles.append(article_data)

    final_output = {
        "scrape_timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "search_query": search_results.get("queries", {}).get("request", [{}])[0].get("searchTerms"),
        "articles": all_scraped_articles
    }

    output_filename = "scraped_articles.json"
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(final_output, f, ensure_ascii=False, indent=4)
        print(f"\n--- Step 3: Successfully saved all scraped data to '{output_filename}' ---")
    except IOError as e:
        print(f"Error writing final results to file: {e}")


if __name__ == "__main__":

    with open("selected_market.json", 'r', encoding = 'utf-8') as f:
        selected_market = json.load(f)


    search_results_data = search_expert_sources("Pacers NBA 2025")

    if search_results_data:
        process_and_save_scraped_data(search_results_data)
    else:
        print("\nSkipping scraping process due to search failure.")

    
    