import argparse
import sys
import subprocess
import threading

from pathlib import Path

if sys.platform == "win32":
    SYS_STDOUT = subprocess.PIPE  # Prefer to use sys.stdout instead of
    SYS_STDERR = subprocess.PIPE  # subprocess.PIPE, but causes Windows to fail
    result = subprocess.check_output(["where", "poetry.bat"])
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
        "--image_path",
        type=str,
        nargs="*",
        required=True,
        help="The full path to image. Annotation should be in a sub-folder 'YOLO_Darknet' of the image folder. "
             "Comma separate (without spaces) if more than one image path selected.",
    )
    args = parser.parse_args()
    return args


def main(args):
    print("\nClass List: ")
    print(args.class_list)
    print(args.image_path)
    if not POETRY_APP.exists():
        raise Exception("\nPoetry app not found: {}".format(str(POETRY_APP)))

    if not SCRIPT_PATH.exists():
        raise Exception("\nApp path not found: {}".format(str(SCRIPT_PATH)))

    # Check if any paths are non-existent
    if not isinstance(args.image_path, list):
        image_paths = [args.image_path]
    else:
        image_paths = args.image_path

    for path_str in image_paths:
        if not Path(path_str).exists():
            raise RuntimeError("Image does not exist: " + path_str)

    def call_run_app():
        cmd = [
            str(POETRY_APP),
            "run",
            "python",
            str(SCRIPT_PATH),
            "-c",
            *args.class_list,
            "--files-list",
        ]
        cmd.extend(image_paths)
        print(" ".join(cmd))
        subprocess.run(cmd, stdout=SYS_STDOUT, stderr=SYS_STDERR, check=True)

    open_labeling_thread = threading.Thread(
        target=call_run_app,  # Pointer to function that will launch OpenLabeling.
        name="OpenLabelingMain",
        #args=image_paths,
    )
    open_labeling_thread.start()


def run():  # used by entry-points??
    args = get_args()
    main(args=args)


if __name__ == "__main__":
    parsed_args = get_args()
    main(args=parsed_args)


TEST_CLASSES = ["D00", "D10", "D20", "D40", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O",
              "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD"]
TEST_IMAGE_1 = (
    Path(__file__).parent.parent / "tests" / "test_data" / "Photos" / "Photo_2018_May_31_10_06_44_296_00_stripping8.jpg"
)
TEST_IMAGE_2 = (
    Path(__file__).parent.parent / "tests" / "test_data" / "Photos" / "Photo_2018_May_31_10_06_45_707_00_stripping8.jpg"
)
MULTI_SELECTED_LIST = [str(TEST_IMAGE_1), str(TEST_IMAGE_2)]


def test_launch_one_image():
    class Args:
        class_list = TEST_CLASSES
        image_path = [str(TEST_IMAGE_1)]

    main(args=Args())


def test_launch_multi_selected_images():
    class Args:
        class_list = TEST_CLASSES
        image_path = MULTI_SELECTED_LIST

    main(args=Args())
