import includes
import logging
from engineve.enginecommands.command import Command
from engineve.enginecommands.compositecommand import CompositeCommand
from engineve.factory import factory
from engineve.gamestatemanager import GameStateManager
from engineve.enginecommands.attackcommand import AttackCommand
from engineve.actorai.basicai import BasicAI


def test_initialize():
    client = factory()
    client.main()
    
def test_attack_command():
    state = GameStateManager.instantiate()
    first_id = list(state.actors.values())[0].id
    target_id = BasicAI.get_target(state=state, attacker_id=first_id)
    new_command = AttackCommand(attacker_id=first_id, target_id=target_id)
    new_command.execute(state=state)

def test_reation_command():
    """ test reactable actions
    make a state with combatants A and B
    B can react to an attack that misses or hits or somehting
    A attacks B
    B attacks A with its reaction
    reaction occurs before effects of triggering attack

    TODO:
    observer pattern
    tags
    pytest stubs?

    """
    # verify reaction Attack happens
    return