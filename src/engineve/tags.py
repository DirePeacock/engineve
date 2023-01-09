import yaml
import pathlib
from enum import IntEnum, auto
import logging
from .config.tags_list import tags_list

TAGS = IntEnum("TAGS", {thing: auto() for thing in tags_list})
    
class meta(dict):
    """indexable by str"""

    pass


class TaggedClass:
    def __init__(self, tags=None, *args, **kwargs):
        self.tags = tags if tags is not None else {}

    def add_tag(self, tag, value=None):
        """Note Bene: if you pass strings that often and check str in keys, it defeats the puropose of less str comparisons"""
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
            print("RIP")

        # if tag in TAGS:
        #     self.tags[tag] = None


def tag(string):
    return TAGS._member_map_[string]


def check_tag(obj, tag, value=None):
    """args: object, tag, value
    # TODO rename to check_tag
    """
    key = tag if not isinstance(tag, str) else TAGS._member_map_[tag]
    tag_dict = {}

    if isinstance(obj, TaggedClass):
        tag_dict = obj.tags
    elif isinstance(obj, dict):
        tag_dict = obj

    retval = key in tag_dict.keys()
    if value is not None:
        retval = retval and tag_dict[key] == value

    return retval


def check_tags(*args, **kwargs):
    logging.debug("pls use check_tag")
    return check_tag(*args, **kwargs)


def check_tags_all(obj, tags):
    """checks that the object has all the tags listed
    either give values for all of them or none of them
    """
    if isinstance(tags, dict):

        # are all values in obj's tags
        has_all_tags = all([check_tag(obj, tag) for tag in tags.keys()])
        if not has_all_tags:
            return False

        # are all values equal
        for key, value in tags.items():
            # tag_key = key if isinstance(key, TAGS) else tag(key)
            if not check_tag(obj, key, value):
                return False

        # all tags are present in both dicts and all values are equal
        return True

    else:
        return all([check_tags(obj, tag) for tag in tags])


# def str_to_tag(tag):
#     return TAGS._member_map_[t] if not isinstance(t, str) else t
# def check_tags(obj, tag, use_any=False):
#     tags_list = [tag] if not isinstance(tag, list) else [str_to_tag(t) for t in tag]
#     return all()
if __name__ == "__main__":
    print("ayy lmao")