from enum import Enum


class CommandType(Enum):
    INIT = 0
    COMPILE = 1
    RUN = 2
    DELETE = 3


class CommandData:

    def __init__(self, command=None, type=CommandType.RUN, input=None,
                 regex=None):
        self.command = command
        self.type = type
        self.regex = regex
        self.input = input
