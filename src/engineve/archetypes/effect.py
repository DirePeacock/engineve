import logging
from ..enginecommands.observer.observer import Observer
from ..tags import TaggedClass, tag, check_tag, check_tags_all
from ..utils import yield_command_with_id, get_id

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

    def __init__(self, parent_id=None, duration=None, start_time=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = get_id()
        self.name = type(self).__name__
        self.duration = duration
        self.parent_id = parent_id
        self.start_time = start_time

    # @classmethod
    # def apply_effect(cls, *args, **kwargs):

    #     logging.debug("we did it!!!!!!!!!!!")
    #     pass


class ConditionalBonus(Effect):
    def __init__(self, parent_id, tag=None, duration=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def check_applicable(self, meta, state=None, invoker=None):
        return False

    def apply_modifier(self, meta, state=None, invoker=None):
        pass


EFFECTS = {}


# fighting_style_dueling = Effect(
#     value_func=(lambda x: 2),
#     applicable_func=(lambda tags: (check_tag(tags, "one_handed") and not check_tag(tags, "dual_wielding"))),
#     duration=0,
# )
# dodge_action = Effect()
