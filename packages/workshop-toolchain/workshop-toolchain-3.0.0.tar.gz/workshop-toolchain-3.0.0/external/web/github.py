from github import Github, BadCredentialsException, GithubException
from external.local import json_handler
from external.local.file_operator import lang_convert, name_converter, save_file  # nopep8
from external.local.user_presenter import download_succes, error_message, bad_credential, wrong_repo, confirm_repo_name, message  # nopep8
from external.web.url_handler import transform_to_test_path
from external.web.http_request_handler import http_request_handling
from gf.settings import FILE_ENCODING, ORGANIZATION, ORGANIZATION_ID, ASSET_FILE_EXTENSIONS, TOKEN_REQUEST_URL  # nopep8
import json


def get_token(credential):
    payload = json.dumps(get_post_object(credential))
    request_result = json.loads(http_request_handling("request_token",
                                                      payload, ""))
    if request_result["returncode"] == 0:
        credential.token = request_result["result"]
    else:
        bad_credential()


def find_working_repo(credential):
    repos = get_user_owned_repos(credential.token)
    probably_repo = search_first_org_repo(repos)
    credential.repo = confirm_repo_name(probably_repo)


def search_first_org_repo(repos):
    for repo in repos:
        if is_org_repo(repo):
            return repo.name
    return None


def get_user_owned_repos(token):
    return Github(token).get_user().get_repos("member")


def is_org_repo(repo):
    try:
        return repo.organization is not None and \
            repo.organization.id == ORGANIZATION_ID
    except GithubException:
        return False


def get_organization(token):
    return Github(token).get_organization(ORGANIZATION)


def get_repo(repo_name):
    token = json_handler.get_token()
    return get_organization(token).get_repo(repo_name)


def get_file_content(repo, path):
    try:
        return get_and_decode(repo, path)
    except AttributeError:
        error_message("Exercise or test not found!")


def get_and_decode(repo, path):
    return repo.get_file_contents(path).decoded_content.decode(FILE_ENCODING)


def get_post_object(credential):
    return dict(username=credential.username, password=credential.password)


def content_handler(contents, repo, lang, test_paths):
    for content in contents:
        if is_needed_file(lang, content.name):
            file_name = name_converter(content.path, lang)
            test_paths[file_name] = search_test_path(
                content, repo, lang_convert(lang))
            save_file(
                file_name, get_file_content(repo, content.path))
            download_succes(file_name)


def is_needed_file(lang, filename):
    return lang_convert(lang) in get_extension(filename)  \
        or get_extension(filename) in ASSET_FILE_EXTENSIONS \
        or lang == get_name(filename)


def get_contents(workshop_data):
    repo = get_repo(workshop_data["repo"])
    test_paths = {}
    exercise_dirs = get_directory_list(
        repo, workshop_data["workshop-path"])
    for exercise_dir in exercise_dirs:
        contents = repo.get_contents(
            workshop_data["workshop-path"] + "/" + exercise_dir)
        content_handler(contents, repo, workshop_data["lang"], test_paths)

    return test_paths


def generate_issues(issue_name_list):
    repo = get_repo(json_handler.get_working_repo())
    check_if_student_repo(repo)
    issues = repo.get_issues()
    for issue_name in issue_name_list:
        if is_not_issue_already(issue_name, issues):
            generate_single_issue(issue_name, repo)


def check_if_student_repo(repo):
    handle = json_handler.get_gh_handle()
    contributors = repo.get_contributors()
    check_if_user_is_contributors(handle, contributors)


def check_if_user_is_contributors(handle, contributors):
    for contributor in contributors:
        if contributor.login == handle:
            return True
    wrong_repo()


def generate_single_issue(issue_name, repo):
    if not get_extension(issue_name) in ASSET_FILE_EXTENSIONS:
        repo.create_issue(issue_name)


def is_not_issue_already(new_issue, issues):
    for issue in issues:
        if issue.title == new_issue:
            return False
    return True


def get_extension(filename):
    return filename.split(".")[-1]


def get_name(filename):
    return filename.split(".")[0]


def search_test_path(github_content, repo, lang):
    test_directory = transform_to_test_path(github_content.path)
    try:
        contents = repo.get_contents(test_directory)
    except GithubException:
        return ""
    for content in contents:
        if lang in content.name or ".json" in content.name:
            return content.path


def get_directory_list(repo, url):
    dirs = []
    contents = repo.get_contents(url)
    for content in contents:
        if content.type == "dir":
            dirs.append(content.name)
    return dirs
