from typing import List, Dict


def is_import_user_file(py_files: List[Dict], import_name: str) -> bool:
    true_filename = import_name + ".py"
    for file_info in py_files:
        if file_info["basename"] == true_filename or import_name.startswith("."):
            return True
    return False


def get_base_import_name(import_name: str) -> str:
    return import_name.split(".")[0]


def import_printer(import_info: dict):
    dot_count = 70 - len(import_info["base_import_name"])
    print(import_info["base_import_name"] + "." * dot_count + import_info["filename"] + f" ({import_info['filepath']})")
