from gf.verify.exercise_test_builder import ExerciseTestBuilder
from gf.verify.command_data import CommandData, CommandType
from gf.settings import CS_COMPILER as base


class CSTestBuilder(ExerciseTestBuilder):
    def build_unit_test_command(self, test_filename):
        project = (test_filename.split("_")[1]).split(".")[0]
        test_project = project + "Test"
        solution = "./" + project + "/"
        self.command_list.extend(
            [
                CommandData(self.create_project_init_command(test_project,
                                                             "mstest",
                                                             solution),
                            CommandType.INIT),
                CommandData(self.create_add_project_to_solution_command(
                    solution, project),
                            CommandType.INIT),
                CommandData(self.create_file_move_command(test_filename,
                                                          solution +
                                                          test_project,
                                                          test_filename),
                            CommandType.INIT),
                CommandData(self.create_unittest_set_reference_command(
                    solution + test_project, solution + project),
                            CommandType.INIT),
                CommandData(self.create_unittest_run_command(solution +
                                                             test_project),
                            CommandType.RUN)
            ]
        )

    def build_regex_test_command(self, exercise_filename, requirements):
        self.command_list.append(
            CommandData(self.create_cs_compile_command(exercise_filename),
                        CommandType.COMPILE))
        self.regex_run_builder(requirements, self.create_cs_run_command,
                               [exercise_filename, False])

    def build_delete_command(self, test_filename, exercise_filename):
        self.command_list.extend(
            [
                CommandData(self.get_safe_delete_command(test_filename),
                            CommandType.DELETE)
            ]
        )

    def build_applicataion_init_command(self, solution, project,
                                        isNewSolution=True):
        if isNewSolution:
            self.command_list.append(
                CommandData(self.create_project_init_command(solution),
                            CommandType.INIT))
        self.command_list.extend(
            [
                CommandData(
                    self.create_project_init_command(
                        project, "console", path=self.get_cs_project_path(
                            solution)), CommandType.INIT),
                CommandData(self.create_add_project_to_solution_command(
                    self.get_cs_project_path(solution),
                    self.get_cs_project_path(solution, project) + project +
                    ".csproj"))
            ]
        )

    def build_file_move_command(self, filename, destination, newName):
        self.command_list.append(CommandData(self.create_file_move_command(
            filename, destination, newName), CommandType.INIT))

    def create_file_move_command(self, filename, destination, newName):
        return "cp -f " + filename + " " + destination + "/" + newName

    def create_cs_compile_command(self, filename):
        return base + " build " + self.get_cs_project_path(filename, filename)

    def create_cs_run_command(self, filename, is_unit_test=True):
        path = self.get_cs_project_path(filename, filename)
        command = "dotnet run --project " + path
        if is_unit_test:
            command.replace("run", "test")
        return command

    def get_cs_project_path(self, solution, project=None):
        result = "./" + solution + "/"
        if project is not None:
            result + project + "/"
        return result

    def create_add_project_to_solution_command(self, solutionFileWithPath,
                                               projectFileWithPath):
        return base + " sln " + solutionFileWithPath + " add " + \
               projectFileWithPath

    def create_project_init_command(self, name, type="sln", path="./"):
        return base + " new " + type + " -o " + path + name

    def create_unittest_run_command(self, testProjectPath):
        return base + " test " + testProjectPath

    def create_unittest_set_reference_command(self, testProjectPath,
                                              projectWithPath):
        return base + " add " + testProjectPath + " reference " +\
               projectWithPath
