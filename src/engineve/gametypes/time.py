import datetime
import math


class GameTime(datetime.datetime):
    """use all the built in things of a datetime object with a seconds property
    which is just 6s rounded down if needed.

    This will probably work alright for my cases, with little effort and all the existing utils.
    """

    @property
    def round(self):
        return math.floor(self.second / 6)

    @round.setter
    def round(self, value):
        self.second = value * 6

    def serialize(self):
        return self.strftime("%d/%m/%y %H:%M:%S")

    # def __sub__(self, *args, **kwargs):
    #     return GameTimeDelta(super().__sub__(*args, **kwargs))

    # def __add__(self, other):
    #     return GameTime(super().__add__(other))


def roundsdelta(rounds):
    return datetime.timedelta(seconds=rounds * 6)


class GameTimeDelta(datetime.timedelta):
    # TODO UGH why is this so hard, it probably isn't worth it
    # delete i guess?
    kws_for_parent = ["days", "seconds", "microseconds"]

    def __new__(self, *args, **kwargs):
        if "rounds" in kwargs.keys():
            if isinstance(kwargs["rounds"], datetime.timedelta):
                return super().__new__(self, *args, **kwargs)

            elif not isinstance(kwargs["rounds"], (datetime.datetime)):
                kwargs["seconds"] = kwargs["rounds"] * 6
        return super().__new__(self, *args, **{kw: arg for kw, arg in kwargs.items() if kw in self.kws_for_parent})

        # new_obj = super().__new__(cls)
        # if rounds is not None:
        #     new_obj.seconds = rounds * 6

        # return new_obj

        # def __init__(self, rounds=None, *args, **kwargs):
        # if rounds is not None:
        #     kwargs["seconds"] = rounds * 6
        # super().__init__(*args, **{kw: arg for kw, arg in kwargs.items() if kw in self.kws_for_parent})

    @property
    def rounds(self):
        return math.floor(self.seconds / 6)

    @rounds.setter
    def rounds(self, value):
        self.seconds = value * 6
