import yaml
import pathlib
from enum import IntEnum, auto

tags_path = pathlib.Path(__file__).parent / 'config' / 'tags.yaml'
TAGS = None

with open(tags_path, 'r') as tags_file:
    _tags = yaml.safe_load(tags_file)
    TAGS = IntEnum('TAGS', {thing: auto() for thing in _tags['data']})

class meta(dict):
    """indexable by str
    """
    pass

class TaggedClass:
    def __init__(self, tags=None, *args, **kwargs):
        self.tags = tags if tags is not None else {}
    def add_tag(self, tag, value=None):
        '''Note Bene: if you pass strings that often and check str in keys, it defeats the puropose of less str comparisons'''
        # TODO tag trees for things  with value
        if isinstance(tag, TAGS):
            self.tags[tag] = value
        elif isinstance(tag, dict):
            for key, val in tag.items():
                if isinstance(tag, str):   
                    self.tags[TAGS._member_map_[key]] = val
                else:
                    self.tags[key] = val
        elif isinstance(tag, str):
            self.tags[TAGS._member_map_[tag]] = value
        else:
            print('RIP')

        # if tag in TAGS:
        #     self.tags[tag] = None
def tag(string):
    return TAGS._member_map_[string]


def check_tags(obj, tag):
    key = tag if not isinstance(tag, str) else TAGS._member_map_[tag]
    if isinstance(obj, TaggedClass):
        return key in obj.tags
    elif isinstance(obj, dict):
        return key in obj.keys()

def check_tags_all(obj, tags):
    return all([check_tags(obj, tag) for tag in tags])

# def str_to_tag(tag):
#     return TAGS._member_map_[t] if not isinstance(t, str) else t
# def check_tags(obj, tag, use_any=False):
#     tags_list = [tag] if not isinstance(tag, list) else [str_to_tag(t) for t in tag]
#     return all()