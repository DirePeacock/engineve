import includes
from unittest.mock import Mock

from utils import setup_game_engine, actor_put_command

from engineve.archetypes import characterclass
from engineve.archetypes.effect import Effect, Dodge
from engineve.utils import get_tag_enum
from engineve.tags import check_tags, check_tags_all

mock = Mock()
# test_fighting_style_dueling = Effect(
#     value_func=(lambda x: 2),
#     applicable_func=(
#         lambda tagz: (
#             check_tags_all(tagz, ["one_handed", "melee_attack", "weapon_attack"])
#             and not check_tags(tagz, "dual_wielding")
#         )
#     ),
#     duration=0,
# )

# input_tags = {get_tag_enum("one_handed"): None, get_tag_enum("melee_attack"): None, get_tag_enum("weapon_attack"): None}


def test_effect_checking():
    # is_good = test_fighting_style_dueling.is_applicable(tags=input_tags)

    # assert is_good
    is_good = False
    assert is_good


def test_effect_apply_to_thing():
    # is_good = 2 == test_fighting_style_dueling.get_value(input_tags)
    # assert is_good
    is_good = False
    assert is_good


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
    assert not check_tags(engine.invoker.command_stack[0], "disadvantage")
    engine.invoker.notify(meta=engine.invoker.command_stack[0].tags, state=engine.game_state, invoker=engine.invoker)
    assert check_tags(engine.invoker.command_stack[0], "disadvantage")


def test_effect_duration():
    pass
