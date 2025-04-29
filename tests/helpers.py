import pathlib

import orjson

DATA_DIR = pathlib.Path(__file__).parent / "data"


def load_fixture(filepath) -> str:
    with open(filepath, "r") as f:
        return f.read()


def load_json_fixture(filepath: str) -> dict:
    return orjson.loads(load_fixture(f"{filepath}.json"))
