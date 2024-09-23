import os, whisper, warnings

from typing import Any, Dict
from package.main.load_index import get_index
from package.commands import build_index
from package.dependencies import check_if_cuda_is_available

SETTINGS: Dict[str,Any]
FILE_INDEX = Dict[str,bool]
CUDA_ENABLED: bool = False
MODEL: str = "tiny"

def run_transcriptions(setting_init: Dict[str, Any], enable_cuda: bool = False) -> None:

    global SETTINGS, FILE_INDEX, MODEL, CUDA_ENABLED
    SETTINGS = setting_init
    FILE_INDEX = get_index(SETTINGS)
    MODEL = SETTINGS.get('whisper-model', 'tiny')

    ### SUPPRESS FP16 WARNING ###
    warnings.filterwarnings("ignore", category=UserWarning, message=".*FP16 is not supported on CPU; using FP32 instead.*")

    print_start_msg()
    
    if enable_cuda and check_if_cuda_is_available():
        CUDA_ENABLED = enable_cuda

    print_session_settings() 

    file_queue = initialize_queue()
    start_file_loop(file_queue)

    print_end_message()

    build_index.main(SETTINGS)
    
    return None

def initialize_queue() -> list:

    global FILE_INDEX

    queue: list = []
    amount_transcribed: int = 0

    for file, transcribed in FILE_INDEX.items():

        if transcribed == False:

            queue.append(file)

        else:

            amount_transcribed += 1
    
    print_progress((amount_transcribed, len(FILE_INDEX)))

    return queue
    
def print_start_msg()->None:

    start_message = '| USE CTRL-C TO ABORT - USE COMMAND "transcribe settings -o" TO EDIT SETTINGS |'
    border = '+' + ('-' * (len(start_message)-2)) + '+'

    print(border)
    print(start_message)
    print(border)

    return None

def print_end_message() -> None:

    message = "| Finished transcribing, udpating index |"
    border = '+' + ('-' * (len(message)-2)) + '+'

    print(border)
    print(message)
    print(border)

    return None

def print_session_settings()->None:
    print('Starting transciption...')
    print(f"Model size:\t\t{MODEL}")
    print(f"CUDA enabled:\t\t{CUDA_ENABLED}")

    return None

def print_progress(progress: tuple) -> None:
    print(f"Total progress: \t{progress[0]} / {progress[1]} ({ (progress[0]/progress[1]) * 100.}%)")

    return None

def start_file_loop(queue: list) -> None:

    global MODEL, SETTINGS
    custom_prompt = SETTINGS.get('custom-prompt', "")
    device = "cuda" if CUDA_ENABLED else "cpu"

    print('Loading transcription-model...')
    transcribe_model = whisper.load_model(MODEL, device=device)
    print('Model finished loading')
    print("\n"+"#"*80+"\n")
    try:
        for filepath in queue:
            try:
                print(f"Transcribing file: {filepath}")
                result = transcribe_model.transcribe(
                    audio=filepath,
                    initial_prompt=custom_prompt
                    )
                
                transcription_filename: str = SETTINGS['transcription_prefix'] + os.path.splitext(os.path.basename(filepath))[0] + ".txt"
                transcription_filepath: str = os.path.join(os.path.dirname(filepath), transcription_filename)
                save_success: bool = save_transcription(result, transcription_filepath)

                if result and save_success:
                    print(f"Successfully transcribed {filepath}")

            except:
                print(f"###! Failed transcribing {filepath} !###")
    except KeyboardInterrupt:
        print('\nStopped by user')
        return None
    return None


def save_transcription(transcription: Dict[str, str | list], path: str) -> bool:

    try:
        with open(path, 'w') as file:
            file.write("Start time\tEnd time\tText\n")
            
            for segment in transcription['segments']:
                start_time = segment['start']
                end_time = segment['end']
                text = segment['text']

                formatted_start = f"{int(start_time // 3600):02}:{int((start_time % 3600) // 60):02}:{int(start_time % 60):02}"
                formatted_end = f"{int(end_time // 3600):02}:{int((end_time % 3600) // 60):02}:{int(end_time % 60):02}"

                file.write(f"{formatted_start}\t{formatted_end}\t{text}\n")

            return True
            
    except:

        print(f"error saving {path}")
        return False
    
