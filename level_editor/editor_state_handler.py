import json

EDITOR_STATE_FILE = "level_editor/editor_state.json"


def get_json_data():
    with open(EDITOR_STATE_FILE) as f:
        return json.load(f)


def save_json_data(dic: dict):
    with open(EDITOR_STATE_FILE, "w") as f:
        json.dump(dic, f, indent=4)
