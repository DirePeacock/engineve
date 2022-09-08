import pathlib
import pprint
import os
import yaml
import utils
import logging

from engineve.mainfactory import factory
from engineve.archetypes import characterclass
from engineve.actorai.movefactory import load_game_move


def test_loader_init():
    """make sure that all the dirs are there when you make the thing"""
    game_engine = utils.new_game_engine()
    paths_to_check = {"base": game_engine.base_dir, "characters": game_engine.characters_dir}
    is_good = all(path.exists() for path in paths_to_check.values())
    assert is_good


def test_save_game():
    """"""
    # TODO make sure this goes to the right place after where that is has been figured out
    pp = pprint.PrettyPrinter(indent=4)
    game_engine = utils.new_game_engine()
    test_name = "Solaire"
    test_actor = game_engine.import_character(name=test_name)
    save_data = game_engine.serialize()
    pp.pprint(save_data)
    game_engine._save_slot = "test"
    test_save_path = game_engine.base_dir / game_engine.save_file_name
    if test_save_path.exists():
        os.remove(test_save_path)
    game_engine.save_game()

    assert test_save_path.exists()
    data_we_just_saved = None
    with open(test_save_path, "r") as test_save_file:
        data_we_just_saved = yaml.safe_load(test_save_file)

    pp.pprint(data_we_just_saved)
    # logging.debug("aaaa")


def test_load_game():
    """the game should be able to be loaded
    should have all the actors
    should have all the party
    should have the combat order too

    """
    game_engine = utils.new_game_engine()
    game_engine.load_game("test")

    assert len(game_engine.game_state.actors) > 0


from engineve.gametypes.actor import Actor
import pathlib


def get_good_data():
    mypath = pathlib.Path(__file__).parent / "test_data_save_loc" / "characters" / "solaire.yml"
    gooddata = {}
    with open(mypath, "r") as goodfile:
        gooddata = yaml.safe_load(goodfile)["Solaire"]
        return gooddata


def add_test_actor(engine):
    engine.game_state.add_actor(Actor(**get_good_data()))


def test_save_char():
    game_engine = utils.new_game_engine()
    test_name = "Solaire"
    test_actor = None
    add_test_actor(game_engine)
    game_engine.import_character(name=test_name)
    for actor in game_engine.game_state.actors.values():
        if actor.name == test_name:
            test_actor = actor
    assert len(game_engine.game_state.actors) > 0
    loaded_data = game_engine._get_char_data(name=test_name)
    serialized_actor = test_actor.serialize()
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(loaded_data)
    # logging.debug("aaaa")


def test_load_char():
    game_engine = utils.new_game_engine()
    test_name = "Solaire"
    test_data = game_engine._get_char_data("test_name")
    test_actor = None
    game_engine.import_character(name=test_name)
    for actor in game_engine.game_state.actors.values():
        if actor.name == test_name:
            test_actor = actor
    game_engine.import_character(name=test_name)

    assert test_actor is not None
    assert test_actor.critical_threat == 19


def test_load_game_move():
    is_good = False
    assert is_good


def test_save_game_move():
    is_good = False
    assert is_good
