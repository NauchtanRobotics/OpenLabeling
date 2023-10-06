# import os
# import sys
from pathlib import Path

#
# def resource_path(relative_path):
#     """ Get the absolute path to the resource, works for dev and for PyInstaller """
#     try:
#         # PyInstaller creates a temp folder and stores path in _MEIPASS
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")
#
#     return os.path.join(base_path, relative_path)


def check_if_folder_contains_sufficient_images(input_dir: Path, threshold: int = 3):
    """
    Raises a runtime error which provides a useful tip to GUI user if
    the selected folder does not contain sufficient images.
    """
    if not input_dir.is_dir():
        raise RuntimeError("")
    image_file_paths = list(input_dir.iterdir())
    image_file_paths = [
        image_file_path for image_file_path in image_file_paths if image_file_path.suffix.lower() == ".jpg"
    ]
    if len(image_file_paths) <= threshold:
        raise RuntimeError(
            f"\nInsufficient jpg files found directly in {str(input_dir)}"
            "\nDid you remember to double-click the folder?"
        )
