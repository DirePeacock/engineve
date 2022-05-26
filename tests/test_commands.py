import includes
import logging
from engineve.enginecommands.basecommands.command import Command
from engineve.enginecommands.basecommands.compositecommand import CompositeCommand
from engineve.factory import factory
from engineve.gamestatemanager import GameStateManager
from engineve.enginecommands.gamecommands.attackcommand import AttackCommand
from engineve.actorai.basicai import BasicAI
from engineve.gametypes.actor import Actor

def test_initialize():
    client = factory()
    # client.main()
    
def test_attack_command():
    engine = factory()
    for team_id in [0, 1]:
        engine.spawn_actors(actor_class=Actor, num=1, team=team_id)
    first_id = list(engine.game_state.actors.values())[0].id
    target_id = BasicAI.get_target(state=engine.game_state, attacker_id=first_id)
    
    new_command = AttackCommand(attacker_id=first_id, target_id=target_id)
    new_command.execute(state=engine.game_state)

def _test_get_command():
    state = GameStateManager.instantiate()
    first_id = list(state.actors.values())[0].id
    target_id = BasicAI.get_target(state=state, attacker_id=first_id)
    
    return