import argparse
import sys
import subprocess
import threading
import PySimpleGUI as sg
from pathlib import Path


if sys.platform == "win32":
    result = subprocess.check_output(["where", "poetry.bat"])
    POETRY_APP = result.split(b"\r\n")[0]
else:
    result = subprocess.check_output(["which", "poetry"])
    POETRY_APP = result.split(b"\r\n")[0]

POETRY_APP = Path(POETRY_APP.decode('utf-8'))
SCRIPT_PATH = Path(__file__).parent / "run_app.py"

CLASS_LIST = ['D00', 'D10', 'D20', 'D40', 'EB', 'P', 'R', 'FC', 'L0', 'LG', 'AP', 'CD', 'WS', 'RK', 'SD', 'S', "BC", "Asphalt", "Bitumen", "Concrete", "Unsealed", "Kb", "Sh", "Pt", "UG", "UP", "US"]


def get_args():
    parser = argparse.ArgumentParser(description='Open-source image labeling tool')
    parser.add_argument(
            "-c",
            "--class-list",
            default=None,
            nargs="*",
            help="Pass in the class list instead of reading from txt file.",
        )
    args = parser.parse_args()
    return args


def main(args):
    if args.class_list:
        class_list = args.class_list
        print("\nUsing class List provided: ")
    else:
        class_list = CLASS_LIST
        print("\nAssuming class List: ")
    print(class_list)

    if not POETRY_APP.exists():
        raise Exception("\nPoetry app not found: {}".format(str(POETRY_APP)))
    if not SCRIPT_PATH.exists():
        raise Exception("\nApp path not found: {}".format(str(SCRIPT_PATH)))

    file_list_column = [
        [
            sg.Text("Image Folder"),
            sg.In(size=(40, 1), enable_events=True, key="-FOLDER-"),
            sg.FolderBrowse(),
        ],
    ]

    # ----- Full layout -----
    layout = [
        [
            sg.Column(file_list_column),
        ]
    ]

    window = sg.Window(title="OpenLabeling Launcher", layout=layout, margins=(80, 15))
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        # Folder name was filled in, make a list of files in the folder
        if event == "-FOLDER-":
            folder = Path(values["-FOLDER-"])

            def call_run_app(folder):
                cmd = [str(POETRY_APP), "run", "python", str(SCRIPT_PATH), '-i', str(folder), '-c', *class_list]
                subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr, shell=True)  # cwd=str(THIS_DIR))

            open_labeling_thread = threading.Thread(
                target=call_run_app,  # Pointer to function that will launch OpenLabeling.
                name="OpenLabelingMain",
                args=[folder],
            )
            open_labeling_thread.start()

            window.close()


if __name__ == '__main__':
    parsed_args = get_args()
    main(args=parsed_args)


def test_launch():
    class Args:
        class_list = None

    main(args=Args())
