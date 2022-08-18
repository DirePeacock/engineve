import os
import pathlib
import logging
import yaml
from .gametypes.actor import Actor


class Loader:
    save_data_loc = "~"

    def __init__(self, base_dir=None, *args, **kwargs):
        # TODO IMPORTANT as a library we may not want for this to require a cfg file in the lib itself
        # self.config_data = self._init_config_data(config_yml)
        # self.base_dir = pathlib.Path(self.config_data["base_dir"])
        #
        self.base_dir = (
            base_dir
            if base_dir is not None
            else pathlib.Path(os.path.expanduser("~")) / "engineve"
            # else pathlib.Path(__file__).parent.parent.parent / "tests" / "test_data_load_loc"
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

    def _get_char_data(self, name) -> dict:
        """get dict of character data out of the file

        allows us to test save&load a bit easier.
        """
        char_data = {}
        name_file = name if ".yml" in name else name + ".yml"
        # character_file_path = self.characters_dir / name_file
        # with open(character_file_path, "r") as character_file:
        #     char_data = yaml.safe_load(character_file)
        # TODO find adventureres
        logging.debug(self.characters_dir.glob("*"))
        for character_file_path in self.characters_dir.iterdir():
            thing = str(character_file_path)
            logging.debug(thing)
            if name.lower() in character_file_path.name.lower():
                with open(character_file_path, "r") as character_file:
                    char_data = yaml.safe_load(character_file)

        # if
        for key, val in char_data.items():
            retval = val
            if "name" not in retval.keys():
                retval["name"] = key
            return retval

        # for char_name in char_data["Adventurers"].keys():
        #     if name.lower() == char_name.lower():
        #         retval = char_data["Adventurers"][char_name]
        #         if "name" not in retval.keys():
        #             retval["name"] = char_name
        #         return retval

    def load_character(self, name) -> Actor:
        """load this one character"""
        actor_kwargs = self._get_char_data(name)
        if actor_kwargs is not None:
            return Actor(**actor_kwargs)
        else:
            logging.debug(f"char with {name} not found")

    def export_character(self, actor):
        """from actor dump a charactersheet"""
        character_file_path = self.characters_dir / actor.name
        return

    @property
    def save_file_name(self):
        return self._save_slot if ".yml" in self._save_slot else self._save_slot + ".yml"

    def save_game(self):
        """game should be saved and overwritten to the save slot"""
        filename = self.save_file_name
        with open(self.base_dir / filename, "w") as game_data_file:
            return yaml.dump(self.serialize(), game_data_file)

    def load_game(self, save_slot):
        self._save_slot = save_slot
        game_data = None
        with open(self.base_dir / self.save_file_name, "r") as game_data_file:
            game_data = yaml.safe_load(game_data_file)

        if game_data is None:
            return
        # else redo __init__ with new kwargs
        self.__init__(**game_data)
