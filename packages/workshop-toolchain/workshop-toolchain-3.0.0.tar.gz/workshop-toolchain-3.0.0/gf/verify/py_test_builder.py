from gf.verify.exercise_test_builder import ExerciseTestBuilder
from gf.verify.command_data import CommandData, CommandType
from gf.settings import PY_RUN, PY_TESTER, PY_BYTECODE_EXTENSION, PY_BYTECODE_FOLDER  # nopep8


class PyTestBuilder(ExerciseTestBuilder):
    def build_unit_test_command(self, test_filename):
        self.command_list.append(
            CommandData(self.create_py_run_command(
                test_filename), CommandType.RUN)
        )

    def build_regex_test_command(self, exercise_filename, requirements):
        self.regex_run_builder(requirements, self.create_py_run_command,
                               [exercise_filename, False])

    def build_delete_command(self, test_filename, exercise_filename):
        self.command_list.extend(
            [
                CommandData(self.get_safe_delete_command(
                    "*." + PY_BYTECODE_EXTENSION),
                            CommandType.DELETE),
                CommandData(
                    self.get_safe_delete_command(PY_BYTECODE_FOLDER),
                    CommandType.DELETE),
                CommandData(self.get_safe_delete_command(
                    test_filename), CommandType.DELETE)
            ]
        )

    def create_py_run_command(self, filename, test=True):
        command, filename = (PY_TESTER, filename.split(".")[0]) if test else (
            PY_RUN, filename)
        return "{} {}".format(command, filename)
