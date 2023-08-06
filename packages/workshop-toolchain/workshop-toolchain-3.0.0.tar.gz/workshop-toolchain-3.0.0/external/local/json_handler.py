from external.local import user_presenter
from external.local.file_operator import get_work_dir, does_exist
from external.local.json_io import save_json_content, get_json_content
from gf.settings import WORKSHOP_DATA_FILENAME, CONFIG_FILENAME


def wrap_and_save_credential(credential):
    save_credential(credential_container(credential))


def save_credential(credential):
    save_json_content(get_work_dir() + CONFIG_FILENAME, credential)


def credential_container(credential):
    return {"credentials": {"github":
                            {"accessToken": credential.token,
                             "handle": credential.username,
                             "repository": credential.repo,
                             "language": credential.lang}}}


def get_config_json():
    return get_json_content(get_work_dir() + CONFIG_FILENAME)


def get_working_repo():
    return get_config_json()["credentials"]["github"]["repository"]


def get_token():
    return get_config_json()["credentials"]["github"]["accessToken"]


def get_lang():
    return get_config_json()["credentials"]["github"]["language"]


def get_gh_handle():
    return get_config_json()["credentials"]["github"]["handle"]


def check_token():
    try:
        get_token()
    except FileNotFoundError:
        user_presenter.bad_credential()


def check_gfjson():
    if does_exist(WORKSHOP_DATA_FILENAME):
        user_presenter.gf_json_exists()


def check_exercise_exist(filename):
    if not does_exist(filename) or not is_workshop_exercise(filename):
        user_presenter.file_does_not_exist()


def is_workshop_exercise(filename):
    try:
        get_json_content(WORKSHOP_DATA_FILENAME)["exercises"][filename]
    except KeyError:
        return False
    return True


def check_gfjson_not_exist():
    if not does_exist(WORKSHOP_DATA_FILENAME):
        user_presenter.gf_json_does_not_exist()


def get_ws_exercises():
    check_gfjson_not_exist()
    return get_json_content(WORKSHOP_DATA_FILENAME).get("exercises", None)


def get_ws_url():
    try:
        return get_json_content(WORKSHOP_DATA_FILENAME).get("workshop-url",
                                                            None)
    except FileNotFoundError:
        return None
    except AttributeError:
        user_presenter.gf_json_does_not_exist()


def get_language():
    try:
        return get_json_content(get_work_dir() + CONFIG_FILENAME).get("lang", None)  # nopep8
    except FileNotFoundError:
        return None
