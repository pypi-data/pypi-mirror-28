from external.local.file_operator import get_extension, does_exist
from external.local.file_operator import get_work_dir
from external.local.user_presenter import show_lint_result, file_does_not_exist
from external.local.user_presenter import message
from gf.settings import GOOGLE_CHECKS_FILENAME, CHECKSTYLE_FILENAME
from external.local.environment_checks import check_jslint
from subprocess import PIPE, Popen
import sys


def start(filename):
    try:
        if does_exist(sys.argv[2]) is True:
            lint_check(get_extension(filename))()
        else:
            file_does_not_exist()
    except KeyError:
        raise


def lint_check(case):
    return {
        "py": python_lint,
        "js": js_lint,
        "java": java_lint
    }[case]


def communicate_thread(command):
    process = Popen(command, shell=True,
                    stdout=PIPE,
                    stderr=PIPE)
    out, err = process.communicate()
    result = out.decode("utf-8")
    message(result)
    show_lint_result(len(result))


def python_lint():
    cmd = "pycodestyle " + sys.argv[2]
    communicate_thread(cmd)


def js_lint():
    check_jslint()
    cmd = "jslint --edition=latest " + sys.argv[2]
    communicate_thread(cmd)


def java_lint():
    cmd = r'java -jar "' + get_work_dir() + CHECKSTYLE_FILENAME + '" -c/"' + get_work_dir() + GOOGLE_CHECKS_FILENAME + '" ' + sys.argv[2]  # nopep8
    communicate_thread(cmd)
