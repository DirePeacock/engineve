import logging

from ..basecommands.compositecommand import CompositeCommand
from ..effectcommands.modifyresources import ModifyResources
from .attackrollcommand import AttackRollCommand
from .damagerollcommand import DamageRollCommand
from ...tags import TAGS, check_tag


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

    def _evaluate_attack_roll(self, state, invoker=None):
        self.children["attack_roll"].evaluate(state, invoker)

    def _evaluate_damage_roll(self, state, invoker=None):
        attack_hits = self.children["attack_roll"].value
        attacker_loc_str = ""  # f"@{state.actors[self.attacker_id].loc}"
        target_loc_str = ""  # f"@{state.actors[self.target_id].loc}"
        hit_str = "hits"
        # adding actor locs may be kind of extra
        # attacker_loc = state.actors[self.attacker_id].loc
        # target_loc = state.actors[self.target_id].loc
        if attack_hits:
            self.add_tag("hit")
            if check_tag(self.children["attack_roll"], TAGS["critical_hit"]):
                self.add_tag(TAGS["critical_hit"])
                self.children["damage_roll"].add_tag(TAGS["critical_hit"])
                hit_str = "crits"

            self.children["damage_roll"].evaluate(state, invoker)
            # name attacks tgt_name
            self.log = f"{state.actors[self.attacker_id].name}{attacker_loc_str} {hit_str} {state.actors[self.target_id].name} {self.children['attack_roll'].log} for {self.children['damage_roll'].log}"
            if check_tag(self.children["damage_roll"], TAGS["critical_hit"]):
                logging.debug(f"CRITLOG: {self.log}")
        else:
            self.add_tag("miss")
            self.log = f"{state.actors[self.attacker_id].name}{attacker_loc_str} misses {state.actors[self.target_id].name}{target_loc_str} {self.children['attack_roll'].log}"

    def apply_effects(self, *args, **kwargs):
        super().apply_effects(*args, **kwargs)
        if check_tag(self.children["damage_roll"], TAGS["death"]):
            self.tags[TAGS["death"]] = None

    def evaluate(self, state, invoker=None):
        """split so this is easier to Unit Test"""
        # TODO resistance may want to change the log somewhere
        self.evaluated = True
        self._evaluate_attack_roll(state, invoker)
        self._evaluate_damage_roll(state, invoker)
