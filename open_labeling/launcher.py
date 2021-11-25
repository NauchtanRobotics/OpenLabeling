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
        # [
        #     sg.Listbox(
        #         values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        #     )
        # ],
    ]

    # For now will only show the name of the file that was chosen
    # image_viewer_column = [
    #     [sg.Text("Choose an image from list on left:")],
    #     [sg.Text(size=(40, 1), key="-TOUT-")],
    #     [sg.Image(key="-IMAGE-")],
    # ]

    # ----- Full layout -----
    layout = [
        [
            sg.Column(file_list_column),
            # sg.VSeperator(),
            # sg.Column(image_viewer_column),
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
            # try:
            #     # Get list of files in folder
            #     file_list = os.listdir(folder)
            # except:
            #     file_list = []

            # fnames = [
            #     f
            #     for f in file_list
            #     if os.path.isfile(os.path.join(folder, f))
            #     and f.lower().endswith((".png", ".PNG", ".jpg", ".JPG"))
            # ]
            # window["-FILE LIST-"].update(fnames)

        # elif event == "-FILE LIST-":  # A file was chosen from the listbox
        #     try:
        #         filename = os.path.join(
        #             values["-FOLDER-"], values["-FILE LIST-"][0]
        #         )
        #         window["-TOUT-"].update(filename)
        #         window["-IMAGE-"].update(filename=filename)
        #     except:
        #         pass

    # window.close()


if __name__ == '__main__':
    main()


def test_main():
    main()
