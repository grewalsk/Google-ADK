import requests
import json 

gamma_base_url = "https://gamma-api.polymarket.com"

response = requests.get(f'{gamma_base_url}/markets')
response.raise_for_status()

outfile = {}

filename = "polymarket_markets.json"
data = response.json()

with open(filename, 'w') as outfile:
    json.dump(data, outfile, indent=2, sort_keys=False)
