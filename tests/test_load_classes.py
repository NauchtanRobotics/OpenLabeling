import subprocess
from pathlib import Path

from open_labeling.load_classes import get_class_list_from_text_file

BASE_DIR = Path(__file__).parents[1]
PYTHON_EXE = BASE_DIR / ".venv" / "bin" / "python"

if not PYTHON_EXE.exists():
    PYTHON_EXE = BASE_DIR / "venv" / "bin" / "python"
assert PYTHON_EXE.exists(), f"/.venv not found. Run command `poetry config virtualenvs.in-project true`"

RUN_APP_PATH = BASE_DIR / "open_labeling" / "run_app.py"
TEST_DATA_PHOTOS = Path(__file__).parent / "test_data" / "Photos"


def test_get_class_list():
    classes = get_class_list_from_text_file()
    assert classes == ["person", "billiard ball", "donut"]


CLASSES = ["cAT", "dOG"]


def test_get_classes_from_args():
    cmd = [str(PYTHON_EXE), str(RUN_APP_PATH), f"-i={str(TEST_DATA_PHOTOS)}", "-c"]
    cmd.extend(CLASSES)
    subprocess.run(cmd, cwd=str(BASE_DIR))
