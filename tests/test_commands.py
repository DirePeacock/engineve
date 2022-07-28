import includes
import logging
from unittest.mock import Mock

from utils import setup_game_engine

from engineve.enginecommands.basecommands.command import Command
from engineve.enginecommands.basecommands.compositecommand import CompositeCommand
from engineve.mainfactory import factory
from engineve.gamestatemanager import GameStateManager
from engineve.enginecommands.gamecommands.attackcommand import AttackCommand
from engineve.actorai.basicai import BasicAI
from engineve.actorai.aiutils import get_target
from engineve.gametypes.actor import Actor


def test_initialize():
    client = factory()
    # client.main()


def test_attack_command():
    engine = factory()
    for team_id in [0, 1]:
        engine.spawn_actors(actor_class=Actor, num=1, team=team_id)
    first_id = list(engine.game_state.actors.values())[0].id
    target_id = get_target(attacker_id=first_id, state=engine.game_state)

    new_command = AttackCommand(attacker_id=first_id, target_id=target_id)
    new_command.execute(state=engine.game_state, invoker=engine.invoker)


def test_attack_command_log():
    engine = factory()

    for team_id in [0, 1]:
        engine.spawn_actors(actor_class=Actor, num=1, team=team_id)
    first_id = list(engine.game_state.actors.values())[0].id
    target_id = get_target(attacker_id=first_id, state=engine.game_state)
    dummy_str = "declaration!"
    new_command = AttackCommand(attacker_id=first_id, target_id=target_id, log=dummy_str)
    assert new_command.log == dummy_str
    new_command.execute(state=engine.game_state, invoker=engine.invoker)
    assert new_command.log != dummy_str


def test_commands_call_notify():
    """commands should all call notify weather by default or internally"""
    is_good = False
    engine, first_id, target_id = setup_game_engine()

    command_core = Command()
    dummy_str = "declaration!"
    custom_notification_command = AttackCommand(attacker_id=first_id, target_id=target_id, log=dummy_str)
    assert is_good
