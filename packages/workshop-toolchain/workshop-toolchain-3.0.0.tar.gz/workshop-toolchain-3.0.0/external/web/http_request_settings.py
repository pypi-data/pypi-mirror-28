from gf.settings import ELK_HOST, ELK_INDEX


def get_request_settings(request_type, elk_id):
    elk_host = ELK_HOST
    edu_index = ELK_INDEX
    json_header = {"Content-type": "application/json"}
    return {
        "log_post_elk": {
            "host": elk_host,
            "url": edu_index + "/eventlog",
            "method": "POST",
            "header": json_header
        },
        "exercise_rate": {
            "host": elk_host,
            "url": edu_index + "/exercise_rate",
            "method": "POST",
            "header": {"Content-type": "application/json"}
        },
        "exercise_rate_update": {
            "host": elk_host,
            "url": edu_index + "/exercise_rate/" + elk_id,
            "method": "POST",
            "header": json_header
        },
        "request_token": {
            "host": "18.195.151.95:5000",
            "url": "/tokenpls",
            "method": "POST",
            "header": json_header
        }
    }[request_type]
