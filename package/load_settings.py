import platform, subprocess, os, json, pprint

DEFAULT_SETTINGS = {
    'filetypes' : ['MOV', 'WAV', 'MP4', 'MTS'],
    'ignore' : 'ignoretranscriptions.txt',
    'transcription_prefix' : 'transcription_',
    'last_transcribed_file' : '',
    'index_filename': 'transcription_index.json',
    'whisper-model' : 'medium',
    "custom-prompt": "Our company name is Asimut. Our product is a scheduling software for arts schools."
}

def print_settings(settings: dict[str, any]) -> None:
    pprint.pprint(settings)

def open_file_in_text_editor() -> None:

    file_path = os.getcwd() + '/transcription-settings/settings.json'

    if platform.system() == 'Windows':
        os.system(f'notepad {file_path}')
    elif platform.system() == 'Darwin':  # macOS
        subprocess.call(('open', file_path))
    elif platform.system() == 'Linux':
        subprocess.call(('xdg-open', file_path))
    else:
        raise NotImplementedError(f"Unsupported OS: {platform.system()}")

def check_settings() -> str:

    current_dir = os.getcwd()
    settings_dir = os.path.join(current_dir, 'transcription-settings')
    settings_path = os.path.join(settings_dir, 'settings.json')

    if not os.path.exists(settings_dir):

        user_input = input(f"The directory {settings_dir} doesn't exist. Do you want to create it? (Y/n)")


        if user_input.lower() == 'y':

            os.makedirs(settings_dir)
            print(f"Created settings directory {settings_dir}...")

        else:

            print(f"Aborted")
            return None

    if not os.path.exists(settings_path):

        user_input = input(f"{settings_path} Not found, do you want to create a default settings file? (Y/n)")
            
        if user_input.lower() == 'y':

            with open(settings_path, 'w') as settings_file:
                json.dump(DEFAULT_SETTINGS, settings_file, indent=4)

            print(f"Created default settings file: {settings_path}")

        else:

            print(f"Aborted")
            return None

    return settings_path


def load_settings() -> dict:

    settings_path = check_settings()

    if settings_path is None:
        
        return None
    
    with open(settings_path, 'r') as settings_json:
        settings = json.load(settings_json)

    return settings