import os, pprint, json

from typing import Any, Dict

SETTINGS: Dict[str, any]

SAVE_LOCATION: str

def transcription_file_template(filename: str, transcribed: bool) -> Dict:

    template_file = {
        'filepath' : filename,
        'transcribed': transcribed,
    }

    return template_file

def check_folder_skip(filenames: list) -> bool:

    global SETTINGS

    if SETTINGS['ignore'] in filenames:
        return True
    
    else:
        return False

def check_if_file_is_transcription(filename: str) -> bool:

    global SETTINGS

    return filename.startswith(SETTINGS['transcription_prefix'])

def check_file_extension(filename: str) -> bool:

    global SETTINGS

    extensions_to_transcribe = SETTINGS['filetypes']
    
    for extension in extensions_to_transcribe:
        if filename.lower().endswith(extension.lower()):
            return True
        
    return False

def build_directory_tree() -> Dict[str, Any]:
    
    global SETTINGS

    directory_tree = {}

    for dirpath, dirnames, filenames in os.walk(os.curdir):
        
        relative_path = os.path.relpath(dirpath, os.curdir)

        if relative_path == ".":
            relative_path = ""

        if check_folder_skip(filenames):
            print(f"! Skipping folder: {relative_path} !")
            continue

        list_of_files = []

        for filename in filenames:

            if check_if_file_is_transcription(filename):
                continue

            if not check_file_extension(filename):
                continue
            
            extensionless_filename = filename.split(".")[0]
            transciption_filename = SETTINGS['transcription_prefix'] + extensionless_filename + ".txt"
            full_relative_path = os.path.join(relative_path, filename)

            if transciption_filename in filenames:

                directory_tree[full_relative_path] = True
                print(f"Transcribed\t\t{full_relative_path}")

            else:
                
                directory_tree[full_relative_path] = False
                print(f"Not transcribed\t\t{full_relative_path}")

    return directory_tree

def save_file_index(file_index: Dict[str, any]):

    global SAVE_LOCATION

    try:
        with open(SAVE_LOCATION, 'w') as index_file_path:
            json.dump(file_index, index_file_path, indent=4)

            print(f"Saved index file in settings folder, location: {SAVE_LOCATION}")

    except Exception as e:
        print(f"Error saving index file, error: {e}")

def main(settings_init: Dict[str, Any]):
    
    global SETTINGS
    global SAVE_LOCATION

    SETTINGS = settings_init

    SAVE_LOCATION = 'transcription-settings\\' + SETTINGS['index_filename']

    print("Scanning folders...\nSTATUS\t\t\tFILENAME")
    
    result = build_directory_tree()

    save_file_index(result)

if __name__ == "__main__":
    main()
