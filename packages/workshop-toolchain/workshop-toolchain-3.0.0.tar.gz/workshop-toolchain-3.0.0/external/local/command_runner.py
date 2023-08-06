from gf.verify.subprocess_adapter import run
from gf.verify.command_data import CommandType


class CompileFailureException(Exception):
    """Raise for CompileFailure exception"""


result_list = []


def run_test(commands):
    try:
        run_commands(command_type_finder(commands, CommandType.INIT))
        run_commands(command_type_finder(commands, CommandType.COMPILE))
        result_list.extend(run_commands(command_type_finder(commands,
                                                            CommandType.RUN)))
    except CompileFailureException:
        pass
    finally:
        result_list.extend(run_commands(
            command_type_finder(commands, CommandType.DELETE)))
    return result_list


def command_type_finder(command_list, command_type):
    return list(filter(lambda x: x.type == command_type, command_list))


def run_commands(command_list):
    results = []
    for command in command_list:
        results.append(run_single_command(command))
    return results


def run_single_command(command_data):
    result = run(command_data)
    if result.returncode != 0 and command_data.type is CommandType.COMPILE:
        raise CompileFailureException
    return result
