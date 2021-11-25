import sys
import subprocess
import threading
import PySimpleGUI as sg
from pathlib import Path

BASE_DIR = Path(__file__).parents[1]
if sys.platform == "win32":
    PYTHON_PATH = BASE_DIR / "venv" / "scripts" / "pythonw.exe"
else:
    PYTHON_PATH = BASE_DIR / "venv" / "scripts" / "python.exe"


def main():

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
            folder = values["-FOLDER-"]

            def call_run_app(folder):
                cmd = [str(PYTHON_PATH), "run_app.py", '-i', folder, '-o', folder]
                subprocess.run(cmd)

            open_labeling_thread = threading.Thread(
                target=call_run_app,  # Pointer to function that will launch OpenLabeling.
                name="OpenLabelingMain",
                args=[folder],
            )
            open_labeling_thread.start()

            window.close()


if __name__ == '__main__':
    main()


def test_main():
    main()
