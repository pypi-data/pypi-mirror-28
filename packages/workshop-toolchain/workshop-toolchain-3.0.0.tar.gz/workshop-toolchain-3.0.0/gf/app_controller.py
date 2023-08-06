from external.local import user_presenter
from gf.config import config_service
from gf.verify import verify_service
from gf.start import start_service
from gf.open import open_service
from gf.rate import rate_service
from gf.dash import dashboard_printer
from external.web import url_handler
from gf.lint import lint_service
from sys import argv
from gf.upgrade import upgrade


def run():
    try:
        task_check(argv[1])()
    except KeyboardInterrupt:
        user_presenter.keyboard_interrupted()
    except (IndexError):
        user_presenter.help_message()


def filename_maker(filename):
    if filename.startswith("./"):
        return filename.split("./")[1]
    else:
        return filename


def task_check(task_name):
    return {
        "config": config_start,
        "verify": verify_start,
        "start": start,
        "rate": rate_start,
        "unsafe-open": unsafe_open_start,
        "--version": version_show,
        "-v": version_show,
        "lint": lint,
        "open": open_start,
        "dash": dash_show,
        "update": update
    }.get(task_name, help_message)


def open_start():
    open_service.open_start()


def update():
    upgrade.upgrade_the_old_module()


def dash_show():
    dashboard_printer.controller()


def help_message():
    user_presenter.help_message()


def config_start():
    config_service.start()


def verify_start():
    verify_service.start(filename_maker(argv[2]))


def start():
    start_service.main(url_handler.make_full_workshop_url(argv[2]))


def rate_start():
    rate_service.start(argv[2])


def unsafe_open_start():
    open_service.unsafe_opener()


def version_show():
    user_presenter.get_version_number()


def lint():
    lint_service.start(filename_maker(argv[2]))
