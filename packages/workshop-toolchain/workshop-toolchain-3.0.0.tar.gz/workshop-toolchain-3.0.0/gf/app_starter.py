from external.local.logger import Logger
from external.local import user_presenter
from external.local.critical_error_handling import set_uncaught_ex_handling
from gf import app_controller
from time import perf_counter
from socket import gaierror


def main():
    set_uncaught_ex_handling()
    logger = Logger.get_logger()
    start = perf_counter()
    logger.info("Application start")
    try:
        app_controller.run()
    except gaierror as e:
        logger.critical(e)
        user_presenter.no_internet_connection()
    end = perf_counter()
    logger.info("Application end", {"duration": end - start})


if __name__ == "__main__":
    main()
