from pathlib import Path
from typing import Literal

MY_DIR = Path(__file__).parent
JS_DIR = MY_DIR / "jsa"


def load_js(file_name: str) -> str:
    return (JS_DIR / file_name).read_text()
