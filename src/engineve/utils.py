import random
import uuid
import math
from .tags import TAGS, check_tag
from collections.abc import Iterable
from .enginecommands.basecommands.abstractcommand import AbstractCommand
import dice


def roll_func(string):
    return sum(dice.roll(string))


def roll_size(size=20):
    return random.randint(1, size)


def roll_range(range_tuple):
    return random.randint(*range_tuple)


def roll(*args, **kwargs):
    # TODO lwo prio probably dont want a switch here if possible idk if it matters that much
    for arg in args:
        if isinstance(arg, int):
            return roll_size(arg)
        elif isinstance(arg, tuple):
            return roll_range(arg)
        else:
            return roll_func(arg)

    for arg in kwargs.values():
        if isinstance(arg, int):
            return roll_size(arg)
        elif isinstance(arg, tuple):
            return roll_range(arg)
        else:
            return roll_func(arg)


def get_id():
    return uuid.uuid4().int


def equals_or_in(obj, obj_or_iter):
    """we may want to have this for tag checking reasons"""
    if isinstance(obj_or_iter, Iterable):
        return obj in obj_or_iter
    else:
        return obj == obj_or_iter


def get_random_coords(x_range=None, y_range=None) -> tuple:
    "given a range of"
    min_x, max_x = x_range if x_range is not None else (0, 9)
    min_y, max_y = y_range if y_range is not None else (0, 9)
    return (random.randint(min_x, max_x), random.randint(min_y, max_y))


def percent_rounding(num: float):
    """takes the remaining percent and rounds it up or down
    rounding chance is equal to the remaining percent
    """
    if random.random() < num % 1:
        return math.ceil(num)
    else:
        return math.floor(num)


rando = 1


def get_rando():
    global rando
    rv = rando
    rando += 1
    return rv


def command_stack_df_traversal(node):
    """needs to walk through these list of nodes"""
    if isinstance(node, AbstractCommand):
        yield node
        if hasattr(node, "children"):
            for child in node.children.values():
                for i in command_stack_df_traversal(child):
                    yield i
    elif isinstance(node, list):
        for child in node:
            for i in command_stack_df_traversal(child):
                yield i


def yield_command_with_id(id, invoker):
    """the same as the the one above but only look yield the thing(s) with the id in the args"""
    for command in command_stack_df_traversal(invoker.command_stack):
        if command.id == id:
            yield command
            break


def get_tag_enum(string):
    return TAGS._member_map_[string]


def get_stat_modifier(stat):
    return math.floor((float(stat) - 10.0) / 2.0)


def calculate_advantage(tags):
    """return pos if advantage 0 for none and neg for disadvantage"""
    advantage = check_tag(tags, "advantage")
    disadvantage = check_tag(tags, "disadvantage")

    # just use the simple math like the base game
    if advantage and disadvantage or (not advantage and not disadvantage):
        return 0
    elif advantage:
        return 1
    else:
        return -1


name_table = [
    "arthur",
    "blaidd",
    "charlemange",
    "diocles",
    "elwing",
    "falcor",
    "gawain",
    "hadrian",
    "iori",
    "jamis",
    "kelvin",
    "llewelyn",
    "malice",
    "nostradamus",
    "ophelia",
    "phelia",
    "quattro",
    "roderick",
    "stefan",
    "theodocian",
    "ullamon",
    "valter",
    "wolfgard",
    "xyna",
    "yorick",
    "zezima",
]

used_names = []


def get_random_name():
    global name_table
    global used_names
    new_name = name_table[random.randint(0, len(name_table) - 1)]
    used_names.append(new_name)
    name_table.remove(new_name)
    if 0 == len(name_table):
        name_table = used_names
        used_names = []
    return new_name


def get_kwarg(string, kwargs, default=None):
    return kwargs[string] if string in kwargs.keys() else default
