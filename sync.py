import re
import os
import time
import shlex
import subprocess
from os import path
from threading import Thread

from display import DisplayManager
from parameters import Parameter as P


class Synchronize:

    def __init__(self, modules) -> None:
        self.modules = modules
        self.console = DisplayManager(modules)


    def create_symlink(self, module, source, destination):
        try:
            os.makedirs(path.dirname(destination), exist_ok=True)

            if path.exists(destination) or path.islink(destination):
                if not P.FORCE_OVERWRITE:
                    raise FileExistsError()
                os.remove(destination)
                module._forced = True

            os.symlink(source, destination)
            self.console.description.append(f'✔ {source} -> {destination}')
            return True

        except PermissionError:
            self.console.description.append(f'✘ Access Error: {destination}')
            return False
        except FileExistsError:
            self.console.description.append(f'✘ File already exists: {destination}')
            return False
        except Exception as e:
            self.console.description.append(f'✘ {source} -> {destination}')
            self.console.description.append(str(e))
            return False
        finally:
            # it just looks cool if texts are moving around
            time.sleep(P.SYNC_INTERVAL_DURATION)


    def sync(self):

        YES = ['a', 'y', 'all', 'yes', 'yeah', 'yep']
        CHOOSE = ['f', 'c', 'choose', 'some']

        def display_with_input(module, *args, **kwargs):
            self.console.display(loop=False)
            print(f"\n --> [{module}]")
            return input(*args, **kwargs)

        if not P.INTERACTIVE_SYNC:
            printer = Thread(target=self.console.display)
            printer.start()

        for module in self.modules.values():

            sync_launch_file = True
            sync_exec = True

            if P.INTERACTIVE_SYNC:
                sync_module = display_with_input(module.name,
                     "Sync this module? [A/Y - All | F/C - Choose files | * - No]: ")
                if sync_module.lower() not in YES+CHOOSE:
                    module._synced = -1
                    continue

            for source, destination in module.files.items():
                if P.INTERACTIVE_SYNC:
                    if sync_module.lower() in CHOOSE:
                        sync_this_file = display_with_input(module.name, destination + '? [Y/N]: ')
                        if sync_this_file.lower() not in YES:
                            continue
                response = self.create_symlink(module, source, destination)
                if response:
                    module._synced += 1

            if P.INTERACTIVE_SYNC and \
                    module.launch_file and sync_module.lower() in CHOOSE:
                sync_launch_file = display_with_input(module.name, "Add launch file? [Y/N]: ")
                sync_launch_file = sync_launch_file.lower() in YES

            if module.launch_file and sync_launch_file:
                launch_file_dir = path.expanduser(P.LAUNCH_FILE_REPOSITORY)
                os.makedirs(launch_file_dir, exist_ok=True)
                response = self.create_symlink(module,
                        path.join(module.local_path, path.basename(module.launch_file)), \
                        path.join(launch_file_dir, path.basename(module.launch_file)))
                if response:
                    module._synced += 1

            if P.INTERACTIVE_SYNC and \
                    module.exec and sync_module.lower() in CHOOSE:
                sync_exec = display_with_input(module.name, "Execute exec script? [Y/N]: ")
                sync_exec = sync_exec.lower() in YES

            if module.exec and sync_exec:
                try:
                    sudo_script = re.match("^echo .* \| sudo \-S", module.exec)

                    if sudo_script:
                        os.system(module.exec)
                        self.console.description.append(
                                f'Executed below script with sudo access:\
                                \n{os.path.expandvars(module.exec[sudo_script.end()+1:])}'
                            )

                    else:
                        _command = shlex.split(os.path.expandvars(module.exec))

                        stdout, stderr = subprocess.Popen(_command, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, env=os.environ, start_new_session=True
                            ).communicate()
                        output = stdout.decode() + stderr.decode()
                        self.console.description.append(
                                f'✔ Output for "{module.exec}" in {module.name}:\n{output.strip()}')
                    module._synced += 1

                except Exception as e:
                    self.console.description.append(
                            f'✘ Exception while executing "{module.exec}" for {module.name}\n{e}')

            if module.files and not module._synced:
                module._synced = -1

        self.console.display(loop=False)
        self.console.syncing = False
