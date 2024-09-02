import os, json

from typing import Any, Dict

SETTINGS: Dict[str, any]
INDEX_DIR: str = 'transcription-settings\\'

def get_index(settings_init: Dict[str, Any]) -> Dict[str, bool]:

    global SETTINGS
    SETTINGS = settings_init

    index_file_path = INDEX_DIR + SETTINGS['index_filename']

    try:
        with open(index_file_path, 'r') as index_json:
            return json.load(index_json)
        
    except Exception as e:
        print(f"Error loading index, error: {e}")

    return {}