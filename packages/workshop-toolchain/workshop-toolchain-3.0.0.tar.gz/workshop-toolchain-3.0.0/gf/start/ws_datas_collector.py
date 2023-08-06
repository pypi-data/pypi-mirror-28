from external.web import url_handler


def collect_workshop_data(url):
    ws_url = url_handler.get_ws_from_url(url)
    lang = url_handler.get_lang_from_url(url)
    repo = url_handler.get_repo_from_url(url)
    return {
        "workshop-path": ws_url,
        "repo": repo,
        "lang": lang,
        "workshop-url": url
    }
