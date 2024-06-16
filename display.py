import os
from time import sleep
from scroll import Scroll

from parameters import Parameter as P


class DisplayManager:

    def __init__(self, modules) -> None:
        self.modules = modules
        self.syncing = True
        self.description = Scroll(maxlen=P.DISPLAY_LINES_ON_CONSOLE)

    @staticmethod
    def status_icon(module):

        action_count = len(module.files)
        if module.exec:
            action_count += 1
        if module.launch_file:
            action_count += 1

        if module._synced == 0:
            return '⚫'
        elif module._synced == action_count:
            return '🟢'
        elif module._synced in range(1, action_count):
            return '⭕'
        return '🔴'


    def display_title(self):
        print(P.APPLICATION_TITLE,end='\n'*2)

    def diplay_sync_status(self):
        for module in self.modules.values():
            print(' ', self.status_icon(module), f' {module.name}', end='')
            print('  (overwritten)' if module._forced else '')
        print()

    def display_description(self):
        for line in self.description:
            print(line)

    def display(self, loop=True):
        try:
            while self.syncing:
                os.system('clear')
                self.display_title()
                self.diplay_sync_status()
                self.display_description()
                sleep(P.REFRESH_FRAME_INTERVAL)

                if not loop:
                    break

        except KeyboardInterrupt:
            print("Exiting...")
            return
