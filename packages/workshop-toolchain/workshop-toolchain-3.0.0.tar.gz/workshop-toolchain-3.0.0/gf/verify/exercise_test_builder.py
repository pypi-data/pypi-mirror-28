import abc
import os
import sys
from gf.verify.command_data import CommandData, CommandType
from gf.settings import REGEX_TEST_INPUT_FIELD_NAME, REGEX_TEST_OUPUT_FIELD_NAME  # nopep8
from external.local.logger import Logger


class ExerciseTestBuilder():
    command_list = []
    logger = None
    is_unix_os = True

    def __init__(self):
        ExerciseTestBuilder.is_unix_os = self.is_unix()
        ExerciseTestBuilder.logger = Logger.get_logger()

    @abc.abstractmethod
    def build_unit_test_command(self, test_filename):
        """Method that fill the command_list with CommandData-s for unit
        testing."""
        raise NotImplementedError

    @abc.abstractmethod
    def build_regex_test_command(self, exercise_filename, requirements):
        """Method that fill the command_list with CommandData-s for regex
        testing."""
        raise NotImplementedError

    @abc.abstractmethod
    def build_delete_command(self, test_filename, exercise_filename):
        """Method that fill the command_list with CommandData-s for clean up
        test files and folders."""
        raise NotImplementedError

    def get_safe_delete_command(self, data_name, is_folder=False):
        self.logger.debug("Build delete command for " + data_name)
        return "rm -rf " + data_name if self.is_unix_os else \
            "if exist " + data_name + " del /Q " + data_name + \
            " & if exist " + data_name + " rd /Q " + data_name

    def regex_run_builder(self, requirements, run_command_creator,
                          run_command_parameters=None):
        self.logger.debug("Build run command for regex test")
        input_list = self.regex_test_data_collect(
            requirements, REGEX_TEST_INPUT_FIELD_NAME)
        output_list = self.regex_test_data_collect(
            requirements, REGEX_TEST_OUPUT_FIELD_NAME)
        for index, regex in enumerate(output_list):
            if len(input_list) == index:
                input_list.append(None)
            self.command_list.append(CommandData(
                run_command_creator() if run_command_parameters is None else
                run_command_creator(*run_command_parameters),
                CommandType.RUN, input_list[index],
                regex))

    def is_unix(self):
        return not sys.platform.__contains__("win32")

    def get_path_for_current_os(self, is_unix, path):
        if not is_unix:
            temporary_path = path.replace("/", "\\")
            temporary_path = temporary_path.replace(":", ";")
            drive_letter = self.get_home_dirs_drive_letter()
            temporary_path = temporary_path.replace(drive_letter + ";",
                                                    drive_letter + ":")
            self.logger.debug("windows formated path: " + temporary_path)
            return temporary_path
        self.logger.debug("unix formated path: " + path)
        return path

    def get_home_dir(self):
        return os.path.expanduser("~") + "/"

    def get_home_dirs_drive_letter(self):
        return self.get_home_dir()[0]

    def regex_test_data_collect(self, requirements, field_name):
        ExerciseTestBuilder.logger.debug(field_name +
                                         " data collecting for regex test")
        data_list = []
        if field_name == REGEX_TEST_INPUT_FIELD_NAME:
            for requirement in requirements:
                data_list.append(["\n".join(str(requirement[field_name]))])
        else:
            for requirement in requirements:
                data_list.append(requirement[field_name])
        return data_list
