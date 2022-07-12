from engineve.mainfactory import factory
from engineve.archetypes import characterclass

def _setup_game_engine_actor():
    game_engine = factory(spawn=False)
    game_engine.spawn_actors(characterclass.ClassActor, num=1, team=0)
    game_engine.spawn_actors(characterclass.ClassActor, num=1, team=1)
    actor_id = [actor_id for actor_id in game_engine.game_state.actors.keys()][0]
    # game_engine.engine_state = CombatState(all_ids)
    # game_engine.game_state.combat = Combat(all_ids)
    return game_engine, actor_id


def test_effect_application():
    engine, actor_id = _setup_game_engine_actor()
    characterclass.Fighter.add_level_to_actor(actor_id=actor_id,
                                              level=1,
                                              state=engine.game_state,
                                              invoker=engine.invoker)
    
    assert 0 < len(engine.game_state.actors[actor_id].effects)
    # assert is_good
    # return is_good

def test_applied_effect():
    engine, actor_id = _setup_game_engine_actor()
    characterclass.Fighter.add_level_to_actor(actor_id=actor_id,
                                              level=1,
                                              state=engine.game_state,
                                              invoker=engine.invoker)
    # add attack command from the ai to the stack

# def test_class_add_level():
#     is_good = False
#     assert is_good

# def test_create_player_character():
#     is_good = False
#     assert is_good