from external.local import user_presenter
from external.web import github
from github import BadCredentialsException
from gf.config.credential import Credential
from external.local import json_handler


def start():
    old_credentials = json_handler.get_config_json()
    if old_credentials:
        re_config(old_credentials)
    else:
        new_config()


def new_config():
    credential = Credential()
    prepare_to_start(credential)
    try:
        github.get_token(credential)
        github.find_working_repo(credential)
    except BadCredentialsException:
        user_presenter.bad_credential()
    finish(credential)


def re_config(old_credentials):
    old_credentials["credentials"]["github"]["language"] = user_presenter.get_lang_from_user()  # nopep8
    json_handler.save_credential(old_credentials)


def prepare_to_start(credential):
    credential.username, credential.password, credential.lang = user_presenter.user_pass_lang()  # nopep8
    user_presenter.start_communicating()


def finish(credential):
    json_handler.wrap_and_save_credential(credential)
    user_presenter.token_created(credential.token)
