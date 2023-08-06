import sys
from gf.settings import VERSION_FILE, APP_NAME
import requests
from pkg_resources import parse_version


def open_file():
    try:
        with open(VERSION_FILE, "r") as file:
            return file.read().split(".")
    except FileNotFoundError:
        print(VERSION_FILE + " not found")


def save_to_file(function):
    try:
        with open(VERSION_FILE, 'w') as file:
            file.write(str(function))
    except FileNotFoundError:
        print(VERSION_FILE + " not found")


def version_update(case):
    data = open_file()
    dictionary = {
        "major": 0,
        "minor": 1,
        "patch": 2
    }
    data[dictionary[case]] = str(int(data[dictionary[case]]) + 1)
    save_to_file(".".join(data))


def get_version():
    try:
        with open(VERSION_FILE, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(VERSION_FILE + " not found")


def version_number():
    url = "https://pypi.python.org/pypi/{}/json".format(APP_NAME)
    return sorted(requests.get(url).json()["releases"], key=parse_version)[-1]


def toolchain_version():
    return "Workshop-toolchain " + version_number()


if __name__ == '__main__':
    try:
        version_update(sys.argv[1])
    except KeyError:
        print("Invalid argument")
