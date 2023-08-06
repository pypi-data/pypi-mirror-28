import json
from external.local.json_handler import check_exercise_exist, get_gh_handle,\
                                        get_ws_url, get_language
from external.local.user_presenter import rate_exercise, rating_out_bound,\
                                          start_communicating, rating_finish
from external.web.http_request_handler import http_request_handling
from external.web.elastic_seacrh_queries import already_in_elk, get_id
from gf.settings import ELK_HOST, ELK_INDEX


def start(filename):
    try:
        rating = int(rate_exercise())
        check_arguments(filename, rating)
        body = json.dumps(collect_rating_params(filename, rating))
        start_communicating()
        check_if_update_and_start_rating(body, filename)
        rating_finish()
    except ValueError:
        rating_out_bound()


def check_arguments(filename, rating):
    check_exercise_exist(filename)
    if rating not in range(1, 6):
        rating_out_bound()


def check_if_update_and_start_rating(body, filename):
    uri = "https://" + ELK_HOST + ELK_INDEX + "/exercise_rate/_search"
    body_dict = json.loads(body)
    if already_in_elk(uri, filename, body_dict["github"]):
        elk_id = get_id(uri, body_dict["exercise"], body_dict["github"])
        send_rating("exercise_rate_update", body, elk_id)
    else:
        send_rating("exercise_rate", body)


def send_rating(elastic_type, body, elk_id=""):
    http_request_handling(elastic_type, body, elk_id)


def collect_rating_params(filename, rating):
    gh_handle = get_gh_handle()
    link = get_ws_url()
    lang = get_language()
    return {
        "name": "exercise-rate",
        "github": gh_handle,
        "rating": rating,
        "exercise": filename,
        "workshop": link,
        "language": lang
    }
