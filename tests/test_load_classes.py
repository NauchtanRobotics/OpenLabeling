from pathlib import Path

from open_labeling.load_classes import get_class_list_from_text_file

BASE_DIR = Path(__file__).parents[1]
PYTHON_EXE = BASE_DIR / "venv" / "bin" / "python"
RUN_APP_PATH = BASE_DIR / "open_labeling" / "run_app.py"


def test_get_class_list():
    classes = get_class_list_from_text_file()
    assert classes == ['person', 'billiard ball', 'donut']


# def test_get_classes_from_args():
#     cmd = [
#         str(PYTHON_EXE),
#         str(RUN_APP_PATH),
#
#     ]