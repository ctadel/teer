from parser import Parser
from scroll import Logger
from schema import Config
from sudo import Sudo
from sync import Synchronize


def main():

    # Setup SysArgs/ConfigArgs
    Parser.parse()

    # Setup logging if enabled
    Logger.setup_logging()

    # Read config json file
    modules = Config.read_config()

    # Manage sudo permissions
    if Sudo.required(modules):
        Sudo(modules).setup()

    # Start syncing
    sync = Synchronize(modules)
    sync.sync()

    # Print log path if logging enabled
    Logger.print_log_path()


if __name__ == "__main__":
    main()
