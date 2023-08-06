import getpass
import sys
import json
from random import choice
from gf.version_control import toolchain_version
from external.local.spinner import Spinner
from external.local.random_ok import okays
from sys import stdout
from gf.settings import DEBUG_FILE_NAME, SUPPORTED_LANGUAGES, USAGE_INFO, FEATURES, ESTIMATED_LENGTH  # nopep8
from external.local.table_display import draw_table


def user_pass_lang():
    username = input("Github Username: ")
    password = getpass.getpass(prompt="Github Password: ")
    lang = get_lang_from_user()
    return (username, password, lang)


def get_lang_from_user():
    lang = None
    while lang not in SUPPORTED_LANGUAGES:
        lang = input("Select your language {} : ".format(str(SUPPORTED_LANGUAGES)))  # nopep8
    return lang


def confirm_repo_name(repo_name):
    if repo_name is not None:
        repo_name = confirm_repo_happy_case(repo_name)
    if repo_name is None:
        repo_name = get_repo_name_manual()
    return repo_name


def confirm_repo_happy_case(repo_name):
    message("Found working repo, " + repo_name)
    confirm = input("Is it your working repo? (y/n): ")
    return {
        "y": repo_name,
        "n": None
    }[confirm]


def issue_generation_finished():
    message("Issue generation finished!")


def get_repo_name_manual():
    return input("Please type your working repository's name: ")


def rate_exercise():
    exercise_rate = input("Rate exercise between 1-5: ")
    return exercise_rate


def need_to_update():
    error_message(
        "Update is avaible, please run gf update !")


def message(message):
    Spinner.stop()
    print(message)


def get_version_number():
    message(toolchain_version())


def random_ok_message():
    random_ok = choice(okays)
    message(random_ok)


def error_message(error_message):
    message(error_message)
    sys.exit(2)


def download_succes(filename):
    message("Downloaded exercise: " + filename)
    start_communicating()


def no_internet_connection():
    error_message("No internet connection!")


def exercise_collect_finished():
    message("Exercise collecting finished!")


def io_error():
    error_message("No such file or directory")


def value_error():
    error_message("Invalid JSON format.")


def wrong_repo():
    error_message(
        "You are not contributor on the configured repository, please run gf config again!")  # nopep8


def keyboard_interrupted():
    error_message("\nTask interrupted!")


def start_communicating():
    Spinner.start()


def invalid_parameter():
    error_message("Missing or not supported command, try gf help!")


def token_created(token):
    message("Token created: " + token)


def bad_credential():
    error_message("Authentication failed, check your credentials!")


def file_does_not_exist():
    error_message("Invalid filename!")


def help_message():
    message(USAGE_INFO)
    draw_table(FEATURES)


def gf_json_exists():
    error_message("Workshop is already started.")


def gf_json_does_not_exist():
    error_message("No workshop config file was found, please run "
                  "\"gf start\".")


def env_not_found(language):
    message = language + " environment not found."
    error_message(message)


def download_test_env():
    message("Downloaded necessary file.")


def wrong_language():
    error_message("Not correct language name, please retry!")


def ws_not_found():
    error_message("Workshop not found, please check the workshop url!")


def fatal_error():
    error_message("Fatal error occured, "
                  "please check the log file and consult with your mentor!")


def rating_out_bound():
    error_message("Rating should be between 1-5!")


def rating_finish():
    message("Thank you for your feedback! It is valuable for us!")


def show_lint_result(result):
    message("Lint success" if result < ESTIMATED_LENGTH else "Lint failed")


def config_file_does_not_exist():
    error_message("No congif file found, please run -gf config- first!")
