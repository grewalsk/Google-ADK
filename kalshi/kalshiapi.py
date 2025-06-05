import requests
import json

url = "https://api.elections.kalshi.com/trade-api/v2/events?limit=200&status=open"
#"https://api.elections.kalshi.com/trade-api/v2/events/KXMUSKCHALLENGERS-26?with_nested_markets=true"
headers = {"accept": "application/json"}
response = requests.get(url, headers=headers)

def get_last_events(json_string, n):
    """
    Parses Kalshi JSON string to return last N events. 
    Returns events that were listed earlier so that betting events have more researchable context.
    """

    if (n <= 0):
        return []
    
    try:
        data = json.loads(json_string)
    except json.JSONDecodeError:
        print("Invalid JSON string provided")
        return []
    
    events_list = data.get("events")
    
    if not events_list:
        print("No events found in the JSON data")
        return []
    
    last_n = events_list[-n:]
    
    return last_n

last_n_events = get_last_events(response.text, 5)

def market_getter(events):
    """
    Gets markets for specific events using their tickers.
    """

    if not events: 
        return []
    
    try:
        for event in events:
            event_name = event.get("event_ticker")
            market_url = f"https://api.elections.kalshi.com/trade-api/v2/markets?event_ticker={event_name}"
            response = requests.get(market_url, headers=headers)
            yield response.text
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

markets = market_getter(last_n_events)


# To print out. 

for market_data in markets:
    print("\n--- Market Data ---\n")
    market_data_json = json.loads(market_data)
    print(json.dumps(market_data_json, indent=2))






    