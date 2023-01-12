from engineve.mainfactory import factory
from engineve.gameengine import GameEngine
from engineve.archetypes import characterclass
import utils
import yaml


def _setup_game_engine_actor():
    game_engine = GameEngine()
    game_engine.spawn_actors(characterclass.ClassActor, num=1, team=0)
    game_engine.spawn_actors(characterclass.ClassActor, num=1, team=1)
    actor_id = [actor_id for actor_id in game_engine.game_state.actors.keys()][0]
    # game_engine.engine_state = CombatState(all_ids)
    # game_engine.game_state.combat = Combat(all_ids)
    return game_engine, actor_id


def test_effect_application():
    engine, actor_id = _setup_game_engine_actor()
    characterclass.Fighter.add_level_to_actor(
        actor_id=actor_id, level=1, state=engine.game_state, invoker=engine.invoker
    )

    assert 0 < len(engine.game_state.actors[actor_id].effects)
    # assert is_good
    # return is_good


def test_applied_effect():
    engine, actor_id = _setup_game_engine_actor()
    characterclass.Fighter.add_level_to_actor(
        actor_id=actor_id, level=1, state=engine.game_state, invoker=engine.invoker
    )
    # add attack command from the ai to the stack


def test_applied_feature():
    """this test should DOSOMETHING"""
    # TODO
    engine, actor_id = _setup_game_engine_actor()
    characterclass.Fighter.add_level_to_actor(
        actor_id=actor_id, level=1, state=engine.game_state, invoker=engine.invoker
    )


def test_load_spawn_fighter():
    """this test should show that a fighter can be loaded from yaml and"""
    # TODO
    game_engine = utils.new_game_engine()

    game_engine.load_character("solaire")
    # assert is fighter


# def test_applied_new_game_move():
#     """this test should add a game_move to a character"""
#     # TODO
#     is_good = False
#     assert is_good


# def test_applied_new_game_move_resource():
#     """this test should add a resource to a character, it should know when it will recharge?"""
#     # TODO
#     is_good = False
#     assert is_good


# def test_rogue_sneak_attack():
#     # make a rogue
#     # verify hit dice size
#     # verify things
#     # TODO
#     is_good = False
#     assert is_good


# def test_save_fighter():
#     """this test should be able to save and save over a fighter that we loaded and modified"""
#     is_good = False
#     assert is_good


# def test_class_add_level():
#     is_good = False
#     assert is_good

# def test_create_player_character():
#     is_good = False
#     assert is_good
