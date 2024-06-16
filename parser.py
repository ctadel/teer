import os
import sys
import argparse
import configparser
from os import path

from parameters import Parameter


class ArgParser:

    def process_args():
        """
            Use this function to add/edit sys arguments
        """

        parser = argparse.ArgumentParser(
                prog='teer',
                description='Sync your dot files with this fancy program.',
                epilog='prajwaldev.com.np',
             )

        parser.add_argument('--force', action='store_true',
                help='Overwrite currently existing configurations'
            )

        parser.add_argument('-i', '--interactive', action='store_true',
                help='Choose what config to sync at run time'
            )

        parser.add_argument('--log', nargs='?',
                help='Log the events of the program to a file'
            )

        return parser.parse_args()



class ParameterParser:

    parameters_file = path.join(Parameter.SCRIPT_DIR, 'parameters.cfg')

    @staticmethod
    def process_params():
        if not os.path.exists(ParameterParser.parameters_file):
            return

        parser = configparser.ConfigParser()
        parser.read(ParameterParser.parameters_file)
        Parameter.update_params(parser)


class Parser(ArgParser, ParameterParser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def parse():
        args = Parser.process_args()

        Parser.process_params()

        if args.force:
            Parameter.FORCE_OVERWRITE = True
        if args.interactive:
            Parameter.INTERACTIVE_SYNC = True
        if '--log' in sys.argv:
            Parameter.LOGGING_ENABLED = True
            if args.log:
                Parameter.LOG_FILE_PATH = args.log

        return Parameter
