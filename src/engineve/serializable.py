import re
import logging
import datetime

"""
def rec_to_dict(obj)


def serialize(self):
"""

blacklist_re = re.compile("^_")


def _is_serializable_type(obj):
    """todo try and put own type in the isinstance tuple"""
    return isinstance(obj, (int, float, str, dict, list)) or hasattr(obj, "serialize")


def rec_to_dict(obj):
    retval = {}

    if not hasattr(obj, "__dict__"):
        return obj
    # elif hasattr(obj, "serialize"):
    #     return obj.serialize()

    for attrname, attr in obj.__dict__.items():
        if attrname == "game_moves":
            # print("fk")
            continue

        if blacklist_re.search(attrname) is not None or callable(attr):
            continue

        if hasattr(attr, "serialize"):
            retval[attrname] = attr.serialize()
        elif isinstance(attr, dict):
            retval[attrname] = {
                key: rec_to_dict(val)
                if not hasattr(val, "serialize")
                else val.serialize()
                for key, val in attr.items()
            }
        elif isinstance(attr, list):
            retval[attrname] = [
                rec_to_dict(val) if not hasattr(val, "serialize") else val.serialize()
                for val in attr
            ]
        elif isinstance(attr, (int, float, str)):
            retval[attrname] = attr
        else:
            pass  # retval[attrname] = f"T:{type(attr).__name__} obj (not_serializable)"
    return retval


class Serializable:
    # serializable_attrs = []
    # return None if you dont want to serialize it

    def _init_serializable_attrs(self, **kwargs):
        # TODO  may not be needed idk if we ever use this over kwargs or something
        for key, value in kwargs.items():
            if key in self.serializable_attrs:
                setattr(self, key, value)

    @classmethod
    def load_dict(cls, data):
        return cls(**data)

    def serialize(self):
        """call the recursive to dict method on self.
        leave room for something that may not be serializable to be serialized in a special way"""
        try:
            retval = rec_to_dict(self)

            # this is where you may want to do more stuff....

            # return the thing
            return retval
        except Exception as e:
            logging.debug("ohno")
            raise e

    @property
    def serializable_attrs(self):
        return [
            key
            for key, val in self.__dict__.items()
            if self.blacklist_re.search(key) is None
            and not callable(val)
            and _is_serializable_type(val)  #  or hasattr(val, "serialize")
        ]

    # def to_dict(self):
    #     retval = {}
    #     for attrname in self.serializable_attrs:
    #         attr = getattr(self, attrname)
    #         # attr is the str ffk
    #         # logging.debug(attr)
    #         if hasattr(attr, "serialize"):
    #             retval[attrname] = attr.serialize()
    #         elif isinstance(attr, dict):
    #             retval[attrname] = {key: to_dict(val) for key, val in attr.items()}
    #         elif isinstance(attr, list):
    #             retval[attrname] = [to_dict(val) for val in attr]
    #         elif "Actor" in type(attr).__name__:
    #             retval[attrname] = attr
    #         else:
    #             retval[attrname] = attr
    #     return retval
