import yaml
import pathlib
from enum import IntEnum, auto

tags_path = pathlib.Path(__file__).parent / 'config' / 'tags.yaml'
TAGS = None

with open(tags_path, 'r') as tags_file:
    _tags = yaml.safe_load(tags_file)
    TAGS = IntEnum('TAGS', {thing: auto() for thing in _tags['data']})

class TaggedClass():
    def __init__(self, tags=None):
        self.tags = tags if tags is not None else []
    
    
class meta(dict):
    pass