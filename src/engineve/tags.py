import yaml
import pathlib
from enum import IntEnum, auto

tags_path = pathlib.Path(__file__).parent / 'config' / 'tags.yaml'
TAGS = None

with open(tags_path, 'r') as tags_file:
    _tags = yaml.safe_load(tags_file)
    TAGS = IntEnum('TAGS', {thing: auto() for thing in _tags['data']})

class meta(dict):
    pass

class TaggedClass():
    def __init__(self, tags=None):
        self.tags = tags if tags is not None else {}
    def add_tag(self, tag):
        '''Note Bene: if you pass strings that often and check str in keys, it defeats the puropose of less str comparisons'''
        if isinstance(tag, TAGS):
            self.tags[tag] = None
        elif isinstance(tag, str):
            self.tags[TAGS._member_map_[tag]] = None
        else:
            print('RIP')
        # if tag in TAGS:
        #     self.tags[tag] = None
    
    
