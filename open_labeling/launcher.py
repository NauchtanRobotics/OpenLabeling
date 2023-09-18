import argparse
import json
import sys
import subprocess
import threading
import PySimpleGUI as sg
from pathlib import Path

from open_labeling.common import check_if_folder_contains_sufficient_images

if sys.platform == "win32":
    SYS_STDOUT = subprocess.PIPE  # Prefer to use sys.stdout instead of
    SYS_STDERR = subprocess.PIPE  # subprocess.PIPE, but causes Windows to fail
    try:
        result = subprocess.check_output(["where", "poetry.bat"])
    except:
        result = subprocess.check_output(["where", "poetry"])
else:
    SYS_STDOUT = sys.stdout
    SYS_STDERR = sys.stderr
    result = subprocess.check_output(["which", "poetry"])

POETRY_APP = result.splitlines()[0]
POETRY_APP = Path(POETRY_APP.decode("utf-8"))
SCRIPT_PATH = Path(__file__).parent / "run_app.py"

CLASS_LIST = ["D00", "D10", "D20", "D40", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O",
              "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD"]


def get_args():
    parser = argparse.ArgumentParser(description="Open-source image labeling tool")
    parser.add_argument(
        "-c",
        "--class-list",
        default=None,
        nargs="*",
        help="Pass in the class list instead of reading from txt file.",
    )
    args = parser.parse_args()
    return args


def label_folder():
    args = get_args()
    main(args)


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
            sg.Text(text="Class definitions JSON file", size=(25, 1)),
            sg.In(size=(40, 1), enable_events=True, key="-JSON-"),
            sg.FileBrowse(),
        ],
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

        if event == "-JSON-":
            classes_json_fp = Path(values["-JSON-"])
            with open(str(classes_json_fp), "r") as file_obj:
                classes_dict = json.load(file_obj)
                #class_ids = list(classes_dict.keys())
                class_list = [class_info["label"] for class_id, class_info in classes_dict.items()]
            print("Loaded classes: [" + ", ".join(class_list) + "]")

        # Folder name was filled in, make a list of files in the folder
        if event == "-FOLDER-":
            folder = Path(values["-FOLDER-"])
            check_if_folder_contains_sufficient_images(input_dir=folder)

            def call_run_app(folder):
                cmd = [
                    str(POETRY_APP),
                    "run",
                    "python",
                    str(SCRIPT_PATH),
                    "-i",
                    str(folder),
                    "-c",
                    *class_list,
                ]
                subprocess.run(cmd, stdout=SYS_STDOUT, stderr=SYS_STDERR, check=True)

            open_labeling_thread = threading.Thread(
                target=call_run_app,  # Pointer to function that will launch OpenLabeling.
                name="OpenLabelingMain",
                args=[folder],
            )
            open_labeling_thread.start()

            window.close()


if __name__ == "__main__":
    parsed_args = get_args()
    main(args=parsed_args)


def test_launch():
    class Args:
        class_list = None

    main(args=Args())
