import sys
from external.local.logger import Logger
from external.local import user_presenter
from external.local.json_io import get_json_content
from external.local.file_operator import save_file


def log_uncaught_exceptions(type, value, traceback):
    logger = Logger.get_logger()
    text_dict = {"type": type,
                 "value": value,
                 "traceback": traceback}
    logger.critical("Unhandled exception: %s", text_dict)
    convert_pretty_log()
    user_presenter.fatal_error()


def convert_pretty_log():
    pretty_log_content = ""
    log_data = get_json_content(Logger._file_to_log)
    padding = max(len(log_element) for log_element in log_data.keys()) + 7
    for key in log_data:
        pretty_log_content += key.ljust(padding).upper() + log_data[key] + "\n"
    save_file(Logger._file_to_log, pretty_log_content)


def set_uncaught_ex_handling():
    sys.excepthook = log_uncaught_exceptions
