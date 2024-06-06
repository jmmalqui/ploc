from __future__ import annotations
import argparse
import pathlib
import random
import time

from table import Table

files = 0


class ExtensionData:
    def __init__(self) -> None:
        self.count = 0
        self.loc = 0


extensions_type = dict[str, ExtensionData]


def get_path_characteristics(path: pathlib.Path):
    return path.is_file(), "".join(path.suffixes)


def iter_directory(path: pathlib.Path, extensions: dict[str, ExtensionData]):
    global files
    files += 1
    for entry in path.iterdir():
        is_file, ext = get_path_characteristics(entry)
        if ext == "":
            ext = "Unknown(.gitignore)"
        if is_file:
            line_count = 0
            with open(entry, "rb") as file:
                try:
                    line_count = len(file.readlines())
                except:
                    print("Couldn't read: ", entry)
            if ext in extensions:
                extensions[ext].count += 1
                extensions[ext].loc += line_count
            else:
                extensions[ext] = ExtensionData()
                extensions[ext].count = 1
                extensions[ext].loc = line_count
        else:
            iter_directory(entry, extensions)


def get_file_count(value: ExtensionData):
    return str(value.count) + " file(s)"


def get_lines_of_code(value: ExtensionData):
    return str(value.loc)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    target_dir = pathlib.Path(args.path)
    if not target_dir.exists():
        print("Target directory does not exist")
        raise SystemExit(1)
    extensions: extensions_type = {}
    begin = time.perf_counter()
    iter_directory(target_dir, extensions)
    duration = time.perf_counter() - begin

    table = Table(
        extensions,
        "Extension",
        ["FileCount", "LinesOfCode"],
        [
            get_file_count,
            get_lines_of_code,
        ],
    )
    table.draw()
