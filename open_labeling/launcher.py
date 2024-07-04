import argparse
import sys
import subprocess
import threading
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


def get_args():
    parser = argparse.ArgumentParser(description="Open-source image labeling tool")
    parser.add_argument(
        "-c",
        "--class-list",
        required=True,
        nargs="*",
        help="Pass in the class list instead of reading from txt file.",
    )
    parser.add_argument(
        "-f",
        "--root-folder",
        required=True,
        help="The full path to root directory for images. Annotation should be in a sub-folder 'YOLO_Darknet'",
    )
    args = parser.parse_args()
    return args


def label_folder():  # Can be used for entry points - well if arguments are passed.
    args = get_args()
    main(args)


def main(args):
    if not POETRY_APP.exists():
        raise Exception("\nPoetry app not found: {}".format(str(POETRY_APP)))

    if not SCRIPT_PATH.exists():
        raise Exception("\nApp path not found: {}".format(str(SCRIPT_PATH)))

    print("\nClass List: ")
    print(args.class_list)

    check_if_folder_contains_sufficient_images(input_dir=args.root_folder)

    def call_run_app(folder):
        cmd = [
            str(POETRY_APP),
            "run",
            "python",
            str(SCRIPT_PATH),
            "-i",
            str(folder),
            "-c",
            *args.class_list,
        ]
        subprocess.run(cmd, stdout=SYS_STDOUT, stderr=SYS_STDERR, check=True)

    open_labeling_thread = threading.Thread(
        target=call_run_app,  # Pointer to function that will launch OpenLabeling.
        name="OpenLabelingMain",
        args=[args.root_folder],
    )
    open_labeling_thread.start()


if __name__ == "__main__":
    parsed_args = get_args()
    main(args=parsed_args)


TEST_CLASSES = ["D00", "D10", "D20", "D40", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O",
              "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD"]
TEST_ROOT_DIR = Path(__file__).parent.parent / "tests" / "test_data" / "Photos"


def test_launch():
    class Args:
        class_list = TEST_CLASSES
        root_folder = TEST_ROOT_DIR

    main(args=Args())
