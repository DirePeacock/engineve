import includes
from unittest.mock import Mock

from utils import setup_game_engine, actor_put_command

from engineve.archetypes import characterclass
from engineve.enginecommands.effectcommands.applyeffect import ApplyEffect
from engineve.archetypes.effect import Effect
from engineve.archetypes.effects.effects import Dodge
from engineve.utils import get_tag_enum
from engineve.tags import check_tags, check_tags_all, TaggedClass
from engineve.gametypes.time import roundsdelta

mock = Mock()


def test_dodge_tag_notification():
    class TestDodge(Dodge):
        # TODO make this a decorator, probly will be useful
        _called_check_applicable = False

        def check_applicable(self, *args, **kwargs):
            super().check_applicable(*args, **kwargs)
            self._called_check_applicable = True

    engine, id_a, id_b = setup_game_engine()
    engine.engine_state.start_combat(engine.game_state, engine.invoker)
    atk_cmd_id = actor_put_command(engine, id_a, cmd_substring="attack")
    dodge_effect_obj = TestDodge(duration=1, parent_id=id_b)
    engine.invoker.register_observer(dodge_effect_obj)
    engine.invoker.periodic(engine.game_state)
    assert dodge_effect_obj._called_check_applicable


def test_effect_adds_tag_to_trigger_cmd():
    engine, id_a, id_b = setup_game_engine()
    engine.engine_state.start_combat(engine.game_state, engine.invoker)
    atk_cmd_id = actor_put_command(engine, id_a, cmd_substring="attack")
    dodge_effect_obj = Dodge(duration=1, parent_id=id_b)
    engine.invoker.register_observer(dodge_effect_obj)
    # this will actually  be on the child attack roll itself but do this to test ofc
    engine.invoker.command_stack[0].add_tag("attack")
    assert not check_tags(engine.invoker.command_stack[0], "disadvantage")
    engine.invoker.notify(meta=engine.invoker.command_stack[0].tags, state=engine.game_state, invoker=engine.invoker)
    assert check_tags(engine.invoker.command_stack[0], "disadvantage")


def test_apply_effect_command():
    engine, id_a, id_b = setup_game_engine()
    engine.engine_state.start_combat(engine.game_state, engine.invoker)
    dodge_effect_obj = Dodge(duration=1, parent_id=id_b)
    apply_effect_cmd_obj = ApplyEffect(effect=dodge_effect_obj, parent_id=id_a, duration=1)
    engine.invoker.put(apply_effect_cmd_obj)
    engine.invoker.periodic(engine.game_state)
    assert any(
        effect_id for effect_id in engine.game_state.actors[id_a].effects.keys() if effect_id == dodge_effect_obj.id
    )


def test_effect_notified():
    engine, id_a, id_b = setup_game_engine()
    engine.engine_state.start_combat(engine.game_state, engine.invoker)
    dodge_effect_obj = Dodge(duration=1, parent_id=id_b)
    apply_effect_cmd_obj = ApplyEffect(effect=dodge_effect_obj, parent_id=id_b, duration=1)
    engine.invoker.put(apply_effect_cmd_obj)
    engine.invoker.periodic(engine.game_state)
    # Actor id_a should have the effect on it
    atk_cmd_id = actor_put_command(engine, id_a, cmd_substring="attack")
    assert not check_tags(engine.invoker.command_stack[0].children["attack_roll"], "disadvantage")
    engine.invoker.notify(
        meta=engine.invoker.command_stack[0].children["attack_roll"].tags,
        state=engine.game_state,
        invoker=engine.invoker,
    )
    # attack roll should now have disadvantage to it
    assert check_tags(engine.invoker.command_stack[0].children["attack_roll"], "disadvantage")


def test_effect_duration():
    engine, id_a, id_b = setup_game_engine()
    engine.engine_state.start_combat(engine.game_state, engine.invoker)
    dodge_effect_obj_a = Dodge(duration=1, parent_id=id_b)
    dodge_effect_obj_global = Dodge(duration=1)
    apply_effect_cmd_obj = ApplyEffect(effect=dodge_effect_obj_a, parent_id=id_b, duration=1)
    engine.invoker.put(apply_effect_cmd_obj)
    engine.invoker.periodic(engine.game_state)
    # Actor id_a should have the effect on it
    dummy_notification = TaggedClass()
    dummy_notification.add_tag("gametime_update", engine.game_state.time + roundsdelta(1))
    engine.invoker.notify(dummy_notification.tags, engine.game_state, engine.invoker)
    assert 1 > len(engine.game_state.actors[id_b].effects)
    assert 1 > len(engine.game_state.global_effects)
    assert not any(obs for obs in engine.invoker.observers if isinstance(obs, Effect))
