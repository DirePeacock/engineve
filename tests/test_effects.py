import includes
from unittest.mock import Mock

from engineve.archetypes import characterclass
from engineve.archetypes.characterclass import Effect
from engineve.utils import get_tag_enum
from engineve.tags import check_tags, check_tags_all

mock = Mock()
test_fighting_style_dueling = Effect(value_func=(lambda x: 2),
                                     applicable_func=(lambda tagz: (check_tags_all(tagz, ['one_handed','melee_attack','weapon_attack']) and not check_tags(tagz, 'dual_wielding'))),
                                     duration=0)

input_tags = {get_tag_enum('one_handed'): None,
              get_tag_enum('melee_attack'): None,
              get_tag_enum('weapon_attack'): None}

def test_effect_checking():
    is_good = test_fighting_style_dueling.is_applicable(tags=input_tags)

    assert is_good

def test_effect_get_value():
    is_good = 2 == test_fighting_style_dueling.get_value(input_tags)
    assert is_good

def test_duration():
    is_good = False
    assert is_good