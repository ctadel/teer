import os
import sys
import subprocess
from typing import List
from getpass import getpass

from schema import ModuleSchema
from display import DisplayManager


class Sudo:

    def __init__(self, modules:List[ModuleSchema]) -> None:
        self.modules = modules
        self.console = DisplayManager(modules)


    @staticmethod
    def required(modules:List[ModuleSchema]):
        for module in modules.values():
            if module.exec and module.exec.startswith('sudo '):
                return True


    def read_sudo_password(self):
        return getpass("Enter the sudo password: ")


    def validate_password(self):
        command = f'echo "{self.password}" | sudo -S echo 1'
        response = os.system(command)
        assert response == 0


    def setup(self):

        self.console.display(loop=False)

        print(
            'Some command/s require sudo permissions \
             \nType in your sudo password or <Ctrl-C> to skip the script execution.\n'
        )

        try:
            self.password = self.read_sudo_password()
            self.validate_password()
        except KeyboardInterrupt:
            self.password = None
        except AssertionError:
            print("Incorrect password. Exiting.")
            sys.exit(1001)

        # attach password to sudo commands
        for module in self.modules.values():
            if module.exec and module.exec.startswith('sudo '):
                if self.password:
                    module.exec = f"echo '{self.password}' | sudo -S " \
                                + module.exec.strip()[5:]
                else:
                    module.exec = 'echo ' + f'Skipped: {module.exec}'
