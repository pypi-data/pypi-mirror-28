from external.web.http_request_handler import open_url_from_task
from external.web import url_handler
from external.local.json_handler import get_ws_url
from gf.verify.subprocess_adapter import run
from gf.verify.command_data import CommandData


def unsafe_opener():
    open_url_from_task(get_ws_url())


def open_start():
    url = get_ws_url()
    run(CommandData("gf unsafe-open"))
