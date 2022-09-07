import includes
import logging
from unittest.mock import Mock

from utils import setup_game_engine

from engineve.enginecommands.basecommands.command import Command
from engineve.enginecommands.basecommands.compositecommand import CompositeCommand
from engineve.mainfactory import factory
from engineve.tags import check_tag, TAGS
from engineve.gamestatemanager import GameStateManager
from engineve.enginecommands.gamecommands.attackcommand import AttackCommand
from engineve.enginecommands.gamecommands.damagerollcommand import DamageRollCommand
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


def test_crit_damage():
    """test to verify dice are doubled on a crit, 1d1+x should become 2d1+x"""
    engine, id_a, id_b = setup_game_engine()
    dice = "1d1"
    expected_roll_val = 2
    dmg_roll_cmd = DamageRollCommand(id_a, id_b, tags={TAGS["critical_hit"]: None}, dmg_dice="1d1", stat="str")
    dmg_roll_cmd.evaluate(engine.game_state, engine.invoker)
    dmg_total = dmg_roll_cmd.tags[TAGS["damage"]]
    actual_roll_val = dmg_total - dmg_roll_cmd.get_total_flat_modifier()

    assert "CRIT" in dmg_roll_cmd.log
    assert actual_roll_val == expected_roll_val
