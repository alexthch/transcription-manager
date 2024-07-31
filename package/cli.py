import argparse
import pprint

from package.dependencies import install_all_dependencies, check_all_dependencies, check_if_cuda_is_available
from package.commands import build_index
from package.load_settings import load_settings, open_file_in_text_editor, print_settings

def main():

    settings = load_settings()

    if settings is None:
        print(f"Settings not loaded. Exiting...")
        return  

    # Main Parsers
    parser = argparse.ArgumentParser(description="Manage transcriptions")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    index_parser = subparsers.add_parser('index', help='Tools for managing the file index tree')
    settings_parser = subparsers.add_parser('settings', help='tools for managing the settings')
    settings_parser.add_argument('-o', action='store_true', help='Open settings in texteditor')
    settings_parser.add_argument('-p', action='store_true', help='Print settings in texteditor')
    # Dependency parser functions
    dependency_parser = subparsers.add_parser('dependency', help='Dependencies tools')
    dependency_parser.add_argument('-c', action='store_true', help='Check dependencies')
    dependency_parser.add_argument('-i', action='store_true', help='Installs missing dependencies')
    dependency_parser.add_argument('-cuda', action='store_true', help='Checks if CUDA is available')

    #Parse and switch arguments
    args = parser.parse_args()


    if args.command == 'index':
        build_index.main(settings)

    elif args.command == 'settings':

        if args.o:
            open_file_in_text_editor()
        elif args.p:
            print_settings(settings)
        else:
            settings_parser.print_help()

    elif args.command == 'dependency':

        if args.c:
            check_all_dependencies()

        elif args.i:
            install_all_dependencies()

        elif args.cuda:
            check_if_cuda_is_available()
            
        elif not args.c and not args.i:
            dependency_parser.print_help()

    else:
        parser.print_help()
    

if __name__ == "__main__":
    main()
