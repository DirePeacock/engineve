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


def test_crit_damage():
    """test to verify dice are doubled on a crit, 1d1+x should become 2d1+x"""
    engine, id_a, id_b = setup_game_engine()
    dice = "1d1"
    expected_roll_val = 2
    dmg_roll_cmd = DamageRollCommand(id_a, id_b, tags={TAGS["critical_hit"]: None}, dmg_dice=dice, stat="str")
    dmg_roll_cmd.evaluate(engine.game_state, engine.invoker)
    dmg_total = dmg_roll_cmd.tags[TAGS["damage"]]
    actual_roll_val = dmg_total - dmg_roll_cmd.get_total_flat_modifier()

    assert f"{dice}+{dice}" in dmg_roll_cmd.log
    assert actual_roll_val == expected_roll_val


def test_critical_attack_log():
    engine, id_a, id_b = setup_game_engine()
    dice = "1d1"
    expected_roll_val = 2
    atk_cmd = AttackCommand(id_a, id_b, tags={TAGS["critical_hit"]: None}, dmg_dice=dice, stat="str")
    atk_cmd.children["attack_roll"].add_tag(TAGS["critical_hit"])
    atk_cmd.children["attack_roll"].value = True
    atk_cmd._evaluate_damage_roll(engine.game_state, engine.invoker)
    logging.debug(f"atk_log = {atk_cmd.log}")
    assert check_tag(atk_cmd.tags, TAGS["critical_hit"])
    assert check_tag(atk_cmd.children["attack_roll"], TAGS["critical_hit"])
    assert check_tag(atk_cmd.children["damage_roll"], TAGS["critical_hit"])
    assert f"{dice}+{dice}" in atk_cmd.log


def test_attack_kill_detection():
    engine, id_a, id_b = setup_game_engine()
    # set 2 actors health and AC to zero so they will always die
    for i in (id_a, id_b):
        engine.game_state.actors[i].hp = 1
        engine.game_state.actors[i].ac = 0

    atk_cmd = AttackCommand(id_a, id_b, tags={TAGS["critical_hit"]: None}, dmg_dice="1d1", stat="str")
    atk_cmd.execute(engine.game_state, engine.invoker)
    assert check_tag(atk_cmd.tags, TAGS["death"])
    logging.debug(f"atk_cmd_keys = {atk_cmd.tags.keys()}")
