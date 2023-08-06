import http.client
import webbrowser
from _socket import gaierror
from external.web import url_handler
from external.local.user_presenter import no_internet_connection
from external.web.http_request_settings import get_request_settings


def http_request_handling(request_type, body, elk_id):
    try:
        request_settings = get_request_settings(request_type, elk_id)
        host = request_settings["host"]
        url = request_settings["url"]
        method = request_settings["method"]
        header = request_settings["header"]
        http_connection = http.client.HTTPConnection(host)
        http_connection.request(method, url, body, header)
        response = http_connection.getresponse().read().decode('utf-8')
        return response
    except gaierror as e:
        no_internet_connection()


def open_url_from_task(url):
    webbrowser.open(url)
