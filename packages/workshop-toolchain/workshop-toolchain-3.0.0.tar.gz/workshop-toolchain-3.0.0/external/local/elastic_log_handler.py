import logging
from external.web.http_request_handler import http_request_handling


class ElasticsearchHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

    def mapLogRecord(self, record):
        return record.__dict__

    def emit(self, record):
        body = self.format(record)
        http_request_handling("log_post_elk", body, elk_id="")
