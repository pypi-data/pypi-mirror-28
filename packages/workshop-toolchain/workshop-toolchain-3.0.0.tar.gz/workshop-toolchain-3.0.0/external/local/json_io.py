import json
from external.local.user_presenter import io_error, value_error


def save_json_content(path, content):
    try:
        return file_save(path, json.dumps(content, indent=2, sort_keys=True))
    except IOError:
        io_error()
    except ValueError:
        value_error()


def get_json_content(path):
    try:
        return json.loads(file_read(path))
    except (IOError, ValueError):
        return None


def file_save(path, content):
    with open(path, "w") as output:
        output.write(content)


def file_read(path):
    with open(path, "r") as input:
        return input.read()
