import json

# Define the input file and the tag name you want to find.
# You can change this to "Sports", "Crypto", etc.
input_filename = '100_events.json'
tag_name_to_find = 'Crypto'

print(f"Loading events from the file: '{input_filename}'...")

try:
    # --- Step 1: Load the local JSON file into a Python list ---
    with open(input_filename, 'r', encoding='utf-8') as f:
        all_events = json.load(f)

    print(f"Successfully loaded {len(all_events)} events.")
    print(f"Filtering for events with the '{tag_name_to_find}' tag...")

    # --- Step 2: Iterate through events and check their tags ---
    filtered_events = []
    for event in all_events:
        # The 'tags' field is a list of tag objects. We need to check each one.
        if 'tags' in event and isinstance(event['tags'], list):
            for tag_object in event['tags']:
                # Each tag object has a 'name'. We check if it matches.
                if tag_object.get('name') == tag_name_to_find:
                    filtered_events.append(event)
                    # Once we find a matching tag, we can stop checking this event and move to the next.
                    break

    # --- Step 3: Save the filtered list to a new JSON file ---
    if filtered_events:
        print(f"\nFound {len(filtered_events)} events matching the tag.")

        output_filename = f"filtered_by_tag_{tag_name_to_find.lower()}.json"

        # Convert the filtered list to a nicely formatted JSON string
        final_json_output = json.dumps(filtered_events, indent=2)

        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(final_json_output)

        print(f"Filtered events have been saved to '{output_filename}'")

        # Display the titles of the first 5 events found to confirm the filter worked
        print("\n--- Sample of Filtered Event Titles ---")
        for event in filtered_events[:5]:
            print(f"- {event.get('title', 'N/A')}")
    else:
        print(f"No events found with the tag '{tag_name_to_find}' in the provided file.")

except FileNotFoundError:
    print(f"Error: The file '{input_filename}' was not found in the same directory.")
except json.JSONDecodeError:
    print(f"Error: The file '{input_filename}' does not contain valid JSON.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")