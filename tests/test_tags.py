import includes
from engineve.tags import TaggedClass, TAGS, check_tags, tag

def test_add_tag():
    t = TaggedClass()
    expected_vals = [123]
    t.add_tag('attack')
    t.add_tag('actor_ids', expected_vals)
    
    assert 2 == len(t.tags)
    assert isinstance(list(t.tags.keys())[0], TAGS)
    assert check_tags(t, 'actor_ids')
    assert t.tags[tag('actor_ids')] == expected_vals
