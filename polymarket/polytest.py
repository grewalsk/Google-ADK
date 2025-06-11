import httpx

gamma_markets_endpoint = "https://gamma-api.polymarket.com/markets"
market_id = "507868"  # Example market ID

# Construct the URL for the specific market
url = f"{gamma_markets_endpoint}/{market_id}"

print(f"Fetching data for market ID: {market_id}...")
response = httpx.get(url)

if response.status_code == 200:
    market_data = response.json()
    print("\n--- Market Details ---")
    print("Question:", market_data['question'])
    print("Outcomes:", market_data['outcomes'])
    print("Volume:", market_data['volume'])
    print("----------------------")
else:
    print(f"Error: Received status code {response.status_code}")