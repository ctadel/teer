import os
import json
from os import path
from dataclasses import dataclass

from parameters import Parameter as P

@dataclass
class ModuleSchema:
    """
        This dataclass is to help parse and hold the configuration file
    """

    name:str
    local_path:path = None
    remote_path:path = P.DEFAULT_REMOTE_DIRECTORY
    exec:str = None
    launch_file:path = None
    files:dict = None

    _synced:int = 0
    _forced:int = False

    def initialize(self):
        if self.local_path:
            self.local_path = path.join(P.DOTFILES_REPOSITORY,
                                    self.local_path)
        else:
            self.local_path = P.DOTFILES_REPOSITORY

        self.remote_path = path.expanduser(self.remote_path)

        assert path.isdir(self.local_path), \
            f"Invalid local path for {self.name}"

        if self.files:
            _absolute_file_paths = {}
            for source, destination in self.files.items():
                assert path.exists(path.join(self.local_path, source)), \
                    f"File not found : {path.join(self.local_path, source)}"
                assert destination, "Must specify a remote path"

                _absolute_file_paths[path.join(self.local_path, source)] = path.join(
                        self.remote_path, destination)

            self.files = _absolute_file_paths

        else:
            self.files = {}
            assert self.local_path, \
                "Must define local_path folder if files are not specified."

            for root, _, files in os.walk(self.local_path):
                for file in files:

                    if file.endswith('.desktop'):
                        continue

                    _absolute_file_path = path.join(root, file)
                    _relative_path = path.relpath(_absolute_file_path, start=self.local_path)

                    self.files[_absolute_file_path] = \
                            path.join(self.remote_path, _relative_path)


        if self.launch_file:
            _relative_path = os.path.relpath(path.join(self.local_path, self.launch_file))
            assert path.exists(_relative_path), \
                    f"Missing launch file: {_relative_path}"

            self.launch_file = _relative_path


    def __repr__(self):
        return f"ModuleSchema<{self.name.replace(' ','-')}>"

    def __str__(self):
        _string = f'\n> {self.name}'
        _string += f'\nLocal path: {self.local_path}'
        _string += f'\nRemote path: {self.remote_path}'
        _string += f'\nExecute: {self.exec}'
        _string += f'\nLaunch File: {self.launch_file}'
        _string += f'\nFile Symlinks:\n'

        for source, destination in self.files.items():
            _string += f'  {source} -> {destination}\n'

        return _string + '\n'


    @classmethod
    def from_json_object(cls, data):
        data = json.loads(data)
        schema = ModuleSchema(**data)
        schema.initialize()
        return schema


class Config:

    @staticmethod
    def read_config():
        config = path.join(P.SCRIPT_DIR, P.CONFIG_FILE_PATH)
        with open(config) as conf:
            data = json.load(conf)

        for module in data.keys():
            data[module] = ModuleSchema(module, **data[module])
            data[module].initialize()

        return data
