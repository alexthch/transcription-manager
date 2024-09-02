import subprocess
import sys
from pkg_resources import working_set, Requirement, DistributionNotFound

required_packages = {
    'pytorch' : {
        'install_command': 'conda install pytorch'
    },
    'ffmpeg' : {
        'install_command': 'conda install -c conda-forge ffmpeg'
    },
    'whisper' : {
        'install_command': 'pip install -U openai-whisper'
    }
}


def check_dependency(package) -> bool:

    try:
        result = subprocess.run(['conda', 'list', package], capture_output=True, text=True, check=True)

        if package in result.stdout:
            print(f"{package} - was found")
            return True
        
        else:
            print(f"{package} - missing")
            return False
        
    except subprocess.CalledProcessError as e:
        print(f"Error checking {package}: {e}")
        return False

def install_dependency(command) -> None:

    try:
        subprocess.check_call(command.split())

    except subprocess.CalledProcessError:
        print(f"Failed to install")
        
def check_all_dependencies() -> None:
    
    print('Checking dependencies...')

    some_was_missing = False

    for package, info in required_packages.items():
        if not check_dependency(package):
            some_was_missing = True
            
    if some_was_missing:
        print('Dependency missing, use "dependency -i" to install them')

def install_all_dependencies() -> None:
    
    for package, info in required_packages.items():
        if not check_dependency(package):
            install_dependency(info['install_command'])

def check_if_cuda_is_available() -> bool:

    try:
        result = subprocess.run(['conda', 'list', 'pytorch'], capture_output=True, text=True, check=True)
        
        if 'torch' in result.stdout or 'pytorch' in result.stdout:

            import torch
            if torch.cuda.is_available():
                print('CUDA is available')
                return True
            else:
                print('CUDA is not available.')
                return False
        else:
            print('PyTorch is not installed in the conda environment.')
            
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_all_dependencies()