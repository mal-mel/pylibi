from stdlib_list import stdlib_list
from typing import List, Dict
import subprocess
import ntpath
import sys
import re
import os

from src import helpers, config

_STD_LIBS = stdlib_list(config.PYTHON_VERSION)
_IMPORT_REGEX = re.compile(r"^(?:from (\S*) import \S*|import (\S*))")


def _pip_installer(package: str) -> int:
    """
    Install python package with pip

    :param package:
    :return:
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package], stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              timeout=config.INSTALL_TIMEOUT)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, KeyboardInterrupt):
        return 1
    else:
        return 0


def _is_std_lib(import_name: str) -> bool:
    """
    Check is package from standard python lib

    :param import_name:
    :return:
    """
    return import_name in _STD_LIBS


def _is_lib_already_installed(package: str) -> bool:
    """
    Check is package already installed

    :param package:
    :return:
    """
    return package in sys.modules.keys()


def _get_python_files(dir_path: str) -> List[Dict]:
    """
    Get all python files from directory

    :param dir_path:
    :return:
    """
    py_files = []
    if os.path.exists(dir_path):
        for directory in os.walk(dir_path):
            for file in directory[-1]:
                if file.endswith(".py"):
                    result_dir = os.path.join(directory[0], file)
                    py_files.append({
                        "basename": ntpath.basename(result_dir),
                        "filepath": result_dir
                    })
    return py_files


def _get_py_files_imports(py_files: List[Dict], wo_flag: bool) -> List[Dict]:
    """
    Get imports from python files

    :param py_files:
    :param wo_flag:
    :return:
    """
    imports = []
    temp_imports_set = set()
    for file_info in py_files:
        with open(file_info["filepath"], "r", errors="ignore") as file_descriptor:
            for line in file_descriptor.readlines():
                if regex_data := _IMPORT_REGEX.search(line):
                    import_name = regex_data.group(1)
                    if import_name and not helpers.is_import_user_file(py_files, import_name):
                        base_import_name = helpers.get_base_import_name(import_name)
                        if wo_flag and _is_std_lib(base_import_name):
                            continue
                        if base_import_name not in temp_imports_set:
                            import_info = {
                                "base_import_name": base_import_name,
                                "full_import_name": import_name,
                                "filename": file_info["basename"],
                                "filepath": file_info["filepath"]
                            }
                            imports.append(import_info)
                            helpers.import_printer(import_info)
                            temp_imports_set.add(base_import_name)
    return imports


def get_imports(dir_path: str, wo_flag: bool) -> List[Dict]:
    """
    Parsing directory and return python file imports

    :param dir_path:
    :param wo_flag:
    :return:
    """
    py_files = _get_python_files(dir_path)
    imports = _get_py_files_imports(py_files, wo_flag)
    return imports


def install_libs(imports: List[Dict]):
    """
    Install python packages

    :param imports:
    :return:
    """
    print(f"\nStart install {len(imports)} packages")
    installed_counter = 0
    for import_info in imports:
        if not _is_lib_already_installed(import_info["base_import_name"]):
            return_code = _pip_installer(import_info["base_import_name"])
            if return_code == 0:
                print(f"{import_info['base_import_name']} successfully installed")
                installed_counter += 1
            else:
                print(f"Can't install {import_info['base_import_name']}")
        else:
            print(f"Package {import_info['base_import_name']} already installed")
    print(f"Successfully installed {installed_counter} packages")
