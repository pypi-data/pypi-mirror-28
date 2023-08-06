VERSION_FILE = "gf/version.txt"
USAGE_INFO = "Usage: gf <command> <additional parameter>\n\nAvailable features:"  # nopep8
FEATURES = [
    ["<command>", "description"],
    ["config", "configurate the application"],
    ["start <workshop name>", "download the workshop exercises"],
    ["open", "open the workshop page in the default browser"],
    ["verify <exercise name>", "verify the choosen exercise"],
    ["rate <exercise name>", "rate the choosen exercise"],
    ["lint <exercise name>", "detect stylistic errors in the choosen exercise"],  # nopep8
    ["--version / -v", "show the version number"],
    ["dash", "show the dashboard"],
    ["update", "update the program"]
]
ESTIMATED_LENGTH = 33
# configuration for the json files.
WORKSHOP_DATA_FILENAME = ".gf.json"
CONFIG_FILENAME = "config.json"
FILE_ENCODING = "utf-8"
DEBUG_FILE_NAME = "gf-debug.log"

# configuration for gihub
ORGANIZATION = "greenfox-academy"
ORGANIZATION_ID = 14247612
TOKEN_REQUEST_URL = "http://18.195.151.95:5000/tokenpls"

# configuration for app
APP_BASE_FOLDER_NAME = ".gf"
APP_NAME = "workshop-toolchain"
APP_OUTDATED_COMMAND = "pip list --outdated"
ASSET_FILE_EXTENSIONS = ["txt", "csv"]
SUPPORTED_LANGUAGES = ["java", "cs", "python", "js", "c"]

# configuration for spinner
SPINNING_CURSOR_SEQUENCE = "|/-\\"

# configuration for c_environment and testing
C_COMPILER = "gcc"
C_UNITTEST_HEADER = "minunit.h"
C_COMPILED_FILENAME = "test.o"
C_UNITTEST_URL = "https://unit-testing.000webhostapp.com/test_files/minunit.h"

# configuration for cs_environment and testing
CS_COMPILER = "dotnet"

# configuration for java_environment and testing
JAVA_COMPILER = "javac"
JUNIT_FILENAME = "junit-4.12.jar"
HAMCREST_FILENAME = "hamcrest-core-1.3.jar"
CHECKSTYLE_FILENAME = "checkstyle-8.5-all.jar"
GOOGLE_CHECKS_FILENAME = "google_checks.xml"
JUNIT_URL = "https://unit-testing.000webhostapp.com/test_files/junit-4.12.jar"
HAMCREST_URL = "https://unit-testing.000webhostapp.com/test_files/hamcrest-core-1.3.jar"  # nopep8
CHECKSTYLE_URL = "https://unit-testing.000webhostapp.com/test_files/checkstyle-8.5-all.jar"  # nopep8
GOOGLE_CHECKS_URL = "https://unit-testing.000webhostapp.com/test_files/google_checks.xml"  # nopep8

# configuration for javascript_environment and testing
JS_SERVER = "node"
JS_SERVER_MODULES = "node_modules/"
JS_TESTER = "node"

# configuration for python_environment and testing
PY_RUN = "python"
PY_TESTER = "nose2"
PY_BYTECODE_EXTENSION = "pyc"
PY_BYTECODE_FOLDER = "__pycache__"

# configuration for regex testing
REGEX_TEST_INPUT_FIELD_NAME = "ex_input"
REGEX_TEST_OUPUT_FIELD_NAME = "ex_output"

# configuration for elastic search
ELK_HOST = "search-elk-gf-ev-cli-iyzyiukmibnnzjpsgcha26qheq." \
    "eu-west-2.es.amazonaws.com"
ELK_INDEX = "/edu_monitoring"

# url parts for the worshop name
WORKSHOP_URL_BEGIN = "https://github.com/greenfox-academy/teaching-materials/blob/master/workshop/"  # nopep8
WORKSHOP_URL_JAVA = "/java.md"
WORKSHOP_URL_PYTHON = "/python.md"
WORKSHOP_URL_CS = "/cs.md"
WORKSHOP_URL_JS = "/javascript.md"
