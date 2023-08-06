import subprocess
import sys


def run(command_data):
    shell = is_windows_platform()  # windows needs shell = True to work
    # correctly, linux require False
    command_array = command_data.command.split(" ")
    input_string = ""
    if command_data.input is not None:
        input_string = "".join(command_data.input)
    return subprocess.run(command_array, stdout=subprocess.PIPE,
                          shell=shell, stderr=subprocess.PIPE,
                          input=input_string.encode())


def is_windows_platform():
    return sys.platform.__contains__("win32")
