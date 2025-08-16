from pathlib import Path

MY_DIR = Path(__file__).parent
JS_DIR = MY_DIR / "js"


def load_js(file_name: str) -> str:
    return (JS_DIR / file_name).read_text()
