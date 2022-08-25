import logging

from ..basecommands.compositecommand import CompositeCommand
from ..effectcommands.modifyresources import ModifyResources
from .attackrollcommand import AttackRollCommand
from .damagerollcommand import DamageRollCommand
from ...tags import TAGS


class AttackCommand(CompositeCommand):
    def __init__(
        self, attacker_id, target_id, log=None, stat="str", dmg_dice=None, animation_frames=None, *args, **kwargs
    ):
        """make attackRoll and damage roll command children"""
        super().__init__(*args, **kwargs)
        self.attacker_id = attacker_id
        self.target_id = target_id
        self.log = "" if log is None else log
        self.stat = stat
        self.add_tag("log")
        self.add_tag("attacker_id", self.attacker_id)
        # TODO make sure this doesn't double dip on notifications
        # TODO especially animation frames
        self.add_tag("target_id", self.target_id)
        # self.resources= [] if resources is None else ModifyResources(actor_id=attacker_id, changes={'turn_action': -1})
        self.children["attack_roll"] = AttackRollCommand(
            self.attacker_id, self.target_id, tags=self.tags.copy(), stat=self.stat
        )
        self.children["attack_roll"].add_tag("attack")

        self.children["damage_roll"] = DamageRollCommand(
            self.attacker_id, self.target_id, tags=self.tags.copy(), dmg_dice=dmg_dice, stat=self.stat
        )
        self.children["damage_roll"].add_tag("damage")

        if animation_frames is not None:
            self.add_tag("animation", animation_frames)

    def evaluate(self, state, invoker=None):
        # TODO resistance may want to change the log somewhere
        # TODO crits, crit tags
        self.evaluated = True

        # adding actor locs may be kind of extra
        # attacker_loc = state.actors[self.attacker_id].loc
        # target_loc = state.actors[self.target_id].loc

        self.children["attack_roll"].evaluate(state, invoker)

        attack_hits = self.children["attack_roll"].value
        attacker_loc_str = ""  # f"@{state.actors[self.attacker_id].loc}"
        target_loc_str = ""  # f"@{state.actors[self.target_id].loc}"
        if attack_hits:
            self.add_tag("hit")

            self.children["damage_roll"].evaluate(state, invoker)
            # name attacks tgt_name
            self.log = f"{state.actors[self.attacker_id].name}{attacker_loc_str} hits {state.actors[self.target_id].name} {self.children['attack_roll'].log} for {self.children['damage_roll'].log}"
        else:
            self.log = f"{state.actors[self.attacker_id].name}{attacker_loc_str} misses {state.actors[self.target_id].name}{target_loc_str} {self.children['attack_roll'].log}"
