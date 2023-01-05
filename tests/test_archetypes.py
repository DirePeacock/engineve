import includes
import logging
import yaml
from engineve.archetypes.archetype import load_archetypes, ARCHETYPES, rulebook_dir
from engineve.mainfactory import factory

def test_rulebook_loading():
    assert 0 < len(ARCHETYPES['MonsterArchetypes'])

# def test_monster_loading():
#     '''makes an archetype obj with new'''
#     with open(str(rulebook_dir / 'skeleton.yaml'), 'r') as rb_file:
#         _book = yaml.safe_load(rb_file)
#         for key, val in _book['MonsterArchetypes']['skeleton'].items():
#             logging.debug(f"{key}: {val}")
#             assert getattr(o, name) == val


def test_spawn_skeleton():
    engine = factory(spawn=False)
    mon_arch_name_zero = list(ARCHETYPES['MonsterArchetypes'].keys())[0]
    team_kwarg = 69
    new_actor = ARCHETYPES['MonsterArchetypes'][mon_arch_name_zero].new_actor(team=team_kwarg)
    for key, val in _book['MonsterArchetypes']['skeleton'].items():
        logging.debug(f"{key}: {val}")

        assert getattr(new_actor, key) == val

    assert new_actor.team == team_kwarg

def test_spawn_skeleton():
    engine = factory(spawn=True)
