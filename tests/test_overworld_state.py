import includes

from engineve.enginestates.overworldstate import OverworldState


def test_menu_to_overworld_state():
    """this should be started from tyhe main menu correctly"""
    is_good = False
    # menu picks a game to load
    assert is_good


def test_overworld_to_combat_state():
    """overworld should be able to spawn 1 to 3 skeletons correctly"""
    is_good = False
    assert is_good


def test_overworld_state_rest_command():
    """combat should go back to the overworld"""
    is_good = False
    assert is_good


def test_combat_to_overworld_state():
    """combat should go back to the overworld"""
    is_good = False
    assert is_good
