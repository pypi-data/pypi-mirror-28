from external.local import user_presenter
from external.local.command_runner import run_single_command
from gf.verify.command_data import CommandData
from gf.settings import C_COMPILER, JAVA_COMPILER, JS_SERVER, JS_SERVER_MODULES, JS_TESTER, PY_RUN, CS_COMPILER  # nopep8
from gf.verify.subprocess_adapter import run, is_windows_platform
import os
import sys


def get_command(language):
    try:
        return {
                "javascript": JS_TESTER,
                "python": PY_RUN + " --version",
                "java": JAVA_COMPILER + " -version",
                "c": C_COMPILER + " --version",
                "cs": CS_COMPILER + " --version"
        }[language]
    except KeyError as e:
        user_presenter.wrong_language()


def check_environment(language):
    command = CommandData(get_command(language))
    try:
        returncode = run_single_command(command).returncode
    except FileNotFoundError:
        user_presenter.env_not_found(language)
    else:
        if returncode != 0:
            user_presenter.env_not_found(language)


def is_jslint_installed():
    try:
        result = run(CommandData("jslint --version"))
        return result.returncode == 0
    except OSError:
        return False


def check_jslint():
    try:
        if not is_jslint_installed():
            run(CommandData("sudo npm install -g jslint")) if sys.platform.startswith("linux") else run(CommandData("npm install -g jslint"))  # nopep8
    except Exception as ex:
        print(type(ex))
