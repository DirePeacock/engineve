import includes
from engineve.tags import TaggedClass, TAGS

def test_add_tag():
    t = TaggedClass()
    t.add_tag('attack')
    assert 0<len(t.tags)
    assert isinstance(list(t.tags.keys())[0], TAGS)
