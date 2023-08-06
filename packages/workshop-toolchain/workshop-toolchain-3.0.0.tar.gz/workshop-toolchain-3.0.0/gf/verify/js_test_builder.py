from gf.verify.exercise_test_builder import ExerciseTestBuilder
from gf.verify.command_data import CommandData, CommandType
from gf.settings import JS_SERVER


class JsTestBuilder(ExerciseTestBuilder):
    def build_unit_test_command(self, test_filename):
        self.command_list.append(
            CommandData(self.create_js_run_command(test_filename),
                        CommandType.RUN)
        )

    def build_regex_test_command(self, exercise_filename, requirements):
        self.regex_run_builder(requirements, self.create_js_run_command,
                               [exercise_filename])

    def build_delete_command(self, test_filename, exercise_filename):
        self.command_list.append(
            CommandData(self.get_safe_delete_command(test_filename),
                        CommandType.DELETE)
        )

    def create_js_run_command(self, filename):
        return JS_SERVER + " " + filename
