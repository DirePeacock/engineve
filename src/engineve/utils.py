import random
import uuid
import math
from .tags import TAGS

def roll(size=20):
    return random.randint(1, size)

def get_id():
    return uuid.uuid4().int

rando = 1
def get_rando():
    global rando
    rv = rando
    rando += 1
    return rv
def get_tag_enum(string):
    return TAGS._member_map_[string]

def get_stat_modifier(stat):
    return math.floor((float(stat) - 10.0) / 2.0)


name_table = ['arthur', 'bartholemew', 'charlemange', 'diocles', 'elwing', 'falcor', 'gawain', 'hadrian', 'iori', 'jamis', 
'kelvin', 'llewelyn', 'malice', 'nostradamus', 'ophelia', 'phelia', 'quattro', 'roderick', 'stefan', 'theodocian',  
'ullamon', 'valter', 'wolfgard', 'xyna', 'yorick', 'zezima']
used_names = []
def get_random_name():
    global name_table
    global used_names
    new_name = name_table[random.randint(0, len(name_table)-1)]
    used_names.append(new_name)
    name_table.remove(new_name)
    if 0 == len(name_table):
        name_table = used_names
        used_names = []
    return new_name

