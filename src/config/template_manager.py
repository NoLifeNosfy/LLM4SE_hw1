import json
import os

TEMPLATE_FILE = "watermark_templates.json"

def load_templates():
    """Loads templates from the JSON file."""
    if not os.path.exists(TEMPLATE_FILE):
        return {"__metadata__": {"last_used": None}, "templates": {}}
    try:
        with open(TEMPLATE_FILE, 'r') as f:
            data = json.load(f)
            # Basic validation
            if "__metadata__" not in data or "templates" not in data:
                return {"__metadata__": {"last_used": None}, "templates": {}}
            return data
    except (json.JSONDecodeError, IOError):
        return {"__metadata__": {"last_used": None}, "templates": {}}

def save_templates(templates_data):
    """Saves the templates dictionary to the JSON file."""
    try:
        with open(TEMPLATE_FILE, 'w') as f:
            json.dump(templates_data, f, indent=4)
    except IOError as e:
        print(f"Error saving templates: {e}")
