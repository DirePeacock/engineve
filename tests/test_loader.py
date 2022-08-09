from engineve.mainfactory import factory
from engineve.archetypes import characterclass
from engineve.actorai.movefactory import load_game_move
import utils
import yaml


def test_loader_init():
    """make sure that all the dirs are there when you make the thing"""
    game_engine = utils.new_game_engine()
    paths_to_check = {"base": game_engine.base_dir, "characters": game_engine.characters_dir}
    is_good = all(path.exists() for path in paths_to_check.values())
    assert is_good


def test_save_game():
    is_good = False
    assert is_good


def test_load_game():
    is_good = False
    assert is_good


def test_save_char():
    is_good = False
    # game_engine.load_character("solaire")
    assert is_good


def test_load_char():
    is_good = False
    game_engine = utils.new_game_engine()
    game_engine.load_character("solaire")
    assert is_good


def test_load_game_move():
    is_good = False
    assert is_good


def test_save_game_move():
    is_good = False
    assert is_good
