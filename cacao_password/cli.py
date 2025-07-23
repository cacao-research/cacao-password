"""CLI entry point for cacao-password."""

import argparse
from .gui import launch_gui_app

def main():
    parser = argparse.ArgumentParser(
        description="cacao-password CLI"
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch the GUI application"
    )
    args = parser.parse_args()

    # Launch GUI if --gui is provided or no arguments are given
    if args.gui or len(vars(args)) == 0 or not any(vars(args).values()):
        launch_gui_app()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()