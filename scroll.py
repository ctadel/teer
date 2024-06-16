import os
import sys
import logging
from os import path
from datetime import datetime
from collections import deque
from parameters import Parameter as P


class Scroll(deque):
    def __init__(self, *args, **kwargs):
        self.logger = Logger.logger
        super().__init__(*args, **kwargs)

    def append(self, line):
        if P.LOGGING_ENABLED:
            self.logger.info(line)
        super().append(line)


class Logger:

    logger = None

    def setup_logging():
        """
            Using this makes the program looks a little less printy everywhere.
            Instead of using python's logger module, this seemed more clean.
        """

        if not P.LOGGING_ENABLED:
            return

        logging.basicConfig(
            level=logging.DEBUG,  # Set the logging level to DEBUG to capture all messages
            format='%(message)s',
            handlers=[logging.FileHandler(P.LOG_FILE_PATH, mode='a')]  # Append mode
        )
        logger = logging.getLogger('teer')

        os.chdir(P.SCRIPT_DIR)
        log_file = path.abspath(P.LOG_FILE_PATH)

        try:
            os.makedirs(path.dirname(log_file), exist_ok=True)

            user_login = f'{os.getlogin()}@{os.uname()[1]}'
            sys_args = ' '.join(sys.argv)
            header = f'\n\n[{user_login}] {datetime.now()}\n{sys_args}\n'+'-'*100 + '\n'
            logger.info(header)

            Logger.logger = logger

        except Exception as e:
            print(e)
            exit(2)


    @staticmethod
    def print_log_path():
        if not P.LOGGING_ENABLED:
            return

        print(f"\nLogs: {P.LOG_FILE_PATH}")
