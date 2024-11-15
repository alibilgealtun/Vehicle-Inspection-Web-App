import json


def load_expertise_map(file_path='data/expertise_map.json'):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            expertise_map = json.load(file)
        return expertise_map
    except FileNotFoundError:
        print(f"JSON file not found: {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
        return {}

def get_default_features_for_expertise_type(expertise_name, expertise_map=None):
    if expertise_map is None:
        expertise_map = load_expertise_map()

    # Retrieve the features for the given expertise name
    return expertise_map.get(expertise_name, [])
