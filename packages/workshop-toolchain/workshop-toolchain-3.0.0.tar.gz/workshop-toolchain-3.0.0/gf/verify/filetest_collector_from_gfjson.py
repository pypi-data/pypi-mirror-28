from external.local.json_handler import get_json_content, WORKSHOP_DATA_FILENAME  # nopep8
from external.local.file_operator import get_current_work_dir
from external.web.github import get_file_content, get_repo
from external.web.url_handler import get_filename_from_url
from gf.settings import WORKSHOP_DATA_FILENAME


def collect_test(filename):
    ws_json = get_current_work_dir() + WORKSHOP_DATA_FILENAME
    repo = get_repo(get_json_content(ws_json)["repo"])
    test_path = get_test_path(ws_json, filename)
    content = get_file_content(repo, test_path)
    return get_filename_from_url(test_path), content


def get_test_path(ws_json, filename):
    return get_json_content(ws_json)["exercises"][filename]["test_path"]


def get_test_file_name(filename):
    return get_filename_from_url(get_test_path("./" + WORKSHOP_DATA_FILENAME,
                                               filename))
