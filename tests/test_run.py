from pathlib import Path
from cv2 import cv2

from open_labeling.run_app import get_args, main

TEST_IMAGES_DIR = Path(__file__).parent / "test_data" / "Photos"


def test_run_input_dir():
    class Args:
        input_dir = f"{str(TEST_IMAGES_DIR)}"
        output_dir = f"{str(TEST_IMAGES_DIR)}"
        thickness = 1
        tracker = "KCF"
        n_frames = 200
        files_list = None
        draw_from_PASCAL_files = False

    args = Args()
    main(args=args)


def test_run_files_list():
    FILES_LIST = [
        str(TEST_IMAGES_DIR / "Photo_2018_May_31_10_06_44_296_00_stripping8.jpg"),
        str(TEST_IMAGES_DIR / "Photo_2018_May_31_10_06_45_707_00_stripping8.jpg"),
        str(TEST_IMAGES_DIR / "Photo_2018_May_31_10_06_46_406_00_stripping8.jpg"),
    ]

    class Args:
        # input_dir = f"{str(BASE_DIR)}"
        # output_dir = f"{str(BASE_DIR)}"
        thickness = 1
        tracker = "KCF"
        n_frames = 200
        files_list = *FILES_LIST,
        draw_from_PASCAL_files = False

    args = Args()
    main(args=args)
