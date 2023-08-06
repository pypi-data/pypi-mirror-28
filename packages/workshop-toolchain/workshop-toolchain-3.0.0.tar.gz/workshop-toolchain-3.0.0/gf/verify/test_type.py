from enum import Enum
from external.local.json_handler import get_json_content


class TestType(Enum):
    UNIT = 0
    REGEX = 1


def get_test_type(test_filename):
    return{"c": TestType.UNIT,
           "cs": TestType.UNIT,
           "java": TestType.UNIT,
           "js": TestType.UNIT,
           "py": TestType.UNIT,
           "json": TestType.REGEX}[test_filename.split(".")[-1]]


def get_requirement_data_for_regex(filename):
    return get_json_content(filename)["cases"]
