import os
import pathlib
import yaml
from .gametypes.actor import Actor


class Loader:
    def __init__(self, base_dir=None):
        # TODO IMPORTANT as a library we may not want for this to require a cfg file in the lib itself
        # self.config_data = self._init_config_data(config_yml)
        # self.base_dir = pathlib.Path(self.config_data["base_dir"])
        #
        self.base_dir = (
            base_dir
            if base_dir is not None
            else pathlib.Path(__file__).parent.parent.parent / "tests" / "test_data_load_loc"
        )
        self.characters_dir = self.base_dir / "characters"
        self._init_base_dir()

    def _init_config_data(self, config_yml=None):
        config_file_path = (
            config_yml if config_yml is not None else pathlib.Path(__file__).parent / "config" / "config.yml"
        )
        with open(config_file_path, "r") as config_file:
            return yaml.safe_load(config_file)

    def _init_base_dir(self):
        """make sure the dirs are there"""
        todo = {"base": self.base_dir, "characters": self.characters_dir}
        for key, path_val in todo.items():
            if not path_val.exists():
                os.mkdir(path_val)

    def load(self, thing):
        pass

    def save(self):
        """you probably want to just dump the serializable as a tree starting at the engine"""
        pass

    def load_character(self, name) -> Actor:
        """load this one character"""
        char_data = None
        name_file = name if ".yml" in name else name + ".yml"
        character_file_path = self.characters_dir / name_file
        with open(character_file_path, "r") as character_file:
            char_data = yaml.safe_load(character_file)

        return Actor(char_data)

    def save_character(self):
        """from actor dump a charactersheet"""
        pass
