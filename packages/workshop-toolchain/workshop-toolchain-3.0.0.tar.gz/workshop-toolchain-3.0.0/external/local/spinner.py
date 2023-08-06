from sys import stdout
from time import sleep
from threading import Thread
from gf.settings import SPINNING_CURSOR_SEQUENCE


class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while True:
            for cursor in SPINNING_CURSOR_SEQUENCE:
                yield cursor

    @staticmethod
    def spinner_task():
        spinner_generator = Spinner.spinning_cursor()
        while Spinner.busy:
            stdout.write(next(spinner_generator))
            stdout.flush()
            sleep(Spinner.delay)
            stdout.write("\b")
            stdout.flush()

    @staticmethod
    def start():
        Spinner.busy = True
        Thread(target=Spinner.spinner_task).start()

    @staticmethod
    def stop():
        Spinner.busy = False
        sleep(Spinner.delay)
