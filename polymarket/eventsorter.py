import json
import inquirer

INPUT_FILENAME = 'events.json' 

def get_user_choice() -> str:
    """Gets label to sort for by user choice"""

    category_choices = [
        "Politcs",
        "Sports",
        "Crypto",
        "Tech",
        "Culture",
        "World",
        "Economy",
        "Trump",
        "Elections",
    ]

    questions = [
        inquirer.List(
            'selection',
            message = "What category of events would you like to filter for?",
            choices = category_choices,
            carousel = True,
        )
    ]

    answers = inquirer.prompt(questions)

    if answers:
        print(f"\nYou selected {answers['selection']}.")
        chosen_options = answers['selection']
        return chosen_options
    else:
        print("\nNo seleciton was made.")
        return None
    
if __name__ == "__main__":
    TAG_LABEL_TO_FIND = get_user_choice()


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
        
        output_filename = "filtered_by_label.json"
        
        final_json_output = json.dumps(filtered_events, indent=2)

        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(final_json_output)

        print(f"Filtered events have been saved to '{output_filename}'")
    else:
        print(f"\nNo events were found with the label '{TAG_LABEL_TO_FIND}'.")
        

except FileNotFoundError:
    print(f"\n[ERROR] The file '{INPUT_FILENAME}' was not found.")
    print("Please make sure the JSON file is in the same folder as this script and the filename is correct.")
except json.JSONDecodeError:
    print(f"\n[ERROR] The file '{INPUT_FILENAME}' is not a valid JSON file.")
except Exception as e:
    print(f"\nAn unexpected error occurred: {e}")


def select_event(filename = "filtered_by_label.json"):
    """Takes in a list of events and allows the user to select which even to specifically examine."""

    with open(filename, 'r', encoding = "utf-8") as f:
        filtered_events = json.load(f)

    questions =[
        inquirer.List(
            'selection',
            message = "What event from the filtered category would you like to explore?",
            choices = [event['title'] for event in filtered_events],
            carousel = True,
        )
    ]

    answers = inquirer.prompt(questions)

    if answers:
        print(f"\nYou selected {answers['selection']}.")

        for event in all_events:
            if event['title'] == answers['selection']:
                selected_event = event
                break

        filename = "selected_event.json"
        with open(filename, 'w', encoding = 'utf-8') as f:
            json.dump(selected_event, f, indent=2)
        return None
    else:
        print("\nNo seleciton was made.")
        return None

select_event()

def select_market(filename = "selected_event.json"):
    """Takes in a list of events and allows the user to select which even to specifically examine."""

    with open(filename, 'r', encoding = "utf-8") as f:
        selected_event = json.load(f)

    questions =[
        inquirer.List(
            'selection',
            message = "What market from the selected event would you like to explore?",
            choices = [market['question'] for market in selected_event['markets']],
            carousel = True,
        )
    ]

    answers = inquirer.prompt(questions)

    if answers:
        print(f"\nYou selected {answers['selection']}.")

        for market in selected_event['markets']:
            if market['question'] == answers['selection']:
                selected_market = market
                break

        filename = "selected_market.json"
        with open(filename, 'w', encoding = 'utf-8') as f:
            json.dump(selected_market, f, indent=2)
        return None
    else:
        print("\nNo seleciton was made.")
        return None

select_market()
