from gf.verify.java_test_builder import JavaTestBuilder
from gf.verify.c_test_builder import CTestBuilder
from gf.verify.js_test_builder import JsTestBuilder
from gf.verify.py_test_builder import PyTestBuilder
from gf.verify.cs_test_builder import CSTestBuilder


def collect_commands(filename, test_filename, exercise_language,
                     requirements=None):
    test_builder = select_test_builder(exercise_language)()
    if requirements is None:
        test_builder.build_unit_test_command(test_filename)
    else:
        test_builder.build_regex_test_command(filename, requirements)
    test_builder.build_delete_command(test_filename, filename)
    return test_builder.command_list


def select_test_builder(exercise_language):
    return {
        "c": CTestBuilder,
        "cs": CSTestBuilder,
        "java": JavaTestBuilder,
        "js": JsTestBuilder,
        "py": PyTestBuilder
    }[exercise_language]
