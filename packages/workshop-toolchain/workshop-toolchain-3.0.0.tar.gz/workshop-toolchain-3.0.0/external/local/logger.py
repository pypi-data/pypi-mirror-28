import logging
from platform import system, release
from sys import argv
from external.local.json_handler import get_gh_handle
from external.local.json_handler import get_ws_url
from external.local.json_handler import get_language
from external.local.elastic_log_handler import ElasticsearchHandler
from external.local.custom_json_formatter import CustomJsonFormatter


class Logger:
    LOGGING = logging.getLogger()
    _file_to_log = "gf-debug.log"

    _features = {
        "empty": "empty",
        "help": "help",
        "config": "config",
        "start": "start",
        "verify": "verify",
        "rate": "rate"
    }

    LOGGER = None

    def __init__(self):
        self._init_logging()
        self.message = None
        self._set_system()
        self._set_gh_handle()
        self._set_command()
        self._set_feature()
        if self.feature not in ["EMPTY", "INVALID"]:
            self._set_workshop_url()
            self._set_language()
            self._set_exercise_name()

    def __str__(self):
        return str(self.__dict__)

    def _set_file_log_level(self):
        log_level = logging.CRITICAL
        if "--log-file" in argv:
            log_level = logging.INFO
        return log_level

    def _set_system(self):
        self.system = "{} {}".format(system(), release())

    def _set_gh_handle(self):
        try:
            self.gh_handle = get_gh_handle()
        except Exception:
            self.gh_handle = None

    def _set_command(self):
        self.command = " ".join(argv)

    def _set_feature(self):
        try:
            self.feature = self._features.get(argv[1],
                                              "INVALID")
        except IndexError:
            self.feature = self._features.get("empty")
        self.feature = self.feature.upper()

    def _set_workshop_url(self):
        if argv[1] == self._features["start"]:
            try:
                self.workshop_url = argv[2]
            except IndexError:
                self.workshop_url = None
        elif argv[1] == self._features["verify"]:
            self.workshop_url = argv[2]

    def _set_language(self):
        if argv[1] in [self._features["start"],
                       self._features["verify"]]:
            self.language = get_language()

    def _set_exercise_name(self):
        if argv[1] == self._features["verify"]:
            try:
                self.exercise_name = argv[2]
            except IndexError:
                self.exercise_name = None

    def _init_logging(self):
        self.LOGGING.setLevel(logging.NOTSET)
        formatter = CustomJsonFormatter('(timestamp) (level)')
        file_handler = logging.FileHandler(self._file_to_log, "w", delay=True)
        file_handler.setLevel(self._set_file_log_level())
        file_handler.setFormatter(formatter)
        self.LOGGING.addHandler(file_handler)
        elasticsearch_handler = ElasticsearchHandler()
        elasticsearch_handler.setLevel(logging.INFO)
        elasticsearch_handler.setFormatter(formatter)
        self.LOGGING.addHandler(elasticsearch_handler)

    def _create_message(self, extra):
        information = {**self.__dict__, **extra}
        return information

    def _get_logging_method(self, level):
        return {
            "critical": self.LOGGING.critical,
            "error": self.LOGGING.error,
            "warning": self.LOGGING.warning,
            "info": self.LOGGING.info,
            "debug": self.LOGGING.debug
        }[level]

    def _log(self, level, extra):
        message = self._create_message(extra)
        log = self._get_logging_method(level)
        log(message)

    def debug(self, message=None, extra={}):
        self.message = message
        self._log("debug", extra)

    def info(self, message=None, extra={}):
        self.message = message
        self._log("info", extra)

    def warning(self, message=None, extra={}):
        self.message = message
        self._log("warning", extra)

    def error(self, message=None, extra={}):
        self.message = message
        self._log("error", extra)

    def critical(self, message=None, extra={}):
        self.message = message
        self._log("critical", extra)

    @classmethod
    def get_logger(cls):
        if cls.LOGGER is None:
            cls.LOGGER = Logger()
        return cls.LOGGER
