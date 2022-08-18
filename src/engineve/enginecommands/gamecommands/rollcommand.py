from ..basecommands.command import Command


class RollCommand(Command):
    """this class knows that its got modifiers or stuff to mess with rolled values

    attacks and most things that evaluate rolled dice deal with modifiers in a similar way so that

    Q should modifiers be child commands of things if they need to be calculated
    """

    def __init__(self, flat_modifiers=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flat_modifiers = {} if flat_modifiers == None else flat_modifiers

    def add_flat_modifier(self, key, value):
        """this may need to check for multiples of the same key typecheck maybe?"""
        self.flat_modifiers[key] = value

    def remove_flat_modifier(self, key):
        """may need to be more logic here or something"""
        if key in self.flat_modifiers.keys():
            del self.flat_modifiers[key]

    def get_total_flat_modifier(self):
        return sum([mod for mod in self.flat_modifiers.values()])


class RollModifier:
    """
    flat additive
    dice number increase

    resistance, aka math.floor(N/2)
    double value

    """

    def apply(self):
        pass
