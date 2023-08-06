from gf.settings import WORKSHOP_URL_BEGIN, WORKSHOP_URL_JAVA, WORKSHOP_URL_PYTHON, WORKSHOP_URL_CS, WORKSHOP_URL_JS  # nopep8
from external.local.json_handler import get_lang


def get_ws_from_url(url):
    splitted = url.split("/master/")[1].split("/")
    del splitted[-1]
    return "/".join(splitted)


def make_full_workshop_url(task):
    return WORKSHOP_URL_BEGIN + task + language_dictionary(get_lang())


def language_dictionary(language):
    return {
        "java": WORKSHOP_URL_JAVA,
        "python": WORKSHOP_URL_PYTHON,
        "cs": WORKSHOP_URL_CS,
        "javascript": WORKSHOP_URL_JS,
        "js": WORKSHOP_URL_JS
    }[language]


def get_lang_from_url(url):
    return url.split("/")[-1].split(".")[0]


def get_filename_from_url(url):
    return url.split("/")[-1]


def get_repo_from_url(url):
    return url.split("github.com/greenfox-academy/")[1].split("/")[0]


def transform_to_test_path(url):
    splitted = url.split("/")
    splitted.pop(-1)
    splitted.append("tests")
    return "/".join(splitted)
