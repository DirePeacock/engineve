import functools
import includes

# from engineve import utils as engineve_utils


class effect_decorator(object):
    def __init__(self, func):
        self.func = func


id_counter = 0


def get_id():
    global id_counter
    id_counter += 1
    return id_counter


class Thing(object):
    def __init__(self, children=None, *args, **kwargs):
        self.children = {} if children is None else children
        self.id = get_id()
        self.tags = {}

    def __str__(self):
        return str({"id": self.id, "children": {key: child.__str__() for key, child in self.children.items()}})


from itertools import chain


def recursive_walk(node, tabs=0):
    print(type(node).__name__)
    if isinstance(node, Thing):
        yield node
        for child in node.children.values():
            for i in recursive_walk(child, tabs=tabs + 1):
                yield i
    elif isinstance(node, list):
        for child in node:
            for i in recursive_walk(child, tabs=tabs + 1):
                yield i

    # as_list = node.children if hasattr(node, "children") else node
    # if 1 < len(as_list):
    #     print(type(node).__name__)
    #     for i in recursive_walk(node[1:], tabs=tabs + 1):
    #         yield i
    #     else:
    #         yield node[0]

    # else:
    #     yield node[0]


def do_main():
    thing_a = Thing(children={"B": Thing(), "C": Thing()})

    thing_d = Thing(children={"E": Thing(children={"F": Thing()})})

    stack = [thing_a, thing_d]
    # for thing in stack:
    #     print(thing)
    for node in recursive_walk(stack):
        print(f"id:{node.id}")
        print(f"id:{node.tags}")
        if node.id == 2:
            node.tags = {"ayy": "lmao"}

    for node in recursive_walk(stack):
        print(f"id:{node.id}")
        print(f"id:{node.tags}")


# def test_bruh():
#     do_main()


if __name__ == "__main__":
    do_main()
    # print(list(chain(node.children for node in stack)))
    # deletion of things to see what is shared between places
    # obj_b = thing()
    # obj_a = thing()
    # mylist = [obj_a, obj_b]
    # mydict = {"a": mylist[0], "b": obj_b}

    # print(f"mylist = {mylist}")
    # print(f"mydict = {mydict}")

    # print("\ndel dict['a']\n")
    # print("\ndel list[1]\n")
    # print("\ndel list\n")
    # # del obj_a  # still in lists
    # del mydict["a"]
    # del mylist[0]

    # print(f"mylist = {mylist}")
    # print(f"mydict = {mydict}")
    # print(obj_a)
