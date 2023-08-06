import re
from external.local.command_runner import run_test
from gf.verify.command_data import CommandType
from external.local.command_runner import command_type_finder
from external.local.user_presenter import message, random_ok_message
from gf.settings import FILE_ENCODING


def test_evaluate(command_list):
    result_list = run_test(command_list)
    return processing_result(result_list, command_type_finder(command_list,
                                                              CommandType.RUN))


def processing_result(result_list, run_command_list):
    is_successful_test = True
    for count, result in enumerate(result_list):
        if result.returncode != 0:
            check_failure(result)
            return False
        is_successful_test = evaluate_regex_test(count, is_successful_test,
                                                 result, run_command_list)
    random_ok_message() if is_successful_test else message("failed")
    return is_successful_test


def is_regex_test(command):
    return command.regex is not None


def check_regex_match(output, regex_list):
    output_list = output.decode(FILE_ENCODING).split("\n")
    regex_matches = 0
    for line in output_list:
        if re.match(regex_list[regex_matches], line) is not None:
            regex_matches = regex_matches + 1
            if len(regex_list) == regex_matches:
                return True
    return len(regex_list) == regex_matches


def check_failure(result):
    message(str(result.stderr.decode(FILE_ENCODING)))
    message(str(result.stdout.decode(FILE_ENCODING)))


def evaluate_regex_test(count, is_successful_test, result, run_command_list):
    if count < len(run_command_list) and \
            is_regex_test(run_command_list[count]):
        if not check_regex_match(result.stdout,
                                 run_command_list[count].regex):
            is_successful_test = False
            message(
                "Expected output should be:\n" +
                str("\n".join(run_command_list[count].regex)) +
                "\nYour output was:\n" +
                str(result.stdout.decode(FILE_ENCODING)))
        else:
            is_successful_test = True
    return is_successful_test
