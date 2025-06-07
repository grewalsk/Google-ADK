#!/usr/bin/env python3
"""
Example of how to use the updated kalshiutils.py JSON export function
"""

from kalshi.kalshiutils import export_kalshi_events_to_json

# Method 1: Use default filename (kalshi_events.json)
data = export_kalshi_events_to_json()

# Method 2: Specify custom filename
data = export_kalshi_events_to_json("my_custom_events.json")

# Method 3: Use the returned data in your code
if data:
    print(f"Total events: {len(data.get('events', []))}")
    # Process the data further...
else:
    print("Failed to fetch data")
