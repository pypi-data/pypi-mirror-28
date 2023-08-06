from external.local.file_operator import save_file, get_extension
from external.local import user_presenter
from external.local.json_handler import check_token, check_gfjson_not_exist
from external.local.json_handler import check_exercise_exist
from external.local.logger import Logger
from gf.verify.filetest_collector_from_gfjson import collect_test
from gf.verify.filetest_collector_from_gfjson import get_test_file_name
from gf.verify.test_type import TestType, get_test_type
from gf.verify.test_type import get_requirement_data_for_regex
from gf.verify.command_collector import collect_commands
from gf.verify.result_process import test_evaluate


def start(filename):
    prepare_to_verify(filename)
    verify(filename)
    user_presenter.message("Verify finished")


def prepare_to_verify(filename):
    verify_checking(filename)
    user_presenter.start_communicating()
    file_path, content = collect_test(filename)
    save_test(file_path, content)


def verify_checking(filename):
    check_token()
    check_gfjson_not_exist()
    check_exercise_exist(filename)


def save_test(file_path, content):
    save_file("./" + file_path, content)


def verify(filename):
    logger = Logger.get_logger()
    logger.info("verifying start")
    requirements = None
    test_filename = get_test_file_name(filename)
    language = get_extension(filename)
    if TestType.REGEX == get_test_type(test_filename):
        requirements = get_requirement_data_for_regex(
            test_filename)
    logger.info("test commands collecting")
    commands = collect_commands(filename, test_filename,
                                language, requirements)
    test_result = test_evaluate(commands)
    logger.info("succesfull test" if test_result else "failed test")
    return test_result
