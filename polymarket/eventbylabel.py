import json

INPUT_FILENAME = '100_events.json' 

# 2. Set the tag LABEL you want to filter by (e.g., "Sports", "Politics", "NBA").
TAG_LABEL_TO_FIND = 'Politics'


print(f"Attempting to load events from '{INPUT_FILENAME}'...")

try:
    with open(INPUT_FILENAME, 'r', encoding='utf-8') as f:
        all_events = json.load(f)
    print(f"Successfully loaded {len(all_events)} events.")

    print(f"Filtering for events with the label: '{TAG_LABEL_TO_FIND}'")
    filtered_events = []
    
    for event in all_events:
        if 'tags' in event and isinstance(event['tags'], list):
            for tag_object in event['tags']:
                if tag_object.get('label', '').lower() == TAG_LABEL_TO_FIND.lower():
                    filtered_events.append(event)
                    break 

    if filtered_events:
        print(f"\nSuccess! Found {len(filtered_events)} events matching the label.")
        
        safe_label_name = TAG_LABEL_TO_FIND.lower().replace(' ', '_')
        output_filename = f"filtered_by_label_{safe_label_name}.json"
        
        final_json_output = json.dumps(filtered_events, indent=2)

        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(final_json_output)

        print(f"Filtered events have been saved to '{output_filename}'")
    else:
        print(f"\nNo events were found with the label '{TAG_LABEL_TO_FIND}'.")
        print("Please check the spelling and ensure the label exists in your JSON file.")

except FileNotFoundError:
    print(f"\n[ERROR] The file '{INPUT_FILENAME}' was not found.")
    print("Please make sure the JSON file is in the same folder as this script and the filename is correct.")
except json.JSONDecodeError:
    print(f"\n[ERROR] The file '{INPUT_FILENAME}' is not a valid JSON file.")
except Exception as e:
    print(f"\nAn unexpected error occurred: {e}")