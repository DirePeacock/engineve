import includes

from engineve.enginestates.combatstate import CombatState
from engineve.gametypes.combat import Combat
from engineve.factory import factory



def _setup_game_engine():
    game_engine = factory(spawn=True)
    all_ids = [actor_id for actor_id in game_engine.game_state.actors.keys()]
    game_engine.engine_state = CombatState(all_ids)
    game_engine.game_state.combat = Combat(all_ids)
    return game_engine

def test_roll_init():
    '''update state & obsvrs that initiative has been rolled'''
    game_engine = _setup_game_engine()
    game_engine.engine_state.roll_inits(game_engine.game_state, game_engine.invoker)

def test_transition_to_combat():
    pass

def test_start_combat():
    '''notifies observers that comabt is over'''
    pass

def test_actor_take_turn():
    '''update state & obsvrs that initiative has been rolled'''
    pass

def test_next_turn():
    '''update state & obsvrs that we are on the next turn, whos turn it is has changed'''
    pass

def test_next_round():
    '''update state & obsvrs that we are on the next round'''
    pass

def test_end_combat():
    '''notifies observers that comabt is over'''
    pass
