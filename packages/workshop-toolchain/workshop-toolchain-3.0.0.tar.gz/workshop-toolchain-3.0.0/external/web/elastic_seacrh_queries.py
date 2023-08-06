import json
import requests


def query_by_finame_and_ghandle(uri, filename, gh_handle):
    """Simple Elasticsearch Query"""
    query = json.dumps({
        "query": {
            "bool": {
                "must": [
                    {"match": {"exercise": filename}},
                    {"match": {"github": gh_handle}}
                ]
            }
        }
    })
    response = requests.get(uri, data=query)
    results = json.loads(response.text)
    return results


def get_id(uri, filename, gh_handle):
    results = query_by_finame_and_ghandle(uri, filename, gh_handle)
    elk_id = results["hits"]["hits"][0]["_id"]
    return elk_id


def already_in_elk(uri, filename, gh_handle):
    return True if query_by_finame_and_ghandle(uri, filename,
                                               gh_handle)["hits"]["total"] \
                   is not 0 else False
