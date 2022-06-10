import json
import yaml
import pathlib

class Definitionlaoder():
    def load_file(self, path):
        if '.yaml' in pathlib.Path(path).name:
            self._load_yaml(path)
        if '.yaml' in pathlib.Path(path).name:
            self._load_yaml(path)
    def _load_json(self, path):
        return
    def _load_yaml(self, path):
        return