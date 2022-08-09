from ..effect import Effect
from ...tags import tag, check_tag, check_tags_all
from ...utils import yield_command_with_id


class DuelingFightingStyle(Effect):
    def __init__(self, *args, **kwargs):
        super().__init__(duration=None, trigger=self.check_applicable, reaction=self.apply_modifier, *args, **kwargs)

    def check_applicable(self, meta, state=None, invoker=None):
        retval = check_tags_all(meta, ["one_handed", "melee_attack", "weapon_attack", "damage"])
        retval = retval and not check_tags(tagz, "dual_wielding")
        retval = retval and check_tag(meta, "attack")
        # return check_tags_all(meta, ["one_handed", "melee_attack", "weapon_attack"]) and not check_tags(
        #     tagz, "dual_wielding"
        # )

        tag_vals_to_check = {"target_id": self.parent_id}
        return check_tags_all(meta, tag_vals_to_check) and check_tag(meta, "attack")

    def apply_modifier(self, meta, state=None, invoker=None):
        triggering_cmd_id = meta[tag("command_id")]
        # iterate over stack to get the correct command_id
        for command in yield_command_with_id(triggering_cmd_id, invoker):
            command.add_tag("disadvantage")


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
