from gf.verify.exercise_test_builder import ExerciseTestBuilder
from gf.verify.command_data import CommandData, CommandType
from gf.settings import C_COMPILED_FILENAME, C_COMPILER, APP_BASE_FOLDER_NAME


class CTestBuilder(ExerciseTestBuilder):

    def build_unit_test_command(self, test_filename):
        self.command_list.extend(
            [
                CommandData(self.
                            create_c_compile_command(test_filename),
                            CommandType.COMPILE),
                CommandData(self.create_c_run_command(),
                            CommandType.RUN)
            ]
        )

    def build_regex_test_command(self, exercise_filename, requirements):
        self.command_list.append(CommandData(
            self.create_c_compile_command(exercise_filename),
            CommandType.COMPILE))
        self.regex_run_builder(requirements, self.create_c_run_command)

    def build_delete_command(self, test_filename, exercise_filename):
        self.command_list.extend(
            [
                CommandData(self.
                            get_safe_delete_command(C_COMPILED_FILENAME),
                            CommandType.DELETE),
                CommandData(self.get_safe_delete_command(test_filename),
                            CommandType.DELETE)
            ]
        )

    def create_c_compile_command(self, actual_filename):
        return C_COMPILER + " " + actual_filename + " -I " + \
            self.get_path_for_current_os(
                self.is_unix_os,
                self.get_home_dir() + APP_BASE_FOLDER_NAME + "/") +\
            " -o " + C_COMPILED_FILENAME

    def create_c_run_command(self):
        return self.get_path_for_current_os(self.is_unix_os,
                                            "./" + C_COMPILED_FILENAME)
