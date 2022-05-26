import includes
import logging

from engineve.gametypes.actor import Actor

dummy_data = {
    'name': 'test_actor',
    'team': 1
}

def test_save():
    test_str = 'load_this'
    new_actor = Actor(name='load_this')
    
    init_test = test_str == new_actor.name
    save_test = new_actor.name == new_actor.to_dict()['name']

    assert init_test
    assert save_test

def test_load():
    new_actor = Actor.load_dict(dummy_data)
    assert new_actor.name == dummy_data['name']