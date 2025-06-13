import httpx
from dotenv import load_dotenv
import os
import json

load_dotenv()

INPUT_FILENAME = "filtered_by_label.json"

NEWS_API_KEY = os.get("NEWS_API_KEY")

def keyword_extractor(): 
    """Takes in a list of events and extracts keywords from the event description."""
    
    with open(INPUT_FILENAME, 'r', encoding = 'utf-8') as f:
        all_events = json.load(f)


    


