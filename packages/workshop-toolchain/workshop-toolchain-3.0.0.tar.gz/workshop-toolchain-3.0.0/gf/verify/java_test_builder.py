from gf.verify.exercise_test_builder import ExerciseTestBuilder
from gf.verify.command_data import CommandData, CommandType
from gf.settings import JUNIT_FILENAME, HAMCREST_FILENAME, APP_BASE_FOLDER_NAME


class JavaTestBuilder(ExerciseTestBuilder):
    def build_unit_test_command(self, test_filename):
        self.command_list.extend(
            [
                CommandData(self.
                            create_java_compile_command(test_filename),
                            CommandType.COMPILE),
                CommandData(self.create_java_run_command(test_filename),
                            CommandType.RUN)
            ]
        )

    def build_regex_test_command(self, exercise_filename, requirements):
        self.command_list.append(CommandData(
            self.create_java_compile_command(exercise_filename),
            CommandType.COMPILE))
        self.regex_run_builder(requirements, self.create_java_run_command,
                               [exercise_filename, False])

    def build_delete_command(self, test_filename, exercise_filename):
        exercise_filename = exercise_filename.split(".")[0]

        test_filename_without_ext = test_filename.split(".")[0]
        self.command_list.extend(
            [
                CommandData(self.get_safe_delete_command(exercise_filename
                                                         + ".class"),
                            CommandType.DELETE),
                CommandData(self.get_safe_delete_command(test_filename),
                            CommandType.DELETE),
                CommandData(self.
                            get_safe_delete_command(test_filename_without_ext +
                                                    ".class"),
                            CommandType.DELETE)
            ]
        )

    def create_java_compile_command(self, actual_filename):
        return "javac -cp " + self. \
            get_path_for_current_os(self.is_unix_os,
                                    self.get_class_path()) +\
               actual_filename

    def create_java_run_command(self, exercise_filename, is_unit_test=True):
        command = "java -cp " + self. \
            get_path_for_current_os(self.is_unix_os, self.get_class_path())
        if is_unit_test:
            command += "org.junit.runner.JUnitCore "
        command += exercise_filename.split(".")[0]
        return command

    def get_class_path(self):
        return self.get_home_dir() + APP_BASE_FOLDER_NAME + "/" + \
               JUNIT_FILENAME + ":" + self.get_home_dir() + \
               APP_BASE_FOLDER_NAME + "/" + HAMCREST_FILENAME + ":. "
