import httpx
import json

gamma_events_endpoint = "https://gamma-api.polymarket.com/events"
event_limit = 100

# To implement 1000 events grabbing. 

print(f"Fetching the latest {event_limit} events from Polymarket...")

try:
    params = {
        "active": "true",
        "closed": "false",
        "archived": "false",
        "limit": 100,
        "offset": 0,
    }

    response = httpx.get(gamma_events_endpoint, params=params, timeout=30.0)
    response.raise_for_status()
    limited_events = response.json()
    print(f"\nSuccessfully fetched {len(limited_events)} events.")

    # --- Output to JSON ---

    final_json_output = json.dumps(limited_events, indent=2)

    output_filename = "100_events.json"

    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(final_json_output)

    print(f"The {len(limited_events)} most recent events have been saved to '{output_filename}'")


except httpx.RequestError as e:
    print(f"\nAn error occurred while communicating with the API: {e}")
except json.JSONDecodeError:
    print("\nError: Failed to decode JSON from the API response.")
except Exception as e:
    print(f"\nAn unexpected error occurred: {e}")