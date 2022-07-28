import logging
from ..enginecommands.observer.observer import Observer
from ..tags import TaggedClass, tag, check_tag, check_tags_all
from ..utils import yield_command_with_id

# from ..utils import

# to gametypes
class Effect(Observer, TaggedClass):
    """
    i know what to do whan an applicable thing happens to me on the stack
    - probably exists in some kind of list based on the character effect
    - this

    - how would an something like hold person or a DoT like poison work?:
        as an observer that does a damage effect and then checks duration

    - needs to be able to cross reference tags and state
    - might need to be an observer some times - some sort of thing that happens every time a targets turn starts/ends
        Yes
        probly all the time
    - Needs some kind of tag itself to track it being applied already

    Q: Modifiers as a class - as applied to a command that calculates something?
    or
    Q: tags
    """

    def __init__(self, parent_id=None, duration=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.duration = duration
        self.parent_id = parent_id


class ConditionalBonus(Effect):
    def __init__(self, parent_id, tag=None, duration=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def check_applicable(self, meta, state=None, invoker=None):
        return False

    def apply_modifier(self, meta, state=None, invoker=None):
        pass


EFFECTS = {}


class Dodge(Effect):
    def __init__(self, duration=1, *args, **kwargs):
        super().__init__(
            duration=duration, trigger=self.check_applicable, reaction=self.apply_modifier, *args, **kwargs
        )

    def check_applicable(self, meta, state=None, invoker=None):
        tag_vals_to_check = {"target_id": self.parent_id}
        return check_tags_all(meta, tag_vals_to_check) and check_tag(meta, "attack")

    def apply_modifier(self, meta, state=None, invoker=None):
        triggering_cmd_id = meta[tag("command_id")]
        # iterate over stack to get the correct command_id
        # todo how to edit aan obj ina tree
        for command in yield_command_with_id(triggering_cmd_id, invoker):
            command.add_tag("disadvantage")

    @classmethod
    def apply_effect(cls, parent_id, duration=1, state=None):

        logging.debug("we did it!!!!!!!!!!!")
        pass


# fighting_style_dueling = Effect(
#     value_func=(lambda x: 2),
#     applicable_func=(lambda tags: (check_tag(tags, "one_handed") and not check_tag(tags, "dual_wielding"))),
#     duration=0,
# )
# dodge_action = Effect()
