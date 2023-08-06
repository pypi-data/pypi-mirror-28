import urllib.request

from external.local import user_presenter
from external.local.env_test_datas import get_test_env_datas
from external.local.file_operator import does_exist, get_work_dir


def set_test_environment(language):
    test_env_datas = get_test_env_datas(language)
    for file_data in test_env_datas:
        if not does_exist(get_work_dir() + file_data["file_name"]):
            user_presenter.start_communicating()
            urllib.request.urlretrieve(file_data["link"],
                                       get_work_dir() + file_data["file_name"])
            user_presenter.download_test_env()
