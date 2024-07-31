import os, pprint, json

from typing import Any, Dict

SETTINGS: Dict[str, any]

def transcription_file_template(filename: str, transcribed: bool) -> Dict:

    template_file = {
        'filename' : filename,
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

            if transciption_filename in filenames:
                list_of_files.append(transcription_file_template(filename, True))
                print(f"Transcribed\t\t{filename}")
            else:
                list_of_files.append(transcription_file_template(filename, False))
                print(f"Not transcribed\t\t{filename}")

            

        directory_tree[relative_path] = list_of_files

    return directory_tree

def save_file_index(file_index: Dict[str, any]):

    global SETTINGS

    try:
        with open(SETTINGS['index_filename'], 'w') as index_file:
            json.dump(file_index, index_file, 4)

            print(f"Saved index file in settings folder, file name: {file_index}")

    except:
        print("Error saving index file")

def main(settings_init: Dict[str, Any]):
    
    global SETTINGS

    SETTINGS = settings_init

    print("Scanning folders...\nSTATUS\t\t\tFILENAME")
    
    result = build_directory_tree()

    save_file_index(result)

if __name__ == "__main__":
    main()
