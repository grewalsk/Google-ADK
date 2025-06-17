import json 
import httpx

# Use events grabber in all cases. 


# The base URL for the Polymarket Gamma API
gamma_markets_endpoint = "https://gamma-api.polymarket.com/markets"

all_markets = []
limit = 100
offset = 0

params = {
    "active": "true",
    "closed": "false",
    "archived": "false",
    "limit": limit,
    "offset": offset,
}

print("Fetching all active markets...")

response = httpx.get(gamma_markets_endpoint, params=params)
response.raise_for_status()
data = response.json()

outfile = {}
filename = "polymarket_markets.json"

with open(filename, 'w') as outfile:
    json.dump(data, outfile, indent=2, sort_keys=False)




# If we want to fetch all markets. 
# while True:
#     response = httpx.get(gamma_markets_endpoint, params=params)

#     if response.status_code == 200:
#         market_batch = response.json()
#         all_markets.extend(market_batch)

#         # If the number of markets returned is less than the limit, we are on the last page
#         if len(market_batch) < limit:
#             break
        
#         # Increase the offset for the next page
#         offset += limit
#     else:
#         print(f"Error: Received status code {response.status_code}")
#         break

# print(f"Successfully fetched {len(all_markets)} active markets.")


