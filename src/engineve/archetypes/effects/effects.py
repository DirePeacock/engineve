from ..effect import Effect
from ...tags import tag, check_tag, check_tags_all, TAGS
from ...utils import yield_command_with_id


class DuelingFightingStyle(Effect):
    def __init__(self, *args, **kwargs):
        super().__init__(duration=None, trigger=self.check_applicable, reaction=self.apply_modifier, *args, **kwargs)

    def check_applicable(self, meta, state=None, invoker=None):
        retval = check_tags_all(meta, ["one_handed", "melee_attack", "weapon_attack", "damage"])
        retval = retval and not check_tags(meta, "dual_wielding")
        retval = retval and check_tag(meta, "attack")

        tag_vals_to_check = {"target_id": self.parent_id}
        return check_tags_all(meta, tag_vals_to_check) and check_tag(meta, "attack")

    def apply_modifier(self, meta, state=None, invoker=None):
        """add 2dmg to the flat modifier thing"""
        pass


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
        for command in yield_command_with_id(triggering_cmd_id, invoker):
            command.add_tag("disadvantage")


class SneakAttack(Effect):
    def __init__(self, *args, **kwargs):
        super().__init__(duration=None, trigger=self.check_applicable, reaction=self.apply_modifier, *args, **kwargs)

    def check_applicable(self, meta, state=None, invoker=None):
        """check these things,"""
        is_attack = False
        if not is_attack:
            return is_attack

        ranged_or_finesse = False
        if not ranged_or_finesse:
            return ranged_or_finesse

        has_advantage = False
        has_disadvantage = False
        has_adjacent_ally = False
        return not has_disadvantage and has_advantage or has_adjacent_ally

    def apply_modifier(self, meta, state=None, invoker=None):
        triggering_cmd_id = meta[tag("command_id")]
        # iterate over stack to get the correct command_id
        for command in yield_command_with_id(triggering_cmd_id, invoker):
            command.add_tag("disadvantage")
