import random

rando = 1
def get_rando():
    global rando
    rv = rando
    rando += 1
    return rv

name_table = ['arthur', 'bartholemew', 'charlemange', 'diocles', 'elwing', 'falcor', 'gawain', 'hadrian', 'iori', 'jamis', 
'kelvin', 'llewelyn', 'malice', 'nostradamus', 'ophelia', 'phelia', 'quattro', 'roderick', 'stefan', 'theodocian',  
'ullamon', 'valter', 'wolfgard', 'xxx', 'yorick', 'zezima']
def get_random_name():
    name_table[random.randint(0, len(name_table))]

