import os
import string
from gf.settings import APP_BASE_FOLDER_NAME as BASE_FOLDER


def get_extension(filename):
    return filename.split(".")[-1] if len(filename) > 0 else None


def get_home_dir():
    return os.path.expanduser("~") + "/"


def get_work_dir():
    create_work_folder()
    return get_home_dir() + BASE_FOLDER + "/"


def create_work_folder():
    if not does_exist(get_home_dir() + BASE_FOLDER):
        os.makedirs(get_home_dir() + BASE_FOLDER)


def get_current_work_dir():
    return "./"


def does_exist(filename):
    return os.path.exists(filename)


def get_path_from_filename(filename):
    for path_tuple in os.walk("."):
        if [filename] in path_tuple:
            return path_tuple[0][1::]


def save_file(path, content):
    with open(path, "w") as output:
        output.write(content)


def lang_convert(lang):
    return {
        "python": "py",
        "java": "java",
        "javascript": "js",
        "c": "c",
        "cs": "cs"
    }[lang]


def name_converter(path, lang):
    lang = lang_convert(lang)
    splitted = path.split("/")
    dir_name = path.split("/")[-2].split("-")
    if splitted[-1].split(".")[-1] != "md":
        return splitted[-1]
    elif "py" in lang or "c" in lang:
        return py_or_c_name(dir_name, lang)
    elif "java" in lang:
        return java_name(dir_name)
    elif lang == "js":
        return js_name(dir_name)


def py_or_c_name(name_parts, lang):
    return "_".join(name_parts) + "." + lang


def java_name(name_parts):
    name = ""
    for part in name_parts:
        name += string.capwords(part)
    return name + ".java"


def js_name(name_parts):
    return "-".join(name_parts) + ".js" if len(name_parts) > 0 else None
