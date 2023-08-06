from gf.settings import C_UNITTEST_HEADER, HAMCREST_FILENAME, JUNIT_FILENAME, CHECKSTYLE_FILENAME, GOOGLE_CHECKS_FILENAME, JUNIT_URL, HAMCREST_URL, CHECKSTYLE_URL, GOOGLE_CHECKS_URL, C_UNITTEST_URL  # nopep8


def get_test_env_datas(language):
    return {
        "javascript": [],
        "cs": [],
        "python": [],
        "java": [
            {
                "link": JUNIT_URL,
                "file_name": JUNIT_FILENAME
            },
            {
                "link": HAMCREST_URL,
                "file_name": HAMCREST_FILENAME
            },
            {
                "link": CHECKSTYLE_URL,
                "file_name": CHECKSTYLE_FILENAME
            },
            {
                "link": GOOGLE_CHECKS_URL,
                "file_name": GOOGLE_CHECKS_FILENAME
            }
        ],
        "c": [
            {
                "link": C_UNITTEST_URL,
                "file_name": C_UNITTEST_HEADER
            }
        ]
    }[language]
